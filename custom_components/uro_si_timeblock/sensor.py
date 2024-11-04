"""URO SI TimeBlock sensor for Home Assistant."""
from datetime import datetime, date, timedelta
from dateutil.easter import easter
import logging
from typing import Optional

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN, NAME, ATTRIBUTION

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(
    hass: HomeAssistant,
    config: dict,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,
) -> None:
    """Set up the URO SI TimeBlock sensor."""
    async_add_entities([UROSITimeBlockSensor(hass)], True)

class UROSITimeBlockSensor(SensorEntity):
    """Representation of a URO SI TimeBlock sensor."""

    _attr_has_entity_name = True
    _attr_name = NAME
    _attr_attribution = ATTRIBUTION

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the sensor."""
        self._hass = hass
        self._attr_unique_id = f"{DOMAIN}_current_block"
        self._attr_native_value: Optional[int] = None
        self._attr_extra_state_attributes: dict = {}

    @property
    def device_class(self) -> str:
        """Return the device class."""
        return SensorDeviceClass.ENUM

    @property
    def state_class(self) -> str:
        """Return the state class."""
        return SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self._attr_native_value

    def is_slovenian_holiday(self, dt: date) -> bool:
        """Check if the given date is a Slovenian holiday."""
        # Fixed date holidays
        fixed_holidays = [
            (1, 1),    # New Year's Day
            (1, 2),    # New Year's Day 2
            (2, 8),    # Prešeren Day
            (4, 27),   # Day of Uprising Against Occupation
            (5, 1),    # Labour Day
            (5, 2),    # Labour Day 2
            (6, 25),   # Statehood Day
            (8, 15),   # Assumption Day
            (10, 31),  # Reformation Day
            (11, 1),   # All Saints' Day
            (12, 25),  # Christmas
            (12, 26),  # Independence and Unity Day
        ]

        if (dt.month, dt.day) in fixed_holidays:
            return True

        # Calculate Easter-dependent holidays
        easter_date = easter(dt.year)
        easter_monday = easter_date + timedelta(days=1)
        pentecost = easter_date + timedelta(days=50)

        variable_holidays = [
            easter_monday,
            pentecost
        ]

        return dt in variable_holidays

    def get_time_block(self, dt: datetime) -> int:
        """Calculate the current time block."""
        # Define seasons
        high_season_months = [11, 12, 1, 2]

        time = dt.hour + dt.minute / 60
        month = dt.month

        # Check if it's a workday (not weekend and not holiday)
        is_workday = dt.weekday() < 5 and not self.is_slovenian_holiday(dt.date())
        is_high_season = month in high_season_months

        # Update attributes
        self._attr_extra_state_attributes.update({
            "is_workday": is_workday,
            "is_high_season": is_high_season,
            "current_time": time,
            "month": month,
            "hour": dt.hour,
            "minute": dt.minute,
            "is_holiday": self.is_slovenian_holiday(dt.date())
        })

        # High season logic
        if is_high_season:
            if is_workday:
                if (7 <= time < 14) or (16 <= time < 20):
                    return 1
                elif (6 <= time < 7) or (14 <= time < 16) or (20 <= time < 22):
                    return 2
                elif (0 <= time < 6) or (22 <= time < 24):
                    return 3
            else:
                if (7 <= time < 14) or (16 <= time < 20):
                    return 2
                elif (6 <= time < 7) or (14 <= time < 16) or (20 <= time < 22):
                    return 3
                elif (0 <= time < 6) or (22 <= time < 24):
                    return 4
        # Low season logic
        else:
            if is_workday:
                if (7 <= time < 14) or (16 <= time < 20):
                    return 2
                elif (6 <= time < 7) or (14 <= time < 16) or (20 <= time < 22):
                    return 3
                elif (0 <= time < 6) or (22 <= time < 24):
                    return 4
            else:
                if (7 <= time < 14) or (16 <= time < 20):
                    return 3
                elif (6 <= time < 7) or (14 <= time < 16) or (20 <= time < 22):
                    return 4
                elif (0 <= time < 6) or (22 <= time < 24):
                    return 5

        return 0

    async def async_update(self) -> None:
        """Update the sensor."""
        self._attr_native_value = self.get_time_block(datetime.now())