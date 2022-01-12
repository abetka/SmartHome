
"""

Limits:
    mode:      auto, heating, cooling, ventilation, dry
    fan speed: level_1, level_2, level_3
    direction: swing, position_1, position_2, position_3, position_4, position_5

Mapping:
    mode:
        auto
        heating
        ventilation
        cooling
        dry

    fan_speed:
        level_1
        level_2
        level_3

    direction:
        swing
        position_1
        position_2
        position_3
        position_4
        position_5

"""

class Normalize_DAIKIN(object):
    _mode = {
        "auto":        "auto",
        "heating":     "heating",
        "ventilation": "ventilation",
        "cooling":     "cooling",
        "dry":         "dry"
    }

    _fan_speed = {
        "level_1": "level_1",
        "level_2": "level_2",
        "level_3": "level_3"
    }

    _direction = {
        "swing":      "swing",
        "position_1": "position_1",
        "position_2": "position_2",
        "position_3": "position_3",
        "position_4": "position_4",
        "position_5": "position_5"
    }

    @staticmethod
    def control_mode(value):
        return "unsupported"

    @staticmethod
    def mode(value):
        return Normalize_DAIKIN._mode.get(value, "unknown")

    @staticmethod
    def fan_speed(value):
        return Normalize_DAIKIN._fan_speed.get(value, "unknown")

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
        return Normalize_DAIKIN._direction.get(value, "unknown")

    @staticmethod
    def normalize(value):
        result = {}
        result["control_mode"]   = Normalize_DAIKIN.control_mode(0)
        result["mode"]           = Normalize_DAIKIN.mode(value["mode"])
        result["fan_speed"]      = Normalize_DAIKIN.fan_speed(value["fan_speed"])
        result["set_temp"]       = Normalize_DAIKIN.set_temp(value["set_temp"])
        result["cur_temp"]       = Normalize_DAIKIN.cur_temp(value["room_temp"])
        result["power"]          = Normalize_DAIKIN.power(value["power"])
        result["heating_season"] = Normalize_DAIKIN.heating_season(0)
        result["direction"]      = Normalize_DAIKIN.direction(value["direction"])
        return result


class Denormalize_DAIKIN(object):
    _mode = {
        "auto":        "auto",
        "heating":     "heating",
        "ventilation": "ventilation",
        "cooling":     "cooling",
        "dry":         "dry"
    }

    _fan_speed = {
        "level_1": "level_1",
        "level_2": "level_2",
        "level_3": "level_3"
    }

    _direction = {
        "swing":      "swing",
        "position_1": "position_1",
        "position_2": "position_2",
        "position_3": "position_3",
        "position_4": "position_4",
        "position_5": "position_5"
    }

    @staticmethod
    def mode(value):
        return Denormalize_DAIKIN._mode[value]

    @staticmethod
    def fan_speed(value):
        return Denormalize_DAIKIN._fan_speed[value]

    @staticmethod
    def set_temp(value):
        temp = max(16, min(value / 100, 32))
        return temp

    @staticmethod
    def power(value):
        if value:
            return "on"
        else:
            return "off"

    @staticmethod
    def direction(value):
        return Denormalize_DAIKIN._direction[value]

    @staticmethod
    def denormalize(function, value):
        return getattr(Denormalize_DAIKIN, function.lower())(value)
