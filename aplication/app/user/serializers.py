from rest_framework import serializers

from app.core.utils.utils import Utils
from .models import User


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=11,
        required=True,
        help_text=""
    )

    def validate_phone_number(self, value):
        if not Utils.vilification_pattern_mobile(value):
            raise serializers.ValidationError(
                "شماره تلفن باید با +98 یا 09 شروع شده و دقیقاً ۱۱ رقم داشته باشد.")
        return value


class LoginUserSerializer(PhoneNumberSerializer):
    password = serializers.CharField(
        max_length=32,
        # min_length=8,
        required=True,
        help_text="شماره تلفن باید با +98 یا 09 شروع شده و دقیقاً ۱۱ رقم داشته باشد."
    )


class ValidationCodeSerializers(PhoneNumberSerializer):
    code = serializers.CharField(
        max_length=6,
        # min_length=8,
        required=True,
        help_text="شماره تلفن باید با +98 یا 09 شروع شده و دقیقاً ۱۱ رقم داشته باشد."
    )


class SignupSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', "phone"]
