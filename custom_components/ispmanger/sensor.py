import logging
import requests
from xml.etree import ElementTree as ET
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_HOST = "host"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    host = config.get(CONF_HOST)
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)

    try:
        api = IspManagerAPI(host, username, password)
        add_entities([IspManagerCPUSensor(api), IspManagerRAMSensor(api)], True)
    except Exception as e:
        _LOGGER.error(f"Ошибка при настройке компонента ispmanager: {e}")


class IspManagerAPI:
    def __init__(self, host, username, password):
        self.host = host
        self.authinfo = f"{username}:{password}"
        self.url = f"https://{self.host}:1500/ispmgr?authinfo={self.authinfo}&out=xml&func=server_capacity"

    def get_data(self):
        try:
            _LOGGER.debug(f"Отправка запроса к API: {self.url}")
            response = requests.get(self.url, timeout=10, verify=False)
            _LOGGER.debug(f"Получен ответ от API: {response.status_code}, {response.text}")

            if response.status_code == 200:
                root = ET.fromstring(response.text)
                server_stat = root.find(".//server_stat")
                if server_stat is not None:
                    # Получаем последний элемент <elem>
                    elems = server_stat.findall("elem")
                    if elems:
                        last_elem = elems[-1]
                        data = {
                            "cpu": float(last_elem.find("cpu").text) if last_elem.find("cpu") is not None else None,
                            "ram": float(last_elem.find("us_mem").text)
                            if last_elem.find("us_mem") is not None
                            else None,
                        }
                        _LOGGER.debug(f"Парсинг данных из XML: {data}")
                        return data
                _LOGGER.warning("Тег <server_stat> или его содержимое не найдены в ответе.")
                return None
            else:
                _LOGGER.error(f"Ошибка при запросе к API: Код статуса {response.status_code}")
                return None
        except ET.ParseError:
            _LOGGER.error("Ошибка при парсинге XML-ответа. Проверьте формат ответа сервера.")
            return None
        except requests.exceptions.RequestException as e:
            _LOGGER.error(f"Ошибка при выполнении HTTP-запроса: {e}")
            return None
        except Exception as e:
            _LOGGER.error(f"Неизвестная ошибка при получении данных из API: {e}")
            return None


class IspManagerCPUSensor(Entity):
    def __init__(self, api):
        self._api = api
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return "Ispmanager CPU Usage"

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return "%"

    @property
    def icon(self):
        """Возвращает иконку для сенсора."""
        return "mdi:cpu-64-bit"

    @property
    def device_state_attributes(self):
        return self._attributes

    def update(self):
        data = self._api.get_data()
        if data:
            _LOGGER.debug(f"Обновление данных для CPU: {data}")
            self._state = data["cpu"]
            self._attributes = {"ram_usage": data["ram"]}
        else:
            _LOGGER.warning("Данные для CPU не получены")


class IspManagerRAMSensor(Entity):
    def __init__(self, api):
        self._api = api
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return "Ispmanager RAM Usage"

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return "%"

    @property
    def icon(self):
        """Возвращает иконку для сенсора."""
        return "mdi:memory"

    @property
    def device_state_attributes(self):
        return self._attributes

    def update(self):
        data = self._api.get_data()
        if data:
            _LOGGER.debug(f"Обновление данных для RAM: {data}")
            self._state = data["ram"]
            self._attributes = {"cpu_usage": data["cpu"]}
        else:
            _LOGGER.warning("Данные для RAM не получены")