"""
💰 经济文化地图
展示五代十国时期的经济发展、文化中心、贸易路线和宗教分布
"""

import streamlit as st
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Map, Line, Graph
from pyecharts.globals import ChartType

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import (
    get_economy_data,
    get_cultural_centers,
    get_trade_routes,
    get_religion_data,
    get_art_works,
    get_regime_area_colors,
    PROVINCE_MAPPING,
)

st.set_page_config(
    page_title="经济文化地图",
    page_icon="💰",
    layout="wide"
)

# 标题
st.title("💰 经济文化地图")
st.markdown("展示五代十国时期的经济发展、文化中心、贸易路线和宗教分布")

st.markdown("""
**页面说明**：
- 📊 **经济对比**：各国人口、税收、产业发展对比
- 🏛️ **文化中心**：各地文化中心分布和代表人物
- 🛣️ **贸易路线**：陆路丝绸之路、海上丝绸之路、长江商路、大运河
- 🏯 **宗教分布**：佛教、道教、儒学的中心分布
- 🎨 **艺术作品**：绘画、书法、陶瓷等艺术成就
""")

st.markdown("---")

# ============================================
# 选项卡布局
# ============================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "经济对比", "文化中心", "贸易路线", "宗教分布", "艺术作品"
])

# --------------------------------------------
# 选项卡 1: 经济对比
# --------------------------------------------
with tab1:
    st.subheader("📊 各国经济对比")

    economy_data = get_economy_data()

    # 创建 DataFrame
    df_economy = pd.DataFrame([
        {
            "政权": regime,
            "人口 (万户)": data.get('population', 0),
            "税收 (万贯/年)": data.get('tax', 0),
            "农业指数": data.get('agriculture', 0),
            "商业指数": data.get('commerce', 0),
            "手工业指数": data.get('industry', 0),
        }
        for regime, data in economy_data.items()
    ])

    # 排序
    df_economy = df_economy.sort_values("税收 (万贯/年)", ascending=False)

    # 显示表格
    st.dataframe(df_economy, use_container_width=True, hide_index=True)

    st.markdown("---")

    # 图表对比
    col1, col2 = st.columns(2)

    with col1:
        # 人口对比
        bar_population = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))
        bar_population.add_xaxis(df_economy["政权"].tolist())
        bar_population.add_yaxis("人口 (万户)", df_economy["人口 (万户)"].tolist())
        bar_population.set_global_opts(
            title_opts=opts.TitleOpts(title="各国人口对比"),
            xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45}),
            yaxis_opts=opts.AxisOpts(name="万户"),
        )
        st.components.v1.html(bar_population.render_embed(), height=450, scrolling=False)

    with col2:
        # 税收对比
        bar_tax = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))
        bar_tax.add_xaxis(df_economy["政权"].tolist())
        bar_tax.add_yaxis("税收 (万贯/年)", df_economy["税收 (万贯/年)"].tolist())
        bar_tax.set_global_opts(
            title_opts=opts.TitleOpts(title="各国税收对比"),
            xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45}),
            yaxis_opts=opts.AxisOpts(name="万贯/年"),
        )
        st.components.v1.html(bar_tax.render_embed(), height=450, scrolling=False)

    st.markdown("---")

    # 雷达图 - 综合发展对比
    st.subheader("🕸️ 综合发展对比")

    selected_regimes = st.multiselect(
        "选择政权进行对比",
        options=list(economy_data.keys()),
        default=["南唐", "后周", "吴越"]
    )

    if selected_regimes:
        # 准备雷达图数据
        indicator = [
            {"name": "农业", "max": 100},
            {"name": "商业", "max": 100},
            {"name": "手工业", "max": 100},
            {"name": "人口", "max": 1000},
            {"name": "税收", "max": 200},
        ]

        radar_data = []
        for regime in selected_regimes:
            data = economy_data.get(regime, {})
            radar_data.append({
                "name": regime,
                "value": [
                    data.get('agriculture', 0),
                    data.get('commerce', 0),
                    data.get('industry', 0),
                    data.get('population', 0),
                    data.get('tax', 0),
                ]
            })

        from pyecharts.charts import Radar
        radar = Radar(init_opts=opts.InitOpts(width="100%", height="500px"))
        radar.add_schema(schema=indicator)
        radar.add(
            series_name="综合发展对比",
            data=radar_data,
        )
        radar.set_global_opts(
            title_opts=opts.TitleOpts(title="各国综合发展雷达图"),
            legend_opts=opts.LegendOpts(pos_bottom="10%"),
        )
        st.components.v1.html(radar.render_embed(), height=550, scrolling=False)

# --------------------------------------------
# 选项卡 2: 文化中心
# --------------------------------------------
with tab2:
    st.subheader("🏛️ 文化中心分布")

    cultural_centers = get_cultural_centers()

    # 显示文化中心列表
    for center in cultural_centers:
        with st.expander(f"**{center['name']}** - {center['type']} ({center['regime']})"):
            st.markdown(f"**代表人物**: {', '.join(center.get('figures', ['无']))}")
            st.markdown(f"**简介**: {center.get('description', '')}")

    st.markdown("---")

    # 文化中心类型统计
    type_count = {}
    for center in cultural_centers:
        t = center.get('type', '其他')
        type_count[t] = type_count.get(t, 0) + 1

    col1, col2 = st.columns(2)

    with col1:
        # 饼图
        pie = Pie(init_opts=opts.InitOpts(width="100%", height="400px"))
        pie.add(
            "文化中心类型",
            [(k, v) for k, v in type_count.items()],
            radius=["40%", "75%"]
        )
        pie.set_global_opts(title_opts=opts.TitleOpts(title="文化中心类型分布"))
        st.components.v1.html(pie.render_embed(), height=450, scrolling=False)

    with col2:
        # 政权文化中心统计
        regime_count = {}
        for center in cultural_centers:
            r = center.get('regime', '未知')
            regime_count[r] = regime_count.get(r, 0) + 1

        bar = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))
        bar.add_xaxis(list(regime_count.keys()))
        bar.add_yaxis("文化中心数量", list(regime_count.values()))
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="各政权文化中心数量"),
            xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45}),
        )
        st.components.v1.html(bar.render_embed(), height=450, scrolling=False)

