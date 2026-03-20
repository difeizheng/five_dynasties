"""
数据处理模块
负责数据清洗、转换、分析
"""

import pandas as pd
import re
from typing import List, Dict, Tuple
from datetime import datetime
import streamlit as st

from src.config import (
    WUDAI_REGIMES,
    SHIGUO_REGIMES,
    REGIME_TO_PROVINCE,
    REGIME_COLORS,
    FANZHEN_COLORS,
    FANZHEN_BASE_DATA,
    MAJOR_EVENTS,
    WUDAI_SUCCESSION,
    SHIGUO_SUCCESSION,
    YEARLY_EVENTS,
    REGIME_POWER_DATA,
    REGIME_AREA_DATA,
    CAPITAL_TO_PROVINCE,
)


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
    return REGIME_COLORS.get(regime_name, '#95a5a6')


def calculate_regime_stats() -> Dict:
    """计算政权统计数据"""
    all_regimes = get_all_regimes()

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


def get_all_regimes():
    """获取所有政权列表"""
    return WUDAI_REGIMES + SHIGUO_REGIMES


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


def get_wudai_succession_data() -> Dict:
    """获取五代世系数据"""
    return WUDAI_SUCCESSION


def get_shiguo_succession_data() -> Dict:
    """获取十国世系数据"""
    return SHIGUO_SUCCESSION


def get_all_succession_data() -> Dict:
    """获取所有世系数据"""
    return {**WUDAI_SUCCESSION, **SHIGUO_SUCCESSION}


def get_fanzhen_base_data() -> Dict:
    """获取藩镇基础数据"""
    return FANZHEN_BASE_DATA


def get_major_events() -> List[Dict]:
    """获取重大事件列表"""
    return MAJOR_EVENTS


def get_yearly_events() -> Dict:
    """获取年度事件统计"""
    return YEARLY_EVENTS


def get_regime_power_data() -> List[Dict]:
    """获取政权实力对比数据"""
    return REGIME_POWER_DATA


def get_regime_area_data() -> Dict:
    """获取政权面积数据"""
    return REGIME_AREA_DATA


def get_capital_to_province() -> Dict:
    """获取都城到省份的映射"""
    return CAPITAL_TO_PROVINCE


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
