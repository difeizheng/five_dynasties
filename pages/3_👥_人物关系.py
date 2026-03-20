"""
👥 人物关系页面
展示帝王世系和人物关系网络
"""
import streamlit as st
from streamlit.components.v1 import html

from pyecharts import options as opts
from pyecharts.charts import Graph, Tree
import pandas as pd

from src.data_loader import (
    load_wudai_characters,
    load_wudai_detailed_characters,
)
from src.data_processor import (
    WUDAI_REGIMES,
    SHIGUO_REGIMES,
    get_regime_color,
    get_all_succession_data,
)
from src.config import REGIME_COLORS

st.set_page_config(page_title="人物关系", page_icon="👥", layout="wide")


# ============================================
# 人物详情组件
# ============================================

def show_character_detail(name: str = None):
    """显示人物详情"""
    if not name:
        return

    all_succession = get_all_succession_data()

    # 查找人物
    character_info = None
    regime_name = None

    for regime, rulers in all_succession.items():
        for ruler in rulers:
            if ruler['name'] == name:
                character_info = ruler
                regime_name = regime
                break
        if character_info:
            break

    if not character_info:
        st.warning(f"未找到人物：{name}")
        return

    # 人物详情卡片
    st.markdown(f"### 👤 {name}")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        # 基本信息
        st.markdown("#### 📋 基本信息")
        st.markdown(f"**所属政权**: {regime_name}")
        st.markdown(f"**在位时间**: {character_info.get('years', '未知')}")
        st.markdown(f"**身份关系**: {character_info.get('relation', '未知')}")

        if character_info.get('temple_name'):
            st.markdown(f"**庙号**: {character_info['temple_name']}")
        if character_info.get('posthumous_name'):
            st.markdown(f"**谥号**: {character_info['posthumous_name']}")

    with col2:
        # 政权颜色标签
        color = REGIME_COLORS.get(regime_name, "#999999")
        st.markdown(
            f"""
            <div style="background: {color}20; border-left: 4px solid {color}; padding: 1rem; border-radius: 0.5rem;">
                <h3 style="margin: 0; color: {color}">{regime_name}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        # 关闭按钮
        st.markdown("#### 操作")
        if st.button("❌ 关闭", use_container_width=True, key="close_detail"):
            st.session_state.selected_character = None
            st.rerun()

    # 生平事迹
    if character_info.get('bio'):
        st.markdown("#### 📖 生平事迹")
        st.info(character_info['bio'])

    st.markdown("---")


def render_relationship_header():
    """渲染页面标题"""
    st.title("👥 人物关系网络")
    st.markdown("查看五代十国的帝王世系和重要人物关系")

    st.markdown("""
    **图表说明**：
    - 🌳 **帝王世系树**：树状图展示各政权的帝王继承关系
    - 🕸️ **人物关系网络**：力导向图展示人物之间的亲属、君臣关系
    - 📋 **人物列表**：按政权分类展示历史人物的详细信息
    """)

    st.markdown("---")


def generate_wudai_succession_tree():
    """生成五代世系树数据"""
    return get_all_succession_data()


def generate_shiguo_succession_tree():
    """生成十国世系树数据"""
    return get_all_succession_data()


def render_succession_tree(regime_name: str):
    """渲染单个政权的世系树"""
    all_data = generate_wudai_succession_tree()

    if regime_name not in all_data:
        return None

    succession = all_data[regime_name]

    # 构建树形结构
    tree_data = {
        "name": f"{regime_name}\n({regime_name[:1]})",
        "children": [
            {
                "name": f"{r['name']}\n{r['years']}",
                "symbolSize": 50,
                "value": r['relation'],
            }
            for r in succession
        ],
    }

    # 如果是第一个皇帝，标记为根节点
    if succession:
        tree_data["children"][0]["symbolSize"] = 70

    tree = Tree(init_opts=opts.InitOpts(width="100%", height="400px"))

    tree.add(
        series_name=regime_name,
        data=[tree_data],
        orient="TB",
        label_opts=opts.LabelOpts(
            position="top",
            formatter="{b}",
        ),
    )

    tree.set_global_opts(
        title_opts=opts.TitleOpts(title=f"{regime_name}世系图"),
    )

    return tree


def render_relationship_graph():
    """渲染人物关系网络图"""
    # 构建人物关系数据
    nodes = []
    links = []

    # 使用统一配置的世系数据
    all_succession = get_all_succession_data()

    # 五代帝王
    for regime, rulers in all_succession.items():
        # 添加政权节点
        nodes.append({
            "name": regime,
            "symbolSize": 80,
            "category": 0,
            "value": get_regime_color(regime),
        })

        for i, ruler in enumerate(rulers):
            # 添加人物节点
            nodes.append({
                "name": ruler['name'],
                "symbolSize": 50,
                "category": 1,
            })

            # 连接到政权
            links.append({
                "source": ruler['name'],
                "target": regime,
                "value": "属于",
            })

            # 连接继承关系
            if i > 0:
                prev_ruler = rulers[i - 1]
                links.append({
                    "source": prev_ruler['name'],
                    "target": ruler['name'],
                    "value": ruler['relation'],
                })

    graph = Graph(init_opts=opts.InitOpts(width="100%", height="600px"))

    graph.add(
        "",
        nodes,
        links,
        repulsion=8000,
        edge_symbol=["circle", "arrow"],
        edge_length=[50, 200],
        label_opts=opts.LabelOpts(is_show=True),
        categories=[
            {"name": "政权"},
            {"name": "人物"},
        ],
        linestyle_opts=opts.LineStyleOpts(
            color="source",
        ),
    )

    graph.set_global_opts(
        title_opts=opts.TitleOpts(title="五代帝王关系网络"),
        legend_opts=opts.LegendOpts(is_show=True),
        tooltip_opts=opts.TooltipOpts(
            trigger="item",
            formatter="{b}: {c}"
        ),
    )

    return graph


def render_character_list():
    """渲染人物列表"""
    st.subheader("📜 重要人物列表")

    # 尝试加载人物数据
    try:
        chars = load_wudai_detailed_characters()

        if chars:
            for sheet_name, df in chars.items():
                if not df.empty:
                    with st.expander(f"{sheet_name}"):
                        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.warning(f"加载人物数据失败：{e}")


def render_succession_table():
    """渲染世系对照表"""
    st.subheader("📋 五代帝王世系对照表")

    all_succession = get_all_succession_data()

    for regime, rulers in all_succession.items():
        st.markdown(f"#### {regime}")
        df = pd.DataFrame(rulers)
        st.dataframe(df, use_container_width=True)


def main():
    """主函数"""
    render_relationship_header()

    # 人物详情 - 使用 session state 管理
    if 'selected_character' not in st.session_state:
        st.session_state.selected_character = None

    # 侧边栏 - 人物选择器
    with st.sidebar:
        st.markdown("### 🔍 人物选择")

        all_succession = get_all_succession_data()

        # 按政权分组的人物列表
        selected_regime = st.selectbox(
            "选择政权",
            ["全部"] + list(all_succession.keys())
        )

        # 构建人物列表
        char_list = []
        for regime, rulers in all_succession.items():
            if selected_regime == "全部" or selected_regime == regime:
                for ruler in rulers:
                    char_list.append(f"{ruler['name']} ({regime})")

        selected_char = st.selectbox(
            "选择人物",
            char_list,
            index=0 if char_list else None
        )

        if selected_char:
            char_name = selected_char.split(' (')[0]
            st.session_state.selected_character = char_name

    # 显示人物详情（如果有选择）
    if st.session_state.selected_character:
        show_character_detail(st.session_state.selected_character)
    else:
        # 显示所有人物卡片概览
        st.subheader("👥 人物概览")
        all_succession = get_all_succession_data()

        cols = st.columns(5)
        idx = 0

        for regime, rulers in all_succession.items():
            for ruler in rulers:
                with cols[idx % 5]:
                    if st.button(
                        f"{ruler['name']}\n{regime}",
                        key=f"char_{ruler['name']}",
                        use_container_width=True,
                        help=ruler.get('bio', '')[:50] if ruler.get('bio') else None
                    ):
                        st.session_state.selected_character = ruler['name']
                        st.rerun()
                idx += 1

        st.markdown("---")

    # 关系网络图
    st.subheader("🕸️ 五代帝王关系网络")
    graph = render_relationship_graph()
    html(graph.render_embed(), height=650, scrolling=False)

    st.markdown("---")

    # 世系树选择器
    st.subheader("🌳 政权世系树")

    all_regimes = WUDAI_REGIMES + SHIGUO_REGIMES
    regime_names = [r['name'] for r in all_regimes]

    cols = st.columns(3)

    for i, regime in enumerate(regime_names):
        with cols[i % 3]:
            tree = render_succession_tree(regime)
            if tree:
                html(tree.render_embed(), height=650, scrolling=False)

    st.markdown("---")

    # 世系表
    render_succession_table()


if __name__ == "__main__":
    main()

