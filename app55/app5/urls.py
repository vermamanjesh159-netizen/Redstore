from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings

from.import views
from.import health

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('about/',views.about),
    path('contact/',views.contact),
    path('login/',views.login),
    path('register/',views.register),
    path('verify/',views.verify),
    path('health/', health.health_check, name='health_check'),
    path('api/health/', health.health_check, name='api_health_check'),
    path('myadmin/',include('myadmin.urls')),
    path('user/',include('user.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

