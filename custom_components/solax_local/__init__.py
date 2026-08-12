from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall

from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN
from .coordinator import SolaxDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Configuration au niveau de la plateforme."""
    hass.data.setdefault(DOMAIN, {})
    
    async def refresh_all_inverters(call: ServiceCall) -> None:
        """Service pour actualiser tous les onduleurs."""
        coordinators = hass.data.get(DOMAIN, {}).values()
        for coordinator in coordinators:
            if isinstance(coordinator, SolaxDataUpdateCoordinator):
                await coordinator.async_request_refresh()
        _LOGGER.info("Actualisation manuelle de tous les onduleurs")
    
    hass.services.async_register(DOMAIN, "refresh_all", refresh_all_inverters)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))
    coordinator = SolaxDataUpdateCoordinator(hass, entry.data["host"], entry.data["serial"], scan_interval)
    entry.async_on_unload(entry.add_update_listener(async_update_options))
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "binary_sensor", "switch"])
    return True


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update coordinator interval when options are changed."""
    coordinator: SolaxDataUpdateCoordinator | None = hass.data.get(DOMAIN, {}).get(entry.entry_id)
    if coordinator is None:
        return

    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))
    coordinator.update_interval = timedelta(seconds=scan_interval)
    await coordinator.async_request_refresh()


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor", "binary_sensor", "switch"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
