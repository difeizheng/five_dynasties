"""
五代十国历史信息可视化系统
主应用入口
"""

from streamlit.components.v1 import html

import streamlit as st
from src.data_loader import (
    load_wudai_characters,
    load_wudai_detailed_characters,
    load_fanzhen_relationships,
    load_wudai_history_text,
)
from src.data_processor import (
    WUDAI_REGIMES,
    SHIGUO_REGIMES,
    process_regime_timeline,
    calculate_regime_stats,
    get_regime_color,
)
from src.config import REGIME_COLORS, CAPITAL_TO_PROVINCE
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Timeline, Grid
from pyecharts.commons.utils import JsCode
import pandas as pd

# 页面配置
st.set_page_config(
    page_title="五代十国历史信息可视化系统",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 自定义 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        text-align: center;
        padding: 1rem 0;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
    }
    .regime-tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 2rem;
        font-size: 0.875rem;
        margin: 0.25rem;
    }
    .dataframe {
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


def render_header():
    """渲染页眉"""
    st.markdown('<p class="main-header">📜 五代十国历史信息可视化系统</p>', unsafe_allow_html=True)
    st.markdown("---")


def render_stats_cards():
    """渲染统计卡片"""
    stats = calculate_regime_stats()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🏛️ 政权总数",
            value=stats['total_regimes'],
            delta=f"五代{stats['wudai_count']} | 十国{stats['shiguo_count']}"
        )

    with col2:
        st.metric(
            label="⏳ 历史跨度",
            value=f"{stats['total_years']}年",
            delta="907-979 年"
        )

    with col3:
        st.metric(
            label="📊 平均存续",
            value=f"{stats['avg_duration']:.1f}年",
            delta=f"最长:{stats['longest_regime']['name']}"
        )

    with col4:
        st.metric(
            label="📚 史料文本",
            value="6.7MB",
            delta="五代十国全史"
        )


def render_regime_timeline_chart():
    """渲染政权时间轴图表"""
    df = process_regime_timeline()

    # 创建条形图
    bar = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))

    wudai = df[df['type'] == '五代']
    shiguo = df[df['type'] == '十国']

    bar.add_xaxis(list(range(900, 990, 10)))

    # 添加五代数据
    for _, row in wudai.iterrows():
        bar.add_yaxis(
            row['name'],
            [row['duration'] if row['start'] <= x < row['end'] else 0 for x in range(900, 990, 10)],
            label_opts=opts.LabelOpts(is_show=False),
        )

    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="五代十国政权存续时间"),
        xaxis_opts=opts.AxisOpts(name="年份"),
        yaxis_opts=opts.AxisOpts(name="政权"),
        legend_opts=opts.LegendOpts(is_show=True),
    )

    return bar


def render_regime_distribution():
    """渲染政权分布饼图"""
    df = process_regime_timeline()

    # 按类型分组
    wudai_count = len(df[df['type'] == '五代'])
    shiguo_count = len(df[df['type'] == '十国'])

    pie = Pie(init_opts=opts.InitOpts(width="100%", height="400px"))

    pie.add(
        "",
        [
            ("五代", wudai_count),
            ("十国", shiguo_count),
        ],
        radius=["40%", "70%"],
    )

    pie.set_global_opts(
        title_opts=opts.TitleOpts(title="政权类型分布"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
    )

    return pie


def render_regime_duration_bar():
    """渲染政权存续时长柱状图"""
    df = process_regime_timeline()

    # 按存续时间排序
    df_sorted = df.sort_values('duration', ascending=True)

    bar = Bar(init_opts=opts.InitOpts(width="100%", height="500px"))

    bar.add_xaxis(df_sorted['name'].tolist())
    bar.add_yaxis(
        "存续年数",
        df_sorted['duration'].tolist(),
        label_opts=opts.LabelOpts(position="right"),
    )

    bar.reversal_axis()

    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="政权存续时长排名"),
        xaxis_opts=opts.AxisOpts(name="年数"),
        yaxis_opts=opts.AxisOpts(name="政权"),
    )

    return bar


def render_capital_map():
    """渲染都城分布图（简化版）"""
    df = process_regime_timeline()

    # 都城对应省份 - 使用统一配置
    capital_to_province = CAPITAL_TO_PROVINCE

    capitals = df['capital'].unique()
    province_count = {}

    for capital in capitals:
        if capital in capital_to_province:
            province = capital_to_province[capital]
            province_count[province] = province_count.get(province, 0) + 1

    # 使用地图表示都城分布
    from pyecharts.charts import Map

    m = Map(init_opts=opts.InitOpts(width="100%", height="500px"))

    data = list(province_count.items())

    m.add(
        "都城分布",
        data,
        maptype="china",
    )

    m.set_global_opts(
        title_opts=opts.TitleOpts(title="五代十国都城分布"),
        visualmap_opts=opts.VisualMapOpts(),
    )

    return m


def main():
    """主函数"""
    render_header()

    # 统计卡片
    render_stats_cards()

    st.markdown("---")

    # 内容区域
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏛️ 五代政权")
        wudai_df = pd.DataFrame(WUDAI_REGIMES)
        for _, row in wudai_df.iterrows():
            st.markdown(
                f"**{row['name']}** ({row['start']}-{row['end']}) "
                f"都城：{row['capital']} 开国：{row['founder']}"
            )

    with col2:
        st.subheader("🌸 十国政权")
        shiguo_df = pd.DataFrame(SHIGUO_REGIMES)
        for _, row in shiguo_df.iterrows():
            st.markdown(
                f"**{row['name']}** ({row['start']}-{row['end']}) "
                f"都城：{row['capital']} 开国：{row['founder']}"
            )

    st.markdown("---")

    # 图表区域
    st.subheader("📊 数据可视化")

    tab1, tab2, tab3 = st.tabs(["存续时间", "政权分布", "时长排名"])

    with tab1:
        chart = render_regime_timeline_chart()
        html(chart.render_embed(), height=600, scrolling=False)

    with tab2:
        chart = render_regime_distribution()
        html(chart.render_embed(), height=600, scrolling=False)

    with tab3:
        chart = render_regime_duration_bar()
        html(chart.render_embed(), height=600, scrolling=False)

    # 底部信息
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #6b7280; padding: 1rem;">
            五代十国历史信息可视化系统 v1.0 | 基于 Streamlit 构建
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
