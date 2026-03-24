"""
战争战役可视化页面
展示五代十国时期的主要战役，包括战役地图、详情、统计等
"""

import streamlit as st
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Geo, Bar, Pie
from pyecharts.globals import ChartType
from pyecharts.commons.utils import JsCode

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import (
    get_battles_data, get_battle_types, get_battle_by_name,
    REGIME_COLORS, BATTLE_TYPES
)
from src.streamlit_utils import render_error_message

# 页面配置
st.set_page_config(
    page_title="战争战役 - 五代十国",
    page_icon="⚔️",
    layout="wide"
)

# 标题
st.title("⚔️ 战争战役")
st.markdown("展示五代十国时期的主要战役，包括战役地图、详情信息和统计分析")

# 加载战役数据
@st.cache_data
def load_battles():
    return get_battles_data()

battles = load_battles()

if not battles:
    render_error_message("战役数据加载失败")
    st.stop()

# ============================================
# 侧边栏筛选器
# ============================================
st.sidebar.header("筛选条件")

# 战役类型筛选
battle_types = get_battle_types()
selected_types = st.sidebar.multiselect(
    "战役类型",
    options=battle_types,
    default=battle_types
)

# 政权筛选
all_regimes = set()
for battle in battles:
    for side in battle.get('sides', []):
        all_regimes.add(side)
all_regimes = sorted(list(all_regimes))

selected_regime = st.sidebar.selectbox(
    "参战政权",
    options=["全部"] + all_regimes,
    index=0
)

# 时间范围筛选
min_year = min(b['year'] for b in battles)
max_year = max(b['year'] for b in battles)
year_range = st.sidebar.slider(
    "时间范围",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# 应用筛选
filtered_battles = battles
filtered_battles = [b for b in filtered_battles if b.get('type') in selected_types]
filtered_battles = [b for b in filtered_battles if year_range[0] <= b['year'] <= year_range[1]]
if selected_regime != "全部":
    filtered_battles = [b for b in filtered_battles if selected_regime in b.get('sides', [])]

# 按年份排序
filtered_battles.sort(key=lambda x: x['year'])

# ============================================
# 主内容区域
# ============================================

# 统计卡片
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("战役总数", len(filtered_battles))
with col2:
    decisive_battles = len([b for b in filtered_battles if b.get('type') == '决战'])
    st.metric("决战次数", decisive_battles)
with col3:
    regime_wars = len([b for b in filtered_battles if b.get('type') == '灭国战'])
    st.metric("灭国战次数", regime_wars)
with col4:
    civil_wars = len([b for b in filtered_battles if b.get('type') == '内战'])
    st.metric("内战次数", civil_wars)

st.divider()

# ============================================
# 选项卡布局
# ============================================
tab1, tab2, tab3, tab4 = st.tabs(["战役地图", "战役列表", "战役统计", "战役详情"])

# --------------------------------------------
# 选项卡 1: 战役地图
# --------------------------------------------
with tab1:
    st.subheader("战役地理分布")

    if not filtered_battles:
        st.info("没有符合条件的战役数据")
    else:
        # 准备地图数据
        map_data = []
        for battle in filtered_battles:
            coords = battle.get('coords', [0, 0])
            map_data.append({
                "name": battle['name'],
                "year": battle['year'],
                "location": battle.get('location_detail', ''),
                "sides": " vs ".join(battle.get('sides', [])),
                "result": battle.get('result', ''),
                "coords": coords
            })

        # 使用 pyecharts 创建地图
        from pyecharts.charts import Geo
        from pyecharts import options as opts
        from pyecharts.commons.utils import JsCode

        # 准备 Geo 数据
        geo_data = [(b['name'], b['coords']) for b in map_data]

        geo = Geo(init_opts=opts.InitOpts(width="100%", height="600px"))
        geo.add_schema(
            maptype="china",
            itemstyle_opts=opts.ItemStyleOpts(
                area_color="#f5f5f5",
                border_color="#999999",
                border_width=1
            ),
            center=[105, 38],
            zoom=1.2
        )

        # 添加战役标记点
        geo.add(
            "战役",
            geo_data,
            type_=ChartType.EFFECT_SCATTER,
            color=["#e74c3c", "#3498db", "#2ecc71", "#9b59b6", "#95a5a6"],
            symbol_size=12,
            effect_opts=opts.EffectOpts(
                symbol_size=10
            ),
            label_opts=opts.LabelOpts(
                formatter=JsCode("""
                    function(params) {
                        return params.name;
                    }
                """),
                position="right",
                show=True
            ),
            tooltip_opts=opts.TooltipOpts(
                formatter=JsCode("""
                    function(params) {
                        const battles = """ + str({b['name']: {
                            'year': b['year'],
                            'location': b['location'],
                            'sides': b['sides'],
                            'result': b['result']
                        } for b in map_data}) + """;
                        const data = battles[params.name];
                        if (!data) return params.name;
                        return '<div style="padding: 10px">' +
                               '<h4 style="margin: 0 0 8px 0">' + params.name + '</h4>' +
                               '<p style="margin: 4px 0"><b>时间：</b>' + data.year + '年</p>' +
                               '<p style="margin: 4px 0"><b>地点：</b>' + data.location + '</p>' +
                               '<p style="margin: 4px 0"><b>参战方：</b>' + data.sides + '</p>' +
                               '<p style="margin: 4px 0"><b>结果：</b>' + data.result + '</p>' +
                               '</div>';
                    }
                """)
            )
        )

        geo.set_global_opts(
            title_opts=opts.TitleOpts(title="五代十国战役地理分布"),
            visualmap_opts=opts.VisualMapOpts(
                is_show=False,
                min_=min_year,
                max_=max_year
            )
        )

        # 渲染地图
        st.components.v1.html(geo.render_embed(), height=650, scrolling=False)

        # 显示战役位置列表
        st.write("### 战役位置列表")
        for battle in filtered_battles:
            st.write(f"- **{battle['name']}** ({battle['year']}年): {battle.get('location_detail', '')}")

# --------------------------------------------
# 选项卡 2: 战役列表
# --------------------------------------------
with tab2:
    st.subheader("战役清单")

    # 创建 DataFrame
    df_battles = pd.DataFrame(filtered_battles)

    # 显示表格
    for i, battle in enumerate(filtered_battles):
        with st.expander(f"{i+1}. {battle['name']} ({battle['year']}年) - {battle.get('result', '')}", expanded=False):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**时间**: {battle['year']}年")
                st.write(f"**地点**: {battle.get('location_detail', battle.get('location', ''))}")
                st.write(f"**参战方**: {' vs '.join(battle.get('sides', []))}")
                st.write(f"**指挥官**: {battle.get('commanders', {})}")
            with col2:
                st.write(f"**结果**: {battle.get('result', '')}")
                st.write(f"**类型**: {battle.get('type', '')}")
                if 'troops' in battle:
                    st.write(f"**兵力**: {battle['troops']}")

# --------------------------------------------
# 选项卡 3: 战役统计
# --------------------------------------------
with tab3:
    st.subheader("战役统计分析")

    col1, col2 = st.columns(2)

    with col1:
        # 按类型统计
        type_count = {}
        for battle in filtered_battles:
            t = battle.get('type', '其他')
            type_count[t] = type_count.get(t, 0) + 1

        # 饼图
        pie = Pie(init_opts=opts.InitOpts(width="100%", height="400px"))
        pie.add(
            "战役类型",
            [(k, v) for k, v in type_count.items()],
            radius=["40%", "75%"]
        )
        pie.set_global_opts(
            title_opts=opts.TitleOpts(title="战役类型分布"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%")
        )
        st.components.v1.html(pie.render_embed(), height=450, scrolling=False)

    with col2:
        # 按年代统计
        decade_count = {}
        for battle in filtered_battles:
            decade = (battle['year'] // 10) * 10
            decade_count[decade] = decade_count.get(decade, 0) + 1

        # 柱状图
        bar = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))
        bar.add_xaxis([str(k) for k in sorted(decade_count.keys())])
        bar.add_yaxis(
            "战役数量",
            [decade_count[k] for k in sorted(decade_count.keys())]
        )
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="战役年代分布"),
            xaxis_opts=opts.AxisOpts(name="年代"),
            yaxis_opts=opts.AxisOpts(name="数量")
        )
        st.components.v1.html(bar.render_embed(), height=450, scrolling=False)

    # 参战政权统计
    st.subheader("参战政权统计")
    regime_count = {}
    for battle in filtered_battles:
        for side in battle.get('sides', []):
            regime_count[side] = regime_count.get(side, 0) + 1

    # 排序
    sorted_regimes = sorted(regime_count.items(), key=lambda x: x[1], reverse=True)

    # 显示表格
    df_regimes = pd.DataFrame(sorted_regimes, columns=["政权", "参战次数"])
    st.dataframe(df_regimes, use_container_width=True, hide_index=True)

