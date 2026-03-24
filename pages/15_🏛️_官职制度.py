"""
🏛️ 官职制度可视化
展示五代十国时期的中央官制、地方官制、武官制度等
"""

import streamlit as st
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Tree, Bar

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import (
    get_official_system,
    get_famous_officials,
    get_official_timeline,
)

st.set_page_config(
    page_title="官职制度",
    page_icon="🏛️",
    layout="wide"
)

# 标题
st.title("🏛️ 官职制度可视化")
st.markdown("展示五代十国时期的中央官制、地方官制、武官制度和著名官员")

st.markdown("""
**页面说明**：
- 🏢 **中央官制**：三省六部、枢密院、御史台等中央机构
- 🗺️ **地方官制**：节度使、观察使、刺史、县令等地方官职
- ⚔️ **武官制度**：禁军、藩镇兵的武官体系
- 👥 **著名官员**：五代十国时期的重要历史人物
- 📅 **官制变迁**：官制的历史演变过程
""")

st.markdown("---")

# ============================================
# 选项卡布局
# ============================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "中央官制", "地方官制", "武官制度", "特殊官职", "著名官员"
])

# --------------------------------------------
# 选项卡 1: 中央官制
# --------------------------------------------
with tab1:
    st.subheader("🏢 中央官制")

    official_system = get_official_system()
    central_gov = official_system.get("中央官制", {})

    # 三省
    st.markdown("### 三省")
    san_sheng = central_gov.get("三省", {})

    cols = st.columns(3)
    for i, (sheng_name, sheng_data) in enumerate(san_sheng.items()):
        with cols[i % 3]:
            st.markdown(f"#### {sheng_name}")
            st.markdown(f"**长官**: {sheng_data.get('长官', '未知')}")
            st.markdown(f"**品级**: {sheng_data.get('品级', '未知')}")
            st.markdown(f"**职责**: {sheng_data.get('职责', '未知')}")

    st.markdown("---")

    # 六部
    st.markdown("### 六部")
    liu_bu = central_gov.get("六部", {})

    bu_cols = st.columns(3)
    for i, (bu_name, bu_data) in enumerate(liu_bu.items()):
        with bu_cols[i % 3]:
            st.markdown(f"#### {bu_name}")
            st.markdown(f"**品级**: {bu_data.get('品级', '未知')}")
            st.markdown(f"**职责**: {bu_data.get('职责', '未知')}")

    st.markdown("---")

    # 枢密院和御史台
    st.markdown("### 其他中央机构")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 枢密院")
        shu_mi = central_gov.get("枢密院", {})
        st.markdown(f"**长官**: {shu_mi.get('长官', '未知')}")
        st.markdown(f"**品级**: {shu_mi.get('品级', '未知')}")
        st.markdown(f"**职责**: {shu_mi.get('职责', '未知')}")
        st.info("枢密院掌军国机务，权力极大，是五代时期最重要的中央机构之一")

    with col2:
        st.markdown("#### 御史台")
        yu_shi = central_gov.get("御史台", {})
        st.markdown(f"**长官**: {yu_shi.get('长官', '未知')}")
        st.markdown(f"**品级**: {yu_shi.get('品级', '未知')}")
        st.markdown(f"**职责**: {yu_shi.get('职责', '未知')}")
        st.info("御史台负责监察百官，弹劾违法")

    # 中央官制品级对比
    st.markdown("---")
    st.subheader("中央官制品级对比")

    pinji_data = {
        "枢密使": 1,
        "尚书令": 2,
        "中书令": 3,
        "侍中": 3,
        "六部尚书": 3,
        "御史大夫": 3,
    }

    bar = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))
    bar.add_xaxis(list(pinji_data.keys()))
    bar.add_yaxis("品级（数字越小品级越高）", list(pinji_data.values()))
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="中央主要官职品级"),
        yaxis_opts=opts.AxisOpts(name="品级", is_inverse=True),
    )
    st.components.v1.html(bar.render_embed(), height=450, scrolling=False)

