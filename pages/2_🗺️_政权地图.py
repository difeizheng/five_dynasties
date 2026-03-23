"""
🗺️ 政权地图页面
展示五代十国疆域范围和现代省份对照
"""

import streamlit as st
from streamlit.components.v1 import html
from pyecharts import options as opts
from pyecharts.charts import Bar
import pandas as pd
import json

from src.data_processor import (
    WUDAI_REGIMES,
    SHIGUO_REGIMES,
    REGIME_TO_PROVINCE,
    process_regime_timeline,
    get_regime_color,
    get_province_regime_mapping,
    REGIME_COLORS,
    CAPITAL_COORDS,
    CAPITAL_TO_PROVINCE,
)
from src.config import PROVINCE_MAPPING
from src.streamlit_utils import build_choropleth_map_html, build_simple_highlight_map_html

st.set_page_config(page_title="政权地图", page_icon="🗺️", layout="wide")


def render_map_header():
    """渲染页面标题"""
    st.title("🗺️ 政权疆域地图")
    st.markdown("查看五代十国各政权的疆域范围与现代行政区划的对照")

    st.markdown("""
    **图表说明**：
    - 🗺️ **疆域地图**：在中国地图上展示各政权的疆域范围，不同颜色代表不同政权
    - 🏛️ **都城分布**：散点图展示各政权都城所在地理位置
    - 📊 **疆域面积估算**：柱状图对比各政权的疆域面积（万平方公里）
    - 📋 **现代省份对照**：列出现代各省份在五代十国时期所属的政权
    """)

    st.markdown("---")


def render_regime_map(regime_name: str = None):
    """渲染政权地图 - 使用公共组件"""

    # 读取 GeoJSON 数据
    with open('china_full.geojson', 'r', encoding='utf-8') as f:
        china_geojson = f.read()

    mapping = get_province_regime_mapping()

    if regime_name and regime_name != "全部":
        mapping = mapping[mapping['regime'] == regime_name]

    # 构建省份 - 政权映射
    province_info = {}
    regimes_in_map = set()

    for _, row in mapping.iterrows():
        province = PROVINCE_MAPPING.get(row['province'], row['province'])
        regime = row['regime']
        province_info[province] = {"regime": regime}
        regimes_in_map.add(regime)

    regimes_list = list(regimes_in_map)

    # 为每个政权分配唯一值
    regime_value_map = {regime: idx + 1 for idx, regime in enumerate(regimes_list)}

    # 构建地图数据
    map_data = []
    for province, info in province_info.items():
        regime = info["regime"]
        map_data.append({
            "name": province,
            "value": regime_value_map[regime]
        })

    # 颜色映射
    color_mapping = {
        value: REGIME_COLORS.get(regime, "#999999")
        for regime, value in regime_value_map.items()
    }

    # 构建 tooltip 格式化函数
    tooltip_js = """function(params) {
        var regime = provinceRegimeMap[params.name] || '未知';
        return '<b>' + params.name + '</b><br/>所属政权：' + regime;
    }"""

    title_text = ' '.join(regimes_list) + ' 疆域范围'

    return build_choropleth_map_html(
        geojson_content=china_geojson,
        map_data=map_data,
        value_mapping=regime_value_map,
        color_mapping=color_mapping,
        title=title_text,
        tooltip_formatter=tooltip_js,
    )


def render_capital_scatter():
    """渲染都城分布散点图 - 使用公共组件"""

    # 读取 GeoJSON 数据
    with open('china_full.geojson', 'r', encoding='utf-8') as f:
        china_geojson = f.read()

    # 都城对应省份
    capital_provinces = [
        "河南省", "浙江省", "江苏省", "四川省", "福建省",
        "广东省", "湖南省", "湖北省", "山西省"
    ]

    title = "五代十国都城分布"

    return build_simple_highlight_map_html(
        geojson_content=china_geojson,
        highlight_regions=capital_provinces,
        highlight_color="#e74c3c",
        highlight_label="都城所在地",
        title=title,
        height=500,
    )


