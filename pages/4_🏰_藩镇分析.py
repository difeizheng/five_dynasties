"""
🏰 藩镇分析页面
展示唐末五代藩镇演变和势力关系
"""
import streamlit as st
from streamlit.components.v1 import html
import json

from pyecharts import options as opts
from pyecharts.charts import Sankey, Graph, HeatMap
import pandas as pd

from src.data_loader import (
    load_fanzhen_relationships,
    load_fanzhen_complete,
    load_tang_fanzhen,
)
from src.data_processor import (
    get_regime_color,
    get_fanzhen_base_data,
    FANZHEN_COLORS,
    PROVINCE_MAPPING,
)
from src.config import FANZHEN_CHRONICLES

st.set_page_config(page_title="藩镇分析", page_icon="🏰", layout="wide")


def render_fanzhen_header():
    """渲染页面标题"""
    st.title("🏰 藩镇演变分析")
    st.markdown("查看唐末五代时期藩镇割据的演变过程和势力关系")

    st.markdown("""
    **图表说明**：
    - 🗺️ **藩镇分布图**：展示唐末主要藩镇的地理位置和控制范围
    - 🕸️ **藩镇关系网络**：力导向图展示藩镇之间的联盟、敌对关系
    - 📊 **藩镇实力对比**：从兵力、地盘、经济等维度对比各藩镇的综合实力
    - 🌊 **藩镇演变流向**：桑基图展示藩镇随时间演变的归属变化
    """)

    st.markdown("---")


def generate_fanzhen_evolution_data():
    """生成藩镇演变数据"""
    return get_fanzhen_base_data()


