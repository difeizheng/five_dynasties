"""
用户收藏系统模块
提供收藏/取消收藏、收藏夹管理、快速访问功能
"""
import streamlit as st
import json
from typing import List, Dict, Optional
from datetime import datetime


# ============================================
# 收藏系统核心函数
# ============================================

FAVORITES_KEY = "user_favorites"


def _init_favorites():
    """初始化收藏系统"""
    if FAVORITES_KEY not in st.session_state:
        st.session_state[FAVORITES_KEY] = {
            "items": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }


def get_favorites() -> List[Dict]:
    """获取所有收藏项"""
    _init_favorites()
    return st.session_state[FAVORITES_KEY]["items"]


def add_favorite(
    item_id: str,
    item_name: str,
    item_type: str,
    item_url: str = None,
    item_description: str = None,
    item_metadata: Dict = None
) -> bool:
    """
    添加收藏项

    Args:
        item_id: 收藏项唯一标识
        item_name: 收藏项名称
        item_type: 类型 (page/character/regime/fanzhen/chart)
        item_url: 跳转链接
        item_description: 描述
        item_metadata: 额外元数据

    Returns:
        是否添加成功
    """
    _init_favorites()

    # 检查是否已存在
    for item in st.session_state[FAVORITES_KEY]["items"]:
        if item["id"] == item_id:
            return False

    new_item = {
        "id": item_id,
        "name": item_name,
        "type": item_type,
        "url": item_url,
        "description": item_description,
        "metadata": item_metadata or {},
        "created_at": datetime.now().isoformat(),
    }

    st.session_state[FAVORITES_KEY]["items"].append(new_item)
    st.session_state[FAVORITES_KEY]["updated_at"] = datetime.now().isoformat()

    return True


def remove_favorite(item_id: str) -> bool:
    """
    移除收藏项

    Args:
        item_id: 收藏项 ID

    Returns:
        是否移除成功
    """
    _init_favorites()

    items = st.session_state[FAVORITES_KEY]["items"]
    for i, item in enumerate(items):
        if item["id"] == item_id:
            items.pop(i)
            st.session_state[FAVORITES_KEY]["updated_at"] = datetime.now().isoformat()
            return True

    return False


def is_favorited(item_id: str) -> bool:
    """检查某项是否已收藏"""
    _init_favorites()
    return any(item["id"] == item_id for item in st.session_state[FAVORITES_KEY]["items"])


def toggle_favorite(
    item_id: str,
    item_name: str,
    item_type: str,
    item_url: str = None,
    item_description: str = None,
) -> bool:
    """
    切换收藏状态

    Returns:
        True 表示已收藏，False 表示已取消
    """
    if is_favorited(item_id):
        remove_favorite(item_id)
        return False
    else:
        add_favorite(item_id, item_name, item_type, item_url, item_description)
        return True


def get_favorites_by_type(item_type: str) -> List[Dict]:
    """按类型筛选收藏"""
    _init_favorites()
    return [
        item for item in st.session_state[FAVORITES_KEY]["items"]
        if item["type"] == item_type
    ]


def clear_all_favorites() -> int:
    """
    清空所有收藏

    Returns:
        被清除的收藏数量
    """
    _init_favorites()
    count = len(st.session_state[FAVORITES_KEY]["items"])
    st.session_state[FAVORITES_KEY]["items"] = []
    st.session_state[FAVORITES_KEY]["updated_at"] = datetime.now().isoformat()
    return count


def export_favorites() -> str:
    """导出收藏为 JSON 字符串"""
    _init_favorites()
    return json.dumps(st.session_state[FAVORITES_KEY], indent=2, ensure_ascii=False)


def import_favorites(json_str: str) -> tuple[int, int]:
    """
    从 JSON 导入收藏

    Args:
        json_str: JSON 字符串

    Returns:
        (导入数量，跳过数量)
    """
    _init_favorites()

    try:
        data = json.loads(json_str)
        imported_items = data.get("items", [])

        imported_count = 0
        skipped_count = 0
        existing_ids = {item["id"] for item in st.session_state[FAVORITES_KEY]["items"]}

        for item in imported_items:
            if item.get("id") not in existing_ids:
                st.session_state[FAVORITES_KEY]["items"].append(item)
                imported_count += 1
            else:
                skipped_count += 1

        st.session_state[FAVORITES_KEY]["updated_at"] = datetime.now().isoformat()
        return imported_count, skipped_count

    except json.JSONDecodeError:
        return 0, 0


