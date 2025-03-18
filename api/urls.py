from django.urls import path

from .views import login_user, register_user, user_info

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("me/", user_info, name="user_info"),
]
