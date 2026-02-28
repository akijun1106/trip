"""
ユーザーの旅行投稿を分析して、おすすめの旅行先を提案するエンジン
"""
from django.db.models import Count, Q
from collections import Counter
import random


def analyze_user_travel_preferences(user):
    """
    ユーザーの投稿を分析して、旅行の好みを抽出
    
    Args:
        user: Djangoユーザーオブジェクト
    
    Returns:
        dict: {
            'favorite_categories': ['夜景', 'カップル', ...],
            'visited_locations': ['京都', '東京', ...],
            'travel_style': 'sightseeing' | 'relax' | 'adventure' | 'gourmet',
            'activity_preference': 'nature' | 'culture' | 'shopping' | ...
        }
    """
    from travel.models import TravelPost
    
    # ユーザーの投稿を取得
    posts = TravelPost.objects.filter(user=user).order_by('-created_at')[:20]
    
    if not posts.exists():
        return None
    
    # データ収集
    categories = []
    locations = []
    contents = []
    
    for post in posts:
        if post.category:
            categories.append(post.category)
        if post.start_point:
            locations.append(post.start_point)
        if post.end_point:
            locations.append(post.end_point)
        if post.content:
            contents.append(post.content.lower())
    
    # 分析結果
    analysis = {
        'favorite_categories': Counter(categories).most_common(2),  # 上位2つ
        'visited_locations': list(set(locations)),  # ユニークな場所
        'total_posts': posts.count(),
        'travel_keywords': _extract_keywords(contents),
    }
    
    return analysis


def _extract_keywords(contents):
    """投稿内容からキーワードを抽出"""
    keywords = {
        'nature': ['自然', '山', '滝', '森', '景色', 'ハイキング', '絶景'],
        'culture': ['歴史', '伝統', '寺', '神社', '文化', '古都'],
        'gourmet': ['食べ物', 'グルメ', 'グルメ', '美味しい', 'ラーメン', 'そば', '寿司', 'スイーツ'],
        'nightlife': ['夜景', 'バー', 'ナイト', 'クラブ', '夜間'],
        'relax': ['癒し', '温泉', 'spa', 'リラックス', '休息'],
        'shopping': ['買い物', 'ショッピング', 'お土産', 'セール'],
    }
    
    detected_keywords = {}
    
    for style, words in keywords.items():
        count = sum(1 for content in contents for word in words if word in content)
        if count > 0:
            detected_keywords[style] = count
    
    if detected_keywords:
        return sorted(detected_keywords.items(), key=lambda x: x[1], reverse=True)
    return []


def get_recommended_destination(user, all_destinations):
    """
    ユーザーの投稿分析に基づいて、おすすめの旅行先を提案
    
    Args:
        user: Djangoユーザーオブジェクト
        all_destinations: 全Destinationオブジェクト
    
    Returns:
        Destinationオブジェクト | None
    """
    analysis = analyze_user_travel_preferences(user)
    
    if not analysis:
        # 投稿がない場合はランダムに選択
        destinations_list = list(all_destinations)
        return random.choice(destinations_list) if destinations_list else None
    
    # 訪問済みの場所を除外（未訪問の場所をおすすめする）
    visited_location_names = set(analysis['visited_locations'])
    
    # おすすめを計算
    recommendations = {}
    
    for dest in all_destinations:
        score = 0
        
        # 1. 未訪問エリア（ボーナス点）
        if dest.name not in visited_location_names:
            score += 10
        
        # 2. 好みのキーワードとのマッチ
        description_lower = (dest.description or '').lower()
        for keyword_type, count in analysis['travel_keywords']:
            keyword_mapping = {
                'nature': ['自然', '絶景', 'アルプス', '山'],
                'culture': ['伝統', '文化', '歴史', '寺', '神社'],
                'gourmet': ['グルメ', '食文化', 'ラーメン'],
                'nightlife': ['夜景'],
                'relax': ['温泉', '癒し', 'spa'],
                'shopping': ['ショッピング', '商都'],
            }
            
            if keyword_type in keyword_mapping:
                for word in keyword_mapping[keyword_type]:
                    if word in description_lower:
                        score += count
        
        recommendations[dest.id] = (score, dest)
    
    # スコアが最も高い目的地を選択
    if recommendations:
        best_dest = max(recommendations.values(), key=lambda x: x[0])[1]
        return best_dest
    
    # デフォルト
    destinations_list = list(all_destinations)
    return random.choice(destinations_list) if destinations_list else None


def get_recommendation_reason(user, destination, analysis):
    """
    なぜこの目的地をおすすめしたのか、理由テキストを生成
    
    Args:
        user: ユーザーオブジェクト
        destination: Destinationオブジェクト
        analysis: 分析結果
    
    Returns:
        str: おすすめ理由
    """
    if not analysis:
        return f"{destination.name}はいかがですか？"
    
    # カテゴリの理由
    reasons = []
    
    if analysis['visited_locations']:
        visited_sample = analysis['visited_locations'][0]
        reasons.append(f"「{visited_sample}」と同じ雰囲気が好きそうなので")
    
    if analysis['travel_keywords']:
        primary_style = analysis['travel_keywords'][0][0]
        style_map = {
            'nature': '自然好きの',
            'culture': '文化愛好家の',
            'gourmet': 'グルメ好きの',
            'nightlife': '夜景好きの',
            'relax': 'リラックス好きの',
            'shopping': 'ショッピング好きの',
        }
        if primary_style in style_map:
            reasons.append(f"{style_map[primary_style]}あなたにぴったり")
    
    if reasons:
        return f"{destination.name} - {','.join(reasons)}🌟"
    
    return f"{destination.name}はいかがですか？"
