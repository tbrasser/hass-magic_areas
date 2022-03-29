"""Tests for the auto initialization flow."""
import logging
from unittest import mock

from homeassistant.config_entries import SOURCE_USER
from homeassistant.const import CONF_SOURCE
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry
import voluptuous as vol

from custom_components.magic_areas import async_setup
from custom_components.magic_areas.const import (
    AREA_SCHEMA,
    CONF_ACCENT_ENTITY,
    CONF_ACCENT_STATE,
    CONF_CLEAR_TIMEOUT,
    CONF_DARK_ENTITY,
    CONF_DARK_STATE,
    CONF_ENABLED_FEATURES,
    CONF_EXCLUDE_ENTITIES,
    CONF_EXTENDED_TIME,
    CONF_EXTENDED_TIMEOUT,
    CONF_ICON,
    CONF_ID,
    CONF_INCLUDE_ENTITIES,
    CONF_NAME,
    CONF_ON_STATES,
    CONF_PRESENCE_DEVICE_PLATFORMS,
    CONF_PRESENCE_SENSOR_DEVICE_CLASS,
    CONF_SECONDARY_STATES,
    CONF_SLEEP_ENTITY,
    CONF_SLEEP_STATE,
    CONF_SLEEP_TIMEOUT,
    CONF_TYPE,
    CONF_UPDATE_INTERVAL,
    DEFAULT_ACCENT_STATE,
    DEFAULT_CLEAR_TIMEOUT,
    DEFAULT_DARK_STATE,
    DEFAULT_ENABLED_FEATURES,
    DEFAULT_EXTENDED_TIME,
    DEFAULT_EXTENDED_TIMEOUT,
    DEFAULT_ICON,
    DEFAULT_ON_STATES,
    DEFAULT_PRESENCE_DEVICE_PLATFORMS,
    DEFAULT_PRESENCE_DEVICE_SENSOR_CLASS,
    DEFAULT_SLEEP_STATE,
    DEFAULT_SLEEP_TIMEOUT,
    DEFAULT_TYPE,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger()


async def test_async_setup(hass):
    """Tests the whole async setup process"""
    config = {DOMAIN: {}}

    result = await async_setup(hass, config, test_run=True)

    assert result == True


async def test_async_setup_single(hass):
    """Test single entry async_setup functionality."""

    # Mock entry data
    area_data = {
        CONF_ID: "mock-area",
        CONF_NAME: "Mock Area",
    }

    # Create mock config entry
    config_entry = AREA_SCHEMA({})

    config_entry.update(area_data)

    # Add area to HASS
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={CONF_SOURCE: SOURCE_USER}, data=config_entry
    )

    # Expected output
    expected = {
        "version": 1,
        "type": "create_entry",
        "flow_id": mock.ANY,
        "handler": "magic_areas",
        "title": "Mock Area",
        "data": {
            CONF_CLEAR_TIMEOUT: DEFAULT_CLEAR_TIMEOUT,
            CONF_PRESENCE_SENSOR_DEVICE_CLASS: DEFAULT_PRESENCE_DEVICE_SENSOR_CLASS,
            CONF_ICON: DEFAULT_ICON,
            CONF_ENABLED_FEATURES: DEFAULT_ENABLED_FEATURES,
            CONF_PRESENCE_DEVICE_PLATFORMS: DEFAULT_PRESENCE_DEVICE_PLATFORMS,
            CONF_INCLUDE_ENTITIES: [],
            CONF_EXCLUDE_ENTITIES: [],
            CONF_ON_STATES: DEFAULT_ON_STATES,
            CONF_TYPE: DEFAULT_TYPE,
            CONF_UPDATE_INTERVAL: DEFAULT_UPDATE_INTERVAL,
            CONF_SECONDARY_STATES: {
                CONF_DARK_ENTITY: "",
                CONF_EXTENDED_TIME: DEFAULT_EXTENDED_TIME,
                CONF_ACCENT_STATE: DEFAULT_ACCENT_STATE,
                CONF_DARK_STATE: DEFAULT_DARK_STATE,
                CONF_SLEEP_TIMEOUT: DEFAULT_SLEEP_TIMEOUT,
                CONF_EXTENDED_TIMEOUT: DEFAULT_EXTENDED_TIMEOUT,
                CONF_SLEEP_STATE: DEFAULT_SLEEP_STATE,
                CONF_SLEEP_ENTITY: "",
                CONF_ACCENT_ENTITY: "",
            },
            CONF_ID: "mock-area",
            CONF_NAME: "Mock Area",
        },
        "description": None,
        "description_placeholders": None,
        "result": mock.ANY,
    }

    assert expected == result
