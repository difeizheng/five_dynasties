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
    region_color_map: Dict[str, str],  # {region_name: color}
    title: str,
    tooltip_formatter: str = None,
    province_regime_map: Dict[str, str] = None,
    legend_title: str = None,
    height: int = 600,
) -> str:
    """
    构建 choropleth 地图 HTML（使用 visualMap pieces 映射颜色）

    Args:
        geojson_content: GeoJSON 内容
        map_data: 地图数据列表，每项包含 name 和 value
        region_color_map: 区域名称到颜色的映射 {region_name: color}
        title: 地图标题
        tooltip_formatter: tooltip 格式化模板
        province_regime_map: 省份到政权的映射 {province: regime}，用于 tooltip
        legend_title: 图例标题
        height: 地图高度

    Returns:
        完整的 HTML 字符串
    """
    # 构建数据：给每个省份分配一个唯一 ID（从 1 开始）
    data_with_id = []
    name_to_id = {}
    for idx, item in enumerate(map_data):
        name = item.get('name', '')
        name_to_id[name] = idx + 1
        data_with_id.append({'name': name, 'value': idx + 1})

    # 构建 visualMap 的 pieces 配置 - 将 ID 映射到颜色
    pieces = []
    for item in map_data:
        name = item.get('name', '')
        color = region_color_map.get(name, '#cccccc')
        idx = name_to_id.get(name, 0)
        pieces.append({
            'min': idx,
            'max': idx,
            'color': color,
            'label': name
        })

    # 获取所有区域名称用于图例
    region_names = list(region_color_map.keys())

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
        var provinceRegimeMap = {province_regime_json};
        var mapData = {json.dumps(data_with_id, ensure_ascii=False)};
        var regionNames = {json.dumps(region_names, ensure_ascii=False)};

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
                        areaColor: '#ffd700'
                    }},
                    label: {{
                        color: '#fff',
                        fontWeight: 'bold'
                    }}
                }}
            }}],
            visualMap: {{
                type: 'piecewise',
                show: false,
                min: 0,
                max: {len(map_data) + 1},
                pieces: {json.dumps(pieces, ensure_ascii=False)},
                inRange: {{}},
                outOfRange: {{
                    color: '#f5f5f5'
                }}
            }},
            legend: {{
                data: regionNames,
                top: 50,
                selectedMode: true,
                type: 'scroll',
                orient: 'horizontal',
                textStyle: {{
                    color: '#333'
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


def build_choropleth_map_html_with_regime_legend(
    geojson_content: str,
    map_data: List[Dict],
    province_regime_map: Dict[str, str],  # {province: regime}
    tooltip_formatter: str = None,
    legend_names: List[str] = None,  # 政权名称列表
    legend_colors: Dict[str, str] = None,  # {regime: color}
    title: str = "地图",
    height: int = 600,
) -> str:
    """
    构建 choropleth 地图 HTML（按政权分组的图例）- 使用 visualMap 方案

    Args:
        geojson_content: GeoJSON 内容
        map_data: 地图数据列表，每项包含 name、value 和 itemStyle
        province_regime_map: 省份到政权的映射 {province: regime}
        tooltip_formatter: tooltip 格式化模板
        legend_names: 政权名称列表
        legend_colors: 政权颜色映射 {regime: color}
        title: 地图标题
        height: 地图高度

    Returns:
        完整的 HTML 字符串
    """
    # 给每个省份分配一个唯一 ID，并根据政权设置颜色
    data_with_id = []
    name_to_id = {}
    id_to_regime = {}

    for idx, item in enumerate(map_data):
        name = item.get('name', '')
        name_to_id[name] = idx + 1
        regime = province_regime_map.get(name, '')
        id_to_regime[idx + 1] = regime
        data_with_id.append({'name': name, 'value': idx + 1})

    # 构建 visualMap 的 pieces 配置 - 将 ID 映射到颜色
    pieces = []
    for item in map_data:
        name = item.get('name', '')
        regime = province_regime_map.get(name, '')
        color = legend_colors.get(regime, '#cccccc') if legend_colors else '#cccccc'
        idx = name_to_id.get(name, 0)
        pieces.append({
            'min': idx,
            'max': idx,
            'color': color,
            'label': name
        })

    # 构建图例数据（按政权分组）
    if legend_names is None:
        legend_names = list(set(province_regime_map.values()))

    if legend_colors is None:
        legend_colors = {}

    # 构建自定义图例项
    custom_legend_items = []
    for name in legend_names:
        color = legend_colors.get(name, '#999999')
        custom_legend_items.append({
            'name': name,
            'itemStyle': {'color': color}
        })

    # 构建 tooltip 格式化函数
    if tooltip_formatter:
        tooltip_js = tooltip_formatter
    else:
        tooltip_js = """function(params) {
            return '<b>' + params.name + '</b><br/>所属政权：' + (provinceRegimeMap[params.name] || '未知');
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
        var provinceRegimeMap = {province_regime_json};
        var mapData = {json.dumps(data_with_id, ensure_ascii=False)};
        var customLegendItems = {json.dumps(custom_legend_items, ensure_ascii=False)};

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
                        areaColor: '#ffd700'
                    }},
                    label: {{
                        color: '#fff',
                        fontWeight: 'bold'
                    }}
                }}
            }}],
            visualMap: {{
                type: 'piecewise',
                show: false,
                min: 0,
                max: {len(map_data) + 1},
                pieces: {json.dumps(pieces, ensure_ascii=False)},
                inRange: {{}},
                outOfRange: {{
                    color: '#f5f5f5'
                }}
            }},
            legend: {{
                data: customLegendItems,
                top: 50,
                selectedMode: true,
                type: 'scroll',
                orient: 'horizontal',
                textStyle: {{
                    color: '#333'
                }},
                itemWidth: 15,
                itemHeight: 15
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


def build_capital_map_html(
    geojson_content: str,
    capital_data: dict,
    title: str = "都城分布",
    height: int = 500,
) -> str:
    """
    构建都城地图 HTML（支持自定义 tooltip 显示都城和政权信息）

    Args:
        geojson_content: GeoJSON 内容
        capital_data: 都城数据字典 {省份：[(都城名，政权名), ...]}
        title: 地图标题
        height: 地图高度

    Returns:
        完整的 HTML 字符串
    """
    # 构建高亮省份列表
    highlight_provinces = list(capital_data.keys())

    # 构建省份到都城信息的映射（用于 tooltip）
    capital_info_map = {}
    for province, capitals in capital_data.items():
        capital_info_map[province] = capitals

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
        var highlightProvinces = {json.dumps(highlight_provinces)};
        var capitalInfoMap = {json.dumps(capital_info_map)};

        echarts.registerMap('china', chinaGeojson);

        var mapData = highlightProvinces.map(function(name) {{
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
                formatter: function(params) {{
                    var province = params.name;
                    var capitals = capitalInfoMap[province];
                    if (!capitals || capitals.length === 0) {{
                        return '<b>' + province + '</b>';
                    }}
                    var content = '<b>' + province + '</b><br/>';
                    capitals.forEach(function(cap) {{
                        content += cap[0] + '(' + cap[1] + ')<br/>';
                    }});
                    return content;
                }}
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
                    {{value: 1, label: '都城所在地', color: '#e74c3c'}}
                ],
                textStyle: {{
                    color: '#333'
                }},
                inRange: {{
                    color: ['#f5f5f5', '#e74c3c']
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


# ============================================
# 用户数据导出/导入组件
# ============================================

def export_user_data_to_json(data: dict, filename: str = "user_data.json"):
    """
    导出用户数据为 JSON 文件

    Args:
        data: 用户数据字典
        filename: 文件名
    """
    import base64
    import json

    json_content = json.dumps(data, ensure_ascii=False, indent=2)
    b64 = base64.b64encode(json_content.encode('utf-8')).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="{filename}" style="display: inline-block; padding: 0.5rem 1rem; background: #28a745; color: white; text-decoration: none; border-radius: 0.25rem;">📥 下载 JSON 文件</a>'
    st.markdown(href, unsafe_allow_html=True)


def generate_share_link(data: dict) -> str:
    """
    生成分享链接（基于 base64 编码）

    Args:
        data: 要分享的数据

    Returns:
        分享链接（包含编码数据的 URL）
    """
    import base64
    import json

    json_content = json.dumps(data, ensure_ascii=False)
    b64 = base64.b64encode(json_content.encode('utf-8')).decode()
    return f"?data={b64}"


def parse_share_link_params(query_string: str) -> dict:
    """
    解析分享链接参数

    Args:
        query_string: URL 查询字符串

    Returns:
        解析后的数据字典
    """
    import base64
    import json
    from urllib.parse import parse_qs

    params = parse_qs(query_string)
    if 'data' in params:
        b64 = params['data'][0]
        json_content = base64.b64decode(b64.encode('utf-8')).decode('utf-8')
        return json.loads(json_content)
    return {}


def render_import_file_uploader(file_type: str = "json", key: str = "import_file"):
    """
    渲染文件上传器

    Args:
        file_type: 文件类型
        key: 组件 key

    Returns:
        上传的文件内容（字典）或 None
    """
    uploaded_file = st.file_uploader(
        "选择要导入的文件",
        type=[file_type],
        key=key,
        help=f"请选择.{file_type}格式的文件进行导入"
    )

    if uploaded_file is not None:
        try:
            import json
            content = uploaded_file.read().decode('utf-8')
            data = json.loads(content)
            return data
        except Exception as e:
            st.error(f"文件解析失败：{str(e)}")
            return None
    return None


def export_session_state_to_json(include_keys: list = None, exclude_keys: list = None) -> dict:
    """
    导出 session state 数据

    Args:
        include_keys: 要包含的 key 列表（默认包含所有）
        exclude_keys: 要排除的 key 列表

    Returns:
        用户数据字典
    """
    user_data = {}

    # 默认包含的用户数据 key
    default_keys = [
        'user_score',
        'achievements_unlocked',
        'bookmarked_items',
        'favorite_regimes',
        'quiz_history',
        'story_progress',
    ]

    keys_to_export = include_keys or default_keys

    for key in keys_to_export:
        if exclude_keys and key in exclude_keys:
            continue
        if key in st.session_state:
            user_data[key] = st.session_state[key]

    return user_data


def import_session_state_from_json(data: dict, merge: bool = True):
    """
    导入 session state 数据

    Args:
        data: 要导入的数据字典
        merge: 是否合并（True）还是覆盖（False）
    """
    for key, value in data.items():
        if key not in st.session_state or not merge:
            st.session_state[key] = value
        elif isinstance(value, list) and isinstance(st.session_state[key], list):
            # 列表类型合并
            for item in value:
                if item not in st.session_state[key]:
                    st.session_state[key].append(item)
        elif isinstance(value, dict) and isinstance(st.session_state[key], dict):
            # 字典类型合并
            st.session_state[key].update(value)


def render_user_data_export_import():
    """
    渲染用户数据导出/导入 UI 组件
    """
    st.markdown("### 📤 导出我的数据")
    st.markdown("将你的学习进度、收藏和成就导出为 JSON 文件")

    # 选择要导出的数据类型
    data_types = st.multiselect(
        "选择要导出的数据类型",
        options=[
            ("user_score", "测验得分"),
            ("achievements_unlocked", "解锁成就"),
            ("bookmarked_items", "收藏内容"),
            ("favorite_regimes", "偏好政权"),
            ("quiz_history", "测验历史"),
            ("story_progress", "故事进度"),
        ],
        default=[
            ("user_score", "测验得分"),
            ("achievements_unlocked", "解锁成就"),
            ("bookmarked_items", "收藏内容"),
        ]
    )

    if data_types:
        include_keys = [k for k, v in data_types]

        if st.button("📥 生成导出数据"):
            user_data = export_session_state_to_json(include_keys=include_keys)
            st.session_state.temp_export_data = user_data
            st.success("数据已准备就绪，请点击下方下载按钮")
            export_user_data_to_json(user_data, "my_five_dynasties_data.json")

    st.markdown("---")

    st.markdown("### 📥 导入数据")
    st.markdown("从 JSON 文件恢复你的学习进度")

    imported_data = render_import_file_uploader("json", "import_user_data")

    if imported_data:
        st.success("文件解析成功！")
        st.json(imported_data)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 覆盖当前数据"):
                import_session_state_from_json(imported_data, merge=False)
                st.success("数据已覆盖！")
                st.rerun()
        with col2:
            if st.button("➕ 合并到当前数据"):
                import_session_state_from_json(imported_data, merge=True)
                st.success("数据已合并！")
                st.rerun()
