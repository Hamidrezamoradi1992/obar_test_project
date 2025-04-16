from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from app.core.permissions import RequestUserAttackVerifyCode, RequestUserVerifyPassword
from app.core.tasks import send_email
from app.core.utils.utils import Utils
from django.core.cache import cache
from django.contrib.auth import login
from app.user.serializers import (PhoneNumberSerializer,
                                  LoginUserSerializer,
                                  ValidationCodeSerializers,
                                  SignupSerializers)
from app.user.models import User


# Create your views here.
class SendCode(APIView):
    serializer_class = PhoneNumberSerializer
    permission_classes = []

    def post(self, request):
        ip_user = request.custom_info.get("ip")
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user = User.objects.filter(phone=phone_number).exists()
            if user:
                return Response({"message": "کاربر با این نام در سرور وجود دارد"},
                                status=status.HTTP_301_MOVED_PERMANENTLY)
            code = Utils.code_generator()
            if not (data := cache.get(phone_number)):
                data = {"code": code,
                        "ip": ip_user,
                        "phone": phone_number,
                        "cont_request": 1}
                Utils.set_cache(**data)
            print(data["code"])
            send_email.delay(subject='verify code', to_email=["hamedreza1992@gmail.com"],
                             context=f"code referral {data["code"]}")
            return Response({"message": "کد ارسال شد."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifiCode(APIView):
    serializer_class = ValidationCodeSerializers
    permission_classes = [RequestUserAttackVerifyCode]

    def post(self, request):
        ip_user = request.custom_info.get("ip")
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = request.data['code']
            if (data := Utils.set_cache(phone=phone_number, ip=ip_user)):
                data_code = data["code"]  # noqa
                if code == data_code:
                    data["verifi"] = True
                    cache.set(phone_number, data, 3600)
                    return Response({"message": "کار بر شناسایی شد "}, status=status.HTTP_301_MOVED_PERMANENTLY)
                return Response({"message": " اطلاعات وارد شده صحیح نمی باشد "}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignupView(APIView):
    serializer_class = SignupSerializers
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        phone = request.data.get("phone")

        data = cache.get(phone)
        if data and data.get("verifi") is True:
            if serializer.is_valid():
                User.objects.create_user(**serializer.validated_data)
                cache.delete(phone)
                return Response(
                    {"message": "ثبت‌نام با موفقیت انجام شد."},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "اطلاعات وارد شده صحیح نمی‌باشد."},
            status=status.HTTP_400_BAD_REQUEST
        )

class SingIn(APIView):
    permission_classes = [RequestUserVerifyPassword]
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = request.data['password']
            print(password)
            try:
                user = User.objects.get(phone=phone_number)
                if user.check_password(password):
                    login(request, user)
                    cached_object = cache.get(phone_number)
                    if cached_object:
                        cached_object.delete()
                    return Response({"message": " کاربر  وارد شد"}, status=status.HTTP_200_OK)
                if count := cache.get(phone_number):
                    count += 1
                else:
                    count = 1
                cache.set(phone_number, count, 3600)
                return Response({"message": " کاربر با این مشخصات پیدا نشد"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"message": " کاربر با این مشخصات پیدا نشد"}, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



