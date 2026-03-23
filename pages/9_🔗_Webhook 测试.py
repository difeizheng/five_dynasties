"""
🔗 Webhook 测试工具
测试 webhook URL 的可用性和响应
"""
import streamlit as st
import requests
import time
from datetime import datetime


st.set_page_config(
    page_title="Webhook 测试",
    page_icon="🔗",
    layout="wide"
)


def test_webhook(url: str, method: str = "POST", timeout: int = 10) -> dict:
    """
    测试 webhook URL 的可用性

    Args:
        url: webhook URL
        method: HTTP 方法 (GET/POST)
        timeout: 超时时间（秒）

    Returns:
        测试结果字典
    """
    result = {
        "success": False,
        "status_code": None,
        "response_time": None,
        "error": None,
        "response_headers": {},
        "response_body": None,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        start_time = time.time()

        if method == "GET":
            response = requests.get(url, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, timeout=timeout, json={
                "test": True,
                "timestamp": result["timestamp"],
                "message": "Webhook 测试消息"
            })
        elif method == "PUT":
            response = requests.put(url, timeout=timeout, json={
                "test": True,
                "timestamp": result["timestamp"]
            })
        elif method == "DELETE":
            response = requests.delete(url, timeout=timeout)
        else:
            result["error"] = f"不支持的 HTTP 方法：{method}"
            return result

        end_time = time.time()

        result["success"] = 200 <= response.status_code < 300
        result["status_code"] = response.status_code
        result["response_time"] = round((end_time - start_time) * 1000, 2)  # 毫秒
        result["response_headers"] = dict(response.headers)

        # 尝试解析响应体
        try:
            result["response_body"] = response.json()
        except:
            result["response_body"] = response.text[:1000]  # 限制长度

    except requests.exceptions.Timeout:
        result["error"] = f"请求超时（>{timeout}秒）"
    except requests.exceptions.ConnectionError as e:
        result["error"] = f"连接失败：{str(e)}"
    except requests.exceptions.RequestException as e:
        result["error"] = f"请求错误：{str(e)}"
    except Exception as e:
        result["error"] = f"未知错误：{str(e)}"

    return result


def render_header():
    """渲染页面标题"""
    st.title("🔗 Webhook 测试工具")
    st.markdown("""
    测试 webhook URL 的可用性和响应性能

    **功能说明**：
    - 🧪 发送 HTTP 请求测试 webhook 连通性
    - ⏱️ 测量响应时间（毫秒）
    - 📋 查看响应状态码、headers 和 body
    - 🔒 支持多种 HTTP 方法（GET/POST/PUT/DELETE）
    """)
    st.markdown("---")


def render_test_form():
    """渲染测试表单"""
    st.subheader("🧪 Webhook 测试")

    col1, col2 = st.columns([3, 1])

    with col1:
        webhook_url = st.text_input(
            "Webhook URL",
            placeholder="https://example.com/webhook",
            help="输入要测试的 webhook 完整 URL"
        )

    with col2:
        http_method = st.selectbox(
            "HTTP 方法",
            ["POST", "GET", "PUT", "DELETE"],
            index=0
        )

    timeout = st.slider(
        "超时时间（秒）",
        min_value=1,
        max_value=60,
        value=10,
        step=1
    )

    # 测试按钮
    if st.button("🚀 开始测试", type="primary", use_container_width=True):
        if not webhook_url:
            st.error("请输入 Webhook URL")
            return None

        # 验证 URL 格式
        if not webhook_url.startswith(("http://", "https://")):
            st.error("URL 必须以 http:// 或 https:// 开头")
            return None

        # 执行测试
        with st.spinner("正在测试 webhook..."):
            result = test_webhook(webhook_url, http_method, timeout)

        return result

    return None


def render_result(result: dict):
    """渲染测试结果"""
    if result is None:
        return

    st.markdown("---")
    st.subheader("📊 测试结果")

    # 结果摘要
    if result["success"]:
        st.success(f"✅ Webhook 可用！状态码：{result['status_code']}")
    else:
        if result["error"]:
            st.error(f"❌ 测试失败：{result['error']}")
        else:
            st.warning(f"⚠️ 响应状态码：{result['status_code']}")

    # 关键指标
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "状态码",
            result["status_code"] or "N/A",
            delta="成功" if result["success"] else "失败" if result["error"] else None
        )

    with col2:
        if result["response_time"]:
            st.metric("响应时间", f"{result['response_time']}ms")
        else:
            st.metric("响应时间", "N/A")

    with col3:
        st.metric("测试时间", result["timestamp"].split(" ")[1] if result["timestamp"] else "N/A")

    with col4:
        st.metric("成功率", "100%" if result["success"] else "0%")

    # 详细结果
    with st.expander("📋 查看详细响应", expanded=False):
        # 响应头
        if result["response_headers"]:
            st.markdown("**响应头：**")
            for key, value in result["response_headers"].items():
                st.text(f"{key}: {value}")

        st.markdown("---")

        # 响应体
        if result["response_body"]:
            st.markdown("**响应体：**")
            if isinstance(result["response_body"], dict):
                st.json(result["response_body"])
            else:
                st.code(result["response_body"], language="text")
        elif result["error"]:
            st.markdown("**错误信息：**")
            st.code(result["error"], language="text")


def render_quick_test_presets():
    """渲染预设测试"""
    st.subheader("⚡ 快速测试预设")

    presets = {
        "本地 API (8000)": "http://localhost:8000/",
        "本地 API (8501)": "http://localhost:8501/",
        "Httpbin POST": "https://httpbin.org/post",
        "Httpbin GET": "https://httpbin.org/get",
        "Httpbin Status 200": "https://httpbin.org/status/200",
        "Httpbin Status 404": "https://httpbin.org/status/404",
        "Httpbin Delay": "https://httpbin.org/delay/5",
    }

    cols = st.columns(4)

    for idx, (name, url) in enumerate(presets.items()):
        with cols[idx % 4]:
            if st.button(name, key=f"preset_{name}", use_container_width=True):
                st.session_state["preset_url"] = url
                st.session_state["preset_method"] = "GET" if "GET" in name else "POST"
                st.rerun()


def main():
    """主函数"""
    render_header()

    # 检查预设
    preset_url = st.session_state.get("preset_url")
    preset_method = st.session_state.get("preset_method")

    if preset_url:
        st.info(f"已选择预设：{preset_url}")

    # 测试表单
    result = render_test_form()

    # 显示结果
    if result:
        render_result(result)

    st.markdown("---")

    # 快速测试
    render_quick_test_presets()

    # 说明
    with st.expander("ℹ️ 使用说明"):
        st.markdown("""
        ### Webhook 测试工具说明

        **支持的功能**：
        1. 测试任意 HTTP/HTTPS URL 的连通性
        2. 支持 GET、POST、PUT、DELETE 四种 HTTP 方法
        3. 测量响应时间（毫秒级别）
        4. 显示完整的响应头和响应体
        5. 内置 httpbin 测试服务预设

        **POST 请求默认 payload**：
        ```json
        {
            "test": true,
            "timestamp": "2024-01-01 12:00:00",
            "message": "Webhook 测试消息"
        }
        ```

        **响应状态码说明**：
        - 2xx: 成功
        - 3xx: 重定向
        - 4xx: 客户端错误
        - 5xx: 服务器错误

        **注意事项**：
        - 超时时间默认为 10 秒，可根据需要调整
        - 响应体超过 1000 字符会被截断
        - 请确保测试的 URL 是合法且有权访问的
        """)


if __name__ == "__main__":
    main()
