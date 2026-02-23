"""
URL routing for sportsbooking project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

api_urlpatterns = [
    path('auth/', include('apps.auth_app.urls', namespace='auth')),
    path('sites/', include('apps.sites.urls', namespace='sites')),
    path('courts/', include('apps.courts.urls', namespace='courts')),
    path('reservations/', include('apps.reservations.urls', namespace='reservations')),
    path('payments/', include('apps.payments.urls', namespace='payments')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/', include(api_urlpatterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
