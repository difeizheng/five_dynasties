"""
🗺️ 政权地图页面
展示五代十国疆域范围和现代省份对照
"""

import streamlit as st
from streamlit.components.v1 import html
from pyecharts import options as opts
from pyecharts.charts import Bar
import pandas as pd
import json

from src.data_processor import (
    WUDAI_REGIMES,
    SHIGUO_REGIMES,
    REGIME_TO_PROVINCE,
    process_regime_timeline,
    get_regime_color,
    get_province_regime_mapping,
)

st.set_page_config(page_title="政权地图", page_icon="🗺️", layout="wide")

# 省份名称映射（古 -> 今）- 使用中国地图 JS 中的标准名称格式
PROVINCE_MAPPING = {
    "河南": "河南省",
    "河北": "河北省",
    "山东": "山东省",
    "山西": "山西省",
    "陕西": "陕西省",
    "浙江": "浙江省",
    "江苏": "江苏省",
    "上海": "上海市",
    "安徽": "安徽省",
    "江西": "江西省",
    "湖北": "湖北省",
    "湖南": "湖南省",
    "四川": "四川省",
    "重庆": "重庆市",
    "福建": "福建省",
    "广东": "广东省",
    "广西": "广西",
    "海南": "海南省",
    "甘肃": "甘肃省",
    "辽宁": "辽宁省",
    "内蒙古": "内蒙古",
}

# 政权颜色配置
REGIME_COLORS = {
    "后梁": "#e74c3c", "后唐": "#3498db", "后晋": "#9b59b6",
    "后汉": "#e67e22", "后周": "#2ecc71",
    "吴越": "#1abc9c", "南唐": "#e74c3c", "前蜀": "#f39c12",
    "后蜀": "#d35400", "闽国": "#9b59b6", "南汉": "#3498db",
    "楚": "#3498db", "荆南": "#1abc9c", "北汉": "#95a5a6",
}

# 都城坐标
CAPITAL_COORDS = {
    "开封": (114.34, 34.79, "后梁/后晋/后汉/后周"),
    "洛阳": (112.43, 34.62, "后唐"),
    "杭州": (120.16, 30.27, "吴越"),
    "南京": (118.78, 32.07, "南唐"),
    "成都": (104.07, 30.67, "前蜀/后蜀"),
    "福州": (119.30, 26.08, "闽国"),
    "广州": (113.27, 23.13, "南汉"),
    "长沙": (112.94, 28.23, "楚"),
    "荆州": (112.19, 30.33, "荆南"),
    "太原": (112.55, 37.87, "北汉"),
}


def render_map_header():
    """渲染页面标题"""
    st.title("🗺️ 政权疆域地图")
    st.markdown("查看五代十国各政权的疆域范围与现代行政区划的对照")

    st.markdown("""
    **图表说明**：
    - 🗺️ **疆域地图**：在中国地图上展示各政权的疆域范围，不同颜色代表不同政权
    - 🏛️ **都城分布**：散点图展示各政权都城所在地理位置
    - 📊 **疆域面积估算**：柱状图对比各政权的疆域面积（万平方公里）
    - 📋 **现代省份对照**：列出现代各省份在五代十国时期所属的政权
    """)

    st.markdown("---")