def get_province_history(province: str) -> dict:
    """获取省份历史沿革信息"""
    province_history = {
        "河南省": {
            "regimes": ["后梁", "后唐", "后晋", "后汉", "后周"],
            "capitals": ["开封", "洛阳"],
            "description": "河南是五代时期的政治中心，五代中有四个朝代定都开封（后梁、后晋、后汉、后周），后唐定都洛阳。",
            "key_events": [
                "907 年朱温在开封称帝建立后梁",
                "923 年李存勖在洛阳称帝建立后唐",
                "936 年石敬瑭在开封称帝建立后晋",
                "947 年刘知远在开封称帝建立后汉",
                "951 年郭威在开封称帝建立后周",
                "960 年赵匡胤在陈桥（开封附近）发动兵变建立北宋",
            ],
        },
        "山西省": {
            "regimes": ["后唐", "后晋", "后汉", "北汉"],
            "capitals": ["太原"],
            "description": "山西是沙陀势力的根据地，后唐、后晋、后汉的建立者都是沙陀人。北汉是唯一在北方的十国政权。",
            "key_events": [
                "891 年李克用被封为晋王，据有太原",
                "923 年李存勖在太原称帝建立后唐",
                "936 年石敬瑭在太原起兵建立后晋",
                "947 年刘知远在太原起兵建立后汉",
                "951 年刘崇在太原称帝建立北汉",
                "979 年宋太宗灭北汉，五代十国结束",
            ],
        },
        "山东省": {
            "regimes": ["后梁", "后唐", "后晋", "后汉", "后周"],
            "capitals": [],
            "description": "山东是后梁的根据地，朱温曾任宣武节度使据有此地。",
            "key_events": [
                "882 年朱温降唐，被任命为宣武节度使",
                "907 年朱温建立后梁，山东属后梁",
            ],
        },
        "河北省": {
            "regimes": ["后唐", "后晋", "后汉", "后周"],
            "capitals": [],
            "description": "河北是唐末藩镇割据的核心区域，卢龙、成德、魏博三镇在此。",
            "key_events": [
                "763 年安史之乱后，河北三镇形成割据",
                "923 年后唐灭燕，据有河北",
            ],
        },
        "浙江省": {
            "regimes": ["吴越"],
            "capitals": ["杭州"],
            "description": "吴越国定都杭州，钱镠统治时期兴修水利，发展经济，是十国中最富裕的政权之一。",
            "key_events": [
                "893 年钱镠被唐封为镇海节度使",
                "907 年钱镠被封为吴越王",
                "978 年钱弘俶纳土归宋，和平统一",
            ],
        },
        "江苏省": {
            "regimes": ["南唐", "吴越"],
            "capitals": ["南京"],
            "description": "南唐定都南京（金陵），是十国中疆域最大、文化最繁荣的政权。",
            "key_events": [
                "937 年李昪在金陵称帝建立南唐",
                "961 年李煜即位，南唐文化达到鼎盛",
                "975 年宋灭南唐，李煜被俘",
            ],
        },
        "四川省": {
            "regimes": ["前蜀", "后蜀"],
            "capitals": ["成都"],
            "description": "四川先后建立前蜀和后蜀两个政权，成都成为重要的文化中心。",
            "key_events": [
                "907 年王建在成都称帝建立前蜀",
                "925 年后唐灭前蜀",
                "934 年孟知祥在成都称帝建立后蜀",
                "965 年宋灭后蜀",
            ],
        },
        "福建省": {
            "regimes": ["闽国"],
            "capitals": ["福州"],
            "description": "闽国定都福州，王审知统治时期发展海外贸易。",
            "key_events": [
                "893 年王审知攻占福州",
                "909 年王审知被封为闽王",
                "945 年南唐灭闽",
            ],
        },
        "广东省": {
            "regimes": ["南汉"],
            "capitals": ["广州"],
            "description": "南汉定都广州，统治广东、广西、海南地区。",
            "key_events": [
                "917 年刘䶮在广州称帝建立大越，后改国号为汉",
                "971 年宋灭南汉",
            ],
        },
        "湖南省": {
            "regimes": ["楚"],
            "capitals": ["长沙"],
            "description": "楚国定都长沙，马殷统治时期与中原王朝保持朝贡关系。",
            "key_events": [
                "896 年马殷据有湖南",
                "907 年马殷被封为楚王",
                "951 年南唐灭楚",
            ],
        },
        "湖北省": {
            "regimes": ["荆南", "南唐"],
            "capitals": ["荆州"],
            "description": "荆南是十国中最小的政权，定都荆州，向多国称臣以求生存。",
            "key_events": [
                "924 年高季兴被封为南平王，建立荆南",
                "963 年宋灭荆南",
            ],
        },
        "安徽省": {
            "regimes": ["南唐", "后周"],
            "capitals": [],
            "description": "安徽南部属南唐，北部属后周。",
            "key_events": [
                "937 年南唐建立，据有皖南",
                "956 年后周攻南唐，得皖北",
            ],
        },
        "江西省": {
            "regimes": ["南唐"],
            "capitals": [],
            "description": "江西全境属南唐。",
            "key_events": [
                "937 年南唐建立，据有江西",
                "975 年宋灭南唐，江西归宋",
            ],
        },
        "陕西省": {
            "regimes": ["后梁", "前蜀", "后蜀"],
            "capitals": [],
            "description": "陕西南部属前蜀和后蜀，北部曾属后梁。",
            "key_events": [
                "907 年后梁建立，据有陕西北部",
                "911 年前蜀据有陕南",
            ],
        },
    }
    return province_history.get(province, None)