def render_fanzhen_map():
    """渲染藩镇分布图 - 使用内嵌 GeoJSON + visualMap 方案"""

    # 读取内嵌的 GeoJSON 数据
    with open('china_full.geojson', 'r', encoding='utf-8') as f:
        china_geojson = f.read()

    fanzhen_data = generate_fanzhen_evolution_data()

    # 构建藩镇 - 省份映射
    fanzhen_province_map = {}
    province_fanzhen_map = {}

    for fanzhen_name, data in fanzhen_data.items():
        province = data['province']
        fanzhen_province_map[fanzhen_name] = province
        if province not in province_fanzhen_map:
            province_fanzhen_map[province] = []
        province_fanzhen_map[province].append(fanzhen_name)

    # 为每个藩镇分配唯一值用于 visualMap
    fanzhen_list = list(fanzhen_data.keys())
    fanzhen_value_map = {fanzhen: idx + 1 for idx, fanzhen in enumerate(fanzhen_list)}

    # 构建地图数据
    map_data = []
    for province, fanzhens in province_fanzhen_map.items():
        # 取第一个藩镇作为该省份的代表
        main_fanzhen = fanzhens[0]
        map_data.append({
            "name": province,
            "value": fanzhen_value_map[main_fanzhen]
        })

    # 构建 visualMap pieces 配置和颜色列表
    pieces_config = []
    colors_list = []
    for fanzhen, value in fanzhen_value_map.items():
        color = FANZHEN_COLORS.get(fanzhen, "#999999")
        pieces_config.append({
            "value": value,
            "label": fanzhen,
            "color": color
        })
        colors_list.append(color)

    # 创建自定义 HTML
    html_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>藩镇分布图</title>
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

        // 藩镇 - 省份映射（用于 tooltip）
        var fanzhenProvinceMap = FANZHEN_PROVINCE_PLACEHOLDER;

        // 省份 - 藩镇映射（用于 tooltip）
        var provinceFanzhenMap = PROVINCE_FANZHEN_PLACEHOLDER;

        // 注册地图
        echarts.registerMap('china', chinaGeojson);

        var mapData = DATA_PLACEHOLDER;

        var chart = echarts.init(document.getElementById('map'), 'white');

        var option = {
            title: {
                text: "唐末藩镇分布",
                left: 'center',
                top: 10
            },
            tooltip: {
                trigger: 'item',
                formatter: function(params) {
                    var fanzhen = provinceFanzhenMap[params.name] || [];
                    var fanzhenStr = fanzhen.length > 0 ? fanzhen.join('、') : '无';
                    return '<b>' + params.name + '</b><br/>藩镇：' + fanzhenStr;
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
    html_template = html_template.replace('GEOJSON_PLACEHOLDER', china_geojson)
    html_template = html_template.replace('DATA_PLACEHOLDER', json.dumps(map_data, ensure_ascii=False))
    html_template = html_template.replace('FANZHEN_PROVINCE_PLACEHOLDER', json.dumps(fanzhen_province_map, ensure_ascii=False))
    html_template = html_template.replace('PROVINCE_FANZHEN_PLACEHOLDER', json.dumps(province_fanzhen_map, ensure_ascii=False))
    html_template = html_template.replace('PIECES_PLACEHOLDER', json.dumps(pieces_config, ensure_ascii=False))
    html_template = html_template.replace('COLORS_PLACEHOLDER', json.dumps(colors_list, ensure_ascii=False))
    html_template = html_template.replace('LEGEND_PLACEHOLDER', json.dumps(fanzhen_list, ensure_ascii=False))

    return html_template


def render_fanzhen_sankey():
    """渲染藩镇演变桑基图"""
    # 藩镇演变关系
    nodes = [
        {"name": "唐朝"},
        # 五代来源
        {"name": "宣武 (朱温)"},
        {"name": "河东 (李克用)"},
        {"name": "凤翔 (李茂贞)"},
        # 五代政权
        {"name": "后梁"},
        {"name": "后唐"},
        # 其他藩镇
        {"name": "魏博"},
        {"name": "成德"},
        {"name": "卢龙"},
        {"name": "淮南"},
        {"name": "镇海"},
    ]

    links = [
        {"source": "唐朝", "target": "宣武 (朱温)", "value": "901"},
        {"source": "唐朝", "target": "河东 (李克用)", "value": "880"},
        {"source": "唐朝", "target": "凤翔 (李茂贞)", "value": "887"},
        {"source": "宣武 (朱温)", "target": "后梁", "value": "907"},
        {"source": "河东 (李克用)", "target": "后唐", "value": "923"},
        {"source": "唐朝", "target": "魏博", "value": "763"},
        {"source": "唐朝", "target": "成德", "value": "763"},
        {"source": "唐朝", "target": "卢龙", "value": "763"},
        {"source": "唐朝", "target": "淮南", "value": "763"},
        {"source": "唐朝", "target": "镇海", "value": "787"},
    ]

    sankey = Sankey(init_opts=opts.InitOpts(width="100%", height="500px"))

    sankey.add(
        "藩镇演变",
        nodes=[{"name": n["name"]} for n in nodes],
        links=links,
        label_opts=opts.LabelOpts(position="right", formatter="{b}"),
    )

    sankey.set_global_opts(
        title_opts=opts.TitleOpts(title="藩镇演变流向图"),
    )

    return sankey


def render_fanzhen_relationship_graph():
    """渲染藩镇关系网络图"""
    # 河北三镇关系
    nodes = [
        {"name": "魏博", "symbolSize": 70, "value": "河北最强"},
        {"name": "成德", "symbolSize": 60, "value": "河北中部"},
        {"name": "卢龙", "symbolSize": 65, "value": "河北北部"},
        {"name": "宣武", "symbolSize": 80, "value": "河南/最强"},
        {"name": "河东", "symbolSize": 80, "value": "山西/最强"},
        {"name": "凤翔", "symbolSize": 60, "value": "陕西"},
        {"name": "淮南", "symbolSize": 55, "value": "江淮"},
        {"name": "镇海", "symbolSize": 50, "value": "浙江"},
        {"name": "武安", "symbolSize": 45, "value": "湖南"},
        {"name": "后梁", "symbolSize": 90, "value": "907-923"},
        {"name": "后唐", "symbolSize": 90, "value": "923-936"},
    ]

    links = [
        {"source": "魏博", "target": "宣武", "value": "依附"},
        {"source": "成德", "target": "宣武", "value": "结盟"},
        {"source": "卢龙", "target": "宣武", "value": "结盟"},
        {"source": "河东", "target": "宣武", "value": "敌对"},
        {"source": "凤翔", "target": "宣武", "value": "敌对"},
        {"source": "宣武", "target": "后梁", "value": "建立"},
        {"source": "河东", "target": "后唐", "value": "建立"},
        {"source": "魏博", "target": "后唐", "value": "归附"},
        {"source": "成德", "target": "后唐", "value": "归附"},
        {"source": "卢龙", "target": "后唐", "value": "归附"},
        {"source": "淮南", "target": "后梁", "value": "对抗"},
        {"source": "镇海", "target": "后梁", "value": "归附"},
    ]

    graph = Graph(init_opts=opts.InitOpts(width="100%", height="600px"))

    graph.add(
        "",
        nodes,
        links,
        repulsion=10000,
        edge_symbol=["circle", "arrow"],
        edge_length=[100, 300],
        label_opts=opts.LabelOpts(is_show=True, position="right"),
        linestyle_opts=opts.LineStyleOpts(
            color="source",
        ),
    )

    graph.set_global_opts(
        title_opts=opts.TitleOpts(title="藩镇势力关系网络"),
        legend_opts=opts.LegendOpts(is_show=False),
        tooltip_opts=opts.TooltipOpts(
            trigger="item",
            formatter="{b}: {c}"
        ),
    )

    return graph


def render_fanzhen_power_chart():
    """渲染藩镇实力对比图"""
    from pyecharts.charts import Bar

    fanzhen_data = generate_fanzhen_evolution_data()

    names = list(fanzhen_data.keys())
    powers = [data['power'] for data in fanzhen_data.values()]
    areas = [data['area'] for data in fanzhen_data.values()]

    bar = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))

    bar.add_xaxis(names)
    bar.add_yaxis(
        "实力值",
        powers,
        label_opts=opts.LabelOpts(position="top"),
    )

    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="藩镇实力对比"),
        yaxis_opts=opts.AxisOpts(name="实力值", max_=100),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)),
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            formatter="{b}<br/>实力：{c}<br/>区域：{d}"
        ),
    )

    return bar


