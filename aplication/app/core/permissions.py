from django.core.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from django.core.cache import cache


class RequestUserAttackVerifyCode(BasePermission):
    message = "شما به دیلبل درخواست های زیاد تایک ساعت درسترسی به این بخش ندارید"

    def has_permission(self, request, view):
        ip_user = request.custom_info.get("ip")
        phone = request.data.get("phone_number")
        if (data := cache.get(phone)):
            if data["ip"] == ip_user and data["cont_request"] >= 3:
                cache.set(phone, data, 3600)
                raise PermissionDenied(self.message)
        return bool(True)


class RequestUserVerifyPassword(BasePermission):
    message = "شما به دیلبل بیش از 3 بار نام کار بری و یا رمز عبور را اشتباه وارد کردید به مدت یک ساعت حساب کار بری شما مسدود می باشد"

    def has_permission(self, request, view):
        phone = request.data.get("phone_number")
        if (data := cache.get(phone)):
            if data >= 3:
                cache.set(phone, data, 3600)
                raise PermissionDenied(self.message)
        return bool(True)
