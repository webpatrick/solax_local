from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.const import UnitOfEnergy, UnitOfPower, UnitOfTemperature, UnitOfElectricCurrent, UnitOfElectricPotential, UnitOfFrequency
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.restore_state import RestoreEntity

from .const import CONF_INVERTER_TYPE, DOMAIN, INVERTER_TYPES
from .coordinator import SolaxDataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator: SolaxDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    # Get inverter model from config
    inverter_type = entry.data.get(CONF_INVERTER_TYPE, "Unknown")
    model = INVERTER_TYPES.get(inverter_type, "Unknown")
    
    # Create shared device_info with model
    device_info = {
        "identifiers": {(DOMAIN, coordinator.serial)},
        "name": f"SolaX {coordinator.serial}",
        "manufacturer": "SolaX",
        "model": model,
        "connections": {("ip", coordinator.host)},
    }
    
    entities = [
        SolaxSensor(
            coordinator,
            entry.entry_id,
            "last_update",
            "Last update",
            None,
            SensorDeviceClass.TIMESTAMP,
            entity_category=EntityCategory.DIAGNOSTIC,
            device_info=device_info,
        ),
        SolaxSensor(
            coordinator,
            entry.entry_id,
            "mppt1_puissance",
            "MPPT 1 power",
            UnitOfPower.WATT,
            SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_info=device_info,
        ),
        SolaxSensor(
            coordinator,
            entry.entry_id,
            "mppt1_voltage",
            "MPPT 1 voltage",
            UnitOfElectricPotential.VOLT,
            SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_info=device_info,
        ),
        SolaxSensor(
            coordinator,
            entry.entry_id,
            "mppt1_intensite",
            "MPPT 1 current",
            UnitOfElectricCurrent.AMPERE,
            SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_info=device_info,
        ),
        SolaxSensor(
            coordinator,
            entry.entry_id,
            "mppt2_puissance",
            "MPPT 2 power",
            UnitOfPower.WATT,
            SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_info=device_info,
        ),
        SolaxSensor(
            coordinator,
            entry.entry_id,
            "mppt2_voltage",
            "MPPT 2 voltage",
            UnitOfElectricPotential.VOLT,
            SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_info=device_info,
        ),
        SolaxSensor(
            coordinator,
            entry.entry_id,
            "mppt2_intensite",
            "MPPT 2 current",
            UnitOfElectricCurrent.AMPERE,
            SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_info=device_info,
        ),
        SolaxSensor(
            coordinator,
            entry.entry_id,
            "inverter_voltage",
            "Inverter voltage",
            UnitOfElectricPotential.VOLT,
            SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_info=device_info,
        ),
        SolaxSensor(
            coordinator,
            entry.entry_id,
            "inverter_intensite",
            "Inverter current",
            UnitOfElectricCurrent.AMPERE,
            SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_info=device_info,
        ),
        SolaxSensor(
            coordinator,
            entry.entry_id,
            "inverter_puissance",
            "Inverter power",
            UnitOfPower.WATT,
            SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_info=device_info,
        ),
        SolaxSensor(
            coordinator,
            entry.entry_id,
            "inverter_freq",
            "Inverter frequency",
            UnitOfFrequency.HERTZ,
            SensorDeviceClass.FREQUENCY,
            state_class=SensorStateClass.MEASUREMENT,
            device_info=device_info,
        ),
        SolaxSensor(
            coordinator,
            entry.entry_id,
            "temp",
            "Temperature",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
            device_info=device_info,
        ),
        SolaxSensor(
            coordinator,
            entry.entry_id,
            "prod_auj",
            "Daily production",
            UnitOfEnergy.KILO_WATT_HOUR,
            SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_info=device_info,
        ),
        SolaxSensor(
            coordinator,
            entry.entry_id,
            "prod_total",
            "Total production",
            UnitOfEnergy.KILO_WATT_HOUR,
            SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_info=device_info,
        ),
        SolaxSensor(
            coordinator,
            entry.entry_id,
            "mode",
            "Mode",
            None,
            None,
            EntityCategory.DIAGNOSTIC,
            device_info=device_info,
        ),
        SolaxSensor(
            coordinator,
            entry.entry_id,
            "ip",
            "IP",
            None,
            None,
            EntityCategory.DIAGNOSTIC,
            device_info=device_info,
        ),
        SolaxSensor(
            coordinator,
            entry.entry_id,
            "num_inverter",
            "Serial number",
            None,
            None,
            EntityCategory.DIAGNOSTIC,
            device_info=device_info,
        ),
    ]
    async_add_entities(entities)


class SolaxSensor(CoordinatorEntity[SolaxDataUpdateCoordinator], SensorEntity, RestoreEntity):
    def __init__(
        self,
        coordinator,
        entry_id,
        key,
        name,
        unit,
        device_class,
        entity_category: EntityCategory | None = None,
        state_class: SensorStateClass | None = None,
        device_info: dict | None = None,
    ) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_translation_key = key
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{key}"
        self._attr_has_entity_name = False
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit
        self._attr_entity_category = entity_category
        self._attr_state_class = state_class
        self._attr_device_info = device_info

        # Restored value placeholder (filled in async_added_to_hass)
        self._restored_native_value = None

    async def async_added_to_hass(self) -> None:
        """Restore the last state when Home Assistant starts.

        This helps keep cumulative totals (like total production) persistent across
        Home Assistant restarts and transient connection losses.
        """
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state is not None and last_state.state not in (None, "unknown"):
            # Try to convert to a number if possible; otherwise keep raw state
            try:
                # Many sensors are numeric; keep as float when appropriate
                self._restored_native_value = float(last_state.state)
            except (TypeError, ValueError):
                self._restored_native_value = last_state.state

    @property
    def native_value(self):
        # If coordinator has no data yet, use restored value if available
        if self.coordinator.data is None:
            return self._restored_native_value

        value = self.coordinator.data.get(self._key)

        # If inverter is offline, keep previously restored or last known cumulative values
        if not self.coordinator.data.get("online"):
            if self._key in ("prod_total", "prod_auj"):
                # Prefer the in-memory previous value from coordinator if available
                prev = None
                if self.coordinator.data is not None:
                    prev = self.coordinator.data.get(self._key)
                # If the fetched value looks like a reset (None or 0) and we have a restored value, use it
                if (value in (None, 0, 0.0)) and self._restored_native_value is not None:
                    return self._restored_native_value
                # Otherwise, if prev exists and is meaningful, prefer it
                if value in (None,) and prev is not None:
                    return prev

        return value

    @property
    def should_poll(self) -> bool:
        return False
