from django import forms
from .models import TravelPost, UserPreference, TravelPlan

class TravelPostForm(forms.ModelForm):
    class Meta:
        model = TravelPost
        # titleを外して、新しいフィールドを追加
        fields = ['start_point', 'end_point', 'cost', 'duration', 'transportation', 'content', 'category']
        labels = {
            'start_point': '出発地点',
            'end_point': '到着地点',
            'cost': '旅費（円）',
            'duration': 'かかった時間',
            'transportation': '移動手段',
            'content': '思い出の感想',
            'category': 'シチュエーション',
        }
        widgets = {
            'start_point': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例：東京駅'}),
            'end_point': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例：京都駅'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例：2時間30分'}),
            'transportation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例：新幹線'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': '旅の感想を記入してください'}),
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