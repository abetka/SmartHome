
"""

Limits:
    mode:      auto, heating, cooling, ventilation, dry
    fan speed: auto, level_1, level_2, level_3

Mapping:
    mode:
        0 - cooling
        1 - dehumidify
        2 - fan
        3 - auto
        4 - heating

    speed:
        0 - low
        1 - middle
        2 - high
        3 - auto

"""

class Normalize_LG(object):
    _mode = {
        3: "auto",
        4: "heating",
        0: "cooling",
        2: "ventilation",
        1: "dry"
    }

    _fan_speed = {
        3: "auto",
        0: "level_1",
        1: "level_2",
        2: "level_3",
    }

    @staticmethod
    def control_mode(value):
        return "unsupported"

    @staticmethod
    def mode(value):
        return Normalize_LG._mode.get(value, "unknown")

    @staticmethod
    def fan_speed(value):
        return Normalize_LG._fan_speed.get(value, "unknown")

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
        result["control_mode"]      = Normalize_LG.control_mode(0)
        result["mode"]              = Normalize_LG.mode(value["mode"])
        result["fan_speed"]         = Normalize_LG.fan_speed(value["speed"])
        result["set_temp"]          = Normalize_LG.set_temp(value["desired"])
        result["cur_temp"]          = Normalize_LG.cur_temp(value["current"])
        result["power"]             = Normalize_LG.power(value["power"])
        result["heating_season"]    = Normalize_LG.heating_season(0)
        result["direction"]         = Normalize_LG.direction(0)
        return result


class Denormalize_LG(object):
    _mode = {
        "auto":         3,
        "heating":      4,
        "cooling":      0,
        "ventilation":  2,
        "dry":          1
        }
    
    _fan_speed = {
        "auto":     3,
        "level_1":  0,
        "level_2":  1,
        "level_3":  2
        }

    @staticmethod
    def mode(value):
        return Denormalize_LG._mode[value]

    @staticmethod
    def fan_speed(value):
        return Denormalize_LG._fan_speed[value]

    @staticmethod
    def set_temp(value):
        temp = max(15, min(value / 100, 30))
        return temp

    @staticmethod
    def power(value):
        return bool(value)

    @staticmethod
    def denormalize(function, value):
        return getattr(Denormalize_LG, function.lower())(value)
