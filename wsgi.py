"""
WSGI config for inshala project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# تحديد إعدادات Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inshala.settings')

# إنشاء تطبيق WSGI
application = get_wsgi_application()
