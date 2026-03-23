"""
⭐ 我的收藏
管理用户收藏的页面/人物/政权/藩镇等
"""
import streamlit as st
from src.favorite_manager import (
    render_favorites_sidebar,
    get_favorites,
    get_favorites_by_type,
    remove_favorite,
    clear_all_favorites,
    export_favorites,
    import_favorites,
    handle_navigation,
)


st.set_page_config(page_title="我的收藏", page_icon="⭐", layout="wide")


def main():
    """主函数"""
    # 处理导航
    url = handle_navigation()
    if url:
        st.switch_page(url)

    # 渲染侧边栏
    render_favorites_sidebar()

    st.title("⭐ 我的收藏")
    st.markdown("管理你收藏的页面、人物、政权、藩镇等")
    st.markdown("---")

    favorites = get_favorites()

    if not favorites:
        st.info("📭 暂无收藏项")
        st.markdown("""
        ### 如何添加收藏？
        1. 访问任意页面（如时间轴、政权地图、人物关系等）
        2. 点击页面顶部的 **☆ 收藏** 按钮
        3. 收藏项将在此页面显示

        ### 收藏功能说明
        - ⭐ **快速访问**: 在侧边栏点击收藏项可快速跳转
        - 📤 **导出/导入**: 支持收藏数据的备份和恢复
        - 🗑️ **删除**: 可删除单个收藏或清空所有
        """)
        return

    # 统计
    type_counts = {}
    for item in favorites:
        item_type = item["type"]
        type_counts[item_type] = type_counts.get(item_type, 0) + 1

    # 类型筛选器
    st.subheader("📊 收藏统计")
    cols = st.columns(len(type_counts) + 1)

    with cols[0]:
        st.metric("总收藏数", len(favorites))

    type_icons = {
        "page": "📄",
        "character": "👤",
        "regime": "🏛️",
        "fanzhen": "🏰",
        "chart": "📊",
    }

    for idx, (item_type, count) in enumerate(type_counts.items()):
        with cols[idx + 1]:
            icon = type_icons.get(item_type, "📌")
            st.metric(f"{icon} {item_type}", count)

    st.markdown("---")

    # 筛选器
    st.subheader("🔍 筛选收藏")
    filter_cols = st.columns(4)

    with filter_cols[0]:
        selected_type = st.selectbox(
            "类型",
            ["全部"] + list(type_counts.keys()),
            key="fav_type_filter"
        )

    with filter_cols[1]:
        search_text = st.text_input("搜索", placeholder="输入名称搜索...", key="fav_search")

    # 筛选逻辑
    filtered_favorites = favorites

    if selected_type != "全部":
        filtered_favorites = [f for f in filtered_favorites if f["type"] == selected_type]

    if search_text:
        filtered_favorites = [
            f for f in filtered_favorites
            if search_text.lower() in f["name"].lower()
        ]

    st.markdown(f"共 {len(filtered_favorites)} 项")
    st.markdown("---")

    # 显示收藏列表
    if filtered_favorites:
        st.subheader("📋 收藏列表")

        # 按类型分组显示
        type_groups = {}
        for item in filtered_favorites:
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
            st.markdown(f"### {icon} {item_type}")

            for item in items:
                cols = st.columns([5, 2, 1])

                with cols[0]:
                    if item.get("description"):
                        st.markdown(f"**{item['name']}**")
                        st.caption(item.get("description", "")[:100])
                    else:
                        st.markdown(f"**{item['name']}**")

                    if item.get("metadata"):
                        metadata = item["metadata"]
                        meta_text = " | ".join(f"{k}: {v}" for k, v in metadata.items())
                        st.caption(meta_text[:200])

                with cols[1]:
                    if item.get("url"):
                        if st.button(
                            "📄 查看",
                            key=f"view_{item['id']}",
                            use_container_width=True
                        ):
                            st.session_state["target_url"] = item["url"]
                            st.rerun()

                with cols[2]:
                    if st.button("🗑️", key=f"del_{item['id']}"):
                        remove_favorite(item["id"])
                        st.success(f"已删除 {item['name']}")
                        st.rerun()

                st.markdown("---")
    else:
        st.info("暂无符合条件的收藏项")


if __name__ == "__main__":
    main()
