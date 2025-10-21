import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wondercooking.settings")
django.setup()

from django.contrib.auth.models import User

resultado = User.objects.exclude(is_superuser=True).delete()
print(f"Usuários deletados: {resultado[0]}")
