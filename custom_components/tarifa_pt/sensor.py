from __future__ import annotations
from datetime import datetime, timedelta
import logging
from typing import Callable, List, Tuple
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import TZ_EU_LISBON, segments_bi_weekly, segments_bi_daily, segments_tri_daily

_LOGGER = logging.getLogger(__name__)
DOMAIN = "tarifa_pt"

CONF_MODE = "mode"
CONF_NAME_PREFIX = "name_prefix"
DEFAULT_PREFIX = "Tarifa PT"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_MODE): vol.In(["bi_semanal","bi_diario","tri_diario"]),
    vol.Optional(CONF_NAME_PREFIX, default=DEFAULT_PREFIX): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_PREFIX): cv.string,
})

Segment = Tuple[datetime, datetime, str]

def _picker(mode: str):
    return {"bi_semanal":segments_bi_weekly,"bi_diario":segments_bi_daily,"tri_diario":segments_tri_daily}[mode]

def _now_tz(): return datetime.now(tz=TZ_EU_LISBON)

def _cur_next_for(mode: str, now: datetime):
    today = _picker(mode)(now)
    cur = None
    for s in today:
        if s[0] <= now < s[1]:
            cur = s
            break
    if cur is None:
        cur = today[0] if now < today[0][0] else today[-1]
    idx = today.index(cur)
    if idx + 1 < len(today):
        nxt = today[idx + 1]
    else:
        nxt = _picker(mode)(now + timedelta(days=1))[0]
    return cur, nxt

async def async_setup_platform(hass: HomeAssistant, config: ConfigType, async_add_entities: AddEntitiesCallback, discovery_info: DiscoveryInfoType | None = None):
    mode = config[CONF_MODE]
    name_prefix = config.get(CONF_NAME_PREFIX, DEFAULT_PREFIX)
    sensors = [
        TariffNowSensor(name_prefix, mode),
        NextTariffSensor(name_prefix, mode),
        TariffElapsedSensor(name_prefix, mode),
        TariffRemainingSensor(name_prefix, mode),
        NextTariffDurationSensor(name_prefix, mode),
    ]
    async_add_entities(sensors, True)

class _BaseTariffSensor(SensorEntity):
    _attr_should_poll = True
    def __init__(self, prefix: str, mode: str):
        self._mode = mode
        self._prefix = prefix
    def _compute(self):
        now = _now_tz()
        cur, nxt = _cur_next_for(self._mode, now)
        now_to_end = int((cur[1] - now).total_seconds() // 60)
        cur_elapsed = int((now - cur[0]).total_seconds() // 60)
        next_duration = int((nxt[1] - nxt[0]).total_seconds() // 60)
        return cur, nxt, now_to_end, cur_elapsed, next_duration

class TariffNowSensor(_BaseTariffSensor):
    def __init__(self, prefix, mode):
        super().__init__(prefix, mode)
        self._attr_name = "tarrif-now"
        self._attr_unique_id = f"tarifa_pt_{mode}_now"
    async def async_update(self):
        self._attr_native_value = self._compute()[0][2]

class NextTariffSensor(_BaseTariffSensor):
    def __init__(self, prefix, mode):
        super().__init__(prefix, mode)
        self._attr_name = "next-tarrif"
        self._attr_unique_id = f"tarifa_pt_{mode}_next"
    async def async_update(self):
        self._attr_native_value = self._compute()[1][2]

class TariffElapsedSensor(_BaseTariffSensor):
    _attr_native_unit_of_measurement = "min"
    _attr_device_class = "duration"
    _attr_state_class = "measurement"
    def __init__(self, prefix, mode):
        super().__init__(prefix, mode)
        self._attr_name = "tarrif-now-elapsed"
        self._attr_unique_id = f"tarifa_pt_{mode}_elapsed"
    async def async_update(self):
        self._attr_native_value = max(0, self._compute()[3])

class TariffRemainingSensor(_BaseTariffSensor):
    _attr_native_unit_of_measurement = "min"
    _attr_device_class = "duration"
    _attr_state_class = "measurement"
    def __init__(self, prefix, mode):
        super().__init__(prefix, mode)
        self._attr_name = "tarrif-now-remaing"
        self._attr_unique_id = f"tarifa_pt_{mode}_remaining"
    async def async_update(self):
        self._attr_native_value = max(0, self._compute()[2])

class NextTariffDurationSensor(_BaseTariffSensor):
    _attr_native_unit_of_measurement = "min"
    _attr_device_class = "duration"
    _attr_state_class = "measurement"
    def __init__(self, prefix, mode):
        super().__init__(prefix, mode)
        self._attr_name = "next-tarrif-durantion"
        self._attr_unique_id = f"tarifa_pt_{mode}_next_duration"
    async def async_update(self):
        self._attr_native_value = max(0, self._compute()[4])
