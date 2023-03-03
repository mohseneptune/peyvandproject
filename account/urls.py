from django.urls import path
from account.views import (
    register_view,
    login_view,
    profile_view,
    phone_change_view,
    phone_change_verify_view,
    logout_view,
    register_verify_view,
    login_verify_view,
    profile_change_view,
    khosousiaat_change_view,
    entezaaraat_change_view,
)


app_name = "account"

urlpatterns = [
    path("account/register/", register_view, name="register"),
    path("account/register_verify/", register_verify_view, name="register_verify"),
    path("account/login/", login_view, name="login"),
    path("account/login_verify/", login_verify_view, name="login_verify"),
    path("account/profile/", profile_view, name="profile"),
    path("account/phone_change/", phone_change_view, name="phone_change"),
    path("account/phone_change_verify/", phone_change_verify_view, name="phone_change_verify"),
    path("account/logout/", logout_view, name="logout"),
    path("account/profile_change/", profile_change_view, name="profile_change"),
    path("account/khosousiaat_change/", khosousiaat_change_view, name="khosousiaat_change"),
    path("account/entezaaraat_change/", entezaaraat_change_view, name="entezaaraat_change"),
]
