"""
Streamlit 工具函数
包含错误处理、数据加载装饰器、UI 组件等
"""

import streamlit as st
from streamlit.components.v1 import html
from typing import Optional, Callable, Any, Dict, List
from functools import wraps
import traceback
import json


# ============================================
# 错误处理组件
# ============================================

def render_error_message(message: str, details: str = None, show_retry: bool = True):
    """
    渲染错误信息

    Args:
        message: 错误消息
        details: 详细错误信息（可选）
        show_retry: 是否显示重试按钮
    """
    st.error(f"❌ {message}")

    if details:
        with st.expander("查看详情"):
            st.code(details, language="text")

    if show_retry:
        if st.button("🔄 重试", key=f"retry_{id(message)}"):
            st.rerun()


def render_warning_message(message: str, details: str = None):
    """
    渲染警告信息

    Args:
        message: 警告消息
        details: 详细错误信息（可选）
    """
    st.warning(f"⚠️ {message}")

    if details:
        with st.expander("查看详情"):
            st.code(details, language="text")


def render_success_message(message: str, details: str = None):
    """
    渲染成功信息

    Args:
        message: 成功消息
        details: 详细信息（可选）
    """
    st.success(f"✅ {message}")

    if details:
        with st.expander("查看详情"):
            st.write(details)


def render_info_message(message: str, details: str = None):
    """
    渲染提示信息

    Args:
        message: 提示消息
        details: 详细信息（可选）
    """
    st.info(f"ℹ️ {message}")

    if details:
        with st.expander("查看详情"):
            st.write(details)


# ============================================
# 数据加载装饰器
# ============================================

def with_loading(func: Callable, loading_message: str = "正在加载数据..."):
    """
    为函数添加加载动画

    Args:
        func: 被装饰的函数
        loading_message: 加载时的提示消息
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        with st.spinner(loading_message):
            return func(*args, **kwargs)
    return wrapper


def with_error_handling(func: Callable, fallback_value: Any = None):
    """
    为函数添加错误处理

    Args:
        func: 被装饰的函数
        fallback_value: 错误时的返回值
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"❌ {func.__name__} 执行失败：{str(e)}")
            with st.expander("查看堆栈跟踪"):
                st.code(traceback.format_exc(), language="text")
            return fallback_value
    return wrapper


# ============================================
# 数据加载组件
# ============================================

@st.cache_data
def safe_load_data(load_func: Callable, data_name: str = "数据") -> Optional[Any]:
    """
    安全加载数据

    Args:
        load_func: 数据加载函数
        data_name: 数据名称

    Returns:
        加载的数据或 None
    """
    try:
        result = load_func()
        if result is None or (hasattr(result, '__len__') and len(result) == 0):
            st.warning(f"⚠️ {data_name} 为空")
            return None
        return result
    except FileNotFoundError as e:
        st.error(f"❌ 文件未找到：{str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ {data_name} 加载失败：{str(e)}")
        return None


def render_empty_state(message: str, icon: str = "📭", suggestions: List[str] = None):
    """
    渲染空状态

    Args:
        message: 空状态消息
        icon: 图标
        suggestions: 建议操作列表
    """
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem; color: #666;">
        <div style="font-size: 3rem;">{icon}</div>
        <div style="font-size: 1.2rem; margin-top: 1rem;">{message}</div>
    </div>
    """, unsafe_allow_html=True)

    if suggestions:
        st.markdown("**建议操作：**")
        for suggestion in suggestions:
            st.markdown(f"- {suggestion}")


# ============================================
# ECharts 渲染组件
# ============================================

def render_echarts(chart, height: int = 600, width: str = "100%"):
    """
    渲染 pyecharts 图表到 Streamlit

    Args:
        chart: pyecharts 图表对象
        height: 图表高度（像素）
        width: 图表宽度
    """
    # 生成 HTML
    html_content = chart.render_embed()

    # 使用 components.v1.html 渲染
    html(html_content, height=height, scrolling=False)


def render_custom_html(html_content: str, height: int = 600):
    """
    渲染自定义 HTML 内容

    Args:
        html_content: HTML 内容
        height: 高度（像素）
    """
    html(html_content, height=height, scrolling=False)


# ============================================
# 布局组件
# ============================================

def render_section_header(title: str, subtitle: str = None, icon: str = "📌"):
    """
    渲染章节标题

    Args:
        title: 标题
        subtitle: 副标题（可选）
        icon: 图标
    """
    st.markdown(f"## {icon} {title}")
    if subtitle:
        st.markdown(subtitle)
    st.markdown("---")


def render_card(content: str, title: str = None, color: str = "#f0f2f6"):
    """
    渲染卡片组件

    Args:
        content: 卡片内容
        title: 卡片标题（可选）
        color: 背景颜色
    """
    card_html = f"""
    <div style="background: {color}; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0;">
        {f'<h3 style="margin-top: 0;">{title}</h3>' if title else ''}
        <div>{content}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


# ============================================
# 调试工具
# ============================================

