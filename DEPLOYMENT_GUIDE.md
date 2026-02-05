# Render 用デプロイガイド

## 準備

### 1. 必要なパッケージをインストール
```bash
pip install gunicorn whitenoise dj-database-url psycopg2-binary
pip freeze > requirements.txt
```

### 2. Git にコミット
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

## Render でのセットアップ

### 1. Render アカウント作成
https://render.com に登録

### 2. 新しいサービス作成
- **Service**: Web Service
- **Repository**: あなたの GitHub リポジトリを接続
- **Branch**: main（またはデプロイするブランチ）

### 3. 設定

**Build Command:**
```
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command:**
```
gunicorn config.wsgi:application
```

### 4. 環境変数を設定

`Environment` タブで以下を追加：

| キー | 値 |
|------|-----|
| `SECRET_KEY` | `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` で生成した値 |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app.onrender.com` |
| `DJANGO_SETTINGS_MODULE` | `config.settings` |

### 5. PostgreSQL データベースを作成

Render でPostgreSQL を作成し、`DATABASE_URL` 環境変数が自動設定されます。

## デプロイ後

1. GitHub に push すると自動デプロイ開始
2. コードを修正して push するだけで即座に反映
3. デプロイ状況は Render ダッシュボードで確認

## ドメイン設定

- Render の無料ドメイン: `your-app.onrender.com`
- カスタムドメイン設定も可能（Settings → Custom Domain）

## トラブルシューティング

### ログを確認
Render ダッシュボードの「Logs」タブを確認

### よくある問題

**1. `ModuleNotFoundError`**
→ `requirements.txt` に必要なパッケージが含まれているか確認

**2. `static files not found`**
→ `python manage.py collectstatic` が実行されているか確認

**3. データベース接続エラー**
→ `DATABASE_URL` が正しく設定されているか確認

## AI コードレビュー

GitHub と Claude を統合すれば、コード修正のレビューが可能です：

1. VS Code の GitHub Copilot を有効化
2. コード修正中にいつでも質問可能
3. 本番環境で問題が発生したら、ログを共有して即座に修正

これにより、デプロイ後も迅速に改善できます！
