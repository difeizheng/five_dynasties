"""
📤 数据分享与导出
导出你的学习进度，与朋友分享成就
"""

import streamlit as st
import json
import base64
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.streamlit_utils import (
    export_user_data_to_json,
    export_session_state_to_json,
    import_session_state_from_json,
    render_import_file_uploader,
)

st.set_page_config(
    page_title="数据分享与导出",
    page_icon="📤",
    layout="wide"
)

# 标题
st.title("📤 数据分享与导出")
st.markdown("导出你的学习进度，与朋友分享成就，或在新设备上恢复数据")

st.markdown("""
**功能说明**：
- 📥 **导出数据**：将学习进度、收藏和成就导出为 JSON 文件
- 📦 **导入数据**：从 JSON 文件恢复学习进度
- 🔗 **生成分享卡**：生成精美的成就分享卡片
- 📊 **数据统计**：查看你的学习数据统计
""")

st.markdown("---")

# ============================================
# 初始化 Session State
# ============================================
if 'user_score' not in st.session_state:
    st.session_state.user_score = 0
if 'achievements_unlocked' not in st.session_state:
    st.session_state.achievements_unlocked = []
if 'bookmarked_items' not in st.session_state:
    st.session_state.bookmarked_items = []
if 'quiz_history' not in st.session_state:
    st.session_state.quiz_history = []
if 'story_progress' not in st.session_state:
    st.session_state.story_progress = {}
if 'visit_history' not in st.session_state:
    st.session_state.visit_history = []

# ============================================
# 选项卡布局
# ============================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📥 导出数据", "📦 导入数据", "🔗 生成分享卡", "📊 数据统计"
])

# --------------------------------------------
# 选项卡 1: 导出数据
# --------------------------------------------
with tab1:
    st.subheader("📥 导出我的数据")

    st.markdown("""
    选择要导出的数据类型，生成 JSON 文件保存到本地。
    你可以将这份文件保存到安全的地方，或在新设备上导入恢复。
    """)

    # 选择要导出的数据类型
    st.markdown("### 选择数据类型")

    data_options = {
        "user_score": ("🏆 测验得分", st.session_state.user_score),
        "achievements_unlocked": ("🎖️ 解锁成就", len(st.session_state.achievements_unlocked)),
        "bookmarked_items": ("⭐ 收藏内容", len(st.session_state.bookmarked_items)),
        "quiz_history": ("📝 测验历史", len(st.session_state.quiz_history)),
        "story_progress": ("📖 故事进度", len(st.session_state.story_progress)),
    }

    selected_data_types = st.multiselect(
        "勾选要导出的数据",
        options=list(data_options.keys()),
        default=list(data_options.keys()),
        format_func=lambda x: f"{data_options[x][0]} ({data_options[x][1]})"
    )

    if selected_data_types:
        st.markdown("---")

        if st.button("🔧 生成导出文件", type="primary", use_container_width=True):
            user_data = export_session_state_to_json(
                include_keys=selected_data_types,
                exclude_keys=['temp_export_data']
            )

            # 添加元数据
            user_data['_export_info'] = {
                'export_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'version': '1.0',
                'data_types': selected_data_types
            }

            st.session_state.export_data = user_data

            st.success("✅ 数据已准备就绪！")

            st.markdown("### 下载文件")
            export_user_data_to_json(user_data, f"five_dynasties_backup_{datetime.now().strftime('%Y%m%d')}.json")

            # 显示预览
            with st.expander("👁️ 预览导出数据"):
                st.json(user_data)

    st.markdown("---")

    st.info("""
    💡 **提示**：
    - 导出的文件是 JSON 格式，可以用任何文本编辑器打开查看
    - 建议定期备份你的学习进度
    - 文件包含你的个人数据，请妥善保管
    """)

