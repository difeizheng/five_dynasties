"""
数据处理模块
负责数据清洗、转换、分析
"""

import pandas as pd
import re
from typing import List, Dict, Tuple
from datetime import datetime
import streamlit as st

# 五代十国政权基础数据
WUDAI_REGIMES = [
    {"name": "后梁", "start": 907, "end": 923, "capital": "开封", "founder": "朱温", "color": "#e74c3c"},
    {"name": "后唐", "start": 923, "end": 936, "capital": "洛阳", "founder": "李存勖", "color": "#3498db"},
    {"name": "后晋", "start": 936, "end": 947, "capital": "开封", "founder": "石敬瑭", "color": "#9b59b6"},
    {"name": "后汉", "start": 947, "end": 950, "capital": "开封", "founder": "刘知远", "color": "#e67e22"},
    {"name": "后周", "start": 951, "end": 960, "capital": "开封", "founder": "郭威", "color": "#2ecc71"},
]

SHIGUO_REGIMES = [
    {"name": "吴越", "start": 907, "end": 978, "capital": "杭州", "founder": "钱镠", "color": "#1abc9c"},
    {"name": "南唐", "start": 937, "end": 975, "capital": "南京", "founder": "李昪", "color": "#e74c3c"},
    {"name": "前蜀", "start": 907, "end": 925, "capital": "成都", "founder": "王建", "color": "#f39c12"},
    {"name": "后蜀", "start": 934, "end": 965, "capital": "成都", "founder": "孟知祥", "color": "#d35400"},
    {"name": "闽国", "start": 909, "end": 945, "capital": "福州", "founder": "王审知", "color": "#9b59b6"},
    {"name": "南汉", "start": 917, "end": 971, "capital": "广州", "founder": "刘䶮", "color": "#e74c3c"},
    {"name": "楚", "start": 907, "end": 951, "capital": "长沙", "founder": "马殷", "color": "#3498db"},
    {"name": "荆南", "start": 924, "end": 963, "capital": "荆州", "founder": "高季兴", "color": "#1abc9c"},
    {"name": "北汉", "start": 951, "end": 979, "capital": "太原", "founder": "刘崇", "color": "#95a5a6"},
]

# 政权与现代省份对照
REGIME_TO_PROVINCE = {
    "后梁": ["河南", "山东", "陕西"],
    "后唐": ["河南", "河北", "山西", "山东"],
    "后晋": ["河南", "河北", "山西", "山东"],
    "后汉": ["河南", "河北", "山西", "山东"],
    "后周": ["河南", "河北", "山东", "安徽"],
    "吴越": ["浙江", "上海", "江苏"],
    "南唐": ["江苏", "安徽", "江西", "湖北"],
    "前蜀": ["四川", "重庆", "陕西"],
    "后蜀": ["四川", "重庆", "陕西"],
    "闽国": ["福建"],
    "南汉": ["广东", "广西", "海南"],
    "楚": ["湖南"],
    "荆南": ["湖北"],
    "北汉": ["山西"],
}


def parse_year_range(year_str: str) -> Tuple[int, int]:
    """解析年份范围，如 '907-923' -> (907, 923)"""
    if pd.isna(year_str):
        return (0, 0)

    if isinstance(year_str, (int, float)):
        return (int(year_str), int(year_str))

    year_str = str(year_str).strip()

    if '-' in year_str:
        parts = year_str.split('-')
        try:
            start = int(parts[0].strip())
            end = int(parts[1].strip()) if parts[1].strip() else datetime.now().year
            return (start, end)
        except:
            return (0, 0)

    try:
        year = int(year_str)
        return (year, year)
    except:
        return (0, 0)


def process_regime_timeline() -> pd.DataFrame:
    """处理政权时间线数据"""
    all_regimes = []

    for r in WUDAI_REGIMES:
        regime = r.copy()
        regime['type'] = '五代'
        all_regimes.append(regime)

    for r in SHIGUO_REGIMES:
        regime = r.copy()
        regime['type'] = '十国'
        all_regimes.append(regime)

    df = pd.DataFrame(all_regimes)
    df['duration'] = df['end'] - df['start']

    return df