# ============================================
# UI 组件
# ============================================

def render_favorite_button(
    item_id: str,
    item_name: str,
    item_type: str,
    item_url: str = None,
    item_description: str = None,
    button_key: str = None,
) -> bool:
    """
    渲染收藏按钮

    Args:
        item_id: 收藏项 ID
        item_name: 收藏项名称
        item_type: 类型
        item_url: 跳转链接
        item_description: 描述
        button_key: 按钮唯一标识

    Returns:
        当前收藏状态 (True=已收藏)
    """
    _init_favorites()
    is_favorited_flag = is_favorited(item_id)

    key = button_key or f"fav_btn_{item_id}"

    # 根据收藏状态显示不同图标
    if is_favorited_flag:
        button_label = "⭐ 已收藏"
        button_type = "primary"
    else:
        button_label = "☆ 收藏"
        button_type = "secondary"

    if st.button(button_label, key=key, type=button_type):
        toggle_favorite(item_id, item_name, item_type, item_url, item_description)
        st.rerun()

    return is_favorited_flag


def render_favorites_sidebar():
    """
    在侧边栏渲染收藏夹
    """
    _init_favorites()
    favorites = get_favorites()

    with st.sidebar:
        st.markdown("### ⭐ 我的收藏")

        if not favorites:
            st.info("暂无收藏项\n\n在页面中点击收藏按钮添加")
        else:
            # 按类型分组显示
            type_groups = {}
            for item in favorites:
                item_type = item["type"]
                if item_type not in type_groups:
                    type_groups[item_type] = []
                type_groups[item_type].append(item)

            type_icons = {
                "page": "📄",
                "character": "👤",
                "regime": "🏛️",
                "fanzhen": "🏰",
                "chart": "📊",
            }

            for item_type, items in type_groups.items():
                icon = type_icons.get(item_type, "📌")
                with st.expander(f"{icon} {item_type} ({len(items)})"):
                    for item in items:
                        if item.get("url"):
                            if st.button(item["name"], key=f"fav_link_{item['id']}", use_container_width=True):
                                st.session_state["target_url"] = item["url"]
                                st.rerun()
                        else:
                            st.markdown(f"- {item['name']}")

                        if st.button("🗑️", key=f"fav_del_{item['id']}"):
                            remove_favorite(item["id"])
                            st.rerun()

        st.markdown("---")

        # 导出/导入功能
        with st.expander("📤 导出/导入"):
            if st.button("导出收藏"):
                favorites_json = export_favorites()
                st.download_button(
                    label="下载 JSON",
                    data=favorites_json,
                    file_name=f"favorites_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )

            uploaded_file = st.file_uploader("导入收藏", type=["json"])
            if uploaded_file:
                json_str = uploaded_file.read().decode("utf-8")
                imported, skipped = import_favorites(json_str)
                st.success(f"导入 {imported} 项，跳过 {skipped} 项")
                st.rerun()

        # 清空功能
        if favorites and st.button("🗑️ 清空所有收藏", type="secondary"):
            count = clear_all_favorites()
            st.success(f"已清空 {count} 项收藏")
            st.rerun()


def render_favorite_indicator(item_id: str, item_name: str, item_type: str):
    """
    渲染收藏状态指示器

    Args:
        item_id: 收藏项 ID
        item_name: 收藏项名称
        item_type: 类型
    """
    _init_favorites()
    is_favorited_flag = is_favorited(item_id)

    if is_favorited_flag:
        st.markdown(
            f'<span style="color: gold; font-size: 1.2rem;">⭐ {item_name}</span>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<span style="color: gray; font-size: 1.2rem;">☆ {item_name}</span>',
            unsafe_allow_html=True
        )


# ============================================
# 页面导航辅助
# ============================================

def handle_navigation():
    """处理页面导航"""
    if "target_url" in st.session_state:
        url = st.session_state["target_url"]
        del st.session_state["target_url"]
        return url
    return None
