import os

def create_initial_superuser():
    if os.environ.get('VERCEL') == '1' or os.environ.get('CREATE_SUPERUSER') == 'True':
        import django
        from django.db.models.signals import post_migrate
        from django.dispatch import receiver
        from django.contrib.auth import get_user_model
        
        @receiver(post_migrate)
        def create_superuser_handler(sender, **kwargs):
            User = get_user_model()
            
            username = os.environ.get('SUPERUSER_USERNAME', 'admin')
            email = os.environ.get('SUPERUSER_EMAIL', 'admin@wondercooking.com')
            password = os.environ.get('SUPERUSER_PASSWORD', 'admin123')
            
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                print(f"✅ Superusuário {username} criado com sucesso!")
            else:
                print("ℹ️ Superusuário já existe")


create_initial_superuser()