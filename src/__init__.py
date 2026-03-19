"""
五代十国历史信息可视化系统 - 数据处理模块
"""

from .data_loader import (
    load_excel_data,
    load_all_sheets,
    load_txt_data,
    load_wudai_characters,
    load_wudai_detailed_characters,
    load_fanzhen_relationships,
    load_fanzhen_complete,
    load_tang_fanzhen,
    load_tang_emperors,
    load_history_timeline,
    load_wudai_history_text,
    init_database,
    get_db_path,
)

from .data_processor import (
    WUDAI_REGIMES,
    SHIGUO_REGIMES,
    REGIME_TO_PROVINCE,
    parse_year_range,
    process_regime_timeline,
    process_characters_data,
    process_fanzhen_data,
    get_regime_color,
    calculate_regime_stats,
    get_province_regime_mapping,
    generate_timeline_chart_data,
    generate_map_data,
)

from .text_analyzer import (
    segment_text,
    extract_keywords,
    extract_keywords_by_category,
    generate_wordcloud_data,
    search_text,
    analyze_text_statistics,
    get_text_summary,
)

__all__ = [
    # data_loader
    'load_excel_data',
    'load_all_sheets',
    'load_txt_data',
    'load_wudai_characters',
    'load_wudai_detailed_characters',
    'load_fanzhen_relationships',
    'load_fanzhen_complete',
    'load_tang_fanzhen',
    'load_tang_emperors',
    'load_history_timeline',
    'load_wudai_history_text',
    'init_database',
    'get_db_path',
    # data_processor
    'WUDAI_REGIMES',
    'SHIGUO_REGIMES',
    'REGIME_TO_PROVINCE',
    'parse_year_range',
    'process_regime_timeline',
    'process_characters_data',
    'process_fanzhen_data',
    'get_regime_color',
    'calculate_regime_stats',
    'get_province_regime_mapping',
    'generate_timeline_chart_data',
    'generate_map_data',
    # text_analyzer
    'segment_text',
    'extract_keywords',
    'extract_keywords_by_category',
    'generate_wordcloud_data',
    'search_text',
    'analyze_text_statistics',
    'get_text_summary',
]