def debug_show_data(data: Any, name: str = "数据"):
    """
    调试：显示数据结构

    Args:
        data: 要显示的数据
        name: 数据名称
    """
    with st.expander(f"🔍 调试：{name}"):
        st.write(f"**类型：** {type(data)}")
        if hasattr(data, '__len__'):
            st.write(f"**长度：** {len(data)}")
        if hasattr(data, 'columns'):
            st.write(f"**列名：** {list(data.columns)}")
        if hasattr(data, 'head'):
            st.write("**前 5 行：**")
            st.dataframe(data.head())
        elif isinstance(data, dict):
            st.write("**键名：**")
            st.json(list(data.keys()))
        else:
            st.write("**内容：**")
            st.write(data)


# ============================================
# 导出功能组件
# ============================================

def export_dataframe_to_csv(df, filename: str = "data.csv"):
    """
    导出 DataFrame 为 CSV 文件

    Args:
        df: pandas DataFrame
        filename: 文件名
    """
    import base64

    csv = df.to_csv(index=False, encoding='utf-8-sig')
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:text/csv;base64,{b64}" download="{filename}" style="display: inline-block; padding: 0.5rem 1rem; background: #28a745; color: white; text-decoration: none; border-radius: 0.25rem;">📥 下载 CSV 文件</a>'
    st.markdown(href, unsafe_allow_html=True)


def export_to_excel(df, filename: str = "data.xlsx"):
    """
    导出 DataFrame 为 Excel 文件

    Args:
        df: pandas DataFrame
        filename: 文件名
    """
    import io
    import base64

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)

    b64 = base64.b64encode(output.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}" style="display: inline-block; padding: 0.5rem 1rem; background: #28a745; color: white; text-decoration: none; border-radius: 0.25rem;">📥 下载 Excel 文件</a>'
    st.markdown(href, unsafe_allow_html=True)


