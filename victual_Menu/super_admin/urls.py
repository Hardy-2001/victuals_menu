from django.urls import path
from . import views

app_name = 'super_admin'

urlpatterns = [
    # 🎯 Core platform marketing landing page endpoint path
    path('', views.platform_landing_home_view, name='landing_home'),

    # 🖼️ Supporting background illustration viewport route
    path('landing-images/', views.platform_landing_images_subs_view, name='landing_images_sub'),

    # 🚀 Keeps your template showroom card grids loading flawlessly!
    path('templates/', views.platform_explore_templates_view, name='explore_layouts_gallery'),

    # 📬 Inbound Core System Message Dispatches
    path('dispatch-mail/', views.dispatch_console_mail, name='dispatch_console_mail'),
# 🎯 ADD THIS TO YOUR super_admin/urls.py 'urlpatterns' LIST MATRIX:
    path('portal-login/', views.portal_login_view, name='portal_login'),


  ]
