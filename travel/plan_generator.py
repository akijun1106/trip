"""
旅行プラン自動生成ロジック
"""

DESTINATION_INFO = {
    '京都': {
        'description': '古都京都は日本の伝統文化の中心',
        'attractions': ['伏見稲荷大社', '清水寺', '金閣寺', '伊勢神宮', '祇園'],
        'foods': ['京懐石', '抹茶', 'ゆどうふ', '京漬物'],
        'transport': '京都市営地下鉄、バス',
    },
    '東京': {
        'description': '日本の首都、最新技術と文化が融合',
        'attractions': ['スカイツリー', '浅草寺', '渋谷', '新宿', '秋葉原'],
        'foods': ['寿司', 'ラーメン', 'もんじゃ', '天ぷら'],
        'transport': 'JR、地下鉄、タクシー',
    },
    '大阪': {
        'description': '関西の商都、グルメとエンターテイメント',
        'attractions': ['大阪城', 'ユニバーサルスタジオジャパン', '道頓堀', '心斎橋'],
        'foods': ['たこ焼き', 'お好み焼き', 'うどん', 'ラーメン'],
        'transport': 'JR、地下鉄、モノレール',
    },
    '広島': {
        'description': '歴史と平和の街、瀬戸内海の美景',
        'attractions': ['原爆ドーム', '厳島神社', '平和記念公園', 'もみじ谷'],
        'foods': ['お好み焼き', '牡蠣', 'つけ麺', '熊野筆'],
        'transport': '広島電鉄、タクシー、フェリー',
    },
    '福岡': {
        'description': 'アジアの玄関口、豊かな食文化',
        'attractions': ['大濠公園', '福岡城跡', '屋台街', '志賀島'],
        'foods': ['博多ラーメン', 'もつ鍋', 'イカの唐揚げ', 'あまおう'],
        'transport': 'JR、地下鉄、バス',
    },
    '長野': {
        'description': '自然豊かな信州、アルプスの絶景',
        'attractions': ['上高地', '軽井沢', '白川郷', '善光寺', 'スキー場'],
        'foods': ['そば', '栗', '野沢菜漬け', '信州味噌'],
        'transport': 'バス、ロープウェイ、登山道',
    },
    '沖縄': {
        'description': '南国の楽園、美しい海と文化',
        'attractions': ['青の洞窟', 'ひめゆりの塔', 'シーサー', 'ビーチ'],
        'foods': ['ゴーヤチャンプル', 'ソーキそば', 'サーターアンダギー'],
        'transport': 'モノレール、レンタカー、フェリー',
    },
}

ACTIVITY_TEMPLATES = {
    'sightseeing': '有名観光地を中心に巡る',
    'nature': '自然散策やハイキング、絶景スポット',
    'culture': '伝統文化や歴史遺産を学ぶ',
    'sports': 'スポーツアクティビティやアドベンチャー',
    'shopping': 'ショッピング中心のコース',
    'nightlife': 'グルメとナイトライフを楽しむ',
    'relax': 'スパやリラックス施設でくつろぐ',
}

FOOD_TEMPLATES = {
    'japanese': '地元の和食や伝統料理',
    'italian': 'イタリアンレストラン',
    'chinese': '中華料理',
    'french': 'フランス料理',
    'korean': '韓国料理',
    'local': 'ローカルグルメと屋台',
}

def generate_travel_plan(destination, days, user_preference=None, budget=None):
    """
    旅行プラン生成関数
    
    Args:
        destination (str): 目的地
        days (int): 日数
        user_preference (UserPreference): ユーザーの好み
        budget (int): 予算
    
    Returns:
        dict: プラン内容とその他の情報
    """
    
    plan_lines = []
    
    # ヘッダー
    plan_lines.append(f"🗺️ {destination} - {days}日間の旅行プラン\n")
    
    # 目的地情報
    dest_info = DESTINATION_INFO.get(destination, None)
    
    if dest_info:
        plan_lines.append(f"📍 {destination}について:")
        plan_lines.append(f"{dest_info['description']}\n")
    else:
        plan_lines.append(f"📍 {destination}へようこそ!\n")
    
    # ユーザー好みを取得
    favorite_food = 'local'
    favorite_activity = 'sightseeing'
    
    if user_preference:
        favorite_food = user_preference.favorite_food
        favorite_activity = user_preference.favorite_activity
    
    # アクティビティ情報
    activity_desc = ACTIVITY_TEMPLATES.get(favorite_activity, '観光')
    food_desc = FOOD_TEMPLATES.get(favorite_food, 'ローカルグルメ')
    
    plan_lines.append(f"🎯 このプランについて:")
    plan_lines.append(f"• アクティビティ: {activity_desc}")
    plan_lines.append(f"• グルメ: {food_desc}\n")
    
    # 日数別プラン
    plan_lines.append("📅 日程:")
    
    if days == 1:
        plan_lines.extend(_generate_one_day_plan(destination, dest_info, favorite_activity))
    elif days == 2:
        plan_lines.extend(_generate_two_day_plan(destination, dest_info, favorite_activity))
    elif days == 3:
        plan_lines.extend(_generate_three_day_plan(destination, dest_info, favorite_activity))
    elif days >= 4:
        plan_lines.extend(_generate_multi_day_plan(destination, days, dest_info, favorite_activity))
    
    # 予算情報
    if budget:
        daily_budget = budget // days
        plan_lines.append(f"\n💰 予算:")
        plan_lines.append(f"• 総予算: ¥{budget:,}")
        plan_lines.append(f"• 1日あたり: ¥{daily_budget:,}")
    
    # 交通情報
    if dest_info:
        plan_lines.append(f"\n🚌 交通:")
        plan_lines.append(f"• {dest_info['transport']}")
    
    # 食べ物情報
    if dest_info:
        plan_lines.append(f"\n🍽️ 現地グルメ:")
        for food in dest_info['foods'][:3]:
            plan_lines.append(f"• {food}")
    
    plan_content = '\n'.join(plan_lines)
    
    return {
        'content': plan_content,
        'destination': destination,
        'days': days,
        'favorite_food': favorite_food,
        'favorite_activity': favorite_activity,
    }

