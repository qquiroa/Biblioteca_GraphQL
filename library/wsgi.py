import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')

from django.contrib.auth.models import Group
try:
    g1 = Group.objects.get(name='administrator')
    g2 = Group.objects.get(name='client')
except:
    g1 = Group.objects.create(name='administrator')
    g2 = Group.objects.create(name='client')


application = get_wsgi_application()
