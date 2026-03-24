"""
📚 文化百科
展示五代十国时期的科举制度、教育机构、重要典籍、传统节日、服饰文化、饮食文化、居住文化和科技成就
"""
import streamlit as st
import pandas as pd
from src.config import (
    get_coexam_system,
    get_education_system,
    get_important_books,
    get_printing_tech,
    get_festivals,
    get_clothing_culture,
    get_food_culture,
    get_housing_culture,
    get_tech_achievements,
)

st.set_page_config(page_title="文化百科", page_icon="📚", layout="wide")

st.title("📚 文化百科")
st.markdown("探索五代十国时期的文化制度与民俗风情")

st.markdown("""
**页面说明**：
- 🎓 **科举制度**：考试科目、著名状元、考试内容
- 🏛️ **教育机构**：国子监、书院、私塾
- 📖 **重要典籍**：史书、词集、笔记、专著
- 🖨️ **印刷术**：雕版印刷的发展与代表作品
- 🏮 **传统节日**：春节、元宵、清明、端午等节日习俗
- 👘 **服饰文化**：官服、民服、宫廷服饰、发式
- 🍜 **饮食文化**：名菜、茶酒、饮食习俗
- 🏡 **居住文化**：民居、家具、陈设、宫殿建筑
- 🔬 **科技成就**：印刷术、天文历法、医药学、建筑技术
""")

st.markdown("---")

# 选项卡布局
tabs = st.tabs([
    "🎓 科举制度",
    "🏛️ 教育机构",
    "📖 重要典籍",
    "🖨️ 印刷术",
    "🏮 传统节日",
    "👘 服饰文化",
    "🍜 饮食文化",
    "🏡 居住文化",
    "🔬 科技成就",
])

# --------------------------------------------
# 科举制度
# --------------------------------------------
with tabs[0]:
    st.subheader("🎓 科举制度")

    coexam = get_coexam_system()

    # 概述
    st.markdown(f"**概述**：{coexam.get('概述', '')}")

    st.markdown("---")

    # 考试科目
    st.markdown("### 📝 考试科目")
    exam_subjects = coexam.get('考试科目', [])
    if exam_subjects:
        df_subjects = pd.DataFrame(exam_subjects)
        st.dataframe(df_subjects, use_container_width=True, hide_index=True)

    st.markdown("---")

    # 著名状元
    st.markdown("### 🏆 著名状元")
    famous_zhuangyuan = coexam.get('著名状元', [])
    if famous_zhuangyuan:
        df_zhuangyuan = pd.DataFrame(famous_zhuangyuan)
        st.dataframe(df_zhuangyuan, use_container_width=True, hide_index=True)

    st.markdown("---")

    # 考试内容
    st.markdown("### 📚 考试内容")
    exam_content = coexam.get('考试内容', {})
    for subject, content in exam_content.items():
        st.markdown(f"**{subject}**: {content}")

# --------------------------------------------
# 教育机构
# --------------------------------------------
with tabs[1]:
    st.subheader("🏛️ 教育机构")

    education = get_education_system()

    # 国子监
    st.markdown("### 🏛️ 国子监")
    guozijian = education.get('国子监', {})
    if guozijian:
        st.markdown(f"**描述**: {guozijian.get('description', '')}")
        st.markdown(f"**位置**: {guozijian.get('location', '')}")
        st.markdown(f"**学生**: {guozijian.get('students', '')}")
        st.markdown(f"**课程**: {', '.join(guozijian.get('curriculum', []))}")
        st.markdown(f"**著名教师**: {', '.join(guozijian.get('famous_teachers', []))}")

    st.markdown("---")

    # 书院
    st.markdown("### 📚 书院")
    shuyuan = education.get('书院', {})
    if shuyuan:
        st.markdown(f"**描述**: {shuyuan.get('description', '')}")
        famous_academies = shuyuan.get('famous_academies', [])
        if famous_academies:
            df_academies = pd.DataFrame(famous_academies)
            st.dataframe(df_academies, use_container_width=True, hide_index=True)

    st.markdown("---")

    # 私塾
    st.markdown("### 📖 私塾")
    shudu = education.get('私塾', {})
    if shudu:
        st.markdown(f"**描述**: {shudu.get('description', '')}")
        st.markdown(f"**学生**: {shudu.get('students', '')}")
        st.markdown(f"**课程**: {', '.join(shudu.get('curriculum', []))}")

