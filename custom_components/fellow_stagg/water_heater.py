"""Water heater platform for Fellow Stagg EKG+ kettle."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.water_heater import (
  WaterHeaterEntity,
  WaterHeaterEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
  ATTR_TEMPERATURE,
  UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import FellowStaggDataUpdateCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
  hass: HomeAssistant,
  entry: ConfigEntry,
  async_add_entities: AddEntitiesCallback,
) -> None:
  """Set up Fellow Stagg water heater based on a config entry."""
  coordinator: FellowStaggDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
  async_add_entities([FellowStaggWaterHeater(coordinator)])

class FellowStaggWaterHeater(CoordinatorEntity[FellowStaggDataUpdateCoordinator], WaterHeaterEntity):
  """Water heater entity for Fellow Stagg kettle."""

  _attr_has_entity_name = True
  _attr_name = "Water Heater"
  _attr_supported_features = (
    WaterHeaterEntityFeature.TARGET_TEMPERATURE |
    WaterHeaterEntityFeature.ON_OFF
  )
  _attr_operation_list = ["off", "on"]

  def __init__(self, coordinator: FellowStaggDataUpdateCoordinator) -> None:
    """Initialize the water heater."""
    super().__init__(coordinator)
    self._attr_unique_id = f"{coordinator._address}_water_heater"
    self._attr_device_info = coordinator.device_info

    _LOGGER.debug("Initializing water heater with units: %s", coordinator.temperature_unit)
    
    self._attr_min_temp = coordinator.min_temp
    self._attr_max_temp = coordinator.max_temp
    self._attr_temperature_unit = coordinator.temperature_unit
    
    _LOGGER.debug(
      "Water heater temperature range set to: %s°%s - %s°%s",
      self._attr_min_temp,
      self._attr_temperature_unit,
      self._attr_max_temp,
      self._attr_temperature_unit,
    )

  @property
  def current_temperature(self) -> float | None:
    """Return the current temperature."""
    value = self.coordinator.data.get("current_temp") if self.coordinator.data else None
    _LOGGER.debug("Water heater current temperature read as: %s°%s", value, self.coordinator.temperature_unit)
    return value

  @property
  def target_temperature(self) -> float | None:
    """Return the target temperature."""
    value = self.coordinator.data.get("target_temp") if self.coordinator.data else None
    _LOGGER.debug("Water heater target temperature read as: %s°%s", value, self.coordinator.temperature_unit)
    return value

  @property
  def current_operation(self) -> str | None:
    """Return current operation."""
    if not self.coordinator.data:
      return None
    value = "on" if self.coordinator.data.get("power") else "off"
    _LOGGER.debug("Water heater operation state read as: %s", value)
    return value

  async def async_set_temperature(self, **kwargs: Any) -> None:
    """Set new target temperature."""
    temperature = kwargs.get(ATTR_TEMPERATURE)
    if temperature is None:
      return

    _LOGGER.debug(
      "Setting water heater target temperature to %s°%s",
      temperature,
      self.coordinator.temperature_unit
    )
    
    ble_device = self.coordinator.get_ble_device_for_connect()
    if ble_device is None:
      raise HomeAssistantError(
        f"No BLE device available for {self.coordinator._address}"
      )
    await self.coordinator.kettle.async_set_temperature(
      ble_device,
      int(temperature),
      fahrenheit=self.coordinator.temperature_unit == UnitOfTemperature.FAHRENHEIT
    )
    if self.coordinator.data is not None:
      self.coordinator.async_set_updated_data({**self.coordinator.data, "target_temp": int(temperature)})

  async def async_turn_on(self, **kwargs: Any) -> None:
    """Turn the water heater on."""
    _LOGGER.debug("Turning water heater ON")
    ble_device = self.coordinator.get_ble_device_for_connect()
    if ble_device is None:
      raise HomeAssistantError(
        f"No BLE device available for {self.coordinator._address}"
      )
    await self.coordinator.kettle.async_set_power(ble_device, True)
    if self.coordinator.data is not None:
      self.coordinator.async_set_updated_data({**self.coordinator.data, "power": True})

  async def async_turn_off(self, **kwargs: Any) -> None:
    """Turn the water heater off."""
    _LOGGER.debug("Turning water heater OFF")
    ble_device = self.coordinator.get_ble_device_for_connect()
    if ble_device is None:
      raise HomeAssistantError(
        f"No BLE device available for {self.coordinator._address}"
      )
    await self.coordinator.kettle.async_set_power(ble_device, False)
    if self.coordinator.data is not None:
      self.coordinator.async_set_updated_data({**self.coordinator.data, "power": False})