def render_regime_map(regime_name: str = None):
    """渲染政权地图 - 使用 visualMap + inRange 实现颜色填充"""

    # 读取内嵌的 GeoJSON 数据
    with open('china_full.geojson', 'r', encoding='utf-8') as f:
        china_geojson = f.read()

    mapping = get_province_regime_mapping()

    if regime_name and regime_name != "全部":
        mapping = mapping[mapping['regime'] == regime_name]

    # 构建省份 - 政权映射
    province_info = {}
    regimes_in_map = set()

    for _, row in mapping.iterrows():
        province = PROVINCE_MAPPING.get(row['province'], row['province'])
        regime = row['regime']
        province_info[province] = {"regime": regime}
        regimes_in_map.add(regime)

    regimes_list = list(regimes_in_map)

    # 为每个政权分配唯一值用于 visualMap
    regime_value_map = {regime: idx + 1 for idx, regime in enumerate(regimes_list)}

    # 构建地图数据（包含 value 字段）
    map_data = []
    for province, info in province_info.items():
        regime = info["regime"]
        map_data.append({
            "name": province,
            "value": regime_value_map[regime]
        })

    # 构建 visualMap pieces 配置和颜色列表
    pieces_config = []
    colors_list = []
    for regime, value in regime_value_map.items():
        color = REGIME_COLORS.get(regime, "#999999")
        pieces_config.append({
            "value": value,
            "label": regime,
            "color": color
        })
        colors_list.append(color)

    # 创建自定义 HTML - 内嵌 GeoJSON 数据
    html_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>政权地图</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        body { margin: 0; padding: 0; background: #fff; }
        #map { width: 100%; height: 600px; }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        // 内嵌 GeoJSON 数据
        var chinaGeojson = GEOJSON_PLACEHOLDER;

        // 省份 - 政权映射（用于 tooltip）
        var provinceRegimeMap = PROVINCE_REGIME_PLACEHOLDER;

        // 注册地图
        echarts.registerMap('china', chinaGeojson);

        var mapData = DATA_PLACEHOLDER;

        var chart = echarts.init(document.getElementById('map'), 'white');

        var option = {
            title: {
                text: "TITLE_PLACEHOLDER",
                left: 'center',
                top: 10
            },
            tooltip: {
                trigger: 'item',
                formatter: function(params) {
                    var regime = provinceRegimeMap[params.name] || '未知';
                    return '<b>' + params.name + '</b><br/>所属政权：' + regime;
                }
            },
            series: [{
                type: 'map',
                map: 'china',
                data: mapData,
                label: {
                    show: true,
                    fontSize: 9,
                    color: '#333',
                    formatter: '{b}'
                },
                emphasis: {
                    itemStyle: {
                        areaColor: '#ffd700',
                        borderColor: '#fff',
                        borderWidth: 2
                    },
                    label: {
                        color: '#fff',
                        fontWeight: 'bold'
                    }
                }
            }],
            visualMap: {
                type: 'piecewise',
                show: true,
                right: '10',
                top: '50',
                pieces: PIECES_PLACEHOLDER,
                textStyle: {
                    color: '#333'
                },
                inRange: {
                    color: COLORS_PLACEHOLDER
                }
            },
            legend: {
                data: LEGEND_PLACEHOLDER,
                top: 50,
                selectedMode: true,
                type: 'scroll',
                orient: 'horizontal'
            }
        };

        chart.setOption(option);

        window.addEventListener('resize', function() {
            var chart = echarts.getInstanceByDom(document.getElementById('map'));
            if (chart) chart.resize();
        });
    </script>
</body>
</html>'''

    # 替换占位符
    title_text = ' '.join(regimes_list) + ' 疆域范围'
    html_template = html_template.replace('TITLE_PLACEHOLDER', title_text)
    html_template = html_template.replace('GEOJSON_PLACEHOLDER', china_geojson)
    html_template = html_template.replace('DATA_PLACEHOLDER', json.dumps(map_data, ensure_ascii=False))
    html_template = html_template.replace('PROVINCE_REGIME_PLACEHOLDER', json.dumps({k: v["regime"] for k, v in province_info.items()}, ensure_ascii=False))
    html_template = html_template.replace('PIECES_PLACEHOLDER', json.dumps(pieces_config, ensure_ascii=False))
    html_template = html_template.replace('COLORS_PLACEHOLDER', json.dumps(colors_list, ensure_ascii=False))
    html_template = html_template.replace('LEGEND_PLACEHOLDER', json.dumps(regimes_list, ensure_ascii=False))

    return html_template


def render_capital_scatter():
    """渲染都城分布散点图 - 使用内嵌 GeoJSON 实现颜色填充"""

    # 读取内嵌的 GeoJSON 数据
    with open('china_full.geojson', 'r', encoding='utf-8') as f:
        china_geojson = f.read()

    # 都城对应省份
    capital_provinces = [
        "河南省", "浙江省", "江苏省", "四川省", "福建省",
        "广东省", "湖南省", "湖北省", "山西省"
    ]

    # 构建地图数据
    map_data = []
    province_set = set(capital_provinces)
    # 添加所有省份，都城省份 value=1，其他省份 value=0
    for province in capital_provinces:
        map_data.append({"name": province, "value": 1})

    html_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>都城分布</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        body { margin: 0; padding: 0; background: #fff; }
        #map { width: 100%; height: 500px; }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        // 内嵌 GeoJSON 数据
        var chinaGeojson = GEOJSON_PLACEHOLDER;

        // 注册地图
        echarts.registerMap('china', chinaGeojson);

        // 都城省份列表
        var capitalProvinces = CAPITAL_PROVINCES_PLACEHOLDER;

        // 构建地图数据
        var mapData = [];
        for (var i = 0; i < capitalProvinces.length; i++) {
            mapData.push({name: capitalProvinces[i], value: 1});
        }

        var chart = echarts.init(document.getElementById('map'), 'white');

        var option = {
            title: {
                text: "五代十国都城分布",
                left: 'center',
                top: 10
            },
            tooltip: {
                trigger: 'item',
                formatter: '<b>{b}</b>: 都城所在地'
            },
            series: [{
                type: 'map',
                map: 'china',
                data: mapData,
                label: {
                    show: true,
                    fontSize: 9,
                    color: '#333',
                    formatter: '{b}'
                },
                emphasis: {
                    itemStyle: {
                        areaColor: '#ffd700'
                    }
                }
            }],
            visualMap: {
                type: 'piecewise',
                show: true,
                left: 'right',
                top: '50',
                pieces: [
                    {value: 1, label: '都城所在地', color: '#e74c3c'}
                ],
                textStyle: {
                    color: '#333'
                },
                inRange: {
                    color: ['#f5f5f5', '#e74c3c']
                }
            }
        };

        chart.setOption(option);

        window.addEventListener('resize', function() {
            var chart = echarts.getInstanceByDom(document.getElementById('map'));
            if (chart) chart.resize();
        });
    </script>
</body>
</html>'''

    html_template = html_template.replace('GEOJSON_PLACEHOLDER', china_geojson)
    html_template = html_template.replace('CAPITAL_PROVINCES_PLACEHOLDER', json.dumps(capital_provinces, ensure_ascii=False))

    return html_template


def render_province_regime_table():
    """渲染省份 - 政权对照表"""
    st.subheader("📋 现代省份与五代十国政权对照")

    # 创建 DataFrame
    mapping = get_province_regime_mapping()

    # 按省份分组
    province_groups = mapping.groupby('province')

    for province, group in province_groups:
        regimes = ', '.join(group['regime'].tolist())
        types = ', '.join(group['type'].unique())
        st.markdown(f"**{province}**: {regimes} ({types})")

    return mapping


def render_regime_area_chart():
    """渲染政权面积估算图"""
    # 估算面积（万平方公里）
    area_data = {
        "后周": 50,
        "南唐": 35,
        "前蜀": 25,
        "后蜀": 25,
        "南汉": 20,
        "楚": 21,
        "吴越": 12,
        "闽国": 12,
        "北汉": 8,
        "荆南": 3,
    }

    bar = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))

    bar.add_xaxis(list(area_data.keys()))
    bar.add_yaxis(
        "面积 (万 km²)",
        list(area_data.values()),
        label_opts=opts.LabelOpts(position="top"),
    )

    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="政权疆域面积估算"),
        yaxis_opts=opts.AxisOpts(name="面积 (万 km²)"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
    )

    return bar


