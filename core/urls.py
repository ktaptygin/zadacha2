"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, reverse_lazy
from restaurant import views
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('booking/create/', views.create_booking, name='create_booking'),
    path('contact/create/', views.create_contact, name='create_contact'),
    path('auth/login/', views.login_user, name='login_user'),
    path('auth/register/', views.register_user, name='register_user'),
    path('auth/logout/', views.logout_user, name='logout_user'),
    path('auth/password-reset/', views.password_reset_request, name='password_reset_request'),
    path(
        'auth/password-reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='restaurant/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path(
        'auth/password-reset/complete/',
        PasswordResetCompleteView.as_view(
            template_name='restaurant/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]