# --------------------------------------------
# 选项卡 2: 导入数据
# --------------------------------------------
with tab2:
    st.subheader("📦 导入数据")

    st.markdown("""
    从之前导出的 JSON 文件中恢复学习进度。
    你可以选择覆盖当前数据或合并到现有数据中。
    """)

    st.markdown("### 上传文件")

    uploaded_file = st.file_uploader(
        "选择要导入的 JSON 文件",
        type=["json"],
        help="请选择之前导出的 .json 格式文件"
    )

    if uploaded_file is not None:
        try:
            content = uploaded_file.read().decode('utf-8')
            imported_data = json.loads(content)

            st.success("✅ 文件解析成功！")

            # 显示文件信息
            if '_export_info' in imported_data:
                with st.expander("📋 文件信息"):
                    st.json(imported_data['_export_info'])

            # 显示数据预览
            with st.expander("👁️ 数据预览"):
                display_data = {k: v for k, v in imported_data.items() if not k.startswith('_')}
                st.json(display_data)

            st.markdown("### 选择导入方式")

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "🔄 覆盖当前数据",
                    use_container_width=True,
                    help="将当前数据完全替换为导入的数据"
                ):
                    for key, value in imported_data.items():
                        if not key.startswith('_'):
                            st.session_state[key] = value
                    st.success("✅ 数据已覆盖！页面将自动刷新...")
                    st.rerun()

            with col2:
                if st.button(
                    "➕ 合并到当前数据",
                    use_container_width=True,
                    help="将导入的数据合并到现有数据中"
                ):
                    import_session_state_from_json(
                        {k: v for k, v in imported_data.items() if not k.startswith('_')},
                        merge=True
                    )
                    st.success("✅ 数据已合并！页面将自动刷新...")
                    st.rerun()

            # 显示数据类型
            st.markdown("### 可导入的数据")

            data_summary = []
            for key, value in imported_data.items():
                if key.startswith('_'):
                    continue
                if isinstance(value, list):
                    data_summary.append(f"- **{key}**: {len(value)} 条记录")
                elif isinstance(value, dict):
                    data_summary.append(f"- **{key}**: {len(value)} 项")
                else:
                    data_summary.append(f"- **{key}**: {value}")

            st.markdown("\n".join(data_summary))

        except json.JSONDecodeError as e:
            st.error(f"❌ 文件格式错误：不是有效的 JSON 文件")
            st.error(f"错误详情：{str(e)}")
        except Exception as e:
            st.error(f"❌ 导入失败：{str(e)}")
    else:
        st.info("👆 请选择要导入的 JSON 文件")

    st.markdown("---")

    st.warning("""
    ⚠️ **注意事项**：
    - 覆盖操作会丢失当前未备份的数据
    - 合并操作会保留现有数据并添加新数据
    - 建议导入前先备份当前数据
    """)

# --------------------------------------------
# 选项卡 3: 生成分享卡
# --------------------------------------------
with tab3:
    st.subheader("🔗 生成成就分享卡")

    st.markdown("""
    生成精美的成就卡片，分享给朋友或社交媒体。
    """)

    # 显示用户信息
    st.markdown("### 我的成就")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🏆 当前得分", st.session_state.user_score)

    with col2:
        st.metric("🎖️ 解锁成就", f"{len(st.session_state.achievements_unlocked)} 个")

    with col3:
        st.metric("⭐ 收藏内容", f"{len(st.session_state.bookmarked_items)} 个")

    st.markdown("---")

    # 生成分享卡片
    st.markdown("### 生成分享卡片")

    if st.button("🎨 生成成就卡片", type="primary", use_container_width=True):
        # 创建成就卡片 HTML
        achievements_html = ""
        if st.session_state.achievements_unlocked:
            for achievement in st.session_state.achievements_unlocked:
                achievements_html += f'<span style="font-size: 2rem; margin: 0.5rem;">{achievement}</span> '
        else:
            achievements_html = '<span style="color: #999;">暂无成就</span>'

        card_html = f'''
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 1rem;
            color: white;
            text-align: center;
            margin: 1rem 0;
        ">
            <h1 style="margin: 0; font-size: 2rem;">🏰 五代十国历史之旅</h1>
            <p style="margin: 1rem 0; opacity: 0.8;">学习成就卡片</p>
            <div style="
                background: rgba(255,255,255,0.2);
                padding: 1.5rem;
                border-radius: 0.5rem;
                margin: 1rem 0;
            ">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">👑</div>
                <div style="font-size: 1.5rem; margin-bottom: 1rem;">当前得分</div>
                <div style="font-size: 4rem; font-weight: bold;">{st.session_state.user_score}</div>
                <div style="margin-top: 1rem; font-size: 1.2rem;">
                    🎖️ 解锁成就：{len(st.session_state.achievements_unlocked)} 个
                </div>
                <div style="margin-top: 0.5rem; font-size: 1.2rem;">
                    ⭐ 收藏内容：{len(st.session_state.bookmarked_items)} 个
                </div>
            </div>
            <div style="margin-top: 1rem; font-size: 1.5rem;">
                {achievements_html}
            </div>
            <div style="
                margin-top: 2rem;
                padding-top: 1rem;
                border-top: 1px solid rgba(255,255,255,0.3);
                font-size: 0.9rem;
                opacity: 0.7;
            ">
                生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
            </div>
        </div>
        '''

        st.markdown(card_html, unsafe_allow_html=True)

        st.info("""
        💡 **分享提示**：
        - 使用截图工具截取上方成就卡片
        - 分享到社交媒体时带上 #五代十国历史之旅 标签
        - 邀请朋友一起来挑战历史知识
        """)

    st.markdown("---")

    # 分享成就列表
    st.markdown("### 我的成就徽章")

    if st.session_state.achievements_unlocked:
        cols = st.columns(3)
        for i, achievement in enumerate(st.session_state.achievements_unlocked):
            with cols[i % 3]:
                st.success(f"🏆 {achievement}")
    else:
        st.info("📭 还没有解锁任何成就，继续努力吧！")

