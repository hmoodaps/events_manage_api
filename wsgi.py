import os
from django.core.wsgi import get_wsgi_application

# تعيين إعدادات Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject3.settings')

# إنشاء التطبيق WSGI
application = get_wsgi_application()

# تعيين المتغير handler
handler = application
