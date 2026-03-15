"""
WSGI config for pet_manager project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_manager.settings')

application = get_wsgi_application()