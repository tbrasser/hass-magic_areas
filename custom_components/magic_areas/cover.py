import logging

import homeassistant.components.cover as cover
from homeassistant.components.group.cover import CoverGroup

from .base import MagicEntity
from .const import CONF_FEATURE_COVER_GROUPS, DATA_AREA_OBJECT, MODULE_DATA

DEPENDENCIES = ["magic_areas"]


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Area config entry."""

    area_data = hass.data[MODULE_DATA][config_entry.entry_id]
    area = area_data[DATA_AREA_OBJECT]

    # Check feature availability
    if not area.has_feature(CONF_FEATURE_COVER_GROUPS):
        return

    # Check if there are any covers
    if not area.has_entities(cover.DOMAIN):
        _LOGGER.debug(f"No {cover.DOMAIN} entities for area {area.name} ")
        return

    entities_to_add = []

    # Append None to the list of device classes to catch those covers that
    # don't have a device class assigned (and put them in their own group)
    for device_class in cover.DEVICE_CLASSES + [None]:
        covers_in_device_class = [
            e["entity_id"]
            for e in area.entities[cover.DOMAIN]
            if e.get("device_class") == device_class
        ]

        if any(covers_in_device_class):
            _LOGGER.debug(
                f"Creating {device_class or ''} cover group for {area.name} with covers: {covers_in_device_class}"
            )
            entities_to_add.append(AreaCoverGroup(hass, area, device_class))
    async_add_entities(entities_to_add)


class AreaCoverGroup(MagicEntity, CoverGroup):
    def __init__(self, hass, area, device_class):
        self.area = area
        self.hass = hass

        device_class_name = " ".join(device_class.split("_")).title()

        self._name = (
            f"Area {device_class_name} Covers ({area.name})"
            if device_class
            else f"Area Covers ({area.name})"
        )
        self._device_class = device_class
        self._entities = [
            e
            for e in area.entities[cover.DOMAIN]
            if e.get("device_class") == device_class
        ]
        self._attributes["covers"] = [e["entity_id"] for e in self._entities]

        unique_id = (
            f"magicareas_cover_group_{area.slug}_{device_class}"
            if device_class
            else f"magicareas_cover_group_{area.slug}"
        )

        CoverGroup.__init__(self, unique_id, self._name, self._attributes["covers"])

    @property
    def device_class(self):
        return self._device_class
