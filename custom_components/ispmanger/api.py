import logging
import aiohttp
import time
from xml.etree import ElementTree as ET

_LOGGER = logging.getLogger(__name__)

class IspManagerAPI:
    def __init__(self, host, username, password, cache_timeout=300):
        self.host = host
        self.authinfo = f"{username}:{password}"
        self._cache = {}
        self._cache_timeout = cache_timeout

    async def _fetch_data(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, ssl=False) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        _LOGGER.error(f"Ошибка при запросе к API: Код статуса {response.status}")
                        return None
        except Exception as e:
            _LOGGER.error(f"Ошибка при выполнении HTTP-запроса: {e}")
            return None

    async def get_server_data(self):
        """Получение данных о CPU и RAM."""
        url = f"https://{self.host}:1500/ispmgr?authinfo={self.authinfo}&out=xml&func=server_capacity"
        response_text = await self._fetch_data(url)
        if response_text:
            root = ET.fromstring(response_text)
            server_stat = root.find(".//server_stat")
            if server_stat is not None:
                elems = server_stat.findall("elem")
                if elems:
                    last_elem = elems[-1]
                    return {
                        "cpu": float(last_elem.find("cpu").text) if last_elem.find("cpu") is not None else None,
                        "ram": float(last_elem.find("us_mem").text) if last_elem.find("us_mem") is not None else None,
                    }
        _LOGGER.warning("Тег <server_stat> не найден в ответе.")
        return None

    # async def get_services_data(self):
    #     """Получение списка сервисов."""
    #     url = f"https://{self.host}:1500/ispmgr?authinfo={self.authinfo}&out=xml&func=services"
    #     response_text = await self._fetch_data(url)
    #     if response_text:
    #         root = ET.fromstring(response_text)
    #         services = []
    #         for elem in root.findall("elem"):
    #             service = {
    #                 "name": elem.find("name").text if elem.find("name") is not None else "N/A",
    #                 "state": elem.find("state").text if elem.find("state") is not None else "N/A",
    #             }
    #             services.append(service)
    #         return services
    #     _LOGGER.error("Не удалось получить данные о сервисах.")
    #     return None

    async def get_services_data(self):
        """Получение списка сервисов в виде словаря {имя_сервиса: состояние}."""
        url = f"https://{self.host}:1500/ispmgr?authinfo={self.authinfo}&out=xml&func=services"
        response_text = await self._fetch_data(url)
        if response_text:
            root = ET.fromstring(response_text)
            services = {}
            for elem in root.findall("elem"):
                name = elem.find("name").text if elem.find("name") is not None else "N/A"
                state = elem.find("state").text if elem.find("state") is not None else "unknown"
                services[name] = state  # 👈 Теперь создаем словарь
            return services
        _LOGGER.error("❌ Не удалось получить данные о сервисах.")
        return {}
