
"""

Limits:
    mode:      auto, heating, cooling, ventilation, dry
    fan speed: auto, level_1, level_2, level_3, level_4

Mapping:
    OperationMode:
        Cool
        Heat
        Fan
        Dry
        Auto

    FanSpeed:
        High
        Med
        Low
        Auto
        Top

"""

class Normalize_COOLMASTER(object):
    _mode = {
        "Auto": "auto",
        "Heat": "heating",
        "Cool": "cooling",
        "Fan":  "ventilation",
        "Dry":  "dry"
    }

    _fan_speed = {
        "Auto": "auto",
        "Low":  "level_1",
        "Med":  "level_2",
        "High": "level_3",
        "Top":  "level_4",
    }

    @staticmethod
    def control_mode(value):
        return "unsupported"

    @staticmethod
    def mode(value):
        return Normalize_COOLMASTER._mode.get(value, "unknown")

    @staticmethod
    def fan_speed(value):
        return Normalize_COOLMASTER._fan_speed.get(value, "unknown")

    @staticmethod
    def set_temp(value):
        try:
            if isinstance(value, str):
                value = value.replace(",", ".")
            temp = float(value[:-1]) * 100
        except:
            temp = 0
        return int(temp)

    @staticmethod
    def cur_temp(value):
        try:
            if isinstance(value, str):
                value = value.replace(",", ".")
            temp = float(value[:-1]) * 100
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
        result["control_mode"]      = Normalize_COOLMASTER.control_mode(0)
        result["mode"]              = Normalize_COOLMASTER.mode(value["OperationMode"])
        result["fan_speed"]         = Normalize_COOLMASTER.fan_speed(value["FanSpeed"])
        result["set_temp"]          = Normalize_COOLMASTER.set_temp(value["SetTemp"])
        result["cur_temp"]          = Normalize_COOLMASTER.cur_temp(value["RoomTemp"])
        result["power"]             = Normalize_COOLMASTER.power(value["OperationStatus"])
        result["heating_season"]    = Normalize_COOLMASTER.heating_season(0)
        result["direction"]         = Normalize_COOLMASTER.direction(0)
        return result


class Denormalize_COOLMASTER(object):
    _mode = {
        "auto": "Auto",
        "heating": "Heat",
        "cooling": "Cool",
        "ventilation": "Fan",
        "dry": "Dry"
    }

    _fan_speed = {
        "auto": "Auto",
        "level_1": "Low",
        "level_2": "Med",
        "level_3": "High",
        "level_4": "Top"
    }

    @staticmethod
    def mode(value):
        return Denormalize_COOLMASTER._mode[value]

    @staticmethod
    def fan_speed(value):
        return Denormalize_COOLMASTER._fan_speed[value]

    @staticmethod
    def set_temp(value):
        temp = max(0, min(value / 100, 50))
        return temp

    @staticmethod
    def power(value):
        if value:
            return "ON"
        else:
            return "OFF"

    @staticmethod
    def denormalize(function, value):
        return getattr(Denormalize_COOLMASTER, function.lower())(value)
