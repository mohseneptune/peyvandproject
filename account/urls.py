from django.urls import path
from account.views import register_view, login_view, profile_view, profile_change_view, logout_view, register_verify_view, login_verify_view


app_name = 'account'

urlpatterns = [
    path('account/register/', register_view, name='register'),
    path('account/register_verify/', register_verify_view, name='register_verify'),
    path('account/login/', login_view, name='login'),
    path('account/login_verify/', login_verify_view, name='login_verify'),
    path('account/profile/', profile_view, name='profile'),
    path('account/profile_change/', profile_change_view, name='profile_change'),
    path('account/logout/', logout_view, name='logout'),
]
