"""
🔍 对比分析页面
展示政权、人物、藩镇的多维度对比
"""
import streamlit as st
from streamlit.components.v1 import html
from pyecharts import options as opts
from pyecharts.charts import Bar, Radar, Pie
import pandas as pd
import io
import base64

from src.config import (
    WUDAI_REGIMES,
    SHIGUO_REGIMES,
    REGIME_COLORS,
    REGIME_POWER_DATA,
    REGIME_AREA_DATA,
    WUDAI_SUCCESSION,
    SHIGUO_SUCCESSION,
    FANZHEN_BASE_DATA,
)
from src.data_processor import get_regime_color

st.set_page_config(page_title="对比分析", page_icon="🔍", layout="wide")


def render_comparison_header():
    """渲染页面标题"""
    st.title("🔍 对比分析")
    st.markdown("选择两个对象进行多维度对比分析")

    st.markdown("""
    **图表说明**：
    - 🏛️ **政权对比**：对比两个政权的存续时间、疆域面积、综合实力、文化发展、军事实力
    - 👤 **人物对比**：对比两位帝王/人物的在位时间、功绩评价、历史影响
    - 🏰 **藩镇对比**：对比两个藩镇的实力值、控制区域、历史影响
    """)

    st.markdown("---")


def get_regime_full_info(regime_name: str) -> dict:
    """获取政权完整信息"""
    # 查找政权基础信息
    regime_info = None
    for r in WUDAI_REGIMES + SHIGUO_REGIMES:
        if r['name'] == regime_name:
            regime_info = r.copy()
            break

    if not regime_info:
        return None

    # 添加面积数据
    regime_info['area'] = REGIME_AREA_DATA.get(regime_name, 0)

    # 添加实力数据
    power_data = None
    for p in REGIME_POWER_DATA:
        if p['name'] == regime_name:
            power_data = p
            break

    if power_data:
        regime_info['power'] = power_data['power']
        regime_info['culture'] = power_data['culture']
        regime_info['military'] = power_data['military']
    else:
        # 估算数据
        regime_info['power'] = regime_info.get('power', 50)
        regime_info['culture'] = regime_info.get('culture', 50)
        regime_info['military'] = regime_info.get('military', 50)

    # 帝王数量
    succession = WUDAI_SUCCESSION.get(regime_name, SHIGUO_SUCCESSION.get(regime_name, []))
    regime_info['emperor_count'] = len(succession)

    return regime_info


def render_regime_comparison(regime1: str, regime2: str):
    """渲染政权对比"""
    info1 = get_regime_full_info(regime1)
    info2 = get_regime_full_info(regime2)

    if not info1 or not info2:
        st.warning("无法获取政权信息")
        return

    # 导出功能
    st.subheader("📥 导出对比数据")

    # 构建对比数据 DataFrame
    comparison_df = pd.DataFrame({
        "指标": ["存续时间 (年)", "疆域面积 (万 km²)", "综合实力", "文化发展", "军事实力", "帝王数量"],
        regime1: [
            info1['end'] - info1['start'],
            info1['area'],
            info1['power'],
            info1['culture'],
            info1['military'],
            info1['emperor_count']
        ],
        regime2: [
            info2['end'] - info2['start'],
            info2['area'],
            info2['power'],
            info2['culture'],
            info2['military'],
            info2['emperor_count']
        ]
    })

    # 导出 CSV
    csv_data = comparison_df.to_csv(index=False, encoding='utf-8-sig')
    b64 = base64.b64encode(csv_data.encode()).decode()
    st.markdown(
        f'<a href="data:text/csv;base64,{b64}" download="{regime1}_vs_{regime2}_对比.csv" '
        f'style="display: inline-block; padding: 0.5rem 1rem; background: #28a745; color: white; '
        f'text-decoration: none; border-radius: 0.25rem;">📥 下载对比数据 (CSV)</a>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # 基本信息对比
    st.subheader(f"🏛️ {regime1} vs {regime2}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"#### {regime1}")
        st.markdown(f"- **存续时间**: {info1['start']}-{info1['end']}年 ({info1['end'] - info1['start']}年)")
        st.markdown(f"- **都城**: {info1['capital']}")
        st.markdown(f"- **开国君主**: {info1['founder']}")
        st.markdown(f"- **疆域面积**: 约{info1['area']}万 km²")
        st.markdown(f"- **帝王数量**: {info1['emperor_count']}位")

    with col2:
        st.markdown(f"#### {regime2}")
        st.markdown(f"- **存续时间**: {info2['start']}-{info2['end']}年 ({info2['end'] - info2['start']}年)")
        st.markdown(f"- **都城**: {info2['capital']}")
        st.markdown(f"- **开国君主**: {info2['founder']}")
        st.markdown(f"- **疆域面积**: 约{info2['area']}万 km²")
        st.markdown(f"- **帝王数量**: {info2['emperor_count']}位")

    st.markdown("---")

    # 雷达图对比 - 多维度对比
    st.subheader("📊 综合实力雷达图")

    radar = Radar(init_opts=opts.InitOpts(width="100%", height="500px"))

    radar.add_schema(
        schema=[
            opts.RadarIndicatorItem(name="存续时间", max_=100),
            opts.RadarIndicatorItem(name="疆域面积", max_=60),
            opts.RadarIndicatorItem(name="综合实力", max_=100),
            opts.RadarIndicatorItem(name="文化发展", max_=100),
            opts.RadarIndicatorItem(name="军事实力", max_=100),
        ],
        radius="65%",
    )

    # 数据归一化
    duration1 = min((info1['end'] - info1['start']), 100)
    duration2 = min((info2['end'] - info2['start']), 100)

    radar.add(
        regime1,
        [
            [
                duration1,
                info1['area'],
                info1['power'],
                info1['culture'],
                info1['military']
            ]
        ],
        color=REGIME_COLORS.get(regime1, "#3b82f6"),
    )

    radar.add(
        regime2,
        [
            [
                duration2,
                info2['area'],
                info2['power'],
                info2['culture'],
                info2['military']
            ]
        ],
        color=REGIME_COLORS.get(regime2, "#e74c3c"),
    )

    radar.set_global_opts(
        title_opts=opts.TitleOpts(title="政权综合实力对比"),
        legend_opts=opts.LegendOpts(pos_top="90%"),
    )

    html(radar.render_embed(), height=550, scrolling=False)

    st.markdown("---")

    # 柱状图对比
    st.subheader("📊 具体指标对比")

    bar = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))

    bar.add_xaxis(["存续时间", "疆域面积", "综合实力", "文化发展", "军事实力"])

    bar.add_yaxis(
        regime1,
        [
            duration1,
            info1['area'],
            info1['power'],
            info1['culture'],
            info1['military']
        ],
        color=REGIME_COLORS.get(regime1, "#3b82f6"),
    )

    bar.add_yaxis(
        regime2,
        [
            duration2,
            info2['area'],
            info2['power'],
            info2['culture'],
            info2['military']
        ],
        color=REGIME_COLORS.get(regime2, "#e74c3c"),
    )

    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="各项指标对比"),
        yaxis_opts=opts.AxisOpts(name="数值"),
        legend_opts=opts.LegendOpts(pos_top="90%"),
    )

    html(bar.render_embed(), height=450, scrolling=False)


