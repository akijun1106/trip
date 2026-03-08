"""
本番環境用：テストデータを作成するマネジメントコマンド
使用方法: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from travel.models import TravelPost, Destination


class Command(BaseCommand):
    help = '本番環境用のテストデータを作成します'

    def handle(self, *args, **kwargs):
        # 既にデータがある場合はスキップ
        if TravelPost.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    f'投稿データが既に{TravelPost.objects.count()}件存在します。'
                )
            )
            return

        # テストユーザーを作成（存在しない場合）
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'is_staff': False,
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'ユーザー「{user.username}」を作成しました'))

        # サンプル投稿を作成
        posts_data = [
            {
                'photo_location': '東京スカイツリー',
                'content': '綺麗な夜景が見えました！とても感動的でした。',
                'category': 'night_view',
            },
            {
                'photo_location': '京都 清水寺',
                'content': '歴史を感じる素晴らしい場所でした。また行きたいです。',
                'category': 'friends',
            },
            {
                'photo_location': '大阪城公園',
                'content': '桜がとても綺麗でした。春の大阪は最高です！',
                'category': 'couple',
            },
        ]

        created_count = 0
        for post_data in posts_data:
            post = TravelPost.objects.create(
                user=user,
                **post_data
            )
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'投稿を作成: {post.photo_location}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ {created_count}件の投稿を作成しました！'
            )
        )

        # おすすめの旅先も作成（存在しない場合）
        if not Destination.objects.exists():
            destinations_data = [
                {
                    'name': '北海道・札幌',
                    'description': '美しい自然と美味しい食べ物が楽しめる北の大地',
                    'reason': '四季折々の絶景と新鮮な海の幸が魅力',
                },
                {
                    'name': '沖縄・那覇',
                    'description': '青い海と温暖な気候のリゾート地',
                    'reason': '美しいビーチとゆったりとした時間が流れる',
                },
            ]
            
            for dest_data in destinations_data:
                Destination.objects.create(**dest_data)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'おすすめの旅先を作成: {dest_data["name"]}'
                    )
                )