def render_fanzhen_timeline():
    """渲染藩镇时间线"""
    from pyecharts.charts import Line

    # 藩镇兴衰时间线
    timeline_data = {
        "宣武": [(763, 20), (800, 40), (850, 60), (900, 95), (907, 100), (923, 0)],
        "河东": [(763, 10), (800, 30), (850, 50), (880, 70), (900, 85), (923, 100), (936, 0)],
        "魏博": [(763, 60), (800, 70), (850, 80), (900, 85), (923, 50), (936, 0)],
        "成德": [(763, 50), (800, 60), (850, 65), (900, 70), (923, 40), (936, 0)],
        "卢龙": [(763, 55), (800, 65), (850, 70), (900, 80), (923, 50), (936, 0)],
    }

    line = Line(init_opts=opts.InitOpts(width="100%", height="400px"))

    # 使用所有年份的并集作为 x 轴
    all_years = set()
    for data in timeline_data.values():
        for year, _ in data:
            all_years.add(year)
    x_years = sorted(list(all_years))

    line.add_xaxis(x_years)

    # 为每个藩镇添加数据，需要对齐全 x 轴年份
    for name, data in timeline_data.items():
        data_dict = dict(data)
        values = [data_dict.get(year, 0) for year in x_years]
        line.add_yaxis(name, values, is_symbol_show=True)

    line.set_global_opts(
        title_opts=opts.TitleOpts(title="藩镇实力演变 (763-936 年)"),
        xaxis_opts=opts.AxisOpts(name="年份"),
        yaxis_opts=opts.AxisOpts(name="实力值", max_=100),
        legend_opts=opts.LegendOpts(type_="scroll", pos_top="90%"),
    )

    return line


def render_fanzhen_detail_table():
    """渲染藩镇详情表"""
    st.subheader("📋 藩镇详情")

    fanzhen_data = generate_fanzhen_evolution_data()

    df = pd.DataFrame([
        {
            "藩镇": name,
            "区域": data['area'],
            "实力": data['power'],
            "说明": f"{data['area']}藩镇，实力值{data['power']}"
        }
        for name, data in fanzhen_data.items()
    ])

    st.dataframe(df, use_container_width=True)


