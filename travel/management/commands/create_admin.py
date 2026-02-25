from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = '本番環境でスーパーユーザーを作成'

    def handle(self, *args, **options):
        username = 'akito'
        email = 'akito.junke.1106@icloud.com'
        password = 'Akito135790'
        
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'スーパーユーザー "{username}" を更新しました'))
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'スーパーユーザー "{username}" を作成しました'))
