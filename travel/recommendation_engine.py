"""
ユーザーの旅行投稿を分析して、おすすめの旅行先を提案するエンジン
"""
from collections import Counter
import random


STYLE_KEYWORDS = {
    'nature': ['自然', '山', '滝', '森', '景色', 'ハイキング', '絶景'],
    'culture': ['歴史', '伝統', '寺', '神社', '文化', '古都'],
    'gourmet': ['食べ物', 'グルメ', '美味しい', 'ラーメン', 'そば', '寿司', 'スイーツ'],
    'nightlife': ['夜景', 'バー', 'ナイト', 'クラブ', '夜間'],
    'relax': ['癒し', '温泉', 'spa', 'リラックス', '休息'],
    'shopping': ['買い物', 'ショッピング', 'お土産', 'セール'],
}

DESTINATION_KEYWORD_MAPPING = {
    'nature': ['自然', '絶景', 'アルプス', '山', '渓谷', '森林'],
    'culture': ['伝統', '文化', '歴史', '寺', '神社', '史跡'],
    'gourmet': ['グルメ', '食文化', '名物', 'ご当地', 'ラーメン', '寿司'],
    'nightlife': ['夜景', 'ライトアップ', 'ナイト'],
    'relax': ['温泉', '癒し', 'リラックス', 'spa'],
    'shopping': ['ショッピング', '商店街', 'モール', 'お土産'],
}

CATEGORY_STYLE_MAP = {
    'night_view': 'nightlife',
    'friends': 'shopping',
    'couple': 'relax',
}


def analyze_user_travel_preferences(user):
    """
    ユーザーの投稿を分析して、旅行の好みを抽出
    
    Args:
        user: Djangoユーザーオブジェクト
    
    Returns:
        dict: 投稿傾向分析結果
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
    keyword_scores = _extract_keywords(contents)
    category_style_scores = _extract_category_styles(categories)

    analysis = {
        'favorite_categories': Counter(categories).most_common(2),  # 上位2つ
        'visited_locations': list(set(locations)),  # ユニークな場所
        'total_posts': posts.count(),
        'travel_keywords': keyword_scores,
        'category_styles': category_style_scores,
    }
    
    return analysis


def _extract_keywords(contents):
    """投稿内容からキーワードを抽出"""
    detected_keywords = {}

    for style, words in STYLE_KEYWORDS.items():
        count = sum(1 for content in contents for word in words if word in content)
        if count > 0:
            detected_keywords[style] = count
    
    if detected_keywords:
        return sorted(detected_keywords.items(), key=lambda x: x[1], reverse=True)
    return []


def _extract_category_styles(categories):
    """投稿カテゴリからスタイル傾向を抽出"""
    styles = [CATEGORY_STYLE_MAP[c] for c in categories if c in CATEGORY_STYLE_MAP]
    if not styles:
        return []
    return Counter(styles).most_common()


def _score_destination(destination, analysis):
    """1つの目的地に対する詳細スコアを計算"""
    visited_location_names = set(analysis.get('visited_locations', []))
    destination_text = f"{destination.name} {destination.description or ''} {destination.reason or ''}".lower()

    score = 0
    breakdown = {
        'novelty': 0,
        'keyword_match': 0,
        'category_match': 0,
        'matched_styles': [],
    }

    # 1) 未訪問ボーナス
    if destination.name not in visited_location_names:
        breakdown['novelty'] = 10
        score += 10

    # 2) 投稿文キーワード一致
    for style, count in analysis.get('travel_keywords', []):
        matched_words = DESTINATION_KEYWORD_MAPPING.get(style, [])
        hit_count = sum(1 for word in matched_words if word in destination_text)
        if hit_count > 0:
            style_score = min(count * hit_count, 12)
            breakdown['keyword_match'] += style_score
            score += style_score
            if style not in breakdown['matched_styles']:
                breakdown['matched_styles'].append(style)

    # 3) 投稿カテゴリ傾向一致
    for style, count in analysis.get('category_styles', []):
        matched_words = DESTINATION_KEYWORD_MAPPING.get(style, [])
        if any(word in destination_text for word in matched_words):
            style_score = min(count * 3, 9)
            breakdown['category_match'] += style_score
            score += style_score
            if style not in breakdown['matched_styles']:
                breakdown['matched_styles'].append(style)

    breakdown['total'] = score
    return breakdown


def get_recommended_destination(user, all_destinations, return_detail=False):
    """
    ユーザーの投稿分析に基づいて、おすすめの旅行先を提案
    
    Args:
        user: Djangoユーザーオブジェクト
        all_destinations: 全Destinationオブジェクト
    
    Returns:
        return_detail=False: Destinationオブジェクト | None
        return_detail=True: (Destinationオブジェクト | None, dict)
    """
    analysis = analyze_user_travel_preferences(user)
    destinations_list = list(all_destinations)

    if not analysis:
        # 投稿がない場合はランダムに選択
        selected = random.choice(destinations_list) if destinations_list else None
        if return_detail:
            return selected, {
                'analysis': None,
                'score_breakdown': {
                    'total': 0,
                    'matched_styles': [],
                    'novelty': 0,
                    'keyword_match': 0,
                    'category_match': 0,
                },
            }
        return selected

    recommendations = []
    for dest in destinations_list:
        breakdown = _score_destination(dest, analysis)
        recommendations.append((breakdown['total'], dest, breakdown))

    if recommendations:
        recommendations.sort(key=lambda item: item[0], reverse=True)
        best_score, best_dest, best_breakdown = recommendations[0]
        if return_detail:
            return best_dest, {
                'analysis': analysis,
                'score_breakdown': best_breakdown,
                'best_score': best_score,
            }
        return best_dest

    selected = random.choice(destinations_list) if destinations_list else None
    if return_detail:
        return selected, {'analysis': analysis, 'score_breakdown': {'total': 0, 'matched_styles': []}}
    return selected


def get_recommendation_reason(user, destination, analysis, recommendation_detail=None):
    """
    なぜこの目的地をおすすめしたのか、理由テキストを生成
    
    Args:
        user: ユーザーオブジェクト
        destination: Destinationオブジェクト
        analysis: 分析結果
    
    Returns:
        str: おすすめ理由
    """
    if not destination:
        return ''

    if not analysis:
        return f"{destination.name}はいかがですか？"

    breakdown = recommendation_detail.get('score_breakdown', {}) if recommendation_detail else {}

    reasons = []

    if breakdown.get('novelty', 0) > 0:
        reasons.append("まだ行っていないエリアとして新鮮に楽しめるため")

    matched_styles = breakdown.get('matched_styles', [])
    if matched_styles:
        style_map = {
            'nature': '自然・絶景',
            'culture': '歴史・文化',
            'gourmet': 'グルメ',
            'nightlife': '夜景・ナイトスポット',
            'relax': 'リラックス',
            'shopping': 'ショッピング',
        }
        style_labels = [style_map[s] for s in matched_styles if s in style_map]
        if style_labels:
            reasons.append(f"投稿傾向の「{'・'.join(style_labels)}」に一致しているため")

    if analysis.get('favorite_categories'):
        category_map = {
            'night_view': '夜景',
            'friends': '友達と',
            'couple': 'カップル',
        }
        category_label = category_map.get(analysis['favorite_categories'][0][0])
        if category_label:
            reasons.append(f"特に「{category_label}」系の投稿が多い傾向があるため")

    if reasons:
        return f"{destination.name}は、{' / '.join(reasons)}おすすめです🌟"

    return f"{destination.name}はいかがですか？"
