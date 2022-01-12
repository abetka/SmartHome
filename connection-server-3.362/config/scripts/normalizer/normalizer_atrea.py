
"""

Limits:
    mode:      off, auto, ventilation, periodic_ventilation, periodic, night_precooling, balancing, overpressure
    fan speed: unsupported

Mapping:
    mode:
        off
        auto
        ventilation
        periodic ventilation
        periodic
        night precooling
        balancing
        overpressure

    no fan speed

"""

class Normalize_ATREA(object):
    _mode = {
        "off":                      "off",
        "auto":                     "auto",
        "ventilation":              "ventilation",
        "periodic ventilation":     "periodic_ventilation",
        "periodic":                 "periodic",
        "night precooling":         "night_precooling",
        "balancing":                "balancing",
        "overpressure":             "overpressure"
    }

    _fan_speed = {
    }

    _control_mode = {
        "manual":    "manual",
        "auto":      "auto",
        "temporary": "temporary"
    }

    @staticmethod
    def control_mode(value):
        return Normalize_ATREA._control_mode.get(value, "unknown")

    @staticmethod
    def mode(value):
        return Normalize_ATREA._mode.get(value, "unknown")

    @staticmethod
    def fan_speed(value):
        return "unsupported"

    @staticmethod
    def set_temp(value):
        try:
            if isinstance(value, str):
                value = value.replace(",", ".")
            temp = float(value) * 100
        except:
            temp = 0
        return int(temp)

    @staticmethod
    def cur_temp(value):
        try:
            if isinstance(value, str):
                value = value.replace(",", ".")
            temp = float(value) * 100
        except:
            temp = 0
        return int(temp)

    @staticmethod
    def power(value):
        return int(value)

    @staticmethod
    def heating_season(value):
        return int(bool(value))

    @staticmethod
    def direction(value):
        return "unsupported"

    @staticmethod
    def normalize(value):
        result = {}
        result["control_mode"]      = Normalize_ATREA.control_mode(value["air_handling"])
        result["mode"]              = Normalize_ATREA.mode(value["mode"])
        result["fan_speed"]         = Normalize_ATREA.fan_speed(0)
        result["set_temp"]          = Normalize_ATREA.set_temp(value["requested_temperature"])
        result["cur_temp"]          = Normalize_ATREA.cur_temp(value["supply air temperature"])
        result["power"]             = Normalize_ATREA.power(value["power"])
        result["heating_season"]    = Normalize_ATREA.heating_season(value["heating_season"])
        result["direction"]         = Normalize_ATREA.direction(0)
        return result


class Denormalize_ATREA(object):
    _mode = {
        "off":                      "off",
        "auto":                     "auto",
        "ventilation":              "ventilation",
        "periodic_ventilation":     "periodic ventilation",
        "periodic":                 "periodic",
        "night_precooling":         "night precooling",
        "balancing":                "balancing",
        "overpressure":             "overpressure"
    }

    _fan_speed = {
    }

    _control_mode = {
        "manual":    "manual",
        "auto":      "auto",
        "temporary": "temporary"
    }

    @staticmethod
    def control_mode(value):
        return Denormalize_ATREA._control_mode[value]

    @staticmethod
    def mode(value):
        return Denormalize_ATREA._mode[value]

    @staticmethod
    def fan_speed(value):
        return Denormalize_ATREA._fan_speed[value]

    @staticmethod
    def set_temp(value):
        temp = max(10, min(value / 100.0, 40))
        return temp

    @staticmethod
    def power(value):
        return max(0, min(value, 100))

    @staticmethod
    def heating_season(value):
        return int(bool(value))

    @staticmethod
    def denormalize(function, value):
        return getattr(Denormalize_ATREA, function.lower())(value)
