
"""

Limits:
    mode:      off, heating, cooling
    fan speed: unsupported

Mapping:
    heating
    cooling

"""

class Normalize_UNIVERSAL(object):
    _mode = {
    }

    _fan_speed = {
    }

    @staticmethod
    def control_mode(value):
        return "unsupported"

    @staticmethod
    def mode(value):
        if value["heating"] == value['cooling']:
            return "off"
        elif value["heating"] == "1":
            return "heating"
        elif value["cooling"] == "1":
            return "cooling"

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
        if value == "1":
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
        result["control_mode"]      = Normalize_UNIVERSAL.control_mode(0)
        result["mode"]              = Normalize_UNIVERSAL.mode(value)
        result["fan_speed"]         = Normalize_UNIVERSAL.fan_speed(0)
        result["set_temp"]          = Normalize_UNIVERSAL.set_temp(value["setTemp"])
        result["cur_temp"]          = Normalize_UNIVERSAL.cur_temp(value["actTemp"])
        result["power"]             = Normalize_UNIVERSAL.power(value["on/off"])
        result["heating_season"]    = Normalize_UNIVERSAL.heating_season(0)
        result["direction"]         = Normalize_UNIVERSAL.direction(0)
        return result


class Denormalize_UNIVERSAL(object):
    _mode = {
        "heating": "heating",
        "cooling": "cooling"
    }

    _fan_speed = {
    }

    @staticmethod
    def mode(value):
        return Denormalize_UNIVERSAL._mode[value]

    @staticmethod
    def fan_speed(value):
        return Denormalize_UNIVERSAL._fan_speed[value]

    @staticmethod
    def set_temp(value):
        temp = max(0, min(value / 100, 50))
        return str(temp)

    @staticmethod
    def power(value):
        if value:
            return "1"
        else:
            return "0"

    @staticmethod
    def denormalize(function, value):
        return getattr(Denormalize_UNIVERSAL, function.lower())(value)