# --------------------------------------------
# 选项卡 4: 战役详情
# --------------------------------------------
with tab4:
    st.subheader("查看战役详情")

    # 选择战役
    battle_names = [f"{b['name']} ({b['year']}年)" for b in filtered_battles]
    selected = st.selectbox("选择战役", options=battle_names)

    if selected:
        # 解析选择的战役名
        selected_name = selected.split(' (')[0]
        battle = get_battle_by_name(selected_name)

        if battle:
            # 基本信息
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"### {battle['name']}")
                st.write(f"**时间**: {battle['year']}年")
                st.write(f"**地点**: {battle.get('location_detail', battle.get('location', ''))}")
                st.write(f"**参战方**: {' vs '.join(battle.get('sides', []))}")

                commanders = battle.get('commanders', {})
                if isinstance(commanders, dict):
                    st.write("**指挥官**:")
                    for side, cmd in commanders.items():
                        st.write(f"  - {side}: {cmd}")
                else:
                    st.write(f"**指挥官**: {commanders}")

                troops = battle.get('troops', {})
                if troops:
                    st.write("**兵力对比**:")
                    for side, count in troops.items():
                        st.write(f"  - {side}: {count:,}人")

            with col2:
                st.metric("战役类型", battle.get('type', ''))
                st.metric("结果", battle.get('result', ''))

            st.divider()

            # 战役影响
            st.markdown("### 战役影响")
            st.write(battle.get('impact', ''))

            # 在地图上标记
            coords = battle.get('coords')
            if coords:
                st.map(pd.DataFrame([{
                    "name": battle['name'],
                    "lat": coords[1],
                    "lon": coords[0]
                }]))

# 页脚
st.divider()
st.markdown("数据来源：历史资料整理")
