"""
📖 历史故事模式
互动式历史推演，体验关键历史时刻的选择
"""

import streamlit as st

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import (
    get_history_stories,
    get_story_by_name,
    get_story_categories,
)

st.set_page_config(
    page_title="历史故事模式",
    page_icon="📖",
    layout="wide"
)

# 标题
st.title("📖 历史故事模式")
st.markdown("互动式历史推演，体验关键历史时刻的选择，改写或重现历史")

st.markdown("""
**游戏说明**：
- 📖 选择一个历史故事开始
- 🔀 在关键节点做出选择
- 🎯 不同的选择会导致不同的结局
- 📚 学习真实的历史背景知识
""")

st.markdown("---")

# ============================================
# 初始化 Session State
# ============================================
if 'current_story' not in st.session_state:
    st.session_state.current_story = None
if 'current_chapter' not in st.session_state:
    st.session_state.current_chapter = 0
if 'story_history' not in st.session_state:
    st.session_state.story_history = []
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# ============================================
# 侧边栏 - 故事选择
# ============================================
with st.sidebar:
    st.markdown("### 📚 故事列表")

    # 分类选择
    categories = get_story_categories()
    selected_category = st.selectbox(
        "选择分类",
        options=["全部"] + list(categories.keys())
    )

    # 获取故事列表
    all_stories = get_history_stories()

    if selected_category != "全部":
        story_list = categories.get(selected_category, [])
    else:
        story_list = list(all_stories.keys())

    selected_story = st.selectbox(
        "选择故事",
        options=story_list
    )

    # 开始游戏按钮
    if st.button("🎮 开始游戏", use_container_width=True):
        st.session_state.current_story = selected_story
        st.session_state.current_chapter = 0
        st.session_state.story_history = []
        st.session_state.game_started = True
        st.rerun()

    # 重置按钮
    if st.button("🔄 重置进度", use_container_width=True):
        st.session_state.current_story = None
        st.session_state.current_chapter = 0
        st.session_state.story_history = []
        st.session_state.game_started = False
        st.rerun()

    st.markdown("---")

    # 游戏说明
    st.markdown("### ❓ 如何游玩")
    st.markdown("""
    1. 从侧边栏选择一个历史故事
    2. 点击"开始游戏"
    3. 阅读章节内容
    4. 在关键节点做出选择
    5. 体验不同的历史结局
    """)

# ============================================
# 主游戏区域
# ============================================

if not st.session_state.game_started or not st.session_state.current_story:
    # 显示故事选择卡片
    st.markdown("### 📖 选择一个历史故事开始")

    all_stories = get_history_stories()
    categories = get_story_categories()

    for category, stories in categories.items():
        st.markdown(f"#### {category}")
        cols = st.columns(len(stories))
        for i, story_name in enumerate(stories):
            story = all_stories.get(story_name, {})
            with cols[i % len(cols)]:
                if st.button(
                    f"{story.get('title', story_name)}\n"
                    f"难度：{story.get('difficulty', '未知')}\n"
                    f"时长：{story.get('duration', '未知')}",
                    key=f"story_{story_name}",
                    use_container_width=True
                ):
                    st.session_state.current_story = story_name
                    st.session_state.current_chapter = 0
                    st.session_state.story_history = []
                    st.session_state.game_started = True
                    st.rerun()
        st.markdown("---")

    # 显示故事详情
    st.markdown("### 📜 故事详情")

    if selected_story:
        story = all_stories.get(selected_story, {})
        if story:
            st.markdown(f"**标题**: {story.get('title', selected_story)}")
            st.markdown(f"**时期**: {story.get('period', '未知')}")
            st.markdown(f"**主角**: {story.get('protagonist', '未知')}")
            st.markdown(f"**难度**: {story.get('difficulty', '未知')}")
            st.markdown(f"**时长**: {story.get('duration', '未知')}")
            st.markdown(f"**历史注释**: {story.get('historical_notes', '')}")
else:
    # 游戏进行中
    story_name = st.session_state.current_story
    story = get_story_by_name(story_name)

    if not story:
        st.error("故事数据加载失败")
        st.stop()

    # 显示进度
    progress = st.progress(0)
    chapters = story.get('chapters', [])
    current_index = st.session_state.current_chapter

    if current_index >= len(chapters):
        # 游戏结束
        progress.progress(1.0)
        st.success("🎉 故事已完结！")
        st.markdown("### 游戏历程")
        for i, chapter_name in enumerate(st.session_state.story_history):
            st.markdown(f"{i+1}. {chapter_name}")
        st.markdown(f"**历史注释**: {story.get('historical_notes', '')}")

        if st.button("🔄 重新开始"):
            st.session_state.current_chapter = 0
            st.session_state.story_history = []
            st.rerun()

        if st.button("📚 返回故事列表"):
            st.session_state.current_story = None
            st.session_state.game_started = False
            st.rerun()
    else:
        # 显示当前章节
        chapter = chapters[current_index]

        # 更新进度条
        progress.progress((current_index + 1) / len(chapters))

        # 显示章节标题
        st.markdown(f"### {story.get('title', story_name)}")
        st.markdown(f"**{chapter.get('title', f'第{current_index+1}章')}**")

        # 显示章节内容
        st.markdown(chapter.get('content', ''))

        # 显示选择按钮
        choices = chapter.get('choices', [])

        if choices:
            st.markdown("### 你的选择：")
            cols = st.columns(len(choices))

            for i, choice in enumerate(choices):
                with cols[i % len(cols)]:
                    if st.button(
                        choice.get('text', f"选项{i+1}"),
                        key=f"choice_{current_index}_{i}",
                        use_container_width=True
                    ):
                        # 记录历史
                        st.session_state.story_history.append(chapter.get('title', f'章节{current_index+1}'))

                        # 跳转到下一章节
                        next_chapter = choice.get('next', f'chapter_{current_index+2}')

                        # 查找下一章索引
                        found = False
                        for i, ch in enumerate(chapters):
                            if ch.get('title') == next_chapter or f"chapter_{i+1}" == next_chapter:
                                st.session_state.current_chapter = i
                                found = True
                                break

                        # 如果是结局章节
                        if next_chapter.startswith('ending_'):
                            for i, ch in enumerate(chapters):
                                if ch.get('title', '').startswith('结局'):
                                    st.session_state.current_chapter = i
                                    found = True
                                    break

                        if not found:
                            # 默认下一章
                            st.session_state.current_chapter = current_index + 1

                        st.rerun()

        st.markdown("---")

        # 显示历史注释
        with st.expander("📜 查看历史背景"):
            st.markdown(f"**真实历史**: {story.get('historical_notes', '暂无')}")
            st.markdown(f"**时期**: {story.get('period', '未知')}")
            st.markdown(f"**主角**: {story.get('protagonist', '未知')}")

# 页脚
st.markdown("---")
st.markdown("注：本游戏基于历史资料创作，部分情节有所改编，仅供娱乐学习。")
