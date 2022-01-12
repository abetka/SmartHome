
"""

Limits:
    mode:      unsupported
    fan speed: unsupported

Mapping:
    ---

"""

class Normalize_AIRPOHODA(object):
    _mode = {
    }

    _fan_speed = {
    }

    @staticmethod
    def control_mode(value):
        return "unsupported"

    @staticmethod
    def mode(value):
        return "unsupported"

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
        result["control_mode"]      = Normalize_AIRPOHODA.control_mode(0)
        result["mode"]              = Normalize_AIRPOHODA.mode(0)
        result["fan_speed"]         = Normalize_AIRPOHODA.fan_speed(0)
        result["set_temp"]          = Normalize_AIRPOHODA.set_temp(value["T3"])
        result["cur_temp"]          = Normalize_AIRPOHODA.cur_temp(value["T3"])
        result["power"]             = Normalize_AIRPOHODA.power(value["recuperation on/off"])
        result["heating_season"]    = Normalize_AIRPOHODA.heating_season(0)
        result["direction"]         = Normalize_AIRPOHODA.direction(0)
        return result


class Denormalize_AIRPOHODA(object):
    _mode = {
    }

    _fan_speed = {
    }

    @staticmethod
    def mode(value):
        return Denormalize_AIRPOHODA._mode[value]

    @staticmethod
    def fan_speed(value):
        return Denormalize_AIRPOHODA._fan_speed[value]

    @staticmethod
    def power(value):
        if value:
            return "1"
        else:
            return "0"

    @staticmethod
    def denormalize(function, value):
        return getattr(Denormalize_AIRPOHODA, function.lower())(value)
