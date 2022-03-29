"""Tests for the config flow."""
import logging

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.magic_areas import config_flow
from custom_components.magic_areas.const import CONF_ID, CONF_NAME, DOMAIN

_LOGGER = logging.getLogger()


async def test_flow_user_init(hass):
    """Test config flow initialization from config flow."""

    result = await hass.config_entries.flow.async_init(
        config_flow.DOMAIN, context={"source": "user"}
    )

    # This test should fail as integration cannot be setup standalone
    assert result["type"] == "abort"
    assert result["reason"] == "not_supported"
    assert result["handler"] == "magic_areas"