def _generate_one_day_plan(destination, dest_info, activity):
    """1日プラン生成"""
    lines = []
    lines.append("\n【1日目】")
    lines.append("• 09:00 - ホテルをチェックアウト")
    
    if dest_info and 'attractions' in dest_info:
        attractions = dest_info['attractions']
        lines.append(f"• 10:00 - {attractions[0]}を訪問")
        lines.append(f"• 13:00 - ランチタイム（地元グルメを堪能）")
        lines.append(f"• 15:00 - {attractions[1] if len(attractions) > 1 else '周辺散策'}")
        lines.append(f"• 18:00 - ディナー＆夜景スポット")
    else:
        lines.append("• 10:00 - 主要観光地を訪問")
        lines.append("• 13:00 - ランチタイム")
        lines.append("• 15:00 - 周辺散策")
        lines.append("• 18:00 - ディナー")
    
    lines.append("• 20:00 - 帰路")
    
    return lines

def _generate_two_day_plan(destination, dest_info, activity):
    """2日プラン生成"""
    lines = []
    lines.append("\n【1日目】")
    
    if dest_info and 'attractions' in dest_info:
        attractions = dest_info['attractions']
        lines.append(f"• 10:00 - {attractions[0]}を訪問")
        lines.append(f"• 13:00 - ランチ")
        lines.append(f"• 15:00 - {attractions[1] if len(attractions) > 1 else '周辺散策'}")
        lines.append("• 18:00 - ディナー")
        
        lines.append("\n【2日目】")
        lines.append(f"• 09:00 - {attractions[2] if len(attractions) > 2 else '別の観光地'}")
        lines.append("• 12:00 - ランチ")
        lines.append(f"• 14:00 - {attractions[3] if len(attractions) > 3 else 'ショッピング'}")
        lines.append("• 17:00 - カフェタイム")
        lines.append("• 18:30 - 帰路")
    else:
        lines.append("• 10:00 - 主要観光地1")
        lines.append("• 13:00 - ランチ")
        lines.append("• 15:00 - 観光地2")
        lines.append("• 18:00 - ディナー")
        lines.append("\n【2日目】")
        lines.append("• 09:00 - 観光地3")
        lines.append("• 12:00 - ランチ")
        lines.append("• 14:00 - 自由時間")
        lines.append("• 17:00 - 帰路")
    
    return lines

def _generate_three_day_plan(destination, dest_info, activity):
    """3日プラン生成"""
    lines = []
    lines.append("\n【1日目】")
    lines.append("• 到着後、ホテルチェックイン")
    lines.append("• 夜は地元グルメを堪能")
    
    lines.append("\n【2日目】")
    if dest_info and 'attractions' in dest_info:
        attractions = dest_info['attractions']
        lines.append(f"• 09:00 - {attractions[0]}")
        lines.append(f"• 12:00 - ランチ")
        lines.append(f"• 14:00 - {attractions[1] if len(attractions) > 1 else '周辺散策'}")
        lines.append("• 18:00 - ディナー")
        
        lines.append("\n【3日目】")
        lines.append(f"• 09:00 - {attractions[2] if len(attractions) > 2 else '別のスポット'}")
        lines.append("• 12:00 - ランチ")
        lines.append("• 14:00 - 自由時間・ショッピング")
        lines.append("• 17:00 - 帰路")
    else:
        lines.append("• 終日観光")
        lines.append("\n【3日目】")
        lines.append("• 09:00 - 観光・体験")
        lines.append("• 14:00 - 帰路")
    
    return lines

def _generate_multi_day_plan(destination, days, dest_info, activity):
    """4日以上のプラン生成"""
    lines = []
    
    for i in range(1, days + 1):
        lines.append(f"\n【{i}日目】")
        
        if i == 1:
            lines.append("• 到着・チェックイン・夜景スポット訪問")
        elif i == days:
            lines.append("• 最終日：自由時間・ショッピング")
            lines.append("• チェックアウト・帰路")
        else:
            if dest_info and 'attractions' in dest_info:
                attractions = dest_info['attractions']
                idx = (i - 2) % len(attractions)
                lines.append(f"• {attractions[idx]}を中心に観光")
            else:
                lines.append("• 本日のメイン観光地を訪問")
            lines.append("• 地元グルメ・カフェタイム")
    
    return lines
