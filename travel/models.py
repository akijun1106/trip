from django.db import models
from django.contrib.auth.models import User

class Destination(models.Model):
    """今日のおすすめ旅先用"""
    name = models.CharField("旅先名", max_length=100)
    image = models.ImageField("画像", upload_to='destinations/')
    description = models.TextField("説明")
    reason = models.TextField("おすすめの理由")

    class Meta:
        verbose_name = "おすすめの旅先"
        verbose_name_plural = "おすすめの旅先一覧"

    def __str__(self):
        return self.name

class UserPreference(models.Model):
    """ユーザーの旅行好み"""
    FOOD_CHOICES = [
        ('japanese', '和食'),
        ('italian', 'イタリアン'),
        ('chinese', '中華'),
        ('french', 'フランス料理'),
        ('korean', '韓国料理'),
        ('local', 'ローカルグルメ'),
        ('no_preference', '特になし'),
    ]
    
    ACTIVITY_CHOICES = [
        ('sightseeing', '観光'),
        ('nature', '自然'),
        ('culture', '文化'),
        ('sports', 'スポーツ'),
        ('shopping', 'ショッピング'),
        ('nightlife', 'ナイトライフ'),
        ('relax', 'リラックス'),
        ('no_preference', '特になし'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preference')
    favorite_food = models.CharField("好きな食べ物", max_length=20, choices=FOOD_CHOICES, default='no_preference')
    favorite_activity = models.CharField("好きなアクティビティ", max_length=20, choices=ACTIVITY_CHOICES, default='no_preference')
    budget_per_day = models.IntegerField("1日の予算（円）", default=10000)
    updated_at = models.DateTimeField("更新日時", auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}の旅行好み"
    
    class Meta:
        verbose_name = "ユーザー旅行好み"
        verbose_name_plural = "ユーザー旅行好み"

class TravelPlan(models.Model):
    """AI生成の旅行プラン"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travel_plans')
    destination = models.CharField("目的地", max_length=100)
    days = models.IntegerField("日数")
    plan_content = models.TextField("プラン内容")
    favorite_food = models.CharField("食べ物", max_length=20, blank=True)
    favorite_activity = models.CharField("アクティビティ", max_length=20, blank=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    
    def __str__(self):
        return f"{self.destination}({self.days}日間) - {self.user.username}"
    
    class Meta:
        verbose_name = "旅行プラン"
        verbose_name_plural = "旅行プラン一覧"
        ordering = ['-created_at']

class TravelPost(models.Model):
    """ユーザーの旅行投稿用"""
    CATEGORY_CHOICES = [
        ('night_view', '夜景'),
        ('friends', '友達と'),
        ('couple', 'カップル'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travelpost_set', null=True, blank=True)
    # title を start_point に変更し、end_point と via_points を追加
    start_point = models.CharField("出発地点", max_length=100)
    end_point = models.CharField("到着地点", max_length=100)
    via_points = models.TextField("経由地点", blank=True, default='', help_text="JSON形式で経由地点を保存（自動生成）")
    
    cost = models.IntegerField("旅費（円）", help_text="数値のみ入力してください")
    duration = models.CharField("所要時間", max_length=50)
    TRANSPORT_CHOICES = [
        ('walk', '徒歩'),
        ('bike', '自転車'),
        ('car', 'くるま'),
        ('bus', 'バス'),
        ('train', '電車'),
        ('shinkansen', '新幹線'),
        ('plane', '飛行機'),
    ]
    transportation = models.CharField("交通手段", max_length=20, choices=TRANSPORT_CHOICES, default='walk')
    content = models.TextField("思い出の感想")
    category = models.CharField("カテゴリ", max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField("写真", upload_to='posts/', blank=True, null=True)
    video = models.FileField("動画", upload_to='posts/', blank=True, null=True, help_text="MP4、WebMなどの動画ファイル")
    created_at = models.DateTimeField("投稿日時", auto_now_add=True)

    class Meta:
        verbose_name = "旅行投稿"
        verbose_name_plural = "旅行投稿一覧"

    def __str__(self):
        return f"{self.start_point} ➔ {self.end_point}"


class TravelRoute(models.Model):
    """インタラクティブ日程用ルート管理"""
    plan = models.OneToOneField(TravelPlan, on_delete=models.CASCADE, related_name='route')
    
    # ウェイポイント（JSON形式で保存）
    waypoints = models.TextField(
        "ウェイポイント",
        default='[]',
        help_text='[{"lat": 35.6762, "lng": 139.6503, "name": "地点名", "date": "2026-02-06"}, ...]'
    )
    
    # 計算結果
    total_distance = models.FloatField("総距離（km）", default=0)  # キロメートル
    total_duration = models.IntegerField("総所要時間（分）", default=0)  # 分
    
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)
    
    class Meta:
        verbose_name = "旅行ルート"
        verbose_name_plural = "旅行ルート一覧"
    
    def __str__(self):
        return f"{self.plan.destination}のルート"