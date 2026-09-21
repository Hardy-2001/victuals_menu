from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 🎯 Single unique administration portal path entry
    path('admin/', admin.site.urls),

    # 👑 THE MASTER VAULT ROADMAP:
    path('', include('super_admin.urls')),

    # 📦 Individual Multi-Tenant Application Sub-Links Channels
    path('store/', include('menu.urls')),
    path('modern/', include('modern.urls')),
    path('modern2/', include('advance2.urls')),

    # 🏥 NEW: Wires up your fully dynamic hospital suite modules live!
    path('modern3/', include('modern3.urls')),
    path('modern4/', include('modern4.urls')),
    path('modern5/', include('modern5.urls')),
    path('modern6/', include('modern6.urls')),
    path('modern7/', include('modern7.urls')),
    path('modern8/', include('modern8.urls')),
    path('modern9/', include('modern9.urls')),
]

# Append dynamic physical system media file pathways when debugging locally
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 🎯 Native Customization Engine Configurations (Preserved completely)
admin.site.site_header = "The Victuals & Edibles — Management System"
admin.site.site_title = "The Victuals Admin Portal"
admin.site.index_title = "Restaurant Operations & Digital Menu Controls"
