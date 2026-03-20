"""
📖 文献检索页面
全文搜索和关键词词云
"""
import streamlit as st
from streamlit.components.v1 import html

from pyecharts import options as opts
from pyecharts.charts import WordCloud
import pandas as pd

from src.data_loader import (
    load_wudai_history_text,
)
from src.text_analyzer import (
    segment_text,
    extract_keywords,
    extract_keywords_by_category,
    generate_wordcloud_data,
    search_text,
    analyze_text_statistics,
    get_text_summary,
)
from src.config import HISTORICAL_TERMS, QUICK_SEARCH_TERMS

st.set_page_config(page_title="文献检索", page_icon="📖", layout="wide")


def render_search_header():
    """渲染页面标题"""
    st.title("📖 文献检索")
    st.markdown("搜索《五代十国全史》全文内容，提取关键词")

    st.markdown("""
    **功能说明**：
    - 🔍 **全文搜索**：在《五代十国全史》中搜索关键词，显示相关段落和章节
    - ☁️ **关键词词云**：可视化展示文本中的高频词汇，字体大小代表词频
    - 🏷️ **分类关键词**：按人名、地名、政权、官职、事件分类提取关键词
    - 📊 **文本统计**：展示字符数、词数、段落数等文本基本信息
    """)

    st.markdown("---")


def render_search_box():
    """渲染搜索框"""
    col1, col2 = st.columns([4, 1])

    with col1:
        query = st.text_input(
            "🔍 搜索关键词",
            placeholder="输入关键词，如：朱温、后梁、开封...",
            label_visibility="collapsed"
        )

    with col2:
        search_btn = st.button("搜索", type="primary", use_container_width=True)

    return query, search_btn


def render_search_results(query: str, text: str):
    """渲染搜索结果"""
    if not query:
        return

    results = search_text(text, query, context_size=100)

    st.subheader(f"搜索结果：共找到 {len(results)} 处匹配")

    if results:
        for i, result in enumerate(results[:20], 1):
            with st.expander(f"结果 {i} - {result['chapter'] or '未知章节'}"):
                # 高亮关键词
                context = result['context']
                highlighted = context.replace(
                    query,
                    f"**{query}**"
                )
                st.markdown(f"...{highlighted}...")

                if result['position'] < 500:
                    st.caption(f"位置：第 {result['position']} 字符（文档开头）")
                else:
                    st.caption(f"位置：第 {result['position']} 字符")
    else:
        st.warning("未找到匹配结果")


def render_wordcloud(text: str):
    """渲染词云"""
    st.subheader("☁️ 关键词词云")

    wordcloud_data = generate_wordcloud_data(text, max_words=100)

    if wordcloud_data:
        wc = WordCloud(init_opts=opts.InitOpts(width="100%", height="500px"))

        wc.add(
            series_name="五代十国",
            data_pair=[(item['name'], item['value']) for item in wordcloud_data],
            word_size_range=[10, 50],
        )

        wc.set_global_opts(
            title_opts=opts.TitleOpts(title="《五代十国全史》关键词词云"),
        )

        html(wc.render_embed(), height=650, scrolling=False)


def render_category_keywords(text: str):
    """渲染分类关键词"""
    st.subheader("🏷️ 分类关键词")

    categories = extract_keywords_by_category(text)

    cols = st.columns(3)

    category_names = ['人名', '地名', '政权', '官职', '事件', '其他']

    for i, cat in enumerate(category_names):
        with cols[i % 3]:
            keywords = categories.get(cat, [])
            if keywords:
                st.markdown(f"#### {cat}")
                for word, freq in keywords[:10]:
                    st.markdown(f"- {word} ({freq}次)")


def render_text_overview(text: str):
    """渲染文本概览"""
    st.subheader("📄 文本概览")

    stats = analyze_text_statistics(text)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("总字符数", f"{stats['total_chars']:,}")

    with col2:
        st.metric("总词数", f"{stats['total_words']:,}")

    with col3:
        st.metric("不重复词数", stats['unique_words'])

    with col4:
        st.metric("句子数", stats['sentences'])

    with col5:
        st.metric("段落数", stats['paragraphs'])


def render_hot_keywords(text: str):
    """渲染热门关键词"""
    st.subheader("🔥 高频关键词 Top 50")

    keywords = extract_keywords(text, top_n=50)

    df = pd.DataFrame(keywords, columns=["关键词", "频次"])

    # 使用条形图展示
    from pyecharts.charts import Bar

    bar = Bar(init_opts=opts.InitOpts(width="100%", height="600px"))

    bar.add_xaxis(df['关键词'].tolist())
    bar.add_yaxis(
        "频次",
        df['频次'].tolist(),
        label_opts=opts.LabelOpts(position="top"),
    )

    bar.reversal_axis()

    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="高频关键词排行"),
        xaxis_opts=opts.AxisOpts(name="频次"),
        yaxis_opts=opts.AxisOpts(name="关键词"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
    )

    html(bar.render_embed(), height=650, scrolling=False)


def render_quick_search():
    """渲染快捷搜索"""
    st.subheader("⚡ 快捷搜索")

    # 使用统一配置的快捷搜索词
    quick_terms = QUICK_SEARCH_TERMS

    cols = st.columns(5)

    for i, term in enumerate(quick_terms):
        with cols[i % 5]:
            if st.button(term, key=f"quick_{term}", use_container_width=True):
                st.session_state['search_query'] = term


def render_historical_terms():
    """渲染历史专有名词表"""
    st.subheader("📚 历史专有名词索引")

    # 使用统一配置的分类历史专有名词
    terms_with_category = []

    for category, terms in HISTORICAL_TERMS.items():
        for term in terms:
            terms_with_category.append({'类别': category, '名词': term})

    terms_df = pd.DataFrame(terms_with_category)

    st.dataframe(terms_df, use_container_width=True)


def main():
    """主函数"""
    render_search_header()

    # 加载文本
    @st.cache_data
    def get_text():
        return load_wudai_history_text()

    text = get_text()

    if not text:
        st.error("无法加载《五代十国全史》文本")
        return

    # 文本概览
    render_text_overview(text)

    st.markdown("---")

    # 快捷搜索
    render_quick_search()

    # 搜索框
    query, search_btn = render_search_box()

    # 处理搜索
    if search_btn or query in st.session_state.get('search_query', ''):
        if query:
            render_search_results(query, text)
            st.markdown("---")

    # 词云
    render_wordcloud(text)

    st.markdown("---")

    # 分类关键词
    render_category_keywords(text)

    st.markdown("---")

    # 高频关键词
    render_hot_keywords(text)

    st.markdown("---")

    # 历史专有名词
    render_historical_terms()


if __name__ == "__main__":
    main()

