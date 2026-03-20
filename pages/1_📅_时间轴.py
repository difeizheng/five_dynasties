"""
📅 时间轴页面
展示五代十国政权更迭和历史大事记
"""

import streamlit as st
from streamlit.components.v1 import html
from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline, Line
from pyecharts.commons.utils import JsCode
import pandas as pd

from src.data_processor import (
    WUDAI_REGIMES,
    SHIGUO_REGIMES,
    process_regime_timeline,
    get_regime_color,
    get_major_events,
)
from src.config import YEARLY_EVENTS

st.set_page_config(page_title="时间轴", page_icon="📅", layout="wide")

st.set_page_config(page_title="时间轴", page_icon="📅", layout="wide")

# 自定义 CSS
st.markdown("""
<style>
    .timeline-event {
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
        border-left: 4px solid;
    }
</style>
""", unsafe_allow_html=True)


def render_timeline_header():
    """渲染页面标题"""
    st.title("📅 历史时间轴")
    st.markdown("查看五代十国政权的更迭顺序和重大历史事件")

    st.markdown("""
    **图表说明**：
    - 📊 **政权更迭甘特图**：横向条形图展示各政权的存续时间，条形长度代表统治年数
    - 🏛️ **五代政权**：展示后梁、后唐、后晋、后汉、后周五个中原政权的更迭
    - 🌸 **十国政权**：展示吴越、南唐、前后蜀等十个割据政权的并存情况
    - ⏳ **五代 vs 十国对比**：折线图展示同时期存在的政权数量变化
    - 📜 **重大历史事件**：按时间顺序列出改朝换代的关键节点
    """)

    st.markdown("---")


def render_timeline_filters():
    """渲染时间轴筛选器"""
    st.sidebar.subheader("🔍 筛选条件")

    # 时间范围筛选
    st.sidebar.markdown("**📅 时间范围**")
    min_year, max_year = st.sidebar.slider(
        "选择年份范围",
        min_value=900,
        max_value=980,
        value=(907, 979),
        step=1,
        key="year_range_slider"
    )

    # 政权类型筛选
    st.sidebar.markdown("**🏛️ 政权类型**")
    regime_type = st.sidebar.multiselect(
        "选择政权类型",
        options=["五代", "十国"],
        default=["五代", "十国"],
        key="regime_type_filter"
    )

    # 事件类型筛选
    st.sidebar.markdown("**📜 事件类型**")
    event_types = st.sidebar.multiselect(
        "选择事件类型",
        options=["建国", "战争", "政变", "禅让", "统一"],
        default=["建国", "战争", "政变", "禅让", "统一"],
        key="event_type_filter"
    )

    return min_year, max_year, regime_type, event_types


def render_filtered_events(min_year: int, max_year: int, event_types: list):
    """渲染筛选后的事件列表"""
    all_events = get_major_events()

    # 筛选事件
    filtered_events = [e for e in all_events if min_year <= e['year'] <= max_year]

    # 简单的事件类型分类（根据关键词）
    type_keywords = {
        "建国": ["建立", "篡", "开国"],
        "战争": ["灭", "战", "入侵"],
        "政变": ["兵变", "杀", "篡位"],
        "禅让": ["禅让", "归降", "投降"],
        "统一": ["统一", "结束"],
    }

    st.subheader(f"📜 重大历史事件 ({len(filtered_events)}个)")

    for event in filtered_events:
        # 判断事件类型
        event_type = "其他"
        for etype, keywords in type_keywords.items():
            if any(kw in event['event'] for kw in keywords):
                event_type = etype
                break

        # 只显示选中的事件类型
        if event_type not in event_types and event_type != "其他":
            continue

        regime_color = get_regime_color(event['regime'].split('/')[0])
        st.markdown(
            f"""
            <div class="timeline-event" style="border-left-color: {regime_color}; background: {regime_color}15;">
                <strong>{event['year']}年</strong> <span style="color: {regime_color}; font-size: 0.8em;">[{event_type}]</span> [{event['regime']}] {event['event']}
            </div>
            """,
            unsafe_allow_html=True
        )

    if not filtered_events:
        st.info("该时间范围内没有事件")

    return filtered_events