def render_fanzhen_chronicle():
    """渲染藩镇编年史"""
    st.subheader("📜 藩镇编年史")

    st.markdown("""
    **使用说明**：选择藩镇查看其历史沿革，包括节度使更迭和重大历史事件。
    """)

    # 藩镇选择器
    fanzhen_names = list(FANZHEN_CHRONICLES.keys())
    selected_fanzhen = st.selectbox(
        "选择藩镇",
        fanzhen_names,
        key="fanzhen_chronicle_selector"
    )

    if selected_fanzhen:
        # 显示藩镇详情卡片
        chronicle = FANZHEN_CHRONICLES.get(selected_fanzhen, [])

        if chronicle:
            # 藩镇基本信息
            fanzhen_info = generate_fanzhen_evolution_data().get(selected_fanzhen, {})
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"**区域**: {fanzhen_info.get('area', '未知')}")
            with col2:
                st.markdown(f"**实力**: {fanzhen_info.get('power', '未知')}")
            with col3:
                color = FANZHEN_COLORS.get(selected_fanzhen, "#999999")
                st.markdown(
                    f"""<div style="display:inline-block; padding:0.25rem 0.5rem; border-radius:0.25rem; background:{color}20; color:{color}; font-weight:bold;">
                    {selected_fanzhen}
                    </div>""",
                    unsafe_allow_html=True
                )

            # 编年史时间线
            st.markdown("#### 📅 历史沿革")

            for event in chronicle:
                year = event['year']
                event_desc = event['event']
                jiedushi = event.get('jiedushi', '')

                # 使用卡片样式展示事件
                st.markdown(
                    f"""<div style="
                        padding: 0.75rem 1rem;
                        margin: 0.5rem 0;
                        border-radius: 0.5rem;
                        border-left: 4px solid {FANZHEN_COLORS.get(selected_fanzhen, '#999999')};
                        background: {FANZHEN_COLORS.get(selected_fanzhen, '#999999')}10;">
                        <strong style="font-size: 1.1em;">{year}年</strong><br/>
                        {event_desc}<br/>
                        <span style="color: #666; font-size: 0.9em;">节度使：{jiedushi}</span>
                    </div>""",
                    unsafe_allow_html=True
                )
        else:
            st.warning(f"暂未收录 {selected_fanzhen} 的编年史数据")


def render_hebei_three_towns():
    """渲染河北三镇详解"""
    st.subheader("🏰 河北三镇（河朔三镇）")

    st.markdown("""
    **魏博节度使**
    - 辖区：魏州、博州等（今河北南部、河南北部）
    - 实力：河北最强藩镇
    - 特点：牙兵强悍，屡逐节度使
    - 结局：915 年被后梁分割，后归后唐

    **成德节度使**
    - 辖区：镇州、冀州等（今河北中部）
    - 实力：中等
    - 特点：与魏博、卢龙互为犄角
    - 结局：922 年被后唐所灭

    **卢龙节度使**
    - 辖区：幽州、涿州等（今河北北部、北京、辽宁）
    - 实力：较强
    - 特点：防御契丹，后割让燕云十六州
    - 结局：913 年被后梁所灭
    """)


def main():
    """主函数"""
    render_fanzhen_header()

    # 藩镇分布图
    st.subheader("🗺️ 藩镇分布")
    fanzhen_map = render_fanzhen_map()
    html(fanzhen_map, height=650, scrolling=False)

    st.markdown("---")

    # 藩镇编年史
    render_fanzhen_chronicle()

    st.markdown("---")

    # 实力对比
    st.subheader("📊 藩镇实力对比")
    power_chart = render_fanzhen_power_chart()
    html(power_chart.render_embed(), height=650, scrolling=False)

    st.markdown("---")

    # 演变流向图
    st.subheader("🔄 藩镇演变流向")
    sankey = render_fanzhen_sankey()
    html(sankey.render_embed(), height=650, scrolling=False)

    st.markdown("---")

    # 实力演变时间线
    st.subheader("📈 藩镇实力演变")
    timeline = render_fanzhen_timeline()
    html(timeline.render_embed(), height=650, scrolling=False)

    st.markdown("---")

    # 关系网络
    st.subheader("🕸️ 藩镇关系网络")
    graph = render_fanzhen_relationship_graph()
    html(graph.render_embed(), height=650, scrolling=False)

    st.markdown("---")

    # 河北三镇详解
    render_hebei_three_towns()

    st.markdown("---")

    # 详情表
    render_fanzhen_detail_table()


if __name__ == "__main__":
    main()

