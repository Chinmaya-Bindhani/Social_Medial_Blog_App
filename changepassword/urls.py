from django.urls import path
from . import views

urlpatterns = [
    path("send-otp/", views.send_otp_view, name="send_otp"),
    path("verify-otp/", views.verify_otp_view, name="verify_otp"),
    path('replace/password/',views.new_password,name='password-replace'),
    path('reset/password/',views.change_password_after_otp,name='change-password'),
]