# --------------------------------------------
# 选项卡 4: 数据统计
# --------------------------------------------
with tab4:
    st.subheader("📊 学习数据统计")

    st.markdown("### 总体概览")

    # 总体统计
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🏆 总得分", st.session_state.user_score)

    with col2:
        st.metric("🎖️ 成就数量", f"{len(st.session_state.achievements_unlocked)} 个")

    with col3:
        st.metric("⭐ 收藏数量", f"{len(st.session_state.bookmarked_items)} 个")

    with col4:
        st.metric("📝 测验次数", f"{len(st.session_state.quiz_history)} 次")

    st.markdown("---")

    # 详细统计
    st.markdown("### 详细统计")

    # 成就详情
    st.markdown("#### 🎖️ 成就详情")
    if st.session_state.achievements_unlocked:
        for achievement in st.session_state.achievements_unlocked:
            st.success(f"🏆 {achievement}")
    else:
        st.info("📭 暂无成就记录")

    st.markdown("---")

    # 收藏详情
    st.markdown("#### ⭐ 收藏内容")
    if st.session_state.bookmarked_items:
        for item in st.session_state.bookmarked_items:
            st.info(f"📌 {item}")
    else:
        st.info("📭 暂无收藏内容")

    st.markdown("---")

    # 故事进度
    st.markdown("#### 📖 故事进度")
    if st.session_state.story_progress:
        for story, progress in st.session_state.story_progress.items():
            st.info(f"📖 {story}: {progress}")
    else:
        st.info("📭 暂无故事进度记录")

    st.markdown("---")

    # 测验历史
    st.markdown("#### 📝 最近测验记录")
    if st.session_state.quiz_history:
        # 显示最近 5 条记录
        recent_history = st.session_state.quiz_history[-5:]
        for record in recent_history:
            st.info(f"📝 {record}")
    else:
        st.info("📭 暂无测验记录")

    st.markdown("---")

    # 导出数据统计
    st.markdown("### 导出统计")

    if st.button("📊 生成统计报告", use_container_width=True):
        report = f"""
# 五代十国历史之旅 - 学习统计报告

## 基本信息
- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 数据版本：1.0

## 学习数据
- 总得分：{st.session_state.user_score}
- 解锁成就：{len(st.session_state.achievements_unlocked)} 个
- 收藏内容：{len(st.session_state.bookmarked_items)} 个
- 测验次数：{len(st.session_state.quiz_history)} 次

## 成就列表
{chr(10).join(['- ' + a for a in st.session_state.achievements_unlocked]) if st.session_state.achievements_unlocked else '暂无成就'}

## 收藏内容
{chr(10).join(['- ' + str(i) for i in st.session_state.bookmarked_items]) if st.session_state.bookmarked_items else '暂无收藏'}
"""
        st.download_button(
            label="📥 下载统计报告",
            data=report,
            file_name=f"learning_report_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown",
            use_container_width=True
        )

# 页脚
st.markdown("---")
st.markdown("💡 **提示**：定期备份你的学习数据，避免丢失！")