def process_characters_data(detailed_data: dict) -> pd.DataFrame:
    """处理人物数据"""
    all_chars = []

    for sheet_name, df in detailed_data.items():
        if df.empty:
            continue

        df_copy = df.copy()
        df_copy['period'] = sheet_name
        all_chars.append(df_copy)

    if all_chars:
        return pd.concat(all_chars, ignore_index=True)

    return pd.DataFrame()


def process_fanzhen_data(fanzhen_data: dict) -> pd.DataFrame:
    """处理藩镇数据"""
    all_fanzhen = []

    for sheet_name, df in fanzhen_data.items():
        if df.empty:
            continue

        df_copy = df.copy()
        df_copy['category'] = sheet_name
        all_fanzhen.append(df_copy)

    if all_fanzhen:
        return pd.concat(all_fanzhen, ignore_index=True)

    return pd.DataFrame()


def extract_major_events(text: str) -> List[Dict]:
    """从文本中提取重大事件"""
    events = []

    # 匹配年份 + 事件的格式
    patterns = [
        r'(\d{4}) 年 [.：](.*?)(?=\d{4} 年|$)',
        r'(\d{4})[年](.*?)(?=\d{4}|$)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            year = int(match[0])
            desc = match[1].strip()[:200]  # 限制长度
            if 600 <= year <= 1000:  # 合理年份范围
                events.append({
                    'year': year,
                    'description': desc,
                })

    return events


def get_regime_color(regime_name: str) -> str:
    """获取政权颜色"""
    for r in WUDAI_REGIMES + SHIGUO_REGIMES:
        if r['name'] == regime_name:
            return r['color']
    return '#95a5a6'


def calculate_regime_stats() -> Dict:
    """计算政权统计数据"""
    all_regimes = WUDAI_REGIMES + SHIGUO_REGIMES

    stats = {
        'total_regimes': len(all_regimes),
        'wudai_count': len(WUDAI_REGIMES),
        'shiguo_count': len(SHIGUO_REGIMES),
        'total_years': max(r['end'] for r in all_regimes) - min(r['start'] for r in all_regimes),
        'avg_duration': sum(r['end'] - r['start'] for r in all_regimes) / len(all_regimes),
        'longest_regime': max(all_regimes, key=lambda x: x['end'] - x['start']),
        'shortest_regime': min(all_regimes, key=lambda x: x['end'] - x['start']),
    }

    return stats


def get_province_regime_mapping() -> pd.DataFrame:
    """获取省份 - 政权映射"""
    mapping = []
    for regime, provinces in REGIME_TO_PROVINCE.items():
        for province in provinces:
            mapping.append({
                'regime': regime,
                'province': province,
                'type': '五代' if regime in [r['name'] for r in WUDAI_REGIMES] else '十国'
            })

    return pd.DataFrame(mapping)


def generate_timeline_chart_data() -> Dict:
    """生成时间轴图表数据"""
    df = process_regime_timeline()

    chart_data = {
        'wudai': df[df['type'] == '五代'].to_dict('records'),
        'shiguo': df[df['type'] == '十国'].to_dict('records'),
    }

    return chart_data


def generate_map_data() -> List[Dict]:
    """生成地图数据"""
    mapping = get_province_regime_mapping()

    map_data = []
    for _, row in mapping.iterrows():
        map_data.append({
            'region': row['province'],
            'regime': row['regime'],
            'type': row['type'],
        })

    return map_data


if __name__ == "__main__":
    # 测试数据处理
    print("测试数据处理...")

    # 测试政权时间线
    timeline = process_regime_timeline()
    print(f"政权时间线：{len(timeline)} 条")

    # 测试统计数据
    stats = calculate_regime_stats()
    print(f"政权统计：{stats}")

    # 测试省份映射
    mapping = get_province_regime_mapping()
    print(f"省份映射：{len(mapping)} 条")
