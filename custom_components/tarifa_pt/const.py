from __future__ import annotations
from datetime import datetime, timedelta
import pytz

TZ_EU_LISBON = pytz.timezone("Europe/Lisbon")

VAZIO = "vazio"
FORA_VAZIO = "fora_vazio"
PONTA = "ponta"
CHEIAS = "cheias"

def is_summer(dt: datetime) -> bool:
    off = dt.astimezone(TZ_EU_LISBON).dst()
    return bool(off and off.total_seconds() != 0)

def mk(dt: datetime, hhmm: str):
    h, m = map(int, hhmm.split(":"))
    base = dt.replace(hour=h, minute=m, second=0, microsecond=0)
    if hhmm == "24:00":
        base = (dt + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return base

def segments_bi_weekly(dt: datetime):
    tzdt = dt.astimezone(TZ_EU_LISBON)
    wd = tzdt.weekday()
    summer = is_summer(tzdt)

    def seg(a, b, label):
        return (mk(tzdt, a), mk(tzdt, b), label)

    if 0 <= wd <= 4:
        return [seg("00:00", "07:00", VAZIO), seg("07:00", "24:00", FORA_VAZIO)]
    if wd == 5:
        if summer:
            return [
                seg("00:00","09:00",VAZIO),
                seg("09:00","14:00",FORA_VAZIO),
                seg("14:00","20:00",VAZIO),
                seg("20:00","22:00",FORA_VAZIO),
                seg("22:00","24:00",VAZIO),
            ]
        else:
            return [
                seg("00:00","09:30",VAZIO),
                seg("09:30","13:00",FORA_VAZIO),
                seg("13:00","18:30",VAZIO),
                seg("18:30","22:00",FORA_VAZIO),
                seg("22:00","24:00",VAZIO),
            ]
    return [seg("00:00","24:00",VAZIO)]

def segments_bi_daily(dt: datetime):
    tzdt = dt.astimezone(TZ_EU_LISBON)
    def seg(a,b,label): return (mk(tzdt,a),mk(tzdt,b),label)
    return [seg("00:00","08:00",VAZIO), seg("08:00","22:00",FORA_VAZIO), seg("22:00","24:00",VAZIO)]

def segments_tri_daily(dt: datetime):
    tzdt = dt.astimezone(TZ_EU_LISBON)
    summer = is_summer(tzdt)
    def seg(a,b,label): return (mk(tzdt,a),mk(tzdt,b),label)

    if not summer:
        return [
            seg("00:00","08:00",VAZIO),
            seg("08:00","08:30",PONTA),
            seg("08:30","10:30",CHEIAS),
            seg("10:30","12:00",PONTA),
            seg("12:00","18:00",CHEIAS),
            seg("18:00","20:30",PONTA),
            seg("20:30","22:00",CHEIAS),
            seg("22:00","24:00",VAZIO),
        ]
    else:
        return [
            seg("00:00","08:00",VAZIO),
            seg("08:00","10:30",PONTA),
            seg("10:30","12:00",CHEIAS),
            seg("12:00","13:00",PONTA),
            seg("13:00","19:30",CHEIAS),
            seg("19:30","21:00",PONTA),
            seg("21:00","22:00",CHEIAS),
            seg("22:00","24:00",VAZIO),
        ]