def render_regime_gantt():
    """渲染政权甘特图 - 改进版"""
    df = process_regime_timeline()

    # 自定义 CSS 美化甘特图
    st.markdown("""
    <style>
    .gantt-note {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
    <div class="gantt-note">
        💡 <strong>查看提示</strong>：鼠标悬停在色块上可查看详情，点击图例可隐藏/显示特定政权
    </div>
    """, unsafe_allow_html=True)

    # 分离五代和十国，分开显示更清晰
    wudai_df = df[df['type'] == '五代'].sort_values('start')
    shiguo_df = df[df['type'] == '十国'].sort_values('start', ascending=False)

    # 构建五代政权的起始年份和结束年份映射
    wudai_info = {row['name']: {'start': row['start'], 'end': row['end'], 'duration': row['duration']}
                  for _, row in wudai_df.iterrows()}

    # 创建甘特图 - 五代部分
    bar_wudai = Bar(init_opts=opts.InitOpts(width="100%", height="350px"))
    bar_wudai.add_xaxis([str(y) for y in range(905, 985, 5)])

    tooltip_formatter = """
        function(params) {
            var name = params.seriesName;
            var data = params.data;
            return '<b>' + name + '</b><br/>' +
                   '起始：' + data.start + '年<br/>' +
                   '结束：' + data.end + '年<br/>' +
                   '存续：' + data.duration + '年';
        }
    """

    for _, row in wudai_df.iterrows():
        # 创建起始占位数据
        values = [0] * ((row['start'] - 905) // 5)
        values.append(row['duration'])  # 政权存续时长
        values += [0] * (len(range(905, 985, 5)) - len(values))
        values = values[:len(range(905, 985, 5))]  # 截断到正确长度

        # 添加自定义数据项，包含起始、结束年份
        data_items = []
        for i, v in enumerate(values):
            if v > 0:
                data_items.append({
                    'value': v,
                    'start': row['start'],
                    'end': row['end'],
                    'duration': row['duration']
                })
            else:
                data_items.append({'value': v, 'start': 0, 'end': 0, 'duration': 0})

        bar_wudai.add_yaxis(
            row['name'],
            data_items,
            label_opts=opts.LabelOpts(position="inside", formatter="{b}: {c}年"),
            itemstyle_opts=opts.ItemStyleOpts(color=row['color'], border_radius=3),
            stack="wudai",
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
                formatter=JsCode(tooltip_formatter)
            ),
        )

    bar_wudai.set_global_opts(
        title_opts=opts.TitleOpts(title="🏛️ 五代政权 (907-960 年)", pos_top="0"),
        xaxis_opts=opts.AxisOpts(
            name="公元年份",
            type_="category",
            axislabel_opts=opts.LabelOpts(rotate=0),
        ),
        yaxis_opts=opts.AxisOpts(name=""),
        legend_opts=opts.LegendOpts(type_="scroll", pos_top="90%"),
    )
    bar_wudai.reversal_axis()

    # 构建十国政权的起始年份和结束年份映射
    shiguo_info = {row['name']: {'start': row['start'], 'end': row['end'], 'duration': row['duration']}
                   for _, row in shiguo_df.iterrows()}

    # 创建甘特图 - 十国部分
    bar_shiguo = Bar(init_opts=opts.InitOpts(width="100%", height="500px"))
    bar_shiguo.add_xaxis([str(y) for y in range(895, 985, 5)])

    tooltip_formatter_shiguo = """
        function(params) {
            var name = params.seriesName;
            var data = params.data;
            return '<b>' + name + '</b><br/>' +
                   '起始：' + data.start + '年<br/>' +
                   '结束：' + data.end + '年<br/>' +
                   '存续：' + data.duration + '年';
        }
    """

    for _, row in shiguo_df.iterrows():
        values = [0] * ((row['start'] - 895) // 5)
        values.append(row['duration'])
        values += [0] * (len(range(895, 985, 5)) - len(values))
        values = values[:len(range(895, 985, 5))]

        # 添加自定义数据项，包含起始、结束年份
        data_items = []
        for i, v in enumerate(values):
            if v > 0:
                data_items.append({
                    'value': v,
                    'start': row['start'],
                    'end': row['end'],
                    'duration': row['duration']
                })
            else:
                data_items.append({'value': v, 'start': 0, 'end': 0, 'duration': 0})

        bar_shiguo.add_yaxis(
            row['name'],
            data_items,
            label_opts=opts.LabelOpts(position="inside", formatter="{b}: {c}年"),
            itemstyle_opts=opts.ItemStyleOpts(color=row['color'], border_radius=3),
            stack="shiguo",
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
                formatter=JsCode(tooltip_formatter_shiguo)
            ),
        )

    bar_shiguo.set_global_opts(
        title_opts=opts.TitleOpts(title="🌸 十国政权 (891-979 年)", pos_top="0"),
        xaxis_opts=opts.AxisOpts(
            name="公元年份",
            type_="category",
            axislabel_opts=opts.LabelOpts(rotate=0),
        ),
        yaxis_opts=opts.AxisOpts(name=""),
        legend_opts=opts.LegendOpts(type_="scroll", pos_top="95%"),
    )
    bar_shiguo.reversal_axis()

    return bar_wudai, bar_shiguo


