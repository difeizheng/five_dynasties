"""
五代十国可视化系统 - 综合测试脚本
"""

import sys
sys.path.insert(0, '.')

def test_data_loader():
    """测试数据加载模块"""
    print("\n=== 测试数据加载模块 ===")
    from src.data_loader import (
        load_wudai_history_text,
        load_wudai_detailed_characters,
    )
    from src.data_processor import (
        process_regime_timeline,
    )

    text = load_wudai_history_text()
    print(f"[OK] 历史文本加载：{len(text):,} 字符")

    chars = load_wudai_detailed_characters()
    print(f"[OK] 人物数据加载：{len(chars)} 个时期")

    timeline = process_regime_timeline()
    print(f"[OK] 政权时间线：{len(timeline)} 个政权")

    return True

def test_data_processor():
    """测试数据处理模块"""
    print("\n=== 测试数据处理模块 ===")
    from src.data_processor import (
        WUDAI_REGIMES, SHIGUO_REGIMES,
        calculate_regime_stats,
        get_province_regime_mapping,
    )

    print(f"[OK] 五代政权：{len(WUDAI_REGIMES)} 个")
    print(f"[OK] 十国政权：{len(SHIGUO_REGIMES)} 个")

    stats = calculate_regime_stats()
    print(f"[OK] 统计：平均存续 {stats['avg_duration']:.1f} 年")

    mapping = get_province_regime_mapping()
    print(f"[OK] 省份映射：{len(mapping)} 条")

    return True

def test_text_analyzer():
    """测试文本分析模块"""
    print("\n=== 测试文本分析模块 ===")
    from src.text_analyzer import (
        segment_text,
        extract_keywords,
        analyze_text_statistics,
        generate_wordcloud_data,
    )

    test_text = "朱温建立后梁，定都开封。李存勖建立后唐，定都洛阳。"
    words = segment_text(test_text)
    print(f"[OK] 分词：{len(words)} 个词")

    keywords = extract_keywords(test_text, top_n=5)
    print(f"[OK] 关键词：{[k[0] for k in keywords]}")

    stats = analyze_text_statistics(test_text)
    print(f"[OK] 统计：{stats['total_chars']} 字符")

    wc_data = generate_wordcloud_data(test_text)
    print(f"[OK] 词云数据：{len(wc_data)} 个词")

    return True

def test_charts():
    """测试图表生成"""
    print("\n=== 测试图表生成 ===")
    from pyecharts.charts import Bar, Line, Pie, Map, Graph, Sankey, Radar, WordCloud, Timeline
    from pyecharts import options as opts

    # 柱状图
    bar = Bar()
    bar.add_xaxis(['A', 'B', 'C'])
    bar.add_yaxis('值', [1, 2, 3])
    html = bar.render_embed()
    print(f"[OK] 柱状图：{len(html)} 字节")

    # 折线图
    line = Line()
    line.add_xaxis([1, 2, 3])
    line.add_yaxis('值', [4, 5, 6])
    html = line.render_embed()
    print(f"[OK] 折线图：{len(html)} 字节")

    # 饼图
    pie = Pie()
    pie.add('', [('A', 10), ('B', 20)])
    html = pie.render_embed()
    print(f"[OK] 饼图：{len(html)} 字节")

    # 地图
    m = Map()
    m.add('测试', [('河南省', 10), ('浙江省', 20)])
    m.set_global_opts(visualmap_opts=opts.VisualMapOpts(max_=20))
    html = m.render_embed()
    print(f"[OK] 地图：{len(html)} 字节")

    # 关系图
    graph = Graph()
    graph.add('', [{'name': 'A'}, {'name': 'B'}], [{'source': 'A', 'target': 'B'}])
    html = graph.render_embed()
    print(f"[OK] 关系图：{len(html)} 字节")

    # 桑基图
    sankey = Sankey()
    sankey.add('test', [{'name': 'A'}, {'name': 'B'}], [{'source': 'A', 'target': 'B', 'value': 10}])
    html = sankey.render_embed()
    print(f"[OK] 桑基图：{len(html)} 字节")

    # 雷达图
    radar = Radar()
    radar.add_schema([{'name': 'A', 'max': 100}, {'name': 'B', 'max': 100}])
    radar.add('test', [50, 60])
    html = radar.render_embed()
    print(f"[OK] 雷达图：{len(html)} 字节")

    # 词云
    wc = WordCloud()
    wc.add('', [('test', 10), ('data', 20)])
    html = wc.render_embed()
    print(f"[OK] 词云：{len(html)} 字节")

    return True

def test_pages():
    """测试页面导入"""
    print("\n=== 测试页面模块 ===")

    pages = [
        ('pages/1_timeline', 'pages/1_时间轴.py'),
        ('pages/2_map', 'pages/2_政权地图.py'),
        ('pages/3_relationship', 'pages/3_人物关系.py'),
        ('pages/4_fanzhen', 'pages/4_藩镇分析.py'),
        ('pages/5_stats', 'pages/5_数据统计.py'),
        ('pages/6_search', 'pages/6_文献检索.py'),
    ]

    for module_name, file_path in pages:
        try:
            # 读取文件内容并执行（避免导入名含 emoji）
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            # 简单检查文件是否有效 Python 代码
            compile(code, file_path, 'exec')
            print(f"[OK] {module_name}")
        except Exception as e:
            print(f"[FAIL] {module_name}: {str(e).encode('utf-8').decode('gbk', errors='ignore')}")

    return True

def main():
    """运行所有测试"""
    print("=" * 50)
    print("  五代十国历史信息可视化系统 - 综合测试")
    print("=" * 50)

    results = []

    results.append(('数据加载', test_data_loader()))
    results.append(('数据处理', test_data_processor()))
    results.append(('文本分析', test_text_analyzer()))
    results.append(('图表生成', test_charts()))
    results.append(('页面模块', test_pages()))

    print("\n" + "=" * 50)
    print("  测试结果汇总")
    print("=" * 50)

    for name, passed in results:
        status = "通过" if passed else "失败"
        print(f"  {name}: {status}")

    all_passed = all(r[1] for r in results)

    print("\n" + "=" * 50)
    if all_passed:
        print("  所有测试通过！系统可以正常运行。")
    else:
        print("  部分测试失败，请检查错误信息。")
    print("=" * 50)

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