def render_regime_selector():
    """渲染政权选择器"""
    all_regimes = [r['name'] for r in WUDAI_REGIMES + SHIGUO_REGIMES]

    cols = st.columns(3)

    with cols[0]:
        st.markdown("#### 选择对比政权")

    with cols[1]:
        regime1 = st.selectbox(
            "政权 A",
            all_regimes,
            index=0,
            key="regime_compare_1"
        )

    with cols[2]:
        regime2 = st.selectbox(
            "政权 B",
            all_regimes,
            index=len(all_regimes) // 2,
            key="regime_compare_2"
        )

    return regime1, regime2


def get_character_info(char_name: str, regime: str = None) -> dict:
    """获取人物信息"""
    all_succession = {**WUDAI_SUCCESSION, **SHIGUO_SUCCESSION}

    for regime_name, rulers in all_succession.items():
        for ruler in rulers:
            if ruler['name'] == char_name:
                return {
                    'name': char_name,
                    'regime': regime_name,
                    'relation': ruler.get('relation', ''),
                    'years': ruler.get('years', ''),
                    'temple_name': ruler.get('temple_name', ''),
                    'posthumous_name': ruler.get('posthumous_name', ''),
                    'bio': ruler.get('bio', ''),
                }

    return None


def render_character_comparison(char1: str, char2: str):
    """渲染人物对比"""
    info1 = get_character_info(char1)
    info2 = get_character_info(char2)

    if not info1:
        st.warning(f"未找到人物：{char1}")
        return
    if not info2:
        st.warning(f"未找到人物：{char2}")
        return

    st.subheader(f"👤 {char1} vs {char2}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"#### {char1}")
        st.markdown(f"**所属政权**: {info1['regime']}")
        st.markdown(f"**在位时间**: {info1['years']}")
        st.markdown(f"**身份关系**: {info1['relation']}")
        if info1['temple_name']:
            st.markdown(f"**庙号**: {info1['temple_name']}")
        if info1['posthumous_name']:
            st.markdown(f"**谥号**: {info1['posthumous_name']}")
        if info1['bio']:
            with st.expander("生平事迹"):
                st.write(info1['bio'])

    with col2:
        st.markdown(f"#### {char2}")
        st.markdown(f"**所属政权**: {info2['regime']}")
        st.markdown(f"**在位时间**: {info2['years']}")
        st.markdown(f"**身份关系**: {info2['relation']}")
        if info2['temple_name']:
            st.markdown(f"**庙号**: {info2['temple_name']}")
        if info2['posthumous_name']:
            st.markdown(f"**谥号**: {info2['posthumous_name']}")
        if info2['bio']:
            with st.expander("生平事迹"):
                st.write(info2['bio'])


def render_character_selector():
    """渲染人物选择器"""
    all_succession = {**WUDAI_SUCCESSION, **SHIGUO_SUCCESSION}

    # 扁平化所有人物列表
    all_characters = []
    for regime, rulers in all_succession.items():
        for ruler in rulers:
            all_characters.append(f"{ruler['name']} ({regime})")

    cols = st.columns(3)

    with cols[0]:
        st.markdown("#### 选择对比人物")

    with cols[1]:
        char1 = st.selectbox(
            "人物 A",
            all_characters,
            index=0,
            key="char_compare_1"
        )

    with cols[2]:
        char2 = st.selectbox(
            "人物 B",
            all_characters,
            index=len(all_characters) // 2,
            key="char_compare_2"
        )

    # 提取人名
    if char1:
        char1_name = char1.split(' (')[0]
    else:
        char1_name = None

    if char2:
        char2_name = char2.split(' (')[0]
    else:
        char2_name = None

    return char1_name, char2_name


def get_fanzhen_info(fanzhen_name: str) -> dict:
    """获取藩镇信息"""
    return FANZHEN_BASE_DATA.get(fanzhen_name, None)


def render_fanzhen_comparison(fanzhen1: str, fanzhen2: str):
    """渲染藩镇对比"""
    info1 = get_fanzhen_info(fanzhen1)
    info2 = get_fanzhen_info(fanzhen2)

    if not info1:
        st.warning(f"未找到藩镇：{fanzhen1}")
        return
    if not info2:
        st.warning(f"未找到藩镇：{fanzhen2}")
        return

    st.subheader(f"🏰 {fanzhen1} vs {fanzhen2}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"#### {fanzhen1}")
        st.markdown(f"**控制区域**: {info1['area']}")
        st.markdown(f"**实力值**: {info1['power']}")
        st.markdown(f"**对应省份**: {info1['province']}")
        color = info1['color']
        st.markdown(
            f"""<div style="display:inline-block; padding:0.25rem 0.5rem; border-radius:0.25rem; background:{color}20; color:{color}; font-weight:bold;">
            {fanzhen1}
            </div>""",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(f"#### {fanzhen2}")
        st.markdown(f"**控制区域**: {info2['area']}")
        st.markdown(f"**实力值**: {info2['power']}")
        st.markdown(f"**对应省份**: {info2['province']}")
        color = info2['color']
        st.markdown(
            f"""<div style="display:inline-block; padding:0.25rem 0.5rem; border-radius:0.25rem; background:{color}20; color:{color}; font-weight:bold;">
            {fanzhen2}
            </div>""",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # 柱状图对比
    bar = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))

    bar.add_xaxis(["实力值"])

    bar.add_yaxis(
        fanzhen1,
        [info1['power']],
        color=info1['color'],
        label_opts=opts.LabelOpts(position="top"),
    )

    bar.add_yaxis(
        fanzhen2,
        [info2['power']],
        color=info2['color'],
        label_opts=opts.LabelOpts(position="top"),
    )

    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="藩镇实力对比"),
        yaxis_opts=opts.AxisOpts(name="实力值", max_=100),
    )

    html(bar.render_embed(), height=450, scrolling=False)


