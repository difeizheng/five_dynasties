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
    get_daily_art_work,
    get_all_art_works_flat,
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
    st.subheader("🎨 艺术博物馆")
    st.markdown("探索五代十国时期的艺术瑰宝，感受千年前的文化魅力")

    # 每日推荐模块
    st.markdown("### 🌟 每日艺术品")

    # 初始化 session state
    if 'art_bookmarks' not in st.session_state:
        st.session_state.art_bookmarks = []

    daily_work = get_daily_art_work()
    if daily_work:
        col1, col2 = st.columns([2, 1])
        with col1:
            if daily_work.get('image_url'):
                try:
                    st.image(daily_work['image_url'], use_container_width=True, caption=daily_work['name'])
                except:
                    pass

        with col2:
            st.markdown(f"**🏷️ 名称**: {daily_work.get('name', '')}")
            st.markdown(f"**📂 类别**: {daily_work.get('category', '')}")
            st.markdown(f"**👤 作者/来源**: {daily_work.get('artist', daily_work.get('regime', '佚名'))}")
            st.markdown(f"**🏛️ 政权**: {daily_work.get('regime', '')}")
            st.markdown(f"**📝 简介**: {daily_work.get('description', '')}")

            # 收藏按钮
            work_id = f"{daily_work.get('category', '')}_{daily_work.get('name', '')}"
            is_bookmarked = work_id in [b.get('id') for b in st.session_state.art_bookmarks]

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if is_bookmarked:
                    if st.button("⭐ 已收藏", type="secondary", key=f"bm_{work_id}", use_container_width=True):
                        st.session_state.art_bookmarks = [b for b in st.session_state.art_bookmarks if b.get('id') != work_id]
                        st.success("已取消收藏")
                        st.rerun()
                else:
                    if st.button("⭐ 收藏", type="primary", key=f"bm_{work_id}", use_container_width=True):
                        st.session_state.art_bookmarks.append({
                            'id': work_id,
                            'name': daily_work.get('name', ''),
                            'category': daily_work.get('category', ''),
                            'artist': daily_work.get('artist', ''),
                            'regime': daily_work.get('regime', ''),
                            'description': daily_work.get('description', ''),
                            'type': 'art_work',
                            'url': '/经济文化地图',
                        })
                        st.success("收藏成功！")
                        st.rerun()

            with col_btn2:
                # 换一换按钮（使用随机种子）
                import random
                if st.button("🔄 换一换", key="refresh_daily", use_container_width=True):
                    st.session_state.daily_seed = random.randint(1, 10000)
                    st.rerun()

            # 分享按钮
            if st.button("📤 生成分享卡", key="share_daily", use_container_width=True):
                st.session_state.show_share_card = True
                st.session_state.share_work = daily_work

        # 显示分享卡
        if st.session_state.get('show_share_card', False) and st.session_state.get('share_work'):
            work = st.session_state.share_work
            st.markdown("### 📤 分享卡片")

            share_content = f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white; max-width: 500px; font-family: 'Kaiti', serif;">
                <h2 style="text-align: center; margin-bottom: 20px;">🎨 五代十国艺术珍品</h2>
                <h3 style="text-align: center; margin-bottom: 15px;">{work.get('name', '')}</h3>
                <p style="text-align: center; font-size: 16px;">📂 {work.get('category', '')} | 🏛️ {work.get('regime', '')}</p>
                <p style="text-align: center; font-size: 14px; margin: 20px 0;">{work.get('description', '')}</p>
                <p style="text-align: center; font-size: 12px; opacity: 0.8;">📱 五代十国历史可视化系统</p>
            </div>
            """
            st.markdown(share_content, unsafe_allow_html=True)
            st.info("💡 截图保存分享卡片")
            if st.button("❌ 关闭分享卡", key="close_share"):
                st.session_state.show_share_card = False
                st.session_state.share_work = None
                st.rerun()

    st.markdown("---")

    art_works = get_art_works()

    # 分类选择 - 使用标签页
    category_tabs = st.tabs(["绘画", "书法", "陶瓷", "诗词", "音乐", "建筑", "金银器", "玉器", "漆器", "织绣", "石窟", "雕塑"])

    # 为每个类别定义渲染函数
    def render_art_card(work, category):
        """渲染艺术作品卡片"""
        # 使用 expander 作为卡片容器
        if category in ["绘画", "书法", "建筑"]:
            title = f"**{work['name']}**"
            subtitle = f"🎨 {work.get('artist', '佚名')} | {work.get('regime', '')} | {work.get('year', '?')}年"
        elif category == "陶瓷":
            title = f"**{work['name']}**"
            subtitle = f"🏺 {work.get('type', '')} | {work.get('regime', '')} | {work.get('origin', '')}"
        elif category == "诗词":
            title = f"**{work['name']}**"
            subtitle = f"📜 {work.get('artist', '佚名')} | {work.get('type', '词')} | {work.get('regime', '')}"
        elif category == "音乐":
            title = f"**{work['name']}**"
            subtitle = f"🎵 {work.get('type', '')} | {work.get('regime', '')}"
        elif category in ["金银器", "玉器", "漆器", "织绣"]:
            title = f"**{work['name']}**"
            subtitle = f"🏺 {work.get('type', '')} | {work.get('regime', '')} | {work.get('size', work.get('material', ''))}"
        elif category in ["石窟", "雕塑"]:
            title = f"**{work['name']}**"
            subtitle = f"🗿 {work.get('type', '')} | {work.get('regime', '')} | {work.get('location', work.get('collection', ''))}"
        else:
            title = f"**{work['name']}**"
            subtitle = work.get('description', '')

        with st.expander(f"{title} — {subtitle}", expanded=False):
            # 显示图片（如果有）
            if work.get('image_url'):
                try:
                    st.image(work['image_url'], use_container_width=True, caption=work['name'])
                except:
                    pass

            # 显示详细信息
            cols = st.columns(2)

            if category in ["绘画", "书法"]:
                with cols[0]:
                    st.markdown(f"**🏷️ 类型**: {work.get('type', '')}")
                    st.markdown(f"**📅 年代**: {work.get('year', '')}年")
                    st.markdown(f"**👤 作者**: {work.get('artist', '')}")
                with cols[1]:
                    st.markdown(f"**🏛️ 政权**: {work.get('regime', '')}")
                    st.markdown(f"**📐 尺寸**: {work.get('size', '')}")
                    st.markdown(f"**🎨 材质**: {work.get('material', '')}")
                st.markdown(f"**🏛️ 收藏**: {work.get('collection', '')}")
                st.markdown(f"**📝 简介**: {work.get('description', '')}")
                if work.get('story'):
                    st.info(f"**📖 背后的故事**: {work['story']}")
                if work.get('appreciation'):
                    st.success(f"**💡 艺术赏析**: {work['appreciation']}")

            elif category == "陶瓷":
                with cols[0]:
                    st.markdown(f"**🏷️ 类型**: {work.get('type', '')}")
                    st.markdown(f"**🏛️ 政权**: {work.get('regime', '')}")
                    st.markdown(f"**📍 产地**: {work.get('origin', '')}")
                with cols[1]:
                    st.markdown(f"**📅 时期**: {work.get('period', '')}")
                    st.markdown(f"**🏛️ 收藏**: {work.get('collection', '未知')}")
                st.markdown(f"**📝 简介**: {work.get('description', '')}")
                if work.get('story'):
                    st.info(f"**📖 背后的故事**: {work['story']}")
                if work.get('appreciation'):
                    st.success(f"**💡 艺术赏析**: {work['appreciation']}")

            elif category == "诗词":
                st.markdown(f"**👤 作者**: {work.get('artist', '')}  **🏛️ 政权**: {work.get('regime', '')}  **📅 年代**: {work.get('year', '')}年")
                st.markdown("---")
                # 显示诗词内容，使用更好的格式
                content = work.get('content', '')
                st.markdown(f"<div style='font-family: Kaiti, STKaiti, serif; font-size: 18px; line-height: 2; padding: 20px; background: #f9f9f9; border-radius: 10px; border-left: 4px solid #8B4513;'>{content.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
                st.markdown("---")
                if work.get('background'):
                    st.info(f"**📖 创作背景**: {work['background']}")
                if work.get('appreciation'):
                    st.success(f"**💡 作品赏析**: {work['appreciation']}")
                if work.get('famous_lines'):
                    st.markdown(f"**✨ 名句**: {' | '.join(work['famous_lines'])}")

            elif category == "音乐":
                with cols[0]:
                    st.markdown(f"**🏷️ 类型**: {work.get('type', '')}")
                    st.markdown(f"**🏛️ 政权**: {work.get('regime', '')}")
                with cols[1]:
                    st.markdown(f"**🎹 乐器**: {', '.join(work.get('instruments', []))}")
                st.markdown(f"**📝 简介**: {work.get('description', '')}")
                if work.get('story'):
                    st.info(f"**📖 背后的故事**: {work['story']}")
                if work.get('appreciation'):
                    st.success(f"**💡 艺术赏析**: {work['appreciation']}")

            elif category == "建筑":
                with cols[0]:
                    st.markdown(f"**🏷️ 类型**: {work.get('type', '')}")
                    st.markdown(f"**🏛️ 政权**: {work.get('regime', '')}")
                    st.markdown(f"**📍 位置**: {work.get('location', '')}")
                with cols[1]:
                    st.markdown(f"**📅 建造年份**: {work.get('year', '')}")
                    st.markdown(f"**🏛️ 收藏**: {work.get('collection', '现存')}")
                st.markdown(f"**📝 简介**: {work.get('description', '')}")
                if work.get('story'):
                    st.info(f"**📖 历史故事**: {work['story']}")
                if work.get('appreciation'):
                    st.success(f"**💡 建筑特色**: {work['appreciation']}")
                if work.get('features'):
                    st.markdown(f"**🏛️ 主要特色**: {', '.join(work['features'])}")

            elif category in ["金银器", "玉器", "漆器", "织绣"]:
                with cols[0]:
                    st.markdown(f"**🏷️ 类型**: {work.get('type', '')}")
                    st.markdown(f"**🏛️ 政权**: {work.get('regime', '')}")
                    st.markdown(f"**📐 尺寸**: {work.get('size', '')}")
                with cols[1]:
                    st.markdown(f"**🎨 材质**: {work.get('material', '')}")
                    st.markdown(f"**🏛️ 收藏**: {work.get('collection', '未知')}")
                st.markdown(f"**📝 简介**: {work.get('description', '')}")
                if work.get('story'):
                    st.info(f"**📖 背后的故事**: {work['story']}")
                if work.get('appreciation'):
                    st.success(f"**💡 艺术赏析**: {work['appreciation']}")

            elif category in ["石窟", "雕塑"]:
                with cols[0]:
                    st.markdown(f"**🏷️ 类型**: {work.get('type', '')}")
                    st.markdown(f"**🏛️ 政权**: {work.get('regime', '')}")
                    st.markdown(f"**📍 位置**: {work.get('location', work.get('collection', ''))}")
                with cols[1]:
                    st.markdown(f"**📅 年代**: {work.get('year', '')}")
                    st.markdown(f"**📐 尺寸**: {work.get('size', '未知')}")
                st.markdown(f"**📝 简介**: {work.get('description', '')}")
                if work.get('story'):
                    st.info(f"**📖 历史故事**: {work['story']}")
                if work.get('appreciation'):
                    st.success(f"**💡 艺术赏析**: {work['appreciation']}")
                if work.get('features'):
                    st.markdown(f"**🏛️ 主要特色**: {', '.join(work['features'])}")

    # 渲染每个类别
    all_categories = ["绘画", "书法", "陶瓷", "诗词", "音乐", "建筑", "金银器", "玉器", "漆器", "织绣", "石窟", "雕塑"]
    for idx, category in enumerate(all_categories):
        with category_tabs[idx]:
            works = art_works.get(category, [])
            if works:
                # 显示统计
                st.caption(f"共 {len(works)} 件作品")
                # 渲染每个作品
                for work in works:
                    render_art_card(work, category)
            else:
                st.info(f"暂无{category}数据")

    st.markdown("---")

    # 艺术作品政权分布统计
    st.subheader("📊 艺术作品政权分布")

    regime_art_count = {}
    for category, works in art_works.items():
        for work in works:
            regime = work.get('regime', '未知')
            regime_art_count[regime] = regime_art_count.get(regime, 0) + 1

    bar_art = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))
    bar_art.add_xaxis(list(regime_art_count.keys()))
    bar_art.add_yaxis("艺术作品数量", list(regime_art_count.values()))
    bar_art.set_global_opts(
        title_opts=opts.TitleOpts(title="各政权艺术作品数量"),
        xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45}),
    )
    st.components.v1.html(bar_art.render_embed(), height=450, scrolling=False)

    # 艺术地图可视化
    st.markdown("---")
    st.subheader("🗺️ 艺术地图")

    # 收集所有有位置信息的艺术作品
    map_data = []
    location_coords = {
        "南京": [118.7969, 32.0603],
        "杭州": [120.1551, 30.2741],
        "开封": [114.3074, 34.7972],
        "洛阳": [112.4534, 34.6197],
        "成都": [104.0665, 30.5723],
        "敦煌": [94.6618, 40.1418],
        "重庆": [106.5516, 29.5647],
        "大同": [113.3001, 40.0769],
        "天水": [105.7249, 34.5786],
        "登封": [113.0269, 34.4457],
        "永靖": [103.3156, 35.9387],
        "安岳": [105.3342, 30.0989],
        "金华": [119.6489, 29.0819],
        "铜川": [108.9282, 35.0899],
        "长沙": [112.9388, 28.2282],
        "内丘": [114.5122, 37.2856],
        "曲阳": [114.7141, 38.6238],
        "建阳": [118.1181, 27.3214],
        "余姚": [121.1556, 30.0459],
        "河北": [114.5022, 38.0428],
        "陕西": [108.9398, 34.3416],
        "四川": [104.0665, 30.6723],
        "河南": [113.6253, 34.7965],
        "浙江": [120.1551, 30.2741],
        "福建": [119.2951, 26.0753],
        "甘肃": [103.8343, 36.0611],
    }

    for category, works in art_works.items():
        for work in works:
            location = work.get('location', work.get('origin', ''))
            if location:
                # 提取城市名
                for city, coords in location_coords.items():
                    if city in location:
                        map_data.append({
                            'name': work['name'],
                            'category': category,
                            'location': location,
                            'coords': coords,
                            'regime': work.get('regime', ''),
                        })
                        break

    if map_data:
        from pyecharts.charts import Geo

        # 按类别分组统计
        category_count = {}
        for item in map_data:
            cat = item['category']
            key = f"{item['coords'][0]},{item['coords'][1]}"
            if key not in category_count:
                category_count[key] = {'coords': item['coords'], 'count': 0, 'items': []}
            category_count[key]['count'] += 1
            category_count[key]['items'].append(item)

        geo = Geo(init_opts=opts.InitOpts(width="100%", height="600px"))
        geo.add_schema(
            maptype="china",
            itemstyle_opts=opts.ItemStyleOpts(color="#333"),
        )

        geo_data = [(item['coords'], item['count']) for item in category_count.values()]
        geo.add(
            "艺术作品",
            geo_data,
            type_=ChartType.EFFECT_SCATTER,
            color="#e74c3c",
            symbol_size=10,
        )

        geo.set_global_opts(
            title_opts=opts.TitleOpts(title="艺术作品地理分布"),
            visualmap_opts=opts.VisualMapOpts(
                is_show=True,
                min_=1,
                max_=10,
                orient="horizontal",
                pos_right="50%",
                pos_top="60%",
            ),
        )
        st.components.v1.html(geo.render_embed(), height=650, scrolling=False)

        # 显示各地点详情
        st.markdown("### 📍 各地艺术作品")
        for location_key, data in category_count.items():
            with st.expander(f"📍 {data['coords']} - {data['count']} 件作品"):
                for item in data['items']:
                    st.markdown(f"**{item['name']}** ({item['category']}) - {item['regime']}")

# 页脚
st.markdown("---")
st.markdown("数据来源：历史资料整理")
