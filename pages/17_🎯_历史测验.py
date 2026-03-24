"""
🎯 历史测验与成就系统
测试你的五代十国历史知识，解锁成就徽章
"""

import streamlit as st
import random

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import (
    get_quiz_database,
    get_quiz_levels,
    get_achievements,
    get_score_level,
)

st.set_page_config(
    page_title="历史测验与成就",
    page_icon="🎯",
    layout="wide"
)

# 标题
st.title("🎯 历史测验与成就系统")
st.markdown("测试你的五代十国历史知识，解锁成就徽章！")

st.markdown("""
**游戏说明**：
- 📝 选择难度级别开始测验
- ✅ 每答对一题获得相应分数
- 🏆 累积分数解锁成就徽章
- 📊 查看你的等级和排名
""")

st.markdown("---")

# ============================================
# 初始化 Session State
# ============================================
if 'user_score' not in st.session_state:
    st.session_state.user_score = 0
if 'achievements_unlocked' not in st.session_state:
    st.session_state.achievements_unlocked = []
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = []
if 'quiz_index' not in st.session_state:
    st.session_state.quiz_index = 0
if 'correct_count' not in st.session_state:
    st.session_state.correct_count = 0
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'current_level' not in st.session_state:
    st.session_state.current_level = None

# ============================================
# 侧边栏
# ============================================
with st.sidebar:
    st.markdown("### 👤 用户信息")

    # 显示得分和等级
    level = get_score_level(st.session_state.user_score)
    st.metric("当前得分", st.session_state.user_score)
    st.metric("当前等级", level)

    st.markdown("---")

    st.markdown("### 🏆 成就徽章")
    achievements = get_achievements()

    for name, data in achievements.items():
        if name in st.session_state.achievements_unlocked:
            st.success(f"{data['icon']} {name}")
        else:
            st.info(f"🔒 {name}")

    st.markdown("---")

    # 重置进度按钮
    if st.button("🔄 重置进度", use_container_width=True):
        st.session_state.user_score = 0
        st.session_state.achievements_unlocked = []
        st.session_state.quiz_started = False
        st.session_state.current_quiz = []
        st.session_state.quiz_index = 0
        st.session_state.correct_count = 0
        st.rerun()

# ============================================
# 主游戏区域
# ============================================

if not st.session_state.quiz_started:
    # 显示难度选择
    st.markdown("### 📝 选择难度级别")

    levels = get_quiz_levels()
    level_descriptions = {
        "入门级": "适合新手，5 道题，答对 4 题获得成就",
        "进阶级": "适合进阶学习，5 道题，答对 4 题获得成就",
        "专家级": "挑战高难度，5 道题，答对 4 题获得成就",
    }

    cols = st.columns(3)
    for i, level in enumerate(levels):
        with cols[i % 3]:
            st.markdown(f"#### {level}")
            st.markdown(level_descriptions.get(level, ""))
            if st.button(f"开始 {level}", key=f"start_{level}", use_container_width=True):
                st.session_state.current_level = level
                st.session_state.current_quiz = get_quiz_database(level)
                random.shuffle(st.session_state.current_quiz)
                st.session_state.current_quiz = st.session_state.current_quiz[:5]  # 只取 5 题
                st.session_state.quiz_index = 0
                st.session_state.correct_count = 0
                st.session_state.quiz_started = True
                st.rerun()

    st.markdown("---")

    # 等级说明
    st.markdown("### 📊 等级说明")
    score_levels = {
        "初学者": "0-49 分",
        "学徒": "50-99 分",
        "学者": "100-199 分",
        "博学家": "200-299 分",
        "历史达人": "300-499 分",
        "五代通": "500-999 分",
        "历史宗师": "1000 分以上",
    }

    cols = st.columns(7)
    for i, (level_name, score_range) in enumerate(score_levels.items()):
        with cols[i % 7]:
            if level == level_name:
                st.success(f"**{level_name}**\n{score_range}")
            else:
                st.info(f"{level_name}\n{score_range}")
else:
    # 测验进行中
    st.markdown("### 📝 答题中")

    # 显示进度
    progress = st.progress((st.session_state.quiz_index + 1) / len(st.session_state.current_quiz))

    if st.session_state.quiz_index >= len(st.session_state.current_quiz):
        # 测验结束
        st.success("🎉 测验完成！")

        # 计算得分
        correct_rate = st.session_state.correct_count / len(st.session_state.current_quiz)
        points_earned = int(20 * correct_rate * len(st.session_state.current_quiz))
        st.session_state.user_score += points_earned

        st.metric("答对题数", f"{st.session_state.correct_count} / {len(st.session_state.current_quiz)}")
        st.metric("获得分数", points_earned)

        # 检查成就
        achievements = get_achievements()
        if correct_rate >= 0.8:
            achievement_name = None
            if st.session_state.current_level == "入门级":
                achievement_name = "入门学者"
            elif st.session_state.current_level == "进阶级":
                achievement_name = "进阶学者"
            elif st.session_state.current_level == "专家级":
                achievement_name = "历史专家"

            if achievement_name and achievement_name not in st.session_state.achievements_unlocked:
                st.session_state.achievements_unlocked.append(achievement_name)
                st.balloons()
                st.success(f"🎉 解锁新成就：{achievements[achievement_name]['icon']} {achievement_name}！")

        # 按钮
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 继续测验", use_container_width=True):
                st.session_state.quiz_started = False
                st.session_state.current_quiz = []
                st.session_state.quiz_index = 0
                st.rerun()
        with col2:
            if st.button("📚 返回主页", use_container_width=True):
                st.session_state.quiz_started = False
                st.session_state.current_quiz = []
                st.session_state.quiz_index = 0
                st.rerun()
    else:
        # 显示当前题目
        quiz = st.session_state.current_quiz[st.session_state.quiz_index]

        st.markdown(f"**第 {st.session_state.quiz_index + 1} 题：{quiz['question']}**")

        # 显示选项
        options = quiz['options']

        # 使用 radio 选择
        selected = st.radio(
            "请选择答案：",
            options,
            key=f"q_{st.session_state.quiz_index}"
        )

        # 提交按钮
        if st.button("提交答案"):
            selected_index = options.index(selected)
            correct_index = quiz['answer']

            if selected_index == correct_index:
                st.session_state.correct_count += 1
                st.success(f"✅ 正确！{quiz.get('explanation', '')}")
            else:
                st.error(f"❌ 错误。正确答案是：{options[correct_index]}。\n\n{quiz.get('explanation', '')}")

            st.session_state.quiz_index += 1
            st.rerun()

# 页脚
st.markdown("---")
st.markdown("💡 提示：多浏览网站内容可以提高答题正确率哦！")
