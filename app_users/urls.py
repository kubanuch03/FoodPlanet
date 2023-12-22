from django.urls import path
from .views import (
    RegisterUserView,
    ConfirmEmailView,
    LoginUserView,
    UserCRUDView,
    RequestPasswordResetView,
    ResetPasswordConfirmView,
)
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r"user", UserCRUDView, basename="user")


app_name = "user"

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register_user"),
    path("login/", LoginUserView.as_view(), name="login_user"),
    path(
        "confirm-email/<str:token>/", ConfirmEmailView.as_view(), name="confirm_email"
    ),
    path(
        "reset-password/",
        RequestPasswordResetView.as_view(),
        name="reset-password",
    ),
    path(
        "reset-password-confirm/<str:uidb64>/<str:token>/",
        ResetPasswordConfirmView.as_view(),
        name="reset-password-confirm",
    ),
] + router.urls
