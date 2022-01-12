
"""

Limits:
    mode:      off, auto, heating, cooling, service
    fan speed: off, level_1, level_2, level_3, level_4

Mapping:
    mode:
        0 - off
        1 - heat
        2 - cool
        3 - auto
        4 - service

    speed fan:
        0 - off
        1 - 1
        2 - 2
        3 - 3
        4 - 4

"""

class Normalize_NILAN(object):
    _mode = {
        0: "off",
        3: "auto",
        1: "heating",
        2: "cooling",
        4: "service"
    }

    _fan_speed = {
        0: "off",
        1: "level_1",
        2: "level_2",
        3: "level_3",
        4: "level_4",
    }

    @staticmethod
    def control_mode(value):
        return "unsupported"

    @staticmethod
    def mode(value):
        return Normalize_NILAN._mode.get(value, "unknown")

    @staticmethod
    def fan_speed(value):
        return Normalize_NILAN._fan_speed.get(value, "unknown")

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
        return int(bool(value))

    @staticmethod
    def heating_season(value):
        return "unsupported"

    @staticmethod
    def direction(value):
        return "unsupported"

    @staticmethod
    def normalize(value):
        result = {}
        result["control_mode"]      = Normalize_NILAN.control_mode(0)
        result["mode"]              = Normalize_NILAN.mode(value["mode"])
        result["fan_speed"]         = Normalize_NILAN.fan_speed(value["speed fan"])
        result["set_temp"]          = Normalize_NILAN.set_temp(value["set temperature"])
        result["cur_temp"]          = Normalize_NILAN.cur_temp(value["actual_tmp"])
        result["power"]             = Normalize_NILAN.power(value["on"])
        result["heating_season"]    = Normalize_NILAN.heating_season(0)
        result["direction"]         = Normalize_NILAN.direction(0)
        return result


class Denormalize_NILAN(object):
    _mode = {
        "off":      0,
        "auto":     3,
        "heating":  1,
        "cooling":  2,
        "service":  4
    }

    _fan_speed = {
        "off": 0,
        "level_1": 1,
        "level_2": 2,
        "level_3": 3,
        "level_4": 4
    }

    @staticmethod
    def mode(value):
        return Denormalize_NILAN._mode[value]

    @staticmethod
    def fan_speed(value):
        return Denormalize_NILAN._fan_speed[value]

    @staticmethod
    def set_temp(value):
        temp = max(0, min(value / 100, 50))
        return temp

    @staticmethod
    def power(value):
        return bool(value)

    @staticmethod
    def denormalize(function, value):
        return getattr(Denormalize_NILAN, function.lower())(value)