def render_fanzhen_selector():
    """渲染藩镇选择器"""
    fanzhen_names = list(FANZHEN_BASE_DATA.keys())

    cols = st.columns(3)

    with cols[0]:
        st.markdown("#### 选择对比藩镇")

    with cols[1]:
        fanzhen1 = st.selectbox(
            "藩镇 A",
            fanzhen_names,
            index=0,
            key="fanzhen_compare_1"
        )

    with cols[2]:
        fanzhen2 = st.selectbox(
            "藩镇 B",
            fanzhen_names,
            index=len(fanzhen_names) // 2,
            key="fanzhen_compare_2"
        )

    return fanzhen1, fanzhen2


def main():
    """主函数"""
    render_comparison_header()

    # 对比类型选择
    comparison_type = st.radio(
        "选择对比类型",
        ["政权对比", "人物对比", "藩镇对比"],
        horizontal=True
    )

    st.markdown("---")

    if comparison_type == "政权对比":
        regime1, regime2 = render_regime_selector()

        if regime1 and regime2:
            if regime1 == regime2:
                st.warning("请选择不同的政权进行对比")
            else:
                render_regime_comparison(regime1, regime2)

    elif comparison_type == "人物对比":
        char1, char2 = render_character_selector()

        if char1 and char2:
            if char1 == char2:
                st.warning("请选择不同的人物进行对比")
            else:
                render_character_comparison(char1, char2)

    else:  # 藩镇对比
        fanzhen1, fanzhen2 = render_fanzhen_selector()

        if fanzhen1 and fanzhen2:
            if fanzhen1 == fanzhen2:
                st.warning("请选择不同的藩镇进行对比")
            else:
                render_fanzhen_comparison(fanzhen1, fanzhen2)


if __name__ == "__main__":
    main()
