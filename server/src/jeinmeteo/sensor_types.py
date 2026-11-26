import re

SENSOR_TYPES = {
    "multisensor": {
        "humidity": float, 
        "pressure": float, 
        "temperature": float, 
        "pm2.5": float, 
        "pm10": float,
        "date": str,
        "battery_level": float
        },
    
    "power_meter": {
        "e_in": float,
        "e_out": float,
        "power": float, 
        "date": str},
}

_SQL_TYPES = {float: "REAL", int: "INTEGER", str: "TEXT"}

_HWID_RE = re.compile(r"^[A-Za-z0-9_]{1,64}$")


class UnknownDeviceType(ValueError):
    pass


def validate_device_type(device_type: str) -> str:
    if device_type not in SENSOR_TYPES:
        valid = ", ".join(sorted(SENSOR_TYPES))
        raise UnknownDeviceType(f"unknown device type {device_type!r}, valid types: {valid}")
    return device_type


def columns_for(device_type: str) -> tuple[str, ...]:
    return tuple(SENSOR_TYPES[device_type])

def validate_values(device_type: str, values: dict) -> dict:
    """Reject unknown keys, convert types, fill missing values with None."""
    spec = SENSOR_TYPES[device_type]
    unknown = set(values) - set(spec)
    if unknown:
        raise ValueError(f"unknown fields for {device_type}: {sorted(unknown)}")
    result = {}
    for name, py_type in spec.items():
        v = values.get(name)
        result[name] = None if v is None else py_type(v)   # raises ValueError/TypeError on bad input
    return result


def create_table_sql(table: str, device_type: str) -> str:
    cols = ", ".join(f'"{n}" {_SQL_TYPES[t]}' for n, t in SENSOR_TYPES[device_type].items())
    return f"""CREATE TABLE IF NOT EXISTS {table} (ts INTEGER NOT NULL, {cols})"""


def table_name(hwid: str) -> str:
    if not _HWID_RE.fullmatch(hwid):
        raise ValueError(f"invalid hwid: {hwid!r}")
    return f'"dev_{hwid}"'