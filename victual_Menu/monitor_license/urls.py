from django.urls import path
from .views import license_portal, license_status_api, activation_request_api

urlpatterns = [
    # Main licensing portal
    path('', license_portal, name='license_portal'),
    path('<slug:slug>/', license_portal, name='license_portal_tenant'),

    # Installation-specific portal
    path(
        'installation/<str:installation_id>/',
        license_portal,
        name='license_installation'
    ),

    # License status API
    path(
        'api/status/<str:installation_id>/',
        license_status_api,
        name='license_status_api'
    ),

    path(
        'api/request/',
        activation_request_api,
        name='activation_request_api'
    ),

    # Middleware-compatible tenant fallbacks
    path(
        '<slug:slug>/monitor_license/',
        license_portal,
        name='license_portal_middleware_fallback'
    ),

    path(
        '<slug:slug>/monitor_license/api/status/<str:installation_id>/',
        license_status_api,
        name='license_status_api_middleware_fallback'
    ),

    path(
        '<slug:slug>/monitor_license/api/request/',
        activation_request_api,
        name='activation_request_api_middleware_fallback'
    ),
]