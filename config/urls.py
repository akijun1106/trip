from django.contrib import admin
from django.urls import path, include
from django.conf import settings # 追加
from django.conf.urls.static import static # 追加
import os

# 管理画面のURLを環境変数で設定（デフォルトはadmin/）
ADMIN_URL = os.environ.get('ADMIN_URL', 'admin/')

urlpatterns = [
    path(ADMIN_URL, admin.site.urls),
    path('', include('travel.urls')),
]

# 開発環境や明示指定時にメディアを配信
if settings.DEBUG or os.environ.get('SERVE_MEDIA', 'False') == 'True':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# config/urls.py の末尾に追加
from django.contrib import admin

admin.site.site_header = 'TRIP 管理システム'        # ログイン画面のタイトル
admin.site.site_title = 'TRIP'                      # ブラウザのタブ名
admin.site.index_title = '旅行プラン管理'           # 管理画面のトップ見出し