import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wondercooking.settings")
django.setup()

from django.contrib.auth.models import User
from postagens.models import Perfil

CYPRESS_TEST = os.environ.get('CYPRESS') or os.environ.get('CYPRESS_TEST') or os.environ.get('TESTING_WITH_CYPRESS')

if CYPRESS_TEST:
    users_to_delete = User.objects.exclude(is_superuser=True)
    user_count = users_to_delete.count()
    
    if user_count > 0:
        resultado = users_to_delete.delete()