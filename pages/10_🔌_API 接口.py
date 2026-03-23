"""
🔌 API 接口文档
查看和测试五代十国数据 API
"""
import streamlit as st
import requests
import json


st.set_page_config(page_title="API 接口", page_icon="🔌", layout="wide")


# API 基础 URL
API_BASE_URL = "http://localhost:8000"


def make_request(endpoint: str) -> dict:
    """发送 API 请求"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        response = requests.get(url, timeout=10)
        return {
            "success": True,
            "status_code": response.status_code,
            "data": response.json(),
            "url": url
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "无法连接到 API 服务器",
            "message": "请确保 API 服务正在运行：python api.py"
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "请求超时",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def render_api_card(endpoint: str, method: str, description: str):
    """渲染 API 卡片"""
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(f"`{method}` `{endpoint}`")
        st.caption(description)

    with col2:
        if st.button("🧪 测试", key=f"test_{endpoint}"):
            st.session_state[f"test_{endpoint}"] = True


def main():
    """主函数"""
    st.title("🔌 API 接口文档")
    st.markdown("五代十国数据 API 提供 RESTful 接口，支持获取政权、人物、藩镇、事件等数据")

    st.markdown("---")

    # API 状态检查
    st.subheader("📡 API 状态")

    status = make_request("/")

    if status["success"] and "data" in status:
        st.success("✅ API 服务运行中")
        st.info(f"服务地址：`{status['url']}`")
    else:
        st.error("❌ API 服务未运行")
        st.markdown("""
        **启动 API 服务：**
        ```bash
        pip install fastapi uvicorn pydantic
        python api.py
        ```
        """)

    st.markdown("---")

    # API 文档
    st.subheader("📚 接口列表")

    # 基础信息
    st.markdown("### 基础接口")
    render_api_card("/", "GET", "API 根路径，返回 API 信息")

    st.markdown("### 政权数据")
    render_api_card("/api/regimes", "GET", "获取所有政权列表")
    render_api_card("/api/regimes?type=五代", "GET", "获取五代政权")
    render_api_card("/api/regimes?type=十国", "GET", "获取十国政权")
    render_api_card("/api/regimes/{name}", "GET", "获取特定政权详情")
    render_api_card("/api/colors", "GET", "获取政权颜色映射")

    st.markdown("### 人物数据")
    render_api_card("/api/characters", "GET", "获取人物列表")
    render_api_card("/api/characters?regime=后唐", "GET", "按政权筛选人物")
    render_api_card("/api/characters/{name}", "GET", "获取特定人物详情")

    st.markdown("### 藩镇数据")
    render_api_card("/api/fanzhen", "GET", "获取藩镇列表")
    render_api_card("/api/fanzhen/{name}", "GET", "获取特定藩镇详情（含编年史）")

    st.markdown("### 地理数据")
    render_api_card("/api/provinces", "GET", "获取省份 - 政权映射")
    render_api_card("/api/province_mapping", "GET", "获取古今省份名称映射")

    st.markdown("### 事件数据")
    render_api_card("/api/events", "GET", "获取事件列表")
    render_api_card("/api/events?year=907", "GET", "按年份筛选事件")
    render_api_card("/api/events?regime=后梁", "GET", "按政权筛选事件")
    render_api_card("/api/yearly_events", "GET", "获取年度事件统计")

    st.markdown("### 世系数据")
    render_api_card("/api/succession", "GET", "获取所有帝王世系")
    render_api_card("/api/succession?regime=后唐", "GET", "获取特定政权世系")

    st.markdown("### 统计数据")
    render_api_card("/api/timeline", "GET", "获取时间线数据")
    render_api_card("/api/stats", "GET", "获取统计数据")

    st.markdown("---")

    # API 测试器
    st.subheader("🧪 API 测试器")

    endpoint = st.text_input(
        "输入 API 端点",
        placeholder="/api/regimes",
        help="例如：/api/regimes, /api/characters, /api/fanzhen"
    )

    if st.button("发送请求"):
        if endpoint:
            result = make_request(endpoint)

            if result["success"]:
                st.success(f"请求成功 (状态码：{result.get('status_code', 'N/A')})")
                st.json(result.get("data", {}))
            else:
                st.error(f"请求失败：{result.get('error', '未知错误')}")
                if "message" in result:
                    st.warning(result["message"])
        else:
            st.warning("请输入 API 端点")

    st.markdown("---")

    # 使用示例
    st.subheader("💡 使用示例")

    st.markdown("""
    ### Python 请求示例

    ```python
    import requests

    # 获取所有政权
    response = requests.get("http://localhost:8000/api/regimes")
    data = response.json()
    print(data["data"])

    # 获取特定人物
    response = requests.get("http://localhost:8000/api/characters/李存勖")
    character = response.json()["data"]
    print(character)

    # 获取藩镇列表
    response = requests.get("http://localhost:8000/api/fanzhen")
    fanzhen_list = response.json()["data"]
    ```

    ### JavaScript 请求示例

    ```javascript
    // 获取所有政权
    fetch("http://localhost:8000/api/regimes")
      .then(response => response.json())
      .then(data => console.log(data.data));

    // 获取特定藩镇详情
    fetch("http://localhost:8000/api/fanzhen/宣武")
      .then(response => response.json())
      .then(data => console.log(data.data));
    ```

    ### cURL 示例

    ```bash
    # 获取政权列表
    curl http://localhost:8000/api/regimes

    # 获取人物数据
    curl "http://localhost:8000/api/characters?regime=后唐"

    # 获取统计数据
    curl http://localhost:8000/api/stats
    ```
    """)

    st.markdown("---")

    # 响应格式说明
    st.subheader("📋 响应格式")

    st.json({
        "success": True,
        "data": {...},
        "message": "可选的消息",
        "count": "可选的数据条数"
    })

    st.markdown("""
    **字段说明：**
    - `success`: 请求是否成功
    - `data`: 返回的数据
    - `message`: 可选的消息（错误时包含错误信息）
    - `count`: 可选的数据条数
    """)


if __name__ == "__main__":
    main()
