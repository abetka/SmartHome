
"""

Limits:
    mode:      auto, heating, cooling, ventilation, dry
    fan speed: auto, level_1, level_2, level_3, level_4, level_5, level_6, level_7, level_8, level_9

Mapping:
    mode:
        auto
        heat
        dry
        fan
        cool

    fansp:
        auto
        '1'
        '2'
        '3'
        '4'
        '5'
        '6'
        '7'
        '8'
        '9'

"""

class Normalize_INTESIS(object):
    _mode = {
        "auto": "auto",
        "heat": "heating",
        "cool": "cooling",
        "fan":  "ventilation",
        "dry":  "dry"
    }

    _fan_speed = {
        "auto": "auto",
        "1":    "level_1",
        "2":    "level_2",
        "3":    "level_3",
        "4":    "level_4",
        "5":    "level_5",
        "6":    "level_6",
        "7":    "level_7",
        "8":    "level_8",
        "9":    "level_9",
    }

    @staticmethod
    def control_mode(value):
        return "unsupported"

    @staticmethod
    def mode(value):
        return Normalize_INTESIS._mode.get(value, "unknown")

    @staticmethod
    def fan_speed(value):
        return Normalize_INTESIS._fan_speed.get(value, "unknown")

    @staticmethod
    def set_temp(value):
        try:
            if isinstance(value, str):
                value = value.replace(",", ".")
            temp = float(value) * 10
        except:
            temp = 0
        return int(temp)

    @staticmethod
    def cur_temp(value):
        try:
            if isinstance(value, str):
                value = value.replace(",", ".")
            temp = float(value) * 10
        except:
            temp = 0
        return int(temp)

    @staticmethod
    def power(value):
        if value.lower() == "on":
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
        result["control_mode"]      = Normalize_INTESIS.control_mode(0)
        result["mode"]              = Normalize_INTESIS.mode(value["mode"])
        result["fan_speed"]         = Normalize_INTESIS.fan_speed(value["fansp"])
        result["set_temp"]          = Normalize_INTESIS.set_temp(value["setptemp"])
        result["cur_temp"]          = Normalize_INTESIS.cur_temp(value["ambtemp"])
        result["power"]             = Normalize_INTESIS.power(value["onoff"])
        result["heating_season"]    = Normalize_INTESIS.heating_season(0)
        result["direction"]         = Normalize_INTESIS.direction(0)
        return result


class Denormalize_INTESIS(object):
    _mode = {
        "auto":         "auto",
        "heating":      "heat",
        "cooling":      "cool",
        "ventilation":  "fan",
        "dry":          "dry"
    }

    _fan_speed = {
        "auto":     "auto",
        "level_1":  "1",
        "level_2":  "2",
        "level_3":  "3",
        "level_4":  "4",
        "level_5":  "5",
        "level_6":  "6",
        "level_7":  "7",
        "level_8":  "8",
        "level_9":  "9",
    }

    @staticmethod
    def mode(value):
        return Denormalize_INTESIS._mode[value]

    @staticmethod
    def fan_speed(value):
        return Denormalize_INTESIS._fan_speed[value]

    @staticmethod
    def set_temp(value):
        temp = max(0, min(value / 10, 500))
        return str(temp)

    @staticmethod
    def power(value):
        if value:
            return "on"
        else:
            return "off"

    @staticmethod
    def denormalize(function, value):
        return getattr(Denormalize_INTESIS, function.lower())(value)
