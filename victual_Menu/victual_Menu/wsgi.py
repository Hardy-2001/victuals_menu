import os

from django.core.wsgi import get_wsgi_application

# MAKE SURE THE CASING HERE MATCHES YOUR APP FOLDER EXACTLY
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'victual_Menu.settings')

application = get_wsgi_application()