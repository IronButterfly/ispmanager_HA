from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_HOST, CONF_USERNAME, CONF_PASSWORD, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

class IspManagerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Настройка конфигурации через UI."""
    
    async def async_step_user(self, user_input=None):
        """Первый шаг настройки."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="Ispmanager", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str,
            vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    async def async_step_options(self, user_input=None):
        """Настройка параметров (выбор сенсоров)."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Optional("sensors", default=["cpu", "ram"]): vol.All(
                list, [vol.In(["cpu", "ram", "services"])]
            )
        })

        return self.async_show_form(step_id="options", data_schema=data_schema, errors=errors)
