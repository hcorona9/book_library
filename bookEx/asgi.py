"""
ASGI config for bookEx project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information, see:
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set the default settings module for the 'asgi' command
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookEx.settings")

# Get the ASGI application
application = get_asgi_application()
