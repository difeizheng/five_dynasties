"""
📺 数据可视化大屏
全屏展示模式，适合演示和监控
"""
import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import json

from src.data_processor import (
    WUDAI_REGIMES,
    SHIGUO_REGIMES,
    REGIME_COLORS,
    process_regime_timeline,
    get_province_regime_mapping,
)
from src.config import PROVINCE_MAPPING
from src.streamlit_utils import build_choropleth_map_html, build_simple_highlight_map_html


st.set_page_config(
    page_title="数据可视化大屏",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def render_header():
    """渲染大屏标题"""
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 1rem;
        margin-bottom: 1rem;
        color: white;
    }
    .main-header h1 {
        font-size: 2.5rem;
        margin: 0;
    }
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
    }
    .stat-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 1rem;
        padding: 1.5rem;
        text-align: center;
        color: white;
        height: 100%;
    }
    .stat-card h3 {
        font-size: 3rem;
        margin: 0;
    }
    .stat-card p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    .chart-container {
        background: white;
        border-radius: 1rem;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>

    <div class="main-header">
        <h1>🏯 五代十国历史信息可视化大屏</h1>
        <p>五代 • 十国 • 藩镇 • 人物</p>
    </div>
    """, unsafe_allow_html=True)


def render_stat_cards():
    """渲染统计卡片"""
    # 计算统计数据
    total_regimes = len(WUDAI_REGIMES) + len(SHIGUO_REGIMES)
    total_years = 979 - 907 + 1  # 从 907 年到 979 年

    # 统计人物数量
    from src.data_loader import load_wudai_characters
    characters_df = load_wudai_characters()
    total_characters = len(characters_df) if not characters_df.empty else 0

    # 统计藩镇数量
    from src.data_loader import load_fanzhen_complete
    fanzhen_data = load_fanzhen_complete()
    total_fanzhen = sum(len(df) for df in fanzhen_data.values()) if fanzhen_data else 0

    cols = st.columns(4)

    with cols[0]:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <h3>{total_regimes}</h3>
            <p>政权总数</p>
        </div>
        """, unsafe_allow_html=True)

    with cols[1]:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h3>{total_years}</h3>
            <p>历史跨度 (年)</p>
        </div>
        """, unsafe_allow_html=True)

    with cols[2]:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <h3>{total_characters}</h3>
            <p>收录人物</p>
        </div>
        """, unsafe_allow_html=True)

    with cols[3]:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <h3>{total_fanzhen}</h3>
            <p>藩镇数量</p>
        </div>
        """, unsafe_allow_html=True)


def render_regime_gird():
    """渲染政权网格"""
    st.markdown("### 🏛️ 政权列表")

    cols = st.columns(5)

    # 五代政权
    for idx, regime in enumerate(WUDAI_REGIMES):
        with cols[idx % 5]:
            color = REGIME_COLORS.get(regime['name'], '#999999')
            st.markdown(f"""
            <div style="
                background: {color}20;
                border-left: 4px solid {color};
                padding: 1rem;
                border-radius: 0.5rem;
                margin: 0.5rem 0;
            ">
                <h4 style="margin: 0; color: {color};">{regime['name']}</h4>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #666;">
                    {regime['start']}-{regime['end']} | {regime['capital']}
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    cols = st.columns(5)

    # 十国政权
    for idx, regime in enumerate(SHIGUO_REGIMES):
        with cols[idx % 5]:
            color = REGIME_COLORS.get(regime['name'], '#999999')
            st.markdown(f"""
            <div style="
                background: {color}20;
                border-left: 4px solid {color};
                padding: 1rem;
                border-radius: 0.5rem;
                margin: 0.5rem 0;
            ">
                <h4 style="margin: 0; color: {color};">{regime['name']}</h4>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #666;">
                    {regime['start']}-{regime['end']} | {regime['capital']}
                </p>
            </div>
            """, unsafe_allow_html=True)


def render_timeline_chart():
    """渲染时间轴图表"""
    from pyecharts.charts import Bar
    from pyecharts import options as opts

    st.markdown("### 📅 政权存续时间对比")

    # 准备数据
    all_regimes = WUDAI_REGIMES + SHIGUO_REGIMES
    names = [r['name'] for r in all_regimes]
    durations = [r['end'] - r['start'] for r in all_regimes]
    types = [r['type'] if isinstance(r.get('type'), str) else '十国' for r in all_regimes]

    bar = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))

    bar.add_xaxis(names)
    bar.add_yaxis(
        "存续时间",
        durations,
        label_opts=opts.LabelOpts(position="top"),
        itemstyle_opts=opts.ItemStyleOpts(
            color=lambda x: '#667eea' if x['name'] in [r['name'] for r in WUDAI_REGIMES] else '#f093fb'
        ),
    )

    bar.set_global_opts(
        title_opts=opts.TitleOpts(title=""),
        yaxis_opts=opts.AxisOpts(name="年"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            formatter="{b}<br/>存续：{c}年"
        ),
    )

    html_content = bar.render_embed()
    st.markdown(f'<div class="chart-container">{html_content}</div>', unsafe_allow_html=True)


