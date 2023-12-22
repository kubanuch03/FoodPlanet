from rest_framework import serializers
from .models import CustomUser
from decouple import config

from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode




class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)
    full_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "phone_number",
            "full_name",
            "created_at",
            "password",
            "password2",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Пароль не совпадает, попробуйте еще раз"}
            )
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            username=validated_data.get("username", ""),
            phone_number=validated_data.get("phone_number", ""),
            full_name=validated_data.get("full_name", ""),
            password=validated_data["password"],
            token_auth=get_random_string(64),
            is_active=False
        )

        current_site = get_current_site(self.context["request"])
        domain = current_site.domain
        protocol = "https" if self.context["request"].is_secure() else "http"
        confirmation_link = reverse(
            "user:confirm_email", kwargs={"token": user.token_auth}
        )

        subject = "Подтверждение регистрации"
        message = f'Подтвердите вашу регистрацию по ссылке: \n\n{protocol}://{domain}{confirmation_link}'
        from_email = config("EMAIL_HOST_USER")
        to_email = validated_data["email"]
        send_mail(subject, message, from_email, [to_email], fail_silently=False)
        make_password(validated_data["password"])

        return user


class LoginManagerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password")


class ResetPasswordConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        uidb64 = self.context.get("uidb64")
        token = self.context.get("token")

        if not uidb64 or not token:
            raise serializers.ValidationError(
                {
                    "error": "Отсутствуют необходимые параметры в ссылке для сброса пароля"
                }
            )

        uid = force_str(urlsafe_base64_decode(uidb64))
        manager = get_object_or_404(CustomUser, pk=uid)

        if not default_token_generator.check_token(manager, token):
            raise serializers.ValidationError(
                {"error": "Недействительная ссылка для сброса пароля"}
            )

        password = data.get("password")
        password2 = data.get("password2")

        if password != password2:
            raise serializers.ValidationError({"error": "Пароли не совпадают"})

        return data

    def save(self):
        uidb64 = self.context.get("uidb64")
        uid = force_str(urlsafe_base64_decode(uidb64))
        manager = get_object_or_404(CustomUser, pk=uid)

        password = self.validated_data["password"]
        manager.set_password(password)
        manager.save()
