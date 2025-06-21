from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('client-login/', views.client_login, name='client_login'),
    path('client-verify-otp/', views.client_verify_otp, name='client_verify_otp'),
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),
]