# --------------------------------------------
# 重要典籍
# --------------------------------------------
with tabs[2]:
    st.subheader("📖 重要典籍")

    books = get_important_books()

    # 分类筛选
    categories = list(set(b.get('category') for b in books if b.get('category')))
    selected_category = st.selectbox("按类别筛选", options=["全部"] + categories)

    if selected_category != "全部":
        books = [b for b in books if b.get('category') == selected_category]

    # 显示典籍列表
    for book in books:
        title = book.get('title', '未知典籍')
        with st.expander(f"**📕 {title}** - {book.get('author', '佚名')} ({book.get('regime', '')})"):
            st.markdown(f"**类别**: {book.get('category', '')}")
            st.markdown(f"**年代**: {book.get('year', '未知')}年")
            st.markdown(f"**简介**: {book.get('description', '')}")

# --------------------------------------------
# 印刷术
# --------------------------------------------
with tabs[3]:
    st.subheader("🖨️ 印刷术")

    printing = get_printing_tech()

    # 雕版印刷
    st.markdown("### 📜 雕版印刷")
    diaoban = printing.get('雕版印刷', {})
    if diaoban:
        st.markdown(f"**描述**: {diaoban.get('description', '')}")

        st.markdown("**代表作品**:")
        famous_works = diaoban.get('famous_works', [])
        for work in famous_works:
            st.markdown(f"- **{work.get('name')}** ({work.get('year', '?')}年) - {work.get('description', '')}")

        st.markdown(f"**印刷中心**: {', '.join(diaoban.get('centers', []))}")

    st.markdown("---")

    # 活字印刷
    st.markdown("### 🔤 活字印刷")
    huozi = printing.get('活字印刷', {})
    if huozi:
        st.markdown(f"**描述**: {huozi.get('description', '')}")
        st.info(huozi.get('note', ''))

# --------------------------------------------
# 传统节日
# --------------------------------------------
with tabs[4]:
    st.subheader("🏮 传统节日")

    festivals = get_festivals()

    # 节日选择
    festival_names = list(festivals.keys())
    selected_festival = st.selectbox("选择节日", festival_names)

    if selected_festival:
        festival = festivals.get(selected_festival, {})

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**日期**: {festival.get('date', '')}")
            st.markdown(f"**描述**: {festival.get('description', '')}")
            st.markdown("**活动**:")
            for activity in festival.get('activities', []):
                st.markdown(f"- {activity}")

        with col2:
            st.markdown("**食品**:")
            for food in festival.get('food', []):
                st.markdown(f"- {food}")

        st.markdown("---")
        st.info(f"**📖 历史故事**: {festival.get('story', '')}")

# --------------------------------------------
# 服饰文化
# --------------------------------------------
with tabs[5]:
    st.subheader("👘 服饰文化")

    clothing = get_clothing_culture()

    # 官服
    st.markdown("### 👔 官服")
    guanfu = clothing.get('官服', {})
    if guanfu:
        st.markdown(f"**描述**: {guanfu.get('description', '')}")

        st.markdown("**品级与颜色**:")
        levels = guanfu.get('levels', [])
        for level in levels:
            st.markdown(f"- {level.get('color')}色 ({level.get('rank')}): {level.get('pattern', '')}")

        st.markdown(f"**配饰**: {', '.join(guanfu.get('accessories', []))}")

    st.markdown("---")

    # 民服
    st.markdown("### 👕 民服")
    minfu = clothing.get('民服', {})
    if minfu:
        st.markdown(f"**描述**: {minfu.get('description', '')}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**男子服饰**:")
            for item in minfu.get('men', []):
                st.markdown(f"- {item}")
        with col2:
            st.markdown("**女子服饰**:")
            for item in minfu.get('women', []):
                st.markdown(f"- {item}")

        st.markdown(f"**布料**: {', '.join(minfu.get('fabric', []))}")

    st.markdown("---")

    # 宫廷服饰
    st.markdown("### 👑 宫廷服饰")
    gongting = clothing.get('宫廷服饰', {})
    if gongting:
        for role, items in gongting.items():
            st.markdown(f"**{role}**: {', '.join(items)}")

    st.markdown("---")

    # 发式
    st.markdown("### 💇 发式")
    faishi = clothing.get('发式', {})
    if faishi:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**男子**:")
            for item in faishi.get('男子', []):
                st.markdown(f"- {item}")
        with col2:
            st.markdown("**女子**:")
            for item in faishi.get('女子', []):
                st.markdown(f"- {item}")

        st.markdown(f"**发饰**: {', '.join(faishi.get('accessories', []))}")

