import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ux_analyzer.settings')
django.setup()

from users.models import User, UserProfile
user = User.objects.create_user('test@hotmail.com', 'Test User', '1234')
user.profile = UserProfile()
user.profile.save()