def render_wudai_timeline():
    """渲染五代时间线"""
    st.subheader("🏛️ 五代政权更迭")

    # 创建时间线组件
    timeline = Timeline(init_opts=opts.InitOpts(width="100%", height="400px"))

    years = list(range(907, 961, 5))

    for year in years:
        bar = Bar()
        bar.add_xaxis(["后梁", "后唐", "后晋", "后汉", "后周"])

        values = []
        for regime in WUDAI_REGIMES:
            if regime['start'] <= year < regime['end']:
                values.append(1)
            else:
                values.append(0)

        bar.add_yaxis("存在", values, color="#3b82f6")

        bar.set_global_opts(
            title_opts=opts.TitleOpts(title=f"{year}年"),
            yaxis_opts=opts.AxisOpts(max_=1.5),
        )

        timeline.add(bar, str(year))

    return timeline


def render_shiguo_timeline():
    """渲染十国时间线"""
    st.subheader("🌸 十国政权更迭")

    # 创建时间线组件
    timeline = Timeline(init_opts=opts.InitOpts(width="100%", height="400px"))

    years = list(range(907, 980, 5))

    for year in years:
        bar = Bar()
        regime_names = [r['name'] for r in SHIGUO_REGIMES]
        bar.add_xaxis(regime_names)

        values = []
        for regime in SHIGUO_REGIMES:
            if regime['start'] <= year < regime['end']:
                values.append(1)
            else:
                values.append(0)

        bar.add_yaxis("存在", values, color="#10b981")

        bar.set_global_opts(
            title_opts=opts.TitleOpts(title=f"{year}年"),
            yaxis_opts=opts.AxisOpts(max_=1.5),
        )

        timeline.add(bar, str(year))

    return timeline


def render_major_events():
    """渲染重大事件"""
    st.subheader("📜 重大历史事件")

    events = get_major_events()

    # 使用列表展示
    for event in events:
        regime_color = get_regime_color(event['regime'].split('/')[0])
        st.markdown(
            f"""
            <div class="timeline-event" style="border-left-color: {regime_color}; background: {regime_color}15;">
                <strong>{event['year']}年</strong> [{event['regime']}] {event['event']}
            </div>
            """,
            unsafe_allow_html=True
        )

    return events


def render_timeline_comparison():
    """渲染时间线对比图"""
    st.subheader("⏳ 五代 vs 十国 时间线对比")

    df = process_regime_timeline()

    # 创建 Line 图
    line = Line(init_opts=opts.InitOpts(width="100%", height="400px"))
    line.add_xaxis([str(y) for y in range(900, 985, 5)])

    # 计算每个时间点存在的政权数量
    wudai_counts = []
    shiguo_counts = []

    for year in range(900, 985, 5):
        wudai_count = sum(1 for r in WUDAI_REGIMES if r['start'] <= year < r['end'])
        shiguo_count = sum(1 for r in SHIGUO_REGIMES if r['start'] <= year < r['end'])
        wudai_counts.append(wudai_count)
        shiguo_counts.append(shiguo_count)

    line.add_yaxis("五代", wudai_counts, color="#3b82f6")
    line.add_yaxis("十国", shiguo_counts, color="#10b981")

    line.set_global_opts(
        title_opts=opts.TitleOpts(title="同时期政权数量对比"),
        xaxis_opts=opts.AxisOpts(name="年份"),
        yaxis_opts=opts.AxisOpts(name="政权数量"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
    )

    return line


def main():
    """主函数"""
    render_timeline_header()

    # 侧边栏筛选器
    min_year, max_year, regime_type, event_types = render_timeline_filters()

    # 甘特图 - 分开展示更清晰
    st.subheader("📊 政权更迭甘特图")
    wudai_gantt, shiguo_gantt = render_regime_gantt()

    st.markdown("### 🏛️ 五代政权")
    html(wudai_gantt.render_embed(), height=450, scrolling=False)

    st.markdown("### 🌸 十国政权")
    html(shiguo_gantt.render_embed(), height=600, scrolling=False)

    st.markdown("---")

    # 并排展示
    col1, col2 = st.columns(2)

    with col1:
        timeline_wudai = render_wudai_timeline()
        html(timeline_wudai.render_embed(), height=600, scrolling=False)

    with col2:
        timeline_shiguo = render_shiguo_timeline()
        html(timeline_shiguo.render_embed(), height=600, scrolling=False)

    st.markdown("---")

    # 对比图
    comparison_chart = render_timeline_comparison()
    html(comparison_chart.render_embed(), height=600, scrolling=False)

    st.markdown("---")

    # 重大事件（带筛选）
    render_filtered_events(min_year, max_year, event_types)


if __name__ == "__main__":
    main()