def render_power_chart():
    """渲染政权实力对比图"""
    from pyecharts.charts import Gauge
    from pyecharts import options as opts

    st.markdown("### ⚔️ 政权实力评估")

    # 政权实力数据
    power_data = {
        "后周": 85,
        "南唐": 75,
        "后唐": 70,
        "后晋": 65,
        "前蜀": 60,
        "后蜀": 58,
        "南汉": 50,
        "吴越": 48,
        "北汉": 45,
        "楚": 42,
        "闽国": 40,
        "荆南": 25,
    }

    # 使用柱状图展示
    from pyecharts.charts import Bar

    names = list(power_data.keys())
    powers = list(power_data.values())

    bar = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))

    bar.add_xaxis(names)
    bar.add_yaxis(
        "实力值",
        powers,
        label_opts=opts.LabelOpts(position="top"),
    )

    bar.set_global_opts(
        title_opts=opts.TitleOpts(title=""),
        yaxis_opts=opts.AxisOpts(name="实力值", max_=100),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
    )

    html_content = bar.render_embed()
    st.markdown(f'<div class="chart-container">{html_content}</div>', unsafe_allow_html=True)


def render_area_chart():
    """渲染疆域面积对比图"""
    from pyecharts.charts import Pie
    from pyecharts import options as opts

    st.markdown("### 🗺️ 政权疆域占比")

    # 面积数据
    area_data = {
        "后周": 50,
        "南唐": 35,
        "前蜀": 25,
        "后蜀": 25,
        "南汉": 20,
        "楚": 21,
        "吴越": 12,
        "闽国": 12,
        "北汉": 8,
        "荆南": 3,
    }

    pie = Pie(init_opts=opts.InitOpts(width="100%", height="400px"))

    pie.add(
        "",
        [list(z) for z in area_data.items()],
        radius=["40%", "75%"],
        label_opts=opts.LabelOpts(formatter="{b}: {c}万 km²"),
    )

    pie.set_global_opts(
        title_opts=opts.TitleOpts(title=""),
        legend_opts=opts.LegendOpts(pos_top="5%", orient="vertical"),
    )

    html_content = pie.render_embed()
    st.markdown(f'<div class="chart-container">{html_content}</div>', unsafe_allow_html=True)


def render_map_section():
    """渲染地图区域"""
    st.markdown("### 🗺️ 政权疆域地图")

    # 读取 GeoJSON
    with open('china_full.geojson', 'r', encoding='utf-8') as f:
        china_geojson = f.read()

    mapping = get_province_regime_mapping()

    # 构建省份 - 政权映射
    province_info = {}
    regimes_in_map = set()

    for _, row in mapping.iterrows():
        province = PROVINCE_MAPPING.get(row['province'], row['province'])
        regime = row['regime']
        province_info[province] = {"regime": regime}
        regimes_in_map.add(regime)

    regimes_list = list(regimes_in_map)
    regime_value_map = {regime: idx + 1 for idx, regime in enumerate(regimes_list)}

    map_data = []
    for province, info in province_info.items():
        regime = info["regime"]
        map_data.append({
            "name": province,
            "value": regime_value_map[regime]
        })

    color_mapping = {
        value: REGIME_COLORS.get(regime, "#999999")
        for regime, value in regime_value_map.items()
    }

    tooltip_js = """function(params) {
        var regime = provinceRegimeMap[params.name] || '未知';
        return '<b>' + params.name + '</b><br/>所属政权：' + regime;
    }"""

    map_html = build_choropleth_map_html(
        geojson_content=china_geojson,
        map_data=map_data,
        value_mapping=regime_value_map,
        color_mapping=color_mapping,
        title="五代十国疆域范围",
        tooltip_formatter=tooltip_js,
        height=500,
    )

    st.markdown(f'<div class="chart-container">{map_html}</div>', unsafe_allow_html=True)


def render_auto_refresh():
    """渲染自动刷新功能"""
    st.markdown("---")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("🔄 大屏数据实时更新")

    with col2:
        # 显示当前时间
        import datetime
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(f"最后更新：{now}")

        if st.button("🔄 立即刷新"):
            st.rerun()


def main():
    """主函数"""
    render_header()
    render_stat_cards()

    st.markdown("---")

    # 第一行：地图和实力对比
    col1, col2 = st.columns([2, 1])
    with col1:
        render_map_section()
    with col2:
        render_power_chart()

    st.markdown("---")

    # 第二行：时间轴和疆域占比
    col1, col2 = st.columns([1, 1])
    with col1:
        render_timeline_chart()
    with col2:
        render_area_chart()

    st.markdown("---")

    # 政权列表
    render_regime_gird()

    st.markdown("---")

    # 自动刷新
    render_auto_refresh()

    # 全屏模式按钮
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
