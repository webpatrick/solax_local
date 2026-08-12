from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.storage import Store

from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN
from .coordinator import SolaxDataUpdateCoordinator

STORAGE_VERSION = 1
STORAGE_KEY = f"{DOMAIN}_offsets"

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Platform-level setup.

    Prepare persistent storage for offsets used to keep cumulative counters
    monotonic when a device counter resets.
    """
    hass.data.setdefault(DOMAIN, {})

    # Persistent store for offsets (per config entry)
    store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
    offsets = await store.async_load() or {}
    hass.data[DOMAIN]["_store"] = store
    hass.data[DOMAIN]["offsets"] = offsets

    async def refresh_all_inverters(call: ServiceCall) -> None:
        """Service to refresh all known inverters."""
        coordinators = hass.data.get(DOMAIN, {}).values()
        for coordinator in coordinators:
            if isinstance(coordinator, SolaxDataUpdateCoordinator):
                await coordinator.async_request_refresh()
        _LOGGER.info("Manual refresh requested for all inverters")

    hass.services.async_register(DOMAIN, "refresh_all", refresh_all_inverters)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))
    coordinator = SolaxDataUpdateCoordinator(hass, entry.data["host"], entry.data["serial"], scan_interval)
    entry.async_on_unload(entry.add_update_listener(async_update_options))
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Ensure offsets map has an entry for this config entry
    hass.data[DOMAIN].setdefault("offsets", {})
    hass.data[DOMAIN]["offsets"].setdefault(entry.entry_id, {})

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


async def async_save_offsets(hass: HomeAssistant) -> None:
    """Persist the offsets dictionary to storage."""
    store: Store | None = hass.data.get(DOMAIN, {}).get("_store")
    if store is None:
        return
    offsets = hass.data[DOMAIN].get("offsets", {})
    await store.async_save(offsets)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor", "binary_sensor", "switch"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
