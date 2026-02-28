"""
既存のローカル画像をCloudinaryにアップロードして、データベースを更新するスクリプト
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from travel.models import TravelPost
import cloudinary
import cloudinary.uploader
from pathlib import Path

# Cloudinary設定
cloudinary.config(
    cloud_name='dmvetmzff',
    api_key='795656918771694',
    api_secret='pJ5IqD_eGy2JwXL4fFdoTfXn1zo'
)

BASE_DIR = Path(__file__).resolve().parent

def migrate_images():
    """ローカル画像をCloudinaryに移行"""
    posts = TravelPost.objects.all()
    
    for post in posts:
        if post.image:
            # 画像パスを取得
            image_path = BASE_DIR / 'media' / str(post.image)
            
            # ファイルが存在するか確認
            if image_path.exists():
                print(f"Processing Post ID {post.id}: {post.photo_location}")
                print(f"  Current path: {post.image}")
                
                try:
                    # Cloudinaryにアップロード
                    result = cloudinary.uploader.upload(
                        str(image_path),
                        folder='posts',
                        public_id=image_path.stem,  # 拡張子を除いたファイル名
                        overwrite=True
                    )
                    
                    # 新しいCloudinary URLを取得
                    cloudinary_url = result['secure_url']
                    print(f"  ✅ Uploaded to: {cloudinary_url}")
                    
                    # データベースを更新（パスの相対部分を保持）
                    # Cloudinary storageを使用している場合、自動的にCloudinary URLに変換される
                    print(f"  ℹ️ Database field remains: {post.image}")
                    print()
                    
                except Exception as e:
                    print(f"  ❌ Error uploading: {e}")
                    print()
            else:
                print(f"⚠️ Post ID {post.id}: File not found at {image_path}")
                print()

if __name__ == '__main__':
    print("=" * 60)
    print("Cloudinary画像移行スクリプト")
    print("=" * 60)
    print()
    migrate_images()
    print("=" * 60)
    print("完了！")
    print("=" * 60)