# --------------------------------------------
# 饮食文化
# --------------------------------------------
with tabs[6]:
    st.subheader("🍜 饮食文化")

    food = get_food_culture()

    # 名菜
    st.markdown("### 🍲 名菜")
    mingcai = food.get('名菜', [])
    if mingcai:
        for dish in mingcai:
            st.markdown(f"- **{dish.get('name')}** ({dish.get('regime', '')}): {dish.get('description', '')}")

    st.markdown("---")

    # 茶酒
    st.markdown("### 🍵 茶酒")
    chajiu = food.get('茶酒', {})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 茶")
        cha = chajiu.get('茶', {})
        if cha:
            st.markdown(f"**描述**: {cha.get('description', '')}")
            st.markdown(f"**种类**: {', '.join(cha.get('types', []))}")
            st.markdown(f"**名茶**: {', '.join(cha.get('famous', []))}")
            st.info(cha.get('story', ''))

    with col2:
        st.markdown("#### 酒")
        jiu = chajiu.get('酒', {})
        if jiu:
            st.markdown(f"**描述**: {jiu.get('description', '')}")
            st.markdown(f"**种类**: {', '.join(jiu.get('types', []))}")
            st.markdown(f"**名酒**: {', '.join(jiu.get('famous', []))}")
            st.info(jiu.get('story', ''))

    st.markdown("---")

    # 饮食习俗
    st.markdown("### 🥢 饮食习俗")
    xisu = food.get('饮食习俗', {})
    for key, value in xisu.items():
        st.markdown(f"**{key}**: {value}")

# --------------------------------------------
# 居住文化
# --------------------------------------------
with tabs[7]:
    st.subheader("🏡 居住文化")

    housing = get_housing_culture()

    # 民居
    st.markdown("### 🏠 民居")
    minju = housing.get('民居', {})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 北方民居")
        beifang = minju.get('北方', {})
        if beifang:
            st.markdown(f"**类型**: {', '.join(beifang.get('type', []))}")
            st.markdown(f"**材料**: {', '.join(beifang.get('material', []))}")
            st.markdown(f"**特点**: {', '.join(beifang.get('features', []))}")

    with col2:
        st.markdown("#### 南方民居")
        nanfang = minju.get('南方', {})
        if nanfang:
            st.markdown(f"**类型**: {', '.join(nanfang.get('type', []))}")
            st.markdown(f"**材料**: {', '.join(nanfang.get('material', []))}")
            st.markdown(f"**特点**: {', '.join(nanfang.get('features', []))}")

    st.markdown("---")

    # 家具
    st.markdown("### 🪑 家具")
    jiaju = housing.get('家具', {})
    if jiaju:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("**坐具**:")
            for item in jiaju.get('坐具', []):
                st.markdown(f"- {item}")
        with col2:
            st.markdown("**卧具**:")
            for item in jiaju.get('卧具', []):
                st.markdown(f"- {item}")
        with col3:
            st.markdown("**案几**:")
            for item in jiaju.get('案几', []):
                st.markdown(f"- {item}")
        with col4:
            st.markdown("**储物**:")
            for item in jiaju.get('storage', []):
                st.markdown(f"- {item}")

        st.markdown(f"**特点**: {jiaju.get('features', '')}")

    st.markdown("---")

    # 陈设
    st.markdown("### 🏺 室内陈设")
    chenshe = housing.get('陈设', {})
    if chenshe:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**室内**:")
            for item in chenshe.get('室内', []):
                st.markdown(f"- {item}")
        with col2:
            st.markdown("**文房**:")
            for item in chenshe.get('文房', []):
                st.markdown(f"- {item}")
        with col3:
            st.markdown("**装饰品**:")
            for item in chenshe.get('decorations', []):
                st.markdown(f"- {item}")

    st.markdown("---")

    # 宫殿建筑
    st.markdown("### 🏰 宫殿建筑")
    gongdian = housing.get('宫殿建筑', {})
    if gongdian:
        st.markdown(f"**特点**: {', '.join(gongdian.get('特点', []))}")
        st.markdown(f"**代表**: {', '.join(gongdian.get('代表', []))}")

# --------------------------------------------
# 科技成就
# --------------------------------------------
with tabs[8]:
    st.subheader("🔬 科技成就")

    tech = get_tech_achievements()

    for category, info in tech.items():
        st.markdown(f"### {category}")
        st.markdown(f"**描述**: {info.get('description', '')}")
        st.markdown(f"**代表**: {info.get('representative', '')}")
        st.markdown(f"**影响**: {info.get('impact', '')}")
        st.markdown("---")

st.markdown("---")
st.markdown("数据来源：历史资料整理")