def render_province_detail(province: str):
    """渲染省份详情卡片"""
    history = get_province_history(province)

    if not history:
        st.warning(f"暂未收录 {province} 的历史沿革信息")
        return

    # 省份详情卡片
    st.markdown(f"### 📍 {province} 历史沿革")

    # 描述
    if history.get("description"):
        st.info(history["description"])

    # 基本信息
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 涉及政权")
        regimes_str = ", ".join(history.get("regimes", []))
        st.markdown(f"**{regimes_str}**")

    with col2:
        st.markdown("#### 都城")
        capitals = history.get("capitals", [])
        if capitals:
            st.markdown(f"**{', '.join(capitals)}**")
        else:
            st.markdown("**无**")

    # 重大历史事件
    if history.get("key_events"):
        st.markdown("#### 📜 重大历史事件")
        for event in history["key_events"]:
            st.markdown(f"- {event}")

    st.markdown("---")


def render_province_selector():
    """渲染省份选择器"""
    st.subheader("🔍 省份详情查询")

    # 获取所有省份列表
    mapping = get_province_regime_mapping()
    provinces = sorted(mapping['province'].unique())

    # 省份选择器
    selected_province = st.selectbox(
        "选择省份查看历史沿革",
        provinces,
        key="province_selector"
    )

    return selected_province


def render_province_regime_table():
    """渲染省份 - 政权对照表"""
    st.subheader("📋 现代省份与五代十国政权对照")

    # 创建 DataFrame
    mapping = get_province_regime_mapping()

    # 按省份分组
    province_groups = mapping.groupby('province')

    for province, group in province_groups:
        regimes = ', '.join(group['regime'].tolist())
        types = ', '.join(group['type'].unique())
        st.markdown(f"**{province}**: {regimes} ({types})")

    return mapping


def render_regime_area_chart():
    """渲染政权面积估算图"""
    # 估算面积（万平方公里）
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

    bar = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))

    bar.add_xaxis(list(area_data.keys()))
    bar.add_yaxis(
        "面积 (万 km²)",
        list(area_data.values()),
        label_opts=opts.LabelOpts(position="top"),
    )

    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="政权疆域面积估算"),
        yaxis_opts=opts.AxisOpts(name="面积 (万 km²)"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
    )

    return bar


def render_modern_comparison():
    """渲染现代对照"""
    st.subheader("🌍 政权与现代省份对照")

    cols = st.columns(2)

    with cols[0]:
        st.markdown("#### 五代政权")
        for regime in WUDAI_REGIMES:
            provinces = REGIME_TO_PROVINCE.get(regime['name'], [])
            st.markdown(
                f"**{regime['name']}** ({regime['start']}-{regime['end']})\n"
                f"- 都城：{regime['capital']}\n"
                f"- 范围：{', '.join(provinces)}"
            )

    with cols[1]:
        st.markdown("#### 十国政权")
        for regime in SHIGUO_REGIMES:
            provinces = REGIME_TO_PROVINCE.get(regime['name'], [])
            st.markdown(
                f"**{regime['name']}** ({regime['start']}-{regime['end']})\n"
                f"- 都城：{regime['capital']}\n"
                f"- 范围：{', '.join(provinces)}"
            )


def main():
    """主函数"""
    render_map_header()

    # 地图选择器
    st.subheader("🗺️ 疆域地图")

    regime_names = ["全部"] + [r['name'] for r in WUDAI_REGIMES + SHIGUO_REGIMES]
    selected_regime = st.selectbox("选择政权", regime_names, key="regime_selector")

    if selected_regime == "全部":
        regime_map = render_regime_map()
    else:
        regime_map = render_regime_map(selected_regime)

    # render_regime_map 返回的是修改后的 HTML 字符串
    if isinstance(regime_map, str):
        html(regime_map, height=650, scrolling=False)
    else:
        html(regime_map.render_embed(), height=650, scrolling=False)

    st.markdown("---")

    # 都城分布
    capital_chart = render_capital_scatter()
    html(capital_chart, height=550, scrolling=False)

    st.markdown("---")

    # 省份详情查询（下钻功能）
    selected_province = render_province_selector()
    if selected_province:
        render_province_detail(selected_province)

    # 面积对比
    area_chart = render_regime_area_chart()
    html(area_chart.render_embed(), height=650, scrolling=False)

    st.markdown("---")

    # 现代对照
    render_modern_comparison()


if __name__ == "__main__":
    main()