def export_chart_as_html(chart, filename: str = "chart.html"):
    """
    导出 pyecharts 图表为 HTML 文件

    Args:
        chart: pyecharts 图表对象
        filename: 文件名
    """
    import base64

    html_content = chart.render_embed()
    b64 = base64.b64encode(html_content.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="{filename}" style="display: inline-block; padding: 0.5rem 1rem; background: #28a745; color: white; text-decoration: none; border-radius: 0.25rem;">📥 下载 HTML 图表</a>'
    st.markdown(href, unsafe_allow_html=True)


def render_export_buttons(df=None, chart=None, csv_name: str = "data.csv", excel_name: str = "data.xlsx", html_name: str = "chart.html"):
    """
    渲染导出按钮组

    Args:
        df: 要导出的 DataFrame（可选）
        chart: 要导出的图表（可选）
        csv_name: CSV 文件名
        excel_name: Excel 文件名
        html_name: HTML 文件名
    """
    cols = st.columns(3)

    with cols[0]:
        if df is not None:
            export_dataframe_to_csv(df, csv_name)

    with cols[1]:
        if df is not None:
            try:
                export_to_excel(df, excel_name)
            except ImportError:
                st.warning("需要安装 openpyxl：`pip install openpyxl`")

    with cols[2]:
        if chart is not None:
            export_chart_as_html(chart, html_name)


def export_text_as_file(text: str, filename: str = "export.txt", mime_type: str = "text/plain"):
    """
    导出文本为文件

    Args:
        text: 文本内容
        filename: 文件名
        mime_type: MIME 类型
    """
    import base64

    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:{mime_type};base64,{b64}" download="{filename}" style="display: inline-block; padding: 0.5rem 1rem; background: #28a745; color: white; text-decoration: none; border-radius: 0.25rem;">📥 下载 {filename}</a>'
    st.markdown(href, unsafe_allow_html=True)


def export_comparison_report(regime1: str, regime2: str, report_data: Dict, filename: str = "comparison_report.txt"):
    """
    导出对比报告

    Args:
        regime1: 政权 1 名称
        regime2: 政权 2 名称
        report_data: 报告数据字典
        filename: 文件名
    """
    report_lines = [
        f"五代十国政权对比报告",
        f"===================",
        f"",
        f"对比对象：{regime1} vs {regime2}",
        f"生成时间：{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"",
        f"对比结果:",
        f"-----------",
    ]

    for key, value in report_data.items():
        report_lines.append(f"{key}: {value}")

    report_text = "\n".join(report_lines)
    export_text_as_file(report_text, filename)


# ============================================
# 地图渲染组件
# ============================================

def build_choropleth_map_html(
    geojson_content: str,
    map_data: List[Dict],
    value_mapping: Dict[str, Any],
    color_mapping: Dict[str, str],
    title: str,
    tooltip_formatter: str = None,
    province_regime_map: Dict[str, str] = None,
    legend_title: str = None,
    height: int = 600,
) -> str:
    """
    构建 choropleth 地图 HTML（使用 visualMap 方案）

    Args:
        geojson_content: GeoJSON 内容
        map_data: 地图数据列表，每项包含 name 和 value
        value_mapping: 值到标签的映射 {value: label}
        color_mapping: 值到颜色的映射 {value: color}
        title: 地图标题
        tooltip_formatter: tooltip 格式化模板，支持{name}, {value}, {label}占位符
        province_regime_map: 省份到政权的映射 {province: regime}，用于 tooltip
        legend_title: 图例标题
        height: 地图高度

    Returns:
        完整的 HTML 字符串
    """
    # 构建 pieces 配置
    pieces_config = [
        {"value": value, "label": label, "color": color_mapping.get(value, "#999999")}
        for value, label in value_mapping.items()
    ]
    colors_list = [color_mapping.get(value, "#999999") for value in value_mapping.keys()]
    legend_data = list(value_mapping.values())

    # 构建 tooltip 格式化函数
    if tooltip_formatter:
        tooltip_js = tooltip_formatter
    else:
        tooltip_js = """function(params) {
            return '<b>' + params.name + '</b>';
        }"""

    # 构建省份 - 政权映射用于 tooltip
    province_regime_json = json.dumps(province_regime_map or {}, ensure_ascii=False)

    html_template = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        body {{ margin: 0; padding: 0; background: #fff; }}
        #map {{ width: 100%; height: {height}px; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var chinaGeojson = {geojson_content};
        var provinceDataMap = {json.dumps({k: v for k, v in value_mapping.items()})};
        var provinceRegimeMap = {province_regime_json};
        var mapData = {json.dumps(map_data, ensure_ascii=False)};

        echarts.registerMap('china', chinaGeojson);

        var chart = echarts.init(document.getElementById('map'), 'white');

        var option = {{
            title: {{
                text: "{title}",
                left: 'center',
                top: 10
            }},
            tooltip: {{
                trigger: 'item',
                formatter: {tooltip_js}
            }},
            series: [{{
                type: 'map',
                map: 'china',
                data: mapData,
                label: {{
                    show: true,
                    fontSize: 9,
                    color: '#333',
                    formatter: '{{b}}'
                }},
                emphasis: {{
                    itemStyle: {{
                        areaColor: '#ffd700',
                        borderColor: '#fff',
                        borderWidth: 2
                    }},
                    label: {{
                        color: '#fff',
                        fontWeight: 'bold'
                    }}
                }}
            }}],
            visualMap: {{
                type: 'piecewise',
                show: true,
                right: '10',
                top: '50',
                pieces: {json.dumps(pieces_config, ensure_ascii=False)},
                textStyle: {{
                    color: '#333'
                }},
                inRange: {{
                    color: {json.dumps(colors_list)}
                }}
            }},
            legend: {{
                data: {json.dumps(legend_data, ensure_ascii=False)},
                top: 50,
                selectedMode: true,
                type: 'scroll',
                orient: 'horizontal'
            }}
        }};

        chart.setOption(option);

        window.addEventListener('resize', function() {{
            var chart = echarts.getInstanceByDom(document.getElementById('map'));
            if (chart) chart.resize();
        }});
    </script>
</body>
</html>'''

    return html_template


def build_simple_highlight_map_html(
    geojson_content: str,
    highlight_regions: List[str],
    highlight_color: str = "#e74c3c",
    highlight_label: str = "高亮区域",
    title: str = "地图",
    height: int = 500,
) -> str:
    """
    构建简单的高亮地图 HTML（二分颜色方案）

    Args:
        geojson_content: GeoJSON 内容
        highlight_regions: 需要高亮的区域列表
        highlight_color: 高亮颜色
        highlight_label: 高亮区域标签
        title: 地图标题
        height: 地图高度

    Returns:
        完整的 HTML 字符串
    """
    html_template = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        body {{ margin: 0; padding: 0; background: #fff; }}
        #map {{ width: 100%; height: {height}px; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var chinaGeojson = {geojson_content};
        var highlightRegions = {json.dumps(highlight_regions)};

        echarts.registerMap('china', chinaGeojson);

        var mapData = highlightRegions.map(function(name) {{
            return {{ name: name, value: 1 }};
        }});

        var chart = echarts.init(document.getElementById('map'), 'white');

        var option = {{
            title: {{
                text: "{title}",
                left: 'center',
                top: 10
            }},
            tooltip: {{
                trigger: 'item',
                formatter: '<b>{{b}}</b>: {highlight_label}'
            }},
            series: [{{
                type: 'map',
                map: 'china',
                data: mapData,
                label: {{
                    show: true,
                    fontSize: 9,
                    color: '#333',
                    formatter: '{{b}}'
                }},
                emphasis: {{
                    itemStyle: {{
                        areaColor: '#ffd700'
                    }}
                }}
            }}],
            visualMap: {{
                type: 'piecewise',
                show: true,
                left: 'right',
                top: '50',
                pieces: [
                    {{value: 1, label: '{highlight_label}', color: '{highlight_color}'}}
                ],
                textStyle: {{
                    color: '#333'
                }},
                inRange: {{
                    color: ['#f5f5f5', '{highlight_color}']
                }}
            }}
        }};

        chart.setOption(option);

        window.addEventListener('resize', function() {{
            var chart = echarts.getInstanceByDom(document.getElementById('map'));
            if (chart) chart.resize();
        }});
    </script>
</body>
</html>'''

    return html_template
