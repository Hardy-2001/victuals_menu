import os

from django.core.asgi import get_asgi_application

# MATCH THE CASING HERE TOO
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'victual_Menu.settings')

application = get_asgi_application()