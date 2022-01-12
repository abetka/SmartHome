
from normalizer_lg import Normalize_LG, Denormalize_LG
from normalizer_coolmaster import Normalize_COOLMASTER, Denormalize_COOLMASTER
from normalizer_airpohoda import Normalize_AIRPOHODA, Denormalize_AIRPOHODA
from normalizer_atrea import Normalize_ATREA, Denormalize_ATREA
from normalizer_universal import Normalize_UNIVERSAL, Denormalize_UNIVERSAL
from normalizer_nilan import Normalize_NILAN, Denormalize_NILAN
from normalizer_intesis import Normalize_INTESIS, Denormalize_INTESIS
from normalizer_daikin import Normalize_DAIKIN, Denormalize_DAIKIN
from normalizer_mitsubishi import Normalize_MITSUBISHI, Denormalize_MITSUBISHI
from normalizer_cairox import Normalize_CAIROX, Denormalize_CAIROX


_normalize_control_mode = {
    0:  "unsupported",
    1:  "unknown",
    2:  "manual",
    3:  "auto",
    4:  "temporary"
    }

_denormalize_control_mode = {
    "unsupported":  0,
    "unknown":      1,
    "manual":       2,
    "auto":         3,
    "temporary":    4
    }


_normalize_mode = {
    0:  "unsupported",
    1:  "unknown",
    2:  "off",
    3:  "auto",
    4:  "heating",
    5:  "cooling",
    6:  "ventilation",
    7:  "dry",
    8:  "periodic_ventilation",
    9:  "periodic",
    10: "night_precooling",
    11: "balancing",
    12: "overpressure",
    13: "service"
    }

_denormalize_mode = {
    "unsupported":          0,
    "unknown":              1,
    "off":                  2,
    "auto":                 3,
    "heating":              4,
    "cooling":              5,
    "ventilation":          6,
    "dry":                  7,
    "periodic_ventilation": 8,
    "periodic":             9,
    "night_precooling":     10,
    "balancing":            11,
    "overpressure":         12,
    "service":              13
    }

_normalize_fan_speed = {
    0:  "unsupported",
    1:  "unknown",
    2:  "off",
    3:  "auto",
    4:  "level_1",
    5:  "level_2",
    6:  "level_3",
    7:  "level_4",
    8:  "level_5",
    9:  "level_6",
    10: "level_7",
    11: "level_8",
    12: "level_9"
    }

_denormalize_fan_speed = {
    "unsupported":  0,
    "unknown":      1,
    "off":          2,
    "auto":         3,
    "level_1":      4,
    "level_2":      5,
    "level_3":      6,
    "level_4":      7,
    "level_5":      8,
    "level_6":      9,
    "level_7":      10,
    "level_8":      11,
    "level_9":      12
    }

_normalize_direction = {
    0:  "unsupported",
    1:  "unknown",
    2:  "auto",
    3:  "swing",
    4:  "position_1",
    5:  "position_2",
    6:  "position_3",
    7:  "position_4",
    8:  "position_5",
    9:  "position_6",
    10: "position_7",
    11: "position_8",
    12: "position_9"
    }

_denormalize_direction = {
    "unsupported":  0,
    "unknown":      1,
    "auto":         2,
    "swing":        3,
    "position_1":   4,
    "position_2":   5,
    "position_3":   6,
    "position_4":   7,
    "position_5":   8,
    "position_6":   9,
    "position_7":   10,
    "position_8":   11,
    "position_9":   12
    }

# power - 0 / 1
# temp  - int(temp * 100)

def NormalizeAC(clim, value):
    return globals()["Normalize_" + clim.upper()].normalize(value)


def DenormalizeAC(clim, function, value):
    return globals()["Denormalize_" + clim.upper()].denormalize(function, value)


def NormalizeCU(function, value):
    try:
        return globals()["_normalize_" + function.lower()][value]
    except:
        return value


def DenormalizeCU(function, value):
    try:
        return globals()["_denormalize_" + function.lower()][value.lower()]
    except:
        return value


"""
# cu to clim
cu_value = 1
try:
    normalize_value = _normalize_mode[cu_value]
    print Denormalize("lg", "mode", normalize_value)
    # setValue("lg", "mode", denormalize_value) cmd to clim
except Exception as e:
    print "Bad argument/s (%s)" % e

# clim to cu
clim_value = {
    'power'    : True,
    'lock'     : False,
    'auto_swing' : False,
    'speed'    : 2,
    'mode'     : 2,
    'plasma'   : False,
    'desired'  : 22,
    'current'  : 21
}
try:
    normalize_value = Normalize("lg", clim_value)
    print normalize_value
    print _denormalize_mode[normalize_value["mode"]]
    print _denormalize_fan_speed[normalize_value["fan_speed"]]
    # writeValue(uuid, denormalize_value) cmd to cu
except Exception as e:
    print "Bad argument/s (%s)" % e
"""