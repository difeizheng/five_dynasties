# 五代十国历史可视化应用 - 项目记忆

## 项目结构

```
five_dynasties/
├── app.py                      # Streamlit 主应用
├── requirements.txt            # Python 依赖
├── pages/
│   ├── 1_📅_时间线.py          # 历史时间线页面
│   ├── 2_🗺️_政权地图.py        # 政权疆域地图页面
│   ├── 3_👥_人物关系.py        # 人物关系网络页面
│   ├── 4_⚔️_战役分析.py        # 战役分析页面
│   ├── 5_📊_数据分析.py        # 数据分析页面
│   └── 6_📖_文档检索.py        # 文档检索页面
├── src/
│   ├── data_loader.py          # 数据加载模块
│   ├── data_processor.py       # 数据处理模块
│   ├── streamlit_utils.py      # Streamlit 工具函数
│   └── text_analyzer.py        # 文本分析模块
├── data/                       # 数据文件目录
├── china_full.geojson          # 中国地图 GeoJSON 数据
└── memory/                     # 记忆文件目录
```

## 启动命令

```bash
# 启动 Streamlit 服务（端口 8502）
streamlit run pages/2_🗺️_政权地图.py --server.port=8502

# 或启动主应用
streamlit run app.py --server.port=8502
```

## GitHub 仓库

- 地址：https://github.com/difeizheng/five_dynasties
- 标签：v1.0.0

## 已实现的功能

### 政权地图（pages/2_🗺️_政权地图.py）

1. **疆域地图**：使用 ECharts 展示各政权疆域范围
   - 内嵌 GeoJSON 数据解决 CORS 问题
   - visualMap + inRange.color 实现颜色映射
   - 支持按政权筛选

2. **都城分布图**：展示都城所在省份
   - 红色高亮都城所在地
   - 内嵌 GeoJSON 避免外部请求

3. **面积对比图**：柱状图对比各政权疆域面积

4. **现代省份对照表**：列出现代省份与古代政权的对应关系

### 关键配置

```python
# 省份名称映射（古 -> 今）
PROVINCE_MAPPING = {
    "河南": "河南省", "河北": "河北省", "山东": "山东省",
    "山西": "山西省", "陕西": "陕西省", "浙江": "浙江省",
    # ... 完整映射见 pages/2_🗺️_政权地图.py
}

# 政权颜色配置
REGIME_COLORS = {
    "后梁": "#e74c3c", "后唐": "#3498db", "后晋": "#9b59b6",
    "后汉": "#e67e22", "后周": "#2ecc71",
    # ... 完整配置见代码
}
```

## 已解决的地图问题

### 问题 1：地图颜色不显示
**原因**：itemStyle.areaColor 回调函数在 ECharts 地图类型中不可靠

**解决方案**：使用 visualMap + inRange.color
```javascript
visualMap: {
    type: 'piecewise',
    pieces: [{value: 1, label: '后周', color: '#2ecc71'}, ...],
    inRange: {
        color: ['#2ecc71', '#e74c3c', ...]  // 颜色数组
    }
}
```

### 问题 2：GeoJSON 加载失败 (CORS 403)
**原因**：Streamlit iframe 中 fetch() 请求外部域名被 CORS 限制

**解决方案**：内嵌 GeoJSON 数据
```python
with open('china_full.geojson', 'r', encoding='utf-8') as f:
    china_geojson = f.read()

# 在 HTML 模板中直接嵌入
var chinaGeojson = GEOJSON_PLACEHOLDER;
echarts.registerMap('china', chinaGeojson);
```

### 问题 3：CDN 证书过期
**原因**：assets.pyecharts.org 证书过期

**解决方案**：切换到 jsdelivr CDN
```html
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
```

## 数据文件

- `china_full.geojson`：中国地图 GeoJSON 数据（35 个省级行政区）
- `data/` 目录下包含多个 Excel 数据文件

## 测试文件

项目中包含多个测试 HTML 文件用于调试地图问题：
- `test_visualmap_inrange.html`：visualMap + inRange 成功方案
- `test_geojson_fetch.html`：GeoJSON 加载测试
- `test_other_sources.html`：多数据源测试

## 依赖

```
streamlit
pyecharts
pandas
jieba
requests
```
