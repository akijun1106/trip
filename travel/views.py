from django.shortcuts import render, redirect, get_object_or_404
from .models import Destination, TravelPost, UserPreference, TravelPlan, TravelRoute
from .forms import TravelPostForm, UserPreferenceForm, TravelPlanRequestForm
from django.db.models import Q
import random
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .plan_generator import generate_travel_plan
from geopy.distance import geodesic

# ホーム画面（おすすめ表示） - ログイン必須
@login_required(login_url='login')
@cache_page(60 * 5)  # 5分間キャッシュ
def index(request):
    destinations = Destination.objects.all()
    # 1つもデータがないとエラーになるのでチェック
    recommended = random.choice(destinations) if destinations.exists() else None
    posts = TravelPost.objects.all().order_by('-created_at')
    return render(request, 'travel/index.html', {'recommended': recommended, 'posts': posts})

# 投稿ページ用の関数（これが足りなかった！）
def post_create(request):
    if request.method == "POST":
        form = TravelPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index') # 投稿後はホームへ
    else:
        form = TravelPostForm()
    return render(request, 'travel/post_form.html', {'form': form})

# 検索用の関数
def search(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    posts = TravelPost.objects.all()

    if query:
        posts = posts.filter(Q(start_point__icontains=query) | Q(end_point__icontains=query) | Q(content__icontains=query))
    if category:
        posts = posts.filter(category=category)

    return render(request, 'travel/search_results.html', {'posts': posts})

# ユーザー登録
def register(request):
    # ログイン済みならホームへリダイレクト
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            return render(request, 'travel/register.html', {'error': 'パスワードが一致しません'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'travel/register.html', {'error': 'このユーザー名は既に使用されています'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'travel/register.html', {'error': 'このメールアドレスは既に登録されています'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('index')
    
    return render(request, 'travel/register.html')

# ログイン
def login_view(request):
    # ログイン済みならホームへリダイレクト
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        identifier = request.POST.get('username')  # ユーザー名またはメールアドレス
        password = request.POST.get('password')

        # まずユーザー名で認証を試みる
        user = authenticate(request, username=identifier, password=password)

        # ユーザー名で見つからなければメールアドレスで検索して再認証
        if user is None:
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'travel/login.html', {'error': 'ユーザー名またはパスワードが間違っています'})
    
    return render(request, 'travel/login.html')

# ログアウト
def logout_view(request):
    logout(request)
    return redirect('index')

# マイページ
@login_required(login_url='login')
def mypage(request):
    user = request.user
    return render(request, 'travel/mypage.html', {'user': user})

# マイページ編集
@login_required(login_url='login')
def mypage_edit(request):
    user = request.user
    
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        return redirect('mypage')
    
    return render(request, 'travel/mypage_edit.html', {'user': user})

# 旅行好み設定
@login_required(login_url='login')
def preference_settings(request):
    user_preference, created = UserPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=user_preference)
        if form.is_valid():
            form.save()
            return redirect('mypage')
    else:
        form = UserPreferenceForm(instance=user_preference)
    
    return render(request, 'travel/preference_settings.html', {'form': form})

# プラン提案ページ
@login_required(login_url='login')
def plan_suggestion(request):
    user_preference = UserPreference.objects.filter(user=request.user).first()
    generated_plan = None
    form = TravelPlanRequestForm()
    
    if request.method == 'POST':
        form = TravelPlanRequestForm(request.POST)
        if form.is_valid():
            destination = form.cleaned_data['destination']
            days = form.cleaned_data['days']
            budget = form.cleaned_data.get('budget') or None
            
            # プラン生成
            plan_data = generate_travel_plan(destination, days, user_preference, budget)
            
            # プランをデータベースに保存
            travel_plan = TravelPlan.objects.create(
                user=request.user,
                destination=destination,
                days=days,
                plan_content=plan_data['content'],
                favorite_food=plan_data['favorite_food'],
                favorite_activity=plan_data['favorite_activity'],
            )
            
            generated_plan = travel_plan
    
    return render(request, 'travel/plan_suggestion.html', {
        'form': form,
        'generated_plan': generated_plan,
        'user_preference': user_preference,
    })

# プラン履歴
@login_required(login_url='login')
def plan_history(request):
    plans = TravelPlan.objects.filter(user=request.user)
    
    return render(request, 'travel/plan_history.html', {
        'plans': plans,
    })

# プラン詳細
@login_required(login_url='login')
def plan_detail(request, plan_id):
    try:
        plan = TravelPlan.objects.get(id=plan_id, user=request.user)
    except TravelPlan.DoesNotExist:
        return redirect('plan_history')
    
    return render(request, 'travel/plan_detail.html', {
        'plan': plan,
    })

# 管理画面（おすすめの旅先管理）
@login_required(login_url='login')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('index')
    
    destinations = Destination.objects.all()
    posts = TravelPost.objects.all().order_by('-created_at')
    
    return render(request, 'travel/admin_dashboard.html', {
        'destinations': destinations,
        'posts': posts,
        'total_posts': posts.count(),
        'total_destinations': destinations.count(),
    })


# インタラクティブルートエディタ
@login_required(login_url='login')
def route_editor(request, plan_id):
    plan = get_object_or_404(TravelPlan, id=plan_id, user=request.user)
    
    # ルートがなければ作成
    route, created = TravelRoute.objects.get_or_create(plan=plan)
    
    return render(request, 'travel/route_editor.html', {
        'plan': plan,
        'route': route,
    })


# API: 距離・時間計算
@require_POST
@login_required(login_url='login')
def calculate_distance_api(request):
    try:
        data = json.loads(request.body)
        waypoints = data.get('waypoints', [])
        
        if len(waypoints) < 2:
            return JsonResponse({'error': 'ウェイポイントが2つ以上必要です'}, status=400)
        
        # 距離計算
        total_distance = 0
        for i in range(len(waypoints) - 1):
            p1 = (waypoints[i]['lat'], waypoints[i]['lng'])
            p2 = (waypoints[i+1]['lat'], waypoints[i+1]['lng'])
            distance = geodesic(p1, p2).kilometers
            total_distance += distance
        
        # 所要時間推定（平均速度60km/h）
        total_duration = int((total_distance / 60) * 60)  # 分単位
        
        return JsonResponse({
            'total_distance': round(total_distance, 2),
            'total_duration': total_duration,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)