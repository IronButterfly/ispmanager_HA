from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE
from .const import DOMAIN

ICONS = {
    "cpu": "mdi:cpu-64-bit",
    "ram": "mdi:memory",
    "apache2": "mdi:server",
    "dovecot": "mdi:email-fast",
    "nginx": "mdi:web",
    "named": "mdi:dns",
    "docker": "mdi:docker",
    "mysql": "mdi:database",
    "ssh": "mdi:lock",
    "mariadb": "mdi:database",
    "ispmanager-ddos": "mdi:shield-sun",
    "php-fpm74": "mdi:language-php",
    "php-fpm82": "mdi:language-php",
    "exim4": "mdi:email-outline",
    "default": "mdi:checkbox-marked-circle-outline",
}

async def async_setup_entry(hass, entry, async_add_entities):
    """Настройка сенсоров ISPmanager."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Отладка: Проверим структуру данных перед созданием сенсоров
    print("DEBUG: coordinator.data =", coordinator.data)

    sensors = [
        IspManagerSensor(coordinator, "cpu"),
        IspManagerSensor(coordinator, "ram"),
    ]

    # Исправляем обработку сервисов
    services = coordinator.data.get("services", {})
    if isinstance(services, dict):  # Убеждаемся, что services - это словарь
        for service_name, service_status in services.items():
            sensors.append(IspManagerSensor(coordinator, "service", service_name))

    async_add_entities(sensors, True)

class IspManagerSensor(CoordinatorEntity, SensorEntity):
    """Сенсор для мониторинга ресурсов ISPmanager и статуса сервисов."""

    def __init__(self, coordinator, sensor_type, service_name=None):
        """Инициализация сенсора."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._service_name = service_name

        if service_name:
            self._attr_name = f"Service {service_name}"
            self._attr_unique_id = f"ispmanager_service_{service_name}"
            self._attr_icon = ICONS.get(service_name, ICONS["default"])
            self._attr_native_unit_of_measurement = None
        else:
            self._attr_name = f"Ispmanager {sensor_type.upper()}"
            self._attr_unique_id = f"ispmanager_{sensor_type}"
            self._attr_icon = ICONS.get(sensor_type, "mdi:help-circle")
            self._attr_native_unit_of_measurement = PERCENTAGE if sensor_type in ["cpu", "ram"] else None

    @property
    def native_value(self):
        """Возвращает текущее значение сенсора."""
        if self._service_name:
            return self.coordinator.data.get("services", {}).get(self._service_name, "unknown")
        return self.coordinator.data.get(self._sensor_type)
