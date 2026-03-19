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
)

st.set_page_config(page_title="人物关系", page_icon="👥", layout="wide")


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
    # 五代帝王更迭数据
    succession_data = {
        "后梁": [
            {"name": "朱温", "relation": "开国皇帝", "years": "907-912"},
            {"name": "朱友珪", "relation": "子", "years": "912-913"},
            {"name": "朱友贞", "relation": "子", "years": "913-923"},
        ],
        "后唐": [
            {"name": "李存勖", "relation": "开国皇帝", "years": "923-926"},
            {"name": "李嗣源", "relation": "养子", "years": "926-933"},
            {"name": "李从厚", "relation": "子", "years": "933-934"},
            {"name": "李从珂", "relation": "养子", "years": "934-936"},
        ],
        "后晋": [
            {"name": "石敬瑭", "relation": "开国皇帝", "years": "936-942"},
            {"name": "石重贵", "relation": "侄", "years": "942-947"},
        ],
        "后汉": [
            {"name": "刘知远", "relation": "开国皇帝", "years": "947-950"},
            {"name": "刘承祐", "relation": "子", "years": "950-951"},
        ],
        "后周": [
            {"name": "郭威", "relation": "开国皇帝", "years": "951-954"},
            {"name": "柴荣", "relation": "养子", "years": "954-959"},
            {"name": "柴宗训", "relation": "子", "years": "959-960"},
        ],
    }

    return succession_data


def generate_shiguo_succession_tree():
    """生成十国世系树数据"""
    succession_data = {
        "吴越": [
            {"name": "钱镠", "relation": "开国君主", "years": "907-932"},
            {"name": "钱元瓘", "relation": "子", "years": "932-941"},
            {"name": "钱弘佐", "relation": "子", "years": "941-947"},
            {"name": "钱弘倧", "relation": "弟", "years": "947"},
            {"name": "钱弘俶", "relation": "弟", "years": "947-978"},
        ],
        "南唐": [
            {"name": "李昪", "relation": "开国君主", "years": "937-943"},
            {"name": "李璟", "relation": "子", "years": "943-961"},
            {"name": "李煜", "relation": "子", "years": "961-975"},
        ],
        "前蜀": [
            {"name": "王建", "relation": "开国君主", "years": "907-918"},
            {"name": "王衍", "relation": "子", "years": "918-925"},
        ],
        "后蜀": [
            {"name": "孟知祥", "relation": "开国君主", "years": "934-935"},
            {"name": "孟昶", "relation": "子", "years": "935-965"},
        ],
        "闽国": [
            {"name": "王审知", "relation": "开国君主", "years": "909-925"},
            {"name": "王延翰", "relation": "子", "years": "925-927"},
            {"name": "王延钧", "relation": "弟", "years": "927-935"},
            {"name": "王继鹏", "relation": "子", "years": "935-939"},
            {"name": "王延羲", "relation": "叔", "years": "939-944"},
            {"name": "王延政", "relation": "弟", "years": "944-945"},
        ],
        "南汉": [
            {"name": "刘䶮", "relation": "开国君主", "years": "917-942"},
            {"name": "刘玢", "relation": "子", "years": "942-943"},
            {"name": "刘晟", "relation": "弟", "years": "943-958"},
            {"name": "刘鋹", "relation": "子", "years": "958-971"},
        ],
        "楚": [
            {"name": "马殷", "relation": "开国君主", "years": "907-930"},
            {"name": "马希声", "relation": "子", "years": "930-932"},
            {"name": "马希范", "relation": "弟", "years": "932-947"},
            {"name": "马希广", "relation": "弟", "years": "947-950"},
            {"name": "马希萼", "relation": "兄", "years": "950-951"},
        ],
        "荆南": [
            {"name": "高季兴", "relation": "开国君主", "years": "924-928"},
            {"name": "高从诲", "relation": "子", "years": "928-948"},
            {"name": "高保融", "relation": "子", "years": "948-960"},
            {"name": "高保勖", "relation": "子", "years": "960-962"},
            {"name": "高继冲", "relation": "侄", "years": "962-963"},
        ],
        "北汉": [
            {"name": "刘崇", "relation": "开国君主", "years": "951-954"},
            {"name": "刘承钧", "relation": "子", "years": "954-968"},
            {"name": "刘继恩", "relation": "子", "years": "968"},
            {"name": "刘继元", "relation": "养子", "years": "968-979"},
        ],
    }

    return succession_data


def render_succession_tree(regime_name: str):
    """渲染单个政权的世系树"""
    wudai_data = generate_wudai_succession_tree()
    shiguo_data = generate_shiguo_succession_tree()

    all_data = {**wudai_data, **shiguo_data}

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

    # 五代帝王
    wudai_data = generate_wudai_succession_tree()
    for regime, rulers in wudai_data.items():
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

    wudai_data = generate_wudai_succession_tree()

    for regime, rulers in wudai_data.items():
        st.markdown(f"#### {regime}")
        df = pd.DataFrame(rulers)
        st.dataframe(df, use_container_width=True)


def main():
    """主函数"""
    render_relationship_header()

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

