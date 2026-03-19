"""
📊 数据统计页面
各类统计图表和数据看板
"""
import streamlit as st
from streamlit.components.v1 import html

from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Radar, Funnel, WordCloud
import pandas as pd

from src.data_loader import (
    load_wudai_characters,
    load_wudai_detailed_characters,
    load_fanzhen_relationships,
    load_wudai_history_text,
)
from src.data_processor import (
    WUDAI_REGIMES,
    SHIGUO_REGIMES,
    REGIME_TO_PROVINCE,
    process_regime_timeline,
    calculate_regime_stats,
    get_regime_color,
    get_province_regime_mapping,
)
from src.text_analyzer import (
    extract_keywords,
    generate_wordcloud_data,
    analyze_text_statistics,
)

st.set_page_config(page_title="数据统计", page_icon="📊", layout="wide")


def render_stats_header():
    """渲染页面标题"""
    st.title("📊 数据统计看板")
    st.markdown("多维度数据分析图表")

    st.markdown("""
    **图表说明**：
    - 🥧 **政权存续时长分布**：展示五代和十国政权各自存续的总年数对比
    - 📊 **政权类型分布**：统计五代和十国政权的数量
    - 🏛️ **都城分布统计**：展示各都城（开封、洛阳、杭州等）作为政权中心的次数
    - 🗺️ **省份涉及政权数**：统计现代各省份在五代十国时期涉及到的政权数量
    - 🎯 **政权综合实力雷达图**：从存续时间、疆域面积、综合国力、文化发展、军事实力五个维度对比主要政权
    - 📅 **年度事件趋势**：展示 907-979 年间每年发生的重大历史事件数量变化
    - 📚 **文本统计**：分析《五代十国全史》的字符数、词数、高频关键词等
    """)

    st.markdown("---")


def render_overview_stats():
    """渲染总览统计"""
    stats = calculate_regime_stats()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("政权总数", stats['total_regimes'])

    with col2:
        st.metric("五代政权", stats['wudai_count'])

    with col3:
        st.metric("十国政权", stats['shiguo_count'])

    with col4:
        st.metric("历史跨度 (年)", stats['total_years'])

    with col5:
        st.metric("平均存续 (年)", f"{stats['avg_duration']:.1f}")


def render_regime_duration_pie():
    """渲染政权存续时长饼图"""
    df = process_regime_timeline()

    # 按类型分组
    wudai_duration = df[df['type'] == '五代']['duration'].sum()
    shiguo_duration = df[df['type'] == '十国']['duration'].sum()

    pie = Pie(init_opts=opts.InitOpts(width="100%", height="400px"))

    pie.add(
        "政权存续总年数",
        [
            ("五代", wudai_duration),
            ("十国", shiguo_duration),
        ],
        radius=["40%", "70%"],
    )

    pie.set_global_opts(
        title_opts=opts.TitleOpts(title="五代 vs 十国 存续总年数"),
        legend_opts=opts.LegendOpts(pos_top="5%", pos_left="5%"),
    )

    return pie


def render_regime_type_bar():
    """渲染政权类型柱状图"""
    df = process_regime_timeline()

    # 按类型统计
    type_counts = df.groupby('type').size().to_dict()

    bar = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))

    bar.add_xaxis(list(type_counts.keys()))
    bar.add_yaxis(
        "政权数量",
        list(type_counts.values()),
        label_opts=opts.LabelOpts(position="top"),
    )

    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="政权类型分布"),
        yaxis_opts=opts.AxisOpts(name="数量"),
    )

    return bar


def render_capital_distribution():
    """渲染都城分布统计"""
    df = process_regime_timeline()

    # 统计都城
    capital_counts = df['capital'].value_counts().to_dict()

    bar = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))

    bar.add_xaxis(list(capital_counts.keys()))
    bar.add_yaxis(
        "政权数量",
        list(capital_counts.values()),
        label_opts=opts.LabelOpts(position="top"),
    )

    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="都城分布统计"),
        yaxis_opts=opts.AxisOpts(name="政权数量"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)),
    )

    return bar


def render_province_distribution():
    """渲染省份分布统计"""
    mapping = get_province_regime_mapping()

    # 按省份统计
    province_counts = mapping.groupby('province').size().to_dict()

    # 排序
    sorted_provinces = sorted(province_counts.items(), key=lambda x: x[1], reverse=True)

    bar = Bar(init_opts=opts.InitOpts(width="100%", height="500px"))

    bar.add_xaxis([p[0] for p in sorted_provinces])
    bar.add_yaxis(
        "涉及政权数",
        [p[1] for p in sorted_provinces],
        label_opts=opts.LabelOpts(position="top"),
    )

    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="各省份涉及的政权数量"),
        yaxis_opts=opts.AxisOpts(name="数量"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
    )

    return bar


