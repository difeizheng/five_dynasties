"""
🌍 世界历史年表对照
展示五代十国时期同期世界各地区的政权和重大事件
"""

import streamlit as st
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Timeline, Bar, Line

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import (
    get_world_timeline,
    get_world_major_events,
    get_world_regions,
    get_all_world_events,
    get_all_territory_years,
    get_territory_by_year,
)

st.set_page_config(
    page_title="世界历史年表对照",
    page_icon="🌍",
    layout="wide"
)

# 标题
st.title("🌍 世界历史年表对照")
st.markdown("展示五代十国时期（907-979 年）同期世界各地区的政权和重大事件")

st.markdown("""
**页面说明**：
- 📅 **时间轴对照**：按年份展示中国与世界同期发生的重大事件
- 🗺️ **地区政权**：按地区查看同期存在的主要政权
- 📊 **政权存续时间对比**：对比各政权的存续时间
""")

st.markdown("---")

# ============================================
# 侧边栏筛选器
# ============================================
st.sidebar.header("筛选条件")

# 地区筛选
regions = get_world_regions()
selected_region = st.sidebar.multiselect(
    "选择地区",
    options=regions,
    default=regions
)

# 年份范围
min_year = 907
max_year = 979
year_range = st.sidebar.slider(
    "年份范围",
    min_value=min_year,
    max_value=max_year,
    value=(907, 979)
)

# ============================================
# 选项卡布局
# ============================================
tab1, tab2, tab3, tab4 = st.tabs(["时间轴对照", "地区政权", "重大事件", "政权存续对比"])

# --------------------------------------------
# 选项卡 1: 时间轴对照
# --------------------------------------------
with tab1:
    st.subheader("📅 时间轴对照")
    st.markdown("按年份展示中国与世界同期发生的重大事件")

    # 获取所有事件
    china_events = get_all_world_events()

    # 按年份分组
    events_by_year = {}
    for event in china_events:
        year = event['year']
        if year not in events_by_year:
            events_by_year[year] = {"中国": [], "世界": []}

        if event['region'] == "中国":
            events_by_year[year]["中国"].append(event['event'])
        else:
            events_by_year[year]["世界"].append(f"{event['region']}: {event['event']}")

    # 显示时间轴
    for year in sorted(events_by_year.keys()):
        if year_range[0] <= year <= year_range[1]:
            data = events_by_year[year]

            with st.expander(f"**{year}年**", expanded=False):
                col1, col2 = st.columns(2)

                with col1:
                    if data["中国"]:
                        st.markdown("**🇨🇳 中国**:")
                        for event in data["中国"]:
                            st.markdown(f"- {event}")

                with col2:
                    if data["世界"]:
                        st.markdown("**🌍 世界**:")
                        for event in data["世界"]:
                            st.markdown(f"- {event}")

# --------------------------------------------
# 选项卡 2: 地区政权
# --------------------------------------------
with tab2:
    st.subheader("🗺️ 地区政权")
    st.markdown("按地区查看同期存在的主要政权")

    all_timeline = get_world_timeline()

    for region in selected_region:
        st.markdown(f"### {region}")

        region_data = all_timeline.get(region, {})

        if not region_data:
            st.info(f"暂无{region}数据")
            continue

        cols = st.columns(2)

        for i, (regime, info) in enumerate(region_data.items()):
            with cols[i % 2]:
                # 检查政权是否在选定年份范围内存在
                start = info.get('start', 0)
                end = info.get('end', 9999)

                is_active = not (end < year_range[0] or start > year_range[1])

                if is_active:
                    st.markdown(f"#### {regime}")
                    st.markdown(f"- **存在时间**: {start}年 - {end}年")
                    st.markdown(f"- **都城**: {info.get('capital', '未知')}")
                    st.markdown(f"- **建立者**: {info.get('founder', '未知')}")
                    st.markdown(f"- **简介**: {info.get('description', '')}")

        st.markdown("---")

# --------------------------------------------
# 选项卡 3: 重大事件
# --------------------------------------------
with tab3:
    st.subheader("📊 重大事件列表")
    st.markdown("筛选条件内的所有重大事件")

    # 获取筛选后的事件
    events = get_all_world_events()
    events = [e for e in events if year_range[0] <= e['year'] <= year_range[1]]

    if selected_region:
        # 添加"中国"到筛选条件
        filter_regions = selected_region + ["中国"]
        events = [e for e in events if e['region'] in filter_regions]

    # 创建 DataFrame
    df_events = pd.DataFrame(events)

    if not df_events.empty:
        # 按年份排序
        df_events = df_events.sort_values('year')

        # 显示表格
        st.dataframe(
            df_events[['year', 'region', 'event']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "year": st.column_config.NumberColumn("年份"),
                "region": st.column_config.TextColumn("地区"),
                "event": st.column_config.TextColumn("事件")
            }
        )
    else:
        st.info("暂无符合条件的事件")

# --------------------------------------------
# 选项卡 4: 政权存续对比
# --------------------------------------------
with tab4:
    st.subheader("📈 政权存续时间对比")
    st.markdown("对比各政权的存续时间")

    # 收集所有政权
    all_regimes = []

    # 中国政权
    from src.config import get_all_regimes
    for regime in get_all_regimes():
        all_regimes.append({
            "name": regime['name'],
            "start": regime['start'],
            "end": regime['end'],
            "region": "中国",
            "duration": regime['end'] - regime['start'] + 1
        })

    # 世界政权
    world_timeline = get_world_timeline()
    for region, regimes in world_timeline.items():
        for regime, info in regimes.items():
            duration = info.get('end', 979) - info.get('start', 907)
            all_regimes.append({
                "name": regime,
                "start": info.get('start', 0),
                "end": info.get('end', 9999),
                "region": region,
                "duration": duration
            })

    # 创建 DataFrame
    df_regimes = pd.DataFrame(all_regimes)

    # 筛选在时间范围内的政权
    df_regimes = df_regimes[
        (df_regimes['start'] <= year_range[1]) &
        (df_regimes['end'] >= year_range[0])
    ]

    # 按存续时间排序
    df_regimes = df_regimes.sort_values('duration', ascending=False)

    # 显示前 20 个政权
    top_20 = df_regimes.head(20)

    # 柱状图
    bar = Bar(init_opts=opts.InitOpts(width="100%", height="500px"))
    bar.add_xaxis(top_20['name'].tolist())
    bar.add_yaxis("存续时间（年）", top_20['duration'].tolist())
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="政权存续时间 Top 20"),
        xaxis_opts=opts.AxisOpts(name="政权", axislabel_opts={"rotate": 45}),
        yaxis_opts=opts.AxisOpts(name="存续时间（年）"),
        datazoom_opts=opts.DataZoomOpts(type_="slider"),
    )

    st.components.v1.html(bar.render_embed(), height=550, scrolling=False)

    # 显示详细数据
    st.markdown("### 详细数据")
    st.dataframe(
        df_regimes[['name', 'region', 'start', 'end', 'duration']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "name": "政权名称",
            "region": "地区",
            "start": "开始年份",
            "end": "结束年份",
            "duration": "存续时间（年）"
        }
    )

# 页脚
st.markdown("---")
st.markdown("数据来源：历史资料整理")
