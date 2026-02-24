from django import forms
from .models import TravelPost, UserPreference, TravelPlan

class TravelPostForm(forms.ModelForm):
    class Meta:
        model = TravelPost
        # 写真の場所、感想、写真、動画、カテゴリのみ
        fields = ['photo_location', 'content', 'image', 'video', 'category']
        labels = {
            'photo_location': '写真の場所',
            'content': '思い出の感想',
            'image': '写真をアップロード',
            'video': '動画をアップロード',
            'category': 'シチュエーション',
        }
        widgets = {
            'photo_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例：渋谷スクランブル交差点'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '旅の感想を記入してください'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'video': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['favorite_food', 'favorite_activity', 'budget_per_day']
        labels = {
            'favorite_food': '好きな食べ物',
            'favorite_activity': '好きなアクティビティ',
            'budget_per_day': '1日の予算（円）',
        }
        widgets = {
            'favorite_food': forms.Select(attrs={'class': 'form-control'}),
            'favorite_activity': forms.Select(attrs={'class': 'form-control'}),
            'budget_per_day': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '1000'}),
        }

class TravelPlanRequestForm(forms.Form):
    destination = forms.CharField(
        label='目的地',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '例：京都',
            'required': True
        })
    )
    days = forms.IntegerField(
        label='日数',
        min_value=1,
        max_value=30,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '1〜30',
            'required': True
        })
    )
    budget = forms.IntegerField(
        label='総予算（円）',
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '任意',
        })
    )

    AREA_LEVEL_CHOICES = [
        ('spot', '有名スポット'),
        ('city', '市'),
        ('ward', '区'),
    ]
    area_levels = forms.MultipleChoiceField(
        label='提案する粒度',
        choices=AREA_LEVEL_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        initial=['spot', 'city', 'ward'],
        required=False,
    )

    SUGGESTION_COUNT_CHOICES = [
        ('1', '1件'),
        ('2', '2件'),
        ('3', '3件'),
    ]
    suggestion_count = forms.ChoiceField(
        label='提案数',
        choices=SUGGESTION_COUNT_CHOICES,
        initial='3',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )