"""Regression test for Home Assistant 2026.8 dropping `hass` from the
constructors of `IntegrationSensor` and `UtilityMeterSensor`.

home-assistant/core#177596 and #177603 (merged 2026-07-30, shipped in HA
2026.8.0) removed the `hass` parameter from both classes' `__init__` and made
every remaining parameter keyword-only. That change is *not* listed in HA's
official breaking-changes docs (both classes are treated as internal API by
core), so it only surfaces as a `TypeError` at entity-creation time once a
user upgrades.

`custom_components/auto_utility_meter/sensor.py` builds both classes with
`hass=hass` passed unconditionally:

- the module-level `_create_integration_sensor()` helper (used by
  `async_setup_entry` for the Watt->kWh Riemann-sum sensor)
- `AutoUtilityMeterSensor.__init__`, which subclasses `UtilityMeterSensor`
  and forwards `hass=hass` to `super().__init__()`

This test calls those two real code paths directly against whatever
`homeassistant` package is actually installed in the current interpreter, so
it exercises the genuine `IntegrationSensor`/`UtilityMeterSensor` classes
from `homeassistant.components.*` (not a stand-in). No test suite existed in
this repo before this file.

Manually verified against real, actually-installed `homeassistant` packages
from PyPI on both sides of the break (see PR description for the exact pip
commands and output):

- `homeassistant==2026.8.0` (current release, the broken one): the two
  "against_real_class" tests below construct the real `IntegrationSensor` /
  `UtilityMeterSensor` end to end and assert on attributes the real
  `__init__` body sets -- proof the constructor genuinely ran, not just that
  no exception happened to be raised.
- `homeassistant==2026.7.4` (last version before the break): those same two
  tests are skipped there, because pre-2026.8 `IntegrationSensor.__init__`
  and `UtilityMeterSensor.__init__` call
  `async_entity_id_to_device(hass, source_entity)`, which needs a fully
  functional `HomeAssistant` instance (config dir, storage manager, etc.) to
  resolve -- unrelated machinery this fix doesn't touch and isn't worth
  standing up for this test. Backward compatibility (that `hass` is still
  forwarded when the installed signature still accepts it) is instead
  covered, without needing that machinery, by
  `test_hass_still_forwarded_when_parent_signature_accepts_it` (for
  `_create_integration_sensor`) and
  `test_utility_meter_hass_still_forwarded_when_parent_signature_accepts_it`
  (for `AutoUtilityMeterSensor`) below. Those two patch the parent
  `__init__` to the pre-2026.8 shape, so they check the forwarding logic,
  not the real pre-2026.8 constructor body.
"""

from __future__ import annotations

import inspect
import sys
from datetime import timedelta
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from homeassistant.components.integration.sensor import IntegrationSensor  # noqa: E402
from homeassistant.components.utility_meter.sensor import UtilityMeterSensor  # noqa: E402

from custom_components.auto_utility_meter.sensor import (  # noqa: E402
    AutoUtilityMeterSensor,
    _create_integration_sensor,
)


class _FakeHass:
    """The lightest possible stand-in for `HomeAssistant`.

    Deliberately NOT a mock of the entity classes themselves (that would be
    the "bare object instead of exercising the real entity route" mistake) —
    `IntegrationSensor` and `UtilityMeterSensor` are the genuine classes
    imported from the installed `homeassistant` package above, and
    `_create_integration_sensor`/`AutoUtilityMeterSensor.__init__` are this
    repo's real, unmodified production code. Only the `hass` *argument* is a
    stand-in, which is legitimate here: on the currently-shipping HA
    (2026.8+), the fixed code never forwards `hass` into the parent
    constructor at all (confirmed via `inspect.signature` below), so nothing
    ever calls a method on this object — a real `HomeAssistant` instance
    would be inert cargo for this specific test. What IS real: the parent
    class, its full `__init__` body, and this repo's own wrapper logic.

    This stand-in is NOT enough for the pre-2026.8 constructors: there,
    `async_entity_id_to_device(hass, source_entity)` reaches the storage
    manager and fails with `AttributeError: ... has no attribute 'config'`.
    That is why the two "against_real_class" tests skip on pre-2026.8 HA.
    """

    def __init__(self) -> None:
        # Only gets the pre-2026.8 path past `hass.data`; it still stops at
        # `hass.config` (see above). Unused on 2026.8+.
        self.data: dict = {}


def test_current_installed_ha_marks_whether_hass_is_still_accepted():
    """Sanity-check which side of the break the running interpreter is on."""
    integration_accepts_hass = "hass" in inspect.signature(IntegrationSensor.__init__).parameters
    utility_meter_accepts_hass = "hass" in inspect.signature(UtilityMeterSensor.__init__).parameters
    # Both classes changed in the same core PR batch (2026-07-30), so they
    # should always agree on which side of the break the installed
    # `homeassistant` package is on.
    assert integration_accepts_hass == utility_meter_accepts_hass


@pytest.mark.skipif(
    "hass" in inspect.signature(IntegrationSensor.__init__).parameters,
    reason="installed homeassistant is pre-2026.8: full construction needs a functional "
    "HomeAssistant instance for async_entity_id_to_device(); see module docstring",
)
def test_create_integration_sensor_against_real_class():
    """`_create_integration_sensor` must construct the real IntegrationSensor
    against whatever homeassistant.components.integration.sensor.IntegrationSensor
    is actually installed -- on HA 2026.8+ this raises TypeError without the
    `hass in inspect.signature(...)` guard.
    """
    sensor = _create_integration_sensor(
        _FakeHass(),
        source_entity_id="sensor.scooter_power",
        name="Scooter Total Energy",
        unique_id="entry123_total_energy",
    )

    assert isinstance(sensor, IntegrationSensor)
    # These are real attributes set by the real (unmodified) IntegrationSensor.__init__,
    # not attributes we invented -- proof the real constructor body actually ran.
    assert sensor._attr_unique_id == "entry123_total_energy"
    assert sensor._sensor_source_id == "sensor.scooter_power"
    assert sensor._attr_name == "Scooter Total Energy"


@pytest.mark.skipif(
    "hass" in inspect.signature(UtilityMeterSensor.__init__).parameters,
    reason="installed homeassistant is pre-2026.8: full construction needs a functional "
    "HomeAssistant instance for async_entity_id_to_device(); see module docstring",
)
def test_auto_utility_meter_sensor_against_real_class():
    """AutoUtilityMeterSensor.__init__ forwards to the real UtilityMeterSensor.__init__
    -- on HA 2026.8+ this raises TypeError without the `hass in
    inspect.signature(...)` guard.
    """
    sensor = AutoUtilityMeterSensor(
        _FakeHass(),
        source_entity="sensor.scooter_total_energy",
        name="Scooter Daily Energy",
        interval="daily",
        unique_id="entry123_daily",
        device_info=None,
        object_id="scooter_daily_energy",
        sensor_type="watt",
    )

    assert isinstance(sensor, UtilityMeterSensor)
    # Real attributes set by the real (unmodified) UtilityMeterSensor.__init__.
    # (Not asserting on `entity_id`: UtilityMeterSensor.__init__ unconditionally
    # sets `self.entity_id = suggested_entity_id`, which this wrapper never
    # passes, so it always ends up None -- a pre-existing quirk unrelated to
    # the hass-forwarding bug this test targets.)
    assert sensor._attr_unique_id == "entry123_daily"
    assert sensor._sensor_source_id == "sensor.scooter_total_energy"
    assert sensor._attr_device_class == "energy"


def test_hass_still_forwarded_when_parent_signature_accepts_it(monkeypatch):
    """Backward-compat guard: on HA versions that still accept `hass` (pre-2026.8),
    the wrapper must keep forwarding it, not silently drop it.

    This does not construct a full HA-2026.7-era IntegrationSensor (that would
    need a functional `hass.data`-backed entity/device registry, which is
    unrelated machinery this fix does not touch) -- it verifies the actual
    kwargs-building code in `_create_integration_sensor` by making
    `IntegrationSensor.__init__` (patched only for this assertion) require
    `hass`, mirroring the exact pre-2026.8 signature shape, and confirming the
    real helper still supplies it.
    """
    captured = {}

    def fake_init(self, hass, **kwargs):
        captured["hass"] = hass
        captured.update(kwargs)

    monkeypatch.setattr(IntegrationSensor, "__init__", fake_init)

    hass_marker = _FakeHass()
    sensor = _create_integration_sensor(
        hass_marker,
        source_entity_id="sensor.x",
        name="X",
        unique_id="x",
    )

    assert isinstance(sensor, IntegrationSensor)
    assert captured["hass"] is hass_marker


def test_utility_meter_hass_still_forwarded_when_parent_signature_accepts_it(monkeypatch):
    """Backward-compat guard for `AutoUtilityMeterSensor`, the twin of the
    test above: on HA versions whose `UtilityMeterSensor.__init__` still
    requires `hass` (pre-2026.8), the subclass must keep forwarding it.

    `UtilityMeterSensor.__init__` is patched to the pre-2026.8 shape (a
    required `hass` plus keyword arguments), so this checks the real
    `AutoUtilityMeterSensor.__init__` forwarding logic without needing a
    functional `HomeAssistant` for `async_entity_id_to_device`. Without the
    `inspect.signature` guard forwarding `hass`, the call raises
    `TypeError: ... missing 1 required positional argument: 'hass'`.
    """
    captured = {}

    def fake_init(self, hass, **kwargs):
        captured["hass"] = hass
        captured.update(kwargs)

    monkeypatch.setattr(UtilityMeterSensor, "__init__", fake_init)

    hass_marker = _FakeHass()
    sensor = AutoUtilityMeterSensor(
        hass_marker,
        source_entity="sensor.x_total_energy",
        name="X Daily Energy",
        interval="daily",
        unique_id="x_daily",
        device_info=None,
        object_id="x_daily_energy",
        sensor_type="watt",
    )

    assert isinstance(sensor, UtilityMeterSensor)
    assert captured["hass"] is hass_marker
    assert captured["source_entity"] == "sensor.x_total_energy"
    assert captured["unique_id"] == "x_daily"
