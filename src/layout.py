"""
全局布局优化组件
提供统一的页面布局、导航和样式
"""
import streamlit as st


def setup_mobile_layout():
    """
    设置移动端优化的布局样式
    """
    st.markdown("""
    <style>
    /* 主容器优化 */
    .main > div {
        padding: 1rem;
    }

    /* 响应式列布局 */
    @media (max-width: 768px) {
        .stColumns > div {
            flex: 1 1 100% !important;
        }
    }

    /* 卡片样式优化 */
    .stat-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 1rem;
        padding: 1.5rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .stat-card:hover {
        transform: translateY(-5px);
    }

    /* 导航栏优化 */
    .stSidebar {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }

    /* 按钮优化 - 移动端更易点击 */
    .stButton > button {
        min-height: 44px;
        min-width: 44px;
        border-radius: 8px;
    }

    /* 隐藏 Streamlit 默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 标题优化 */
    h1, h2, h3 {
        font-weight: 600;
    }

    /* 图表容器 */
    .chart-container {
        background: white;
        border-radius: 1rem;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: 1rem 0;
    }

    /* 移动端表格优化 */
    @media (max-width: 768px) {
        .stDataFrame {
            font-size: 12px;
        }
    }

    /* 加载动画优化 */
    .stSpinner {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)


def render_navigation():
    """
    渲染侧边栏导航
    """
    with st.sidebar:
        st.markdown("""
        ### 🏯 五代十国
        <style>
        .nav-section {
            margin: 1rem 0;
            padding: 0.5rem;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown("**📊 核心功能**")

        if st.button("📅 时间轴", use_container_width=True, key="nav_timeline"):
            st.switch_page("pages/1_📅_时间轴.py")
        if st.button("🗺️ 政权地图", use_container_width=True, key="nav_map"):
            st.switch_page("pages/2_🗺️_政权地图.py")
        if st.button("👥 人物关系", use_container_width=True, key="nav_characters"):
            st.switch_page("pages/3_👥_人物关系.py")
        if st.button("🏰 藩镇分析", use_container_width=True, key="nav_fanzhen"):
            st.switch_page("pages/4_🏰_藩镇分析.py")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown("**📖 高级功能**")

        if st.button("📊 数据统计", use_container_width=True, key="nav_stats"):
            st.switch_page("pages/5_📊_数据统计.py")
        if st.button("📖 文献检索", use_container_width=True, key="nav_search"):
            st.switch_page("pages/6_📖_文献检索.py")
        if st.button("🔍 对比分析", use_container_width=True, key="nav_compare"):
            st.switch_page("pages/7_🔍_对比分析.py")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown("**🎮 P3 功能**")

        if st.button("📺 数据大屏", use_container_width=True, key="nav_dashboard"):
            st.switch_page("pages/8_📺_数据大屏.py")
        if st.button("⭐ 我的收藏", use_container_width=True, key="nav_favorites"):
            st.switch_page("pages/9_⭐_我的收藏.py")
        if st.button("🔌 API 接口", use_container_width=True, key="nav_api"):
            st.switch_page("pages/10_🔌_API 接口.py")
        if st.button("🎮 历史模拟器", use_container_width=True, key="nav_simulator"):
            st.switch_page("pages/11_🎮_历史模拟器.py")

        st.markdown('</div>', unsafe_allow_html=True)


def render_header(title: str, subtitle: str = None, icon: str = ""):
    """
    渲染统一的页面头部

    Args:
        title: 页面标题
        subtitle: 副标题（可选）
        icon: 图标 emoji
    """
    header_html = f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    ">
        <h1 style="margin: 0; font-size: 2rem;">{icon} {title}</h1>
        {f'<p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">{subtitle}</p>' if subtitle else ''}
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_footer():
    """
    渲染页面底部
    """
    st.markdown("---")
    st.markdown("""
    <div style="
        text-align: center;
        padding: 1rem;
        color: #666;
        font-size: 0.9rem;
    ">
        <p>🏯 五代十国历史信息可视化系统 |
           <a href="https://github.com/difeizheng/five_dynasties" style="color: #667eea; text-decoration: none;">GitHub</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