# --------------------------------------------
# 选项卡 3: 贸易路线
# --------------------------------------------
with tab3:
    st.subheader("🛣️ 贸易路线")

    trade_routes = get_trade_routes()

    # 显示贸易路线列表
    for route in trade_routes:
        st.markdown(f"### {route['name']}")
        st.markdown(f"**起点**: {route['from']} → **终点**: {route['to']}")
        st.markdown(f"**说明**: {route.get('description', '')}")

        # 在地图上显示路线
        if route.get('coords'):
            route_df = pd.DataFrame(
                route['coords'],
                columns=['lon', 'lat']
            )
            st.map(route_df, zoom=4)

        st.markdown("---")

    # 贸易路线网络图
    st.subheader("贸易网络示意")

    nodes = []
    links = []
    city_set = set()

    for route in trade_routes:
        from_city = route['from']
        to_city = route['to']

        if from_city not in city_set:
            nodes.append({"name": from_city, "symbolSize": 50})
            city_set.add(from_city)

        if to_city not in city_set:
            nodes.append({"name": to_city, "symbolSize": 40})
            city_set.add(to_city)

        links.append({
            "source": from_city,
            "target": to_city,
            "value": route['name']
        })

    graph = Graph(init_opts=opts.InitOpts(width="100%", height="500px"))
    graph.add(
        "贸易路线",
        nodes,
        links,
        repulsion=8000,
        edge_length=[100, 300],
        label_opts=opts.LabelOpts(is_show=True),
    )
    graph.set_global_opts(
        title_opts=opts.TitleOpts(title="贸易路线网络图"),
        legend_opts=opts.LegendOpts(is_show=False),
    )
    st.components.v1.html(graph.render_embed(), height=550, scrolling=False)

# --------------------------------------------
# 选项卡 4: 宗教分布
# --------------------------------------------
with tab4:
    st.subheader("🏯 宗教分布")

    religion_data = get_religion_data()

    for religion, data in religion_data.items():
        st.markdown(f"### {religion}")
        st.markdown(f"**分布中心**: {', '.join(data.get('centers', []))}")
        st.markdown(f"**简介**: {data.get('description', '')}")

        # 显示名刹
        if 'famous_temples' in data:
            st.markdown("**著名寺庙/道观**:")
            cols = st.columns(2)
            for i, temple in enumerate(data['famous_temples']):
                with cols[i % 2]:
                    st.markdown(f"- **{temple['name']}** ({temple['location']}, {temple['regime']})")

        st.markdown("---")

    # 宗教中心统计
    st.subheader("宗教中心分布统计")

    all_centers = []
    for religion, data in religion_data.items():
        for center in data.get('centers', []):
            all_centers.append({"宗教": religion, "中心": center})

    df_centers = pd.DataFrame(all_centers)

    st.dataframe(df_centers, use_container_width=True, hide_index=True)

# --------------------------------------------
# 选项卡 5: 艺术作品
# --------------------------------------------
with tab5:
    st.subheader("🎨 艺术作品")

    art_works = get_art_works()

    # 分类选择
    category = st.selectbox(
        "选择艺术类别",
        options=["绘画", "书法", "陶瓷"]
    )

    works = art_works.get(category, [])

    if works:
        if category == "绘画":
            for work in works:
                with st.expander(f"**{work['name']}** - {work.get('artist', '佚名')} ({work.get('regime', '')})"):
                    st.markdown(f"**年代**: {work.get('year', '未知')}年")
                    st.markdown(f"**简介**: {work.get('description', '')}")

        elif category == "书法":
            for work in works:
                with st.expander(f"**{work['name']}** - {work.get('artist', '佚名')}"):
                    st.markdown(f"**年代**: {work.get('regime', '未知')}")
                    st.markdown(f"**简介**: {work.get('description', '')}")

        elif category == "陶瓷":
            cols = st.columns(3)
            for i, work in enumerate(works):
                with cols[i % 3]:
                    st.markdown(f"### {work['name']}")
                    st.markdown(f"**政权**: {work.get('regime', '')}")
                    st.markdown(f"**特点**: {work.get('description', '')}")

    st.markdown("---")

    # 艺术作品政权分布统计
    st.subheader("艺术作品政权分布")

    regime_art_count = {}
    for category, works in art_works.items():
        for work in works:
            regime = work.get('regime', '未知')
            regime_art_count[regime] = regime_art_count.get(regime, 0) + 1

    # 添加陶瓷数据
    for work in art_works.get('陶瓷', []):
        regime = work.get('regime', '未知')
        # 已在上文统计

    bar_art = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))
    bar_art.add_xaxis(list(regime_art_count.keys()))
    bar_art.add_yaxis("艺术作品数量", list(regime_art_count.values()))
    bar_art.set_global_opts(
        title_opts=opts.TitleOpts(title="各政权艺术作品数量"),
        xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45}),
    )
    st.components.v1.html(bar_art.render_embed(), height=450, scrolling=False)

# 页脚
st.markdown("---")
st.markdown("数据来源：历史资料整理")
