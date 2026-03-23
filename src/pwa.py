"""
PWA 组件
为 Streamlit 应用添加 PWA 支持
"""
import streamlit as st


def register_pwa():
    """
    注册 PWA 相关的 HTML 和 JavaScript
    必须在 st.set_page_config 之后调用
    """

    # PWA 注册脚本
    pwa_script = """
    <script>
    // 注册 Service Worker
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('/static/sw.js')
                .then(function(registration) {
                    console.log('ServiceWorker registration successful:', registration.scope);
                })
                .catch(function(err) {
                    console.log('ServiceWorker registration failed: ', err);
                });
        });
    }

    // 安装提示
    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        console.log('PWA install prompt triggered');
    });

    // 监听安装状态
    window.addEventListener('appinstalled', () => {
        console.log('PWA installed successfully');
        deferredPrompt = null;
    });
    </script>
    """

    st.markdown(pwa_script, unsafe_allow_html=True)


def render_install_button():
    """
    渲染 PWA 安装按钮
    """
    install_script = """
    <script>
    function showInstallPrompt() {
        if (deferredPrompt) {
            deferredPrompt.prompt();
            deferredPrompt.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    console.log('User accepted the install prompt');
                }
                deferredPrompt = null;
            });
        } else {
            alert('应用已安装或不支持安装');
        }
    }
    </script>

    <style>
    .install-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 14px;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .install-button:hover {
        transform: scale(1.05);
    }
    </style>

    <button class="install-button" onclick="showInstallPrompt()">
        📲 安装应用
    </button>
    """

    st.markdown(install_script, unsafe_allow_html=True)


def add_pwa_meta():
    """
    添加 PWA 相关的 meta 标签
    """
    # Streamlit 的 _load_config 会处理大部分 meta，这里添加额外的
    meta_html = """
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="五代十国">
    <link rel="apple-touch-icon" href="/static/icons/icon-192x192.png">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="theme-color" content="#667eea">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    """

    st.markdown(meta_html, unsafe_allow_html=True)