# --------------------------------------------
# 选项卡 2: 地方官制
# --------------------------------------------
with tab2:
    st.subheader("🗺️ 地方官制")

    local_gov = official_system.get("地方官制", {})

    # 节度使
    st.markdown("### 节度使")
    jie_du_shi = local_gov.get("节度使", {})
    st.markdown(f"**品级**: {jie_du_shi.get('品级', '未知')}")
    st.markdown(f"**职责**: {jie_du_shi.get('职责', '未知')}")
    st.markdown(f"**属官**: {', '.join(jie_du_shi.get('属官', []))}")
    st.warning("⚠️ 节度使军政大权于一身，是造成藩镇割据的主要原因")

    st.markdown("---")

    # 其他地方官职
    st.markdown("### 其他的地方官职")

    cols = st.columns(3)
    for i, (position, data) in enumerate(local_gov.items()):
        if position == "节度使":
            continue
        with cols[i % 3]:
            st.markdown(f"#### {position}")
            st.markdown(f"**品级**: {data.get('品级', '未知')}")
            st.markdown(f"**职责**: {data.get('职责', '未知')}")

    # 地方官制层级图
    st.markdown("---")
    st.subheader("地方官制层级")

    tree_data = {
        "name": "地方行政体系",
        "children": [
            {
                "name": "节度使\n(从二品，军政大权)",
                "children": [
                    {"name": "掌书记"},
                    {"name": "判官"},
                    {"name": "推官"},
                    {"name": "衙内指挥使"},
                ]
            },
            {
                "name": "观察使\n(正三品，监察州县)",
            },
            {
                "name": "刺史\n(正四品，州级长官)",
            },
            {
                "name": "县令\n(正七品，县级长官)",
            },
        ]
    }

    tree = Tree(init_opts=opts.InitOpts(width="100%", height="400px"))
    tree.add(
        "地方官制",
        [tree_data],
        orient="TB",
        label_opts=opts.LabelOpts(position="top", formatter="{b}"),
    )
    tree.set_global_opts(title_opts=opts.TitleOpts(title="地方官制层级图"))
    st.components.v1.html(tree.render_embed(), height=450, scrolling=False)

# --------------------------------------------
# 选项卡 3: 武官制度
# --------------------------------------------
with tab3:
    st.subheader("⚔️ 武官制度")

    wu_guan = official_system.get("武官制度", {})

    # 禁军
    st.markdown("### 禁军")
    jin_jun = wu_guan.get("禁军", {})

    cols = st.columns(3)
    for i, (position, data) in enumerate(jin_jun.items()):
        with cols[i % 3]:
            st.markdown(f"#### {position}")
            st.markdown(f"**品级**: {data.get('品级', '未知')}")
            st.markdown(f"**职责**: {data.get('职责', '未知')}")

    st.info("禁军是保卫皇室和京城的精锐部队，侍卫亲军都指挥使权力极大")

    st.markdown("---")

    # 藩镇兵
    st.markdown("### 藩镇兵")
    fan_zhen_bing = wu_guan.get("藩镇兵", {})

    cols = st.columns(3)
    for i, (position, data) in enumerate(fan_zhen_bing.items()):
        with cols[i % 3]:
            st.markdown(f"#### {position}")
            st.markdown(f"**品级**: {data.get('品级', '未知')}")
            st.markdown(f"**职责**: {data.get('职责', '未知')}")

    st.warning("藩镇兵是节度使的私人武装，容易造成割据")

# --------------------------------------------
# 选项卡 4: 特殊官职
# --------------------------------------------
with tab4:
    st.subheader("📜 特殊官职")

    special = official_system.get("特殊官职", {})

    for position, data in special.items():
        st.markdown(f"### {position}")
        st.markdown(f"**正式名称**: {data.get('正式名称', position)}")
        st.markdown(f"**品级**: {data.get('品级', '未知')}")
        st.markdown(f"**职责**: {data.get('职责', '未知')}")
        st.markdown("---")

    # 官职名词解释
    st.subheader("📖 官职名词解释")

    st.markdown("""
    - **同中书门下平章事**: 宰相的正式官名，意为"同中书省和门下省一起商议国事"
    - **翰林学士**: 皇帝的文学侍从，负责草拟机密诏令，地位重要
    - **国子祭酒**: 国子监的长官，掌管最高学府，相当于国立大学校长
    - **枢密使**: 枢密院的长官，掌管军事机密和边防，权力极大
    - **节度使**: 地方军政长官，管辖数州，权力极大，容易造成割据
    """)

# --------------------------------------------
# 选项卡 5: 著名官员
# --------------------------------------------
with tab5:
    st.subheader("👥 著名官员")

    # 政权筛选
    all_regimes = ["全部", "后梁", "后唐", "后晋", "后汉", "后周", "北宋"]
    selected_regime = st.selectbox("选择政权", all_regimes)

    officials = get_famous_officials()

    if selected_regime != "全部":
        officials = [o for o in officials if selected_regime in o.get('regime', '')]

    # 显示官员列表
    for official in officials:
        with st.expander(f"**{official['name']}** - {official['position']} ({official['regime']})"):
            st.markdown(f"**简介**: {official.get('description', '')}")

    st.markdown("---")

    # 官制变迁时间线
    st.subheader("📅 官制变迁")

    timeline = get_official_timeline()

    for event in timeline:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"**{event['year']}年**")
        with col2:
            st.markdown(f"**{event['event']}**")
            st.markdown(f"*意义*: {event.get('significance', '')}")
            st.divider()

# 页脚
st.markdown("---")
st.markdown("数据来源：历史资料整理")
