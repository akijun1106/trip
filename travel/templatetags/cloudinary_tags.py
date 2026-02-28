"""
Cloudinaryの画像URLを生成するカスタムテンプレートタグ
"""
from django import template
from django.conf import settings
import os

register = template.Library()

@register.filter
def cloudinary_url(image_field):
    """
    画像フィールドをCloudinary URLに変換
    
    相対パス（posts/IMG_2345.jpeg）の場合、Cloudinary URLを構築
    すでにHTTP(S) URLの場合はそのまま返す
    """
    if not image_field:
        return ''
    
    # URLを取得
    try:
        url = image_field.url
    except:
        url = str(image_field)
    
    # すでにHTTP(S) URLの場合はそのまま返す
    if url.startswith('http://') or url.startswith('https://'):
        return url
    
    # Cloudinary環境変数が設定されている場合、Cloudinary URLを構築
    if os.environ.get('CLOUDINARY_URL'):
        # 相対パス（/media/posts/IMG_2345.jpeg または posts/IMG_2345.jpeg）を取得
        if url.startswith('/media/'):
            relative_path = url[7:]  # /media/ を除去
        else:
            relative_path = url
        
        # ファイル名から拡張子を除去してpublic_idを作成
        # posts/IMG_2345.jpeg → posts/IMG_2345
        if '.' in relative_path:
            public_id = relative_path.rsplit('.', 1)[0]
        else:
            public_id = relative_path
        
        # Cloudinary URLを構築
        cloudinary_base = 'https://res.cloudinary.com/dmvetmzff/image/upload'
        return f'{cloudinary_base}/v1/{public_id}'
    
    # Cloudinaryが設定されていない場合（ローカル環境）は元のURLを返す
    return url
