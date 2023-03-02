from django.urls import path
from account.views import register_view, login_view, profile_view, profile_change_view, logout_view



app_name = 'account'

urlpatterns = [
    path('account/register/', register_view, name='register'),
    path('account/login/', login_view, name='login'),
    path('account/profile/', profile_view, name='profile'),
    path('account/profile_change/', profile_change_view, name='profile_change'),
    path('account/logout/', logout_view, name='logout'),
]