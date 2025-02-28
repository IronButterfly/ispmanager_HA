import logging
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, CONF_HOST, CONF_USERNAME, CONF_PASSWORD, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
from .api import IspManagerAPI

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Настройка интеграции через UI."""
    hass.data.setdefault(DOMAIN, {})

    api = IspManagerAPI(entry.data[CONF_HOST], entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD])
    
    scan_interval = timedelta(seconds=entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))

    coordinator = IspManagerCoordinator(hass, api, scan_interval)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Исправляем на `async_forward_entry_setups`
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Удаление интеграции."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

class IspManagerCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api, scan_interval):
        """Обновление данных с API ISPmanager."""
        self.api = api
        super().__init__(
            hass, _LOGGER, name=DOMAIN, update_interval=scan_interval
        )
    async def _async_update_data(self):
        data = await self.api.get_server_data()
        services = await self.api.get_services_data()
        if not data:
            raise UpdateFailed("Ошибка получения данных")
        return {"cpu": data.get("cpu"), "ram": data.get("ram"), "services": services}
