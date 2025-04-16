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


