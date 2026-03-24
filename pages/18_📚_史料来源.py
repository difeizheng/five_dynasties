"""
📚 史料来源与学术引用
提供五代十国历史研究的史料来源和引用格式
"""

import streamlit as st

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import (
    get_historical_sources,
    get_citation_formats,
    get_citation_examples,
    get_source_categories,
)

st.set_page_config(
    page_title="史料来源与学术引用",
    page_icon="📚",
    layout="wide"
)

# 标题
st.title("📚 史料来源与学术引用")
st.markdown("提供五代十国历史研究的史料来源和标准引用格式")

st.markdown("""
**页面说明**：
- 📖 **史料分类**：正史、杂史野史、十国史料、笔记小说、现代研究
- 📝 **引用格式**：支持 GB/T 7714、APA、MLA、Chicago 等多种格式
- 💡 **引用示例**：展示具体历史事件的规范引用方法
- 🔗 **在线阅读**：提供部分史料的在线资源链接
""")

st.markdown("---")

# ============================================
# 选项卡布局
# ============================================
tab1, tab2, tab3, tab4 = st.tabs([
    "史料分类", "引用格式", "引用示例", "研究建议"
])

# --------------------------------------------
# 选项卡 1: 史料分类
# --------------------------------------------
with tab1:
    st.subheader("📖 史料分类")

    categories = get_source_categories()
    category_icons = {
        "正史": "📜",
        "杂史野史": "📋",
        "十国史料": "🏯",
        "笔记小说": "📔",
        "现代研究": "📖",
    }

    for category in categories:
        icon = category_icons.get(category, "📚")
        st.markdown(f"### {icon} {category}")

        sources = get_historical_sources(category)

        for source in sources:
            with st.expander(f"**{source['name']}** - {source.get('author', '佚名')} ({source.get('period', '')})"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**成书年代**: {source.get('year', '未知')}")
                    st.markdown(f"**卷数**: {source.get('chapters', '未知')}卷")
                    st.markdown(f"**简介**: {source.get('description', '')}")
                with col2:
                    if source.get('url'):
                        st.link_button("📖 在线阅读", source['url'])
                    else:
                        st.info("暂无在线资源")

        st.markdown("---")

# --------------------------------------------
# 选项卡 2: 引用格式
# --------------------------------------------
with tab2:
    st.subheader("📝 标准引用格式")

    formats = get_citation_formats()

    for format_name, template in formats.items():
        st.markdown(f"### {format_name}")
        st.code(template, language="text")
        st.markdown("---")

    # 使用说明
    st.info("""
    **💡 使用建议**：
    - **GB/T 7714**: 中国国家标准，适用于国内学术期刊和论文
    - **APA**: 美国心理学会格式，适用于社会科学领域
    - **MLA**: 现代语言协会格式，适用于人文学科
    - **Chicago**: 芝加哥格式，适用于历史学、艺术史等领域
    """)

# --------------------------------------------
# 选项卡 3: 引用示例
# --------------------------------------------
with tab3:
    st.subheader("💡 引用示例")

    examples = get_citation_examples()

    for example in examples:
        st.markdown(f"#### 📌 {example['content']}")
        st.markdown(f"**出处**: {example['source']}")

        cols = st.columns(3)
        for i, (format_name, citation) in enumerate(example['citation'].items()):
            with cols[i % 3]:
                st.markdown(f"**{format_name}**:")
                st.code(citation, language="text")

        st.divider()

# --------------------------------------------
# 选项卡 4: 研究建议
# --------------------------------------------
with tab4:
    st.subheader("📚 研究建议")

    st.markdown("""
    ### 史料选择建议

    #### 入门级研究
    1. **首选**: 《资治通鉴》- 记载详尽，叙事清晰
    2. **参考**: 《新五代史》- 文笔简练，便于入门
    3. **补充**: 《十国春秋》- 十国史料较为完备

    #### 进阶研究
    1. **核心史料**: 《旧五代史》（辑佚本）- 最接近原始记录
    2. **对比阅读**: 新旧五代史对照 - 发现史料差异
    3. **专题研究**: 《五代会要》- 典章制度研究

    #### 专业研究
    1. **多重印证**: 正史、杂史、笔记互证
    2. **域外史料**: 《高丽史》《日本纪》等周边国家记录
    3. **考古材料**: 墓志铭、出土文献

    ---

    ### 史料辨伪要点

    - **成书年代**: 注意史料成书时间与事件发生时间的间隔
    - **作者立场**: 考虑作者的政治立场和修史背景
    - **版本源流**: 注意版本差异和辑佚真伪
    - **互证比较**: 多方史料印证，避免单一来源

    ---

    ### 常见研究主题与推荐史料

    | 研究主题 | 推荐史料 | 备注 |
    |---------|---------|------|
    | 政治制度 | 《五代会要》《资治通鉴》 | 典章制度详尽 |
    | 军事战争 | 《资治通鉴》《旧五代史》 | 战役记载详细 |
    | 经济文化 | 《五代会要》《北梦琐言》 | 包含社会风貌 |
    | 人物传记 | 《旧五代史》《新五代史》 | 列传丰富 |
    | 十国历史 | 《十国春秋》《南唐书》 | 十国专史 |
    | 藩镇研究 | 《资治通鉴》《唐代藩镇研究》 | 藩镇问题核心 |
    """)

    st.markdown("---")

    st.subheader("🔗 推荐资源")

    st.markdown("""
    #### 在线数据库
    - [中国哲学书电子化计划](https://ctext.org/zhs) - 古代典籍在线检索
    - [国学大师](https://www.guoxuedashi.com/) - 古籍在线阅读
    - [维基文库](https://zh.wikisource.org/) - 免费古籍资源

    #### 学术资源
    - [中国知网](https://www.cnki.net/) - 学术论文检索
    - [JSTOR](https://www.jstor.org/) - 国际学术期刊
    - [Google Scholar](https://scholar.google.com/) - 学术搜索引擎

    #### 博物馆与考古
    - [故宫博物院](https://www.dpm.org.cn/) - 文物藏品
    - [中国国家博物馆](https://www.chnmuseum.cn/) - 历史文物
    """)

# 页脚
st.markdown("---")
st.markdown("💡 **提示**: 史料引用请根据具体研究需求选择合适的格式和版本。")