def render_modern_comparison():
    """渲染现代对照"""
    st.subheader("🌍 政权与现代省份对照")

    cols = st.columns(2)

    with cols[0]:
        st.markdown("#### 五代政权")
        for regime in WUDAI_REGIMES:
            provinces = REGIME_TO_PROVINCE.get(regime['name'], [])
            st.markdown(
                f"**{regime['name']}** ({regime['start']}-{regime['end']})\n"
                f"- 都城：{regime['capital']}\n"
                f"- 范围：{', '.join(provinces)}"
            )

    with cols[1]:
        st.markdown("#### 十国政权")
        for regime in SHIGUO_REGIMES:
            provinces = REGIME_TO_PROVINCE.get(regime['name'], [])
            st.markdown(
                f"**{regime['name']}** ({regime['start']}-{regime['end']})\n"
                f"- 都城：{regime['capital']}\n"
                f"- 范围：{', '.join(provinces)}"
            )


def main():
    """主函数"""
    render_map_header()

    # 地图选择器
    st.subheader("🗺️ 疆域地图")

    regime_names = ["全部"] + [r['name'] for r in WUDAI_REGIMES + SHIGUO_REGIMES]
    selected_regime = st.selectbox("选择政权", regime_names)

    if selected_regime == "全部":
        regime_map = render_regime_map()
    else:
        regime_map = render_regime_map(selected_regime)

    # render_regime_map 返回的是修改后的 HTML 字符串
    if isinstance(regime_map, str):
        html(regime_map, height=650, scrolling=False)
    else:
        html(regime_map.render_embed(), height=650, scrolling=False)

    st.markdown("---")

    # 都城分布
    capital_chart = render_capital_scatter()
    html(capital_chart, height=550, scrolling=False)

    st.markdown("---")

    # 面积对比
    area_chart = render_regime_area_chart()
    html(area_chart.render_embed(), height=650, scrolling=False)

    st.markdown("---")

    # 现代对照
    render_modern_comparison()


if __name__ == "__main__":
    main()
