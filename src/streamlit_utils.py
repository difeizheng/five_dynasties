"""
Streamlit 工具函数
"""

import streamlit as st
from streamlit.components.v1 import html
from pyecharts.charts import BaseChart


def render_echarts(chart: BaseChart, height: int = 600):
    """
    渲染 pyecharts 图表到 Streamlit

    Args:
        chart: pyecharts 图表对象
        height: 图表高度（像素）
    """
    # 生成 HTML
    html_content = chart.render_embed()

    # 使用 components.v1.html 渲染
    html(html_content, height=height, scrolling=False)
