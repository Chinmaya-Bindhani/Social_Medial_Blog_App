"""
PROJECT LEVEL URLS
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('firstapp.urls')),
    path('lg_out/', include('secondapp.urls')),
    path('otp/', include('changepassword.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
