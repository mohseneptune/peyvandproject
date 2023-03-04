from django.urls import path
from myadmin.views import dashboard_view, requests_list_view, user_detail_view

app_name = 'myadmin'

urlpatterns = [
    path('myadmin/dashboard/', dashboard_view, name='dashboard'),
    path('myadmin/requests_list/', requests_list_view, name='requests_list'),
    path('myadmin/user_detail/<int:pk>/', user_detail_view, name='user_detail'),
]