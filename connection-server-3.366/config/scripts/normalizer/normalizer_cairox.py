
"""

Limits:
    fan speed: off, level_1, level_2, level_3

Mapping:

    fan_speed:
        off
        level_1
        level_2
        level_3

"""

class Normalize_CAIROX(object):
    _fan_speed = {
        "off":     "off",
        "level_1": "level_1",
        "level_2": "level_2",
        "level_3": "level_3"
    }

    @staticmethod
    def control_mode(value):
        return "unsupported"

    @staticmethod
    def mode(value):
        return "unsupported"

    @staticmethod
    def fan_speed(value):
        return Normalize_CAIROX._fan_speed.get(value, "unknown")

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
        if value.upper() == "ON":
            return 1
        else:
            return 0

    @staticmethod
    def heating_season(value):
        return "unsupported"

    @staticmethod
    def direction(value):
        return "unsupported"

    @staticmethod
    def normalize(value):
        result = {}
        result["control_mode"]   = Normalize_CAIROX.control_mode(0)
        result["mode"]           = Normalize_CAIROX.mode(0)
        result["fan_speed"]      = Normalize_CAIROX.fan_speed(value["fan_speed_supply"])
        result["set_temp"]       = Normalize_CAIROX.set_temp(0)
        result["cur_temp"]       = Normalize_CAIROX.cur_temp(value["room_temp"])
        result["power"]          = Normalize_CAIROX.power(value["power"])
        result["heating_season"] = Normalize_CAIROX.heating_season(0)
        result["direction"]      = Normalize_CAIROX.direction(0)
        return result


class Denormalize_CAIROX(object):
    _fan_speed = {
        "auto":    "auto",
        "level_1": "level_1",
        "level_2": "level_2",
        "level_3": "level_3"
    }

    @staticmethod
    def fan_speed(value):
        return Denormalize_CAIROX._fan_speed[value]

    @staticmethod
    def power(value):
        if value:
            return "on"
        else:
            return "off"

    @staticmethod
    def denormalize(function, value):
        return getattr(Denormalize_CAIROX, function.lower())(value)
