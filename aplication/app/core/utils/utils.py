import re
from random import randint
from django.core.cache import cache


class Utils:
    @staticmethod
    def code_generator():
        return str(randint(100000, 999999))

    @staticmethod
    def vilification_pattern_mobile(value):
        pattern = re.compile(r'^(\+98|0)?9\d{9}$')
        return pattern.match(value)

    @staticmethod
    def set_cache(ip, phone, cont_request=0, code=0) -> bool:
        if not (data:= cache.get(phone)):
            cache.set(phone, {"ip": ip, "cont_request": cont_request, "code": code})
            return True
        data["cont_request"] += 1
        cache.set(phone, data,240)
        return data