def render_regime_radar():
    """渲染政权对比雷达图"""
    # 选取主要政权进行对比
    regimes_to_compare = [
        {"name": "后周", "duration": 9, "area": 50, "power": 95, "culture": 80, "military": 95},
        {"name": "南唐", "duration": 38, "area": 35, "power": 85, "culture": 95, "military": 75},
        {"name": "吴越", "duration": 71, "area": 12, "power": 60, "culture": 85, "military": 70},
        {"name": "前蜀", "duration": 18, "area": 25, "power": 70, "culture": 75, "military": 65},
        {"name": "后蜀", "duration": 31, "area": 25, "power": 65, "culture": 80, "military": 60},
        {"name": "南汉", "duration": 54, "area": 20, "power": 50, "culture": 60, "military": 55},
    ]

    radar = Radar(init_opts=opts.InitOpts(width="100%", height="500px"))

    # 使用 RadarItem 构建数据
    data = [
        opts.RadarItem(
            name=regime['name'],
            value=[
                regime['duration'],
                regime['area'],
                regime['power'],
                regime['culture'],
                regime['military'],
            ],
        )
        for regime in regimes_to_compare
    ]

    radar.add("政权对比", data)

    # 手动添加 indicator 配置
    radar.options['radar'] = {
        'indicator': [
            {'name': '存续时间', 'max': 80},
            {'name': '疆域面积', 'max': 60},
            {'name': '综合国力', 'max': 100},
            {'name': '文化发展', 'max': 100},
            {'name': '军事实力', 'max': 100},
        ],
    }

    radar.set_global_opts(
        title_opts=opts.TitleOpts(title="主要政权综合实力对比"),
        legend_opts=opts.LegendOpts(type_="scroll", pos_bottom="10%"),
        tooltip_opts=opts.TooltipOpts(trigger="item"),
    )

    return radar


def render_death_reason_pie():
    """渲染死亡原因统计（模拟数据）"""
    # 模拟数据
    death_reasons = [
        ("病逝", 35),
        ("被杀", 25),
        ("自杀", 10),
        ("战死", 15),
        ("其他", 15),
    ]

    pie = Pie(init_opts=opts.InitOpts(width="100%", height="400px"))

    pie.add(
        "死亡原因",
        death_reasons,
        radius=["40%", "70%"],
    )

    pie.set_global_opts(
        title_opts=opts.TitleOpts(title="统治者死亡原因统计"),
        legend_opts=opts.LegendOpts(pos_top="5%", pos_left="5%"),
    )

    return pie


def render_text_statistics():
    """渲染文本统计"""
    st.subheader("📚 《五代十国全史》文本统计")

    try:
        text = load_wudai_history_text()

        if text:
            stats = analyze_text_statistics(text)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("总字符数", f"{stats['total_chars']:,}")

            with col2:
                st.metric("总词数", f"{stats['total_words']:,}")

            with col3:
                st.metric("不重复词数", f"{stats['unique_words']:,}")

            with col4:
                st.metric("段落数", f"{stats['paragraphs']:,}")

            # 关键词
            st.subheader("🔑 高频关键词")
            keywords = extract_keywords(text, top_n=20)

            keyword_df = pd.DataFrame(keywords, columns=["关键词", "频次"])
            st.dataframe(keyword_df, use_container_width=True)
        else:
            st.warning("未找到文本数据")
    except Exception as e:
        st.error(f"加载文本失败：{e}")


def render_yearly_events_chart():
    """渲染年度事件统计图"""
    from pyecharts.charts import Line

    # 模拟年度重大事件数量
    yearly_events = {
        907: 5, 908: 2, 909: 1, 910: 2, 911: 1,
        912: 3, 913: 2, 914: 1, 915: 2, 916: 1,
        917: 2, 918: 1, 919: 1, 920: 1, 921: 1,
        922: 2, 923: 4, 924: 2, 925: 3, 926: 3,
        927: 1, 928: 1, 929: 1, 930: 2, 931: 1,
        932: 2, 933: 2, 934: 3, 935: 1, 936: 4,
        937: 2, 938: 1, 939: 1, 940: 1, 941: 1,
        942: 2, 943: 2, 944: 1, 945: 3, 946: 1,
        947: 4, 948: 1, 949: 1, 950: 3, 951: 4,
        952: 1, 953: 1, 954: 3, 955: 2, 956: 2,
        957: 2, 958: 2, 959: 2, 960: 4, 961: 2,
        962: 1, 963: 3, 964: 1, 965: 3, 966: 1,
        967: 1, 968: 1, 969: 1, 970: 1, 971: 2,
        972: 1, 973: 1, 974: 1, 975: 3, 976: 1,
        977: 1, 978: 2, 979: 3,
    }

    line = Line(init_opts=opts.InitOpts(width="100%", height="400px"))

    line.add_xaxis(list(yearly_events.keys()))
    line.add_yaxis(
        "事件数量",
        list(yearly_events.values()),
        is_smooth=True,
        label_opts=opts.LabelOpts(is_show=False),
    )

    line.set_global_opts(
        title_opts=opts.TitleOpts(title="年度重大事件数量趋势 (907-979 年)"),
        xaxis_opts=opts.AxisOpts(name="年份"),
        yaxis_opts=opts.AxisOpts(name="事件数"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
    )

    return line


def main():
    """主函数"""
    render_stats_header()

    # 总览统计
    render_overview_stats()

    st.markdown("---")

    # 图表区域
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("政权存续时长分布")
        pie = render_regime_duration_pie()
        html(pie.render_embed(), height=650, scrolling=False)

    with col2:
        st.subheader("政权类型分布")
        bar = render_regime_type_bar()
        html(bar.render_embed(), height=650, scrolling=False)

    st.markdown("---")

    # 第二行
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("都城分布统计")
        bar = render_capital_distribution()
        html(bar.render_embed(), height=650, scrolling=False)

    with col2:
        st.subheader("省份涉及政权数")
        bar = render_province_distribution()
        html(bar.render_embed(), height=650, scrolling=False)

    st.markdown("---")

    # 雷达图
    st.subheader("🎯 政权综合实力雷达图")
    radar = render_regime_radar()
    html(radar.render_embed(), height=650, scrolling=False)

    st.markdown("---")

    # 年度事件趋势
    st.subheader("📅 年度事件趋势")
    line = render_yearly_events_chart()
    html(line.render_embed(), height=650, scrolling=False)

    st.markdown("---")

    # 文本统计
    render_text_statistics()


if __name__ == "__main__":
    main()

