# 五代十国历史可视化应用 - 项目记忆

## 项目结构

```
five_dynasties/
├── app.py                      # Streamlit 主应用
├── requirements.txt            # Python 依赖
├── pages/
│   ├── 1_📅_时间轴.py          # 历史时间线页面（甘特图、政权更迭）
│   ├── 2_🗺️_政权地图.py        # 政权疆域地图页面
│   ├── 3_👥_人物关系.py        # 人物关系网络页面
│   ├── 4_🏰_藩镇分析.py        # 藩镇演变分析页面
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
- 最新标签：v1.1.0

## 已实现的功能

### 时间轴（pages/1_📅_时间轴.py）

1. **政权更迭甘特图**：展示各政权存续时间
   - 使用 JsCode 自定义 tooltip formatter
   - 显示起始年份、结束年份、存续年数
   - 五代和十国分开展示

2. **政权时间线对比**：折线图展示同时期政权数量变化

3. **重大历史事件**：按时间顺序列出改朝换代关键节点

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

### 藩镇分析（pages/4_🏰_藩镇分析.py）

1. **藩镇分布图**：使用内嵌 GeoJSON + visualMap 方案
   - 展示唐末主要藩镇的地理位置
   - 不同颜色代表不同藩镇
   - tooltip 显示藩镇名称和所属省份

2. **藩镇实力对比**：柱状图对比各藩镇综合实力

3. **藩镇演变流向图**：桑基图展示藩镇随时间演变的归属变化

4. **藩镇关系网络**：力导向图展示藩镇之间的联盟、敌对关系

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

# 藩镇颜色配置
FANZHEN_COLORS = {
    "宣武": "#e74c3c", "河东": "#3498db", "凤翔": "#9b59b6",
    "成德": "#e67e22", "魏博": "#2ecc71", "卢龙": "#1abc9c",
    # ... 完整配置见 pages/4_🏰_藩镇分析.py
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

### 问题 4：甘特图 tooltip 显示异常
**原因**：堆叠条形图使用默认 tooltip 只显示数值，不显示年份范围

**解决方案**：使用 JsCode 自定义 formatter，在数据项中添加 start/end/duration 字段
```python
from pyecharts.commons.utils import JsCode

# 数据项包含完整信息
data_items.append({
    'value': v,
    'start': row['start'],
    'end': row['end'],
    'duration': row['duration']
})

# 自定义 tooltip formatter
tooltip_formatter = """
    function(params) {
        return '<b>' + params.seriesName + '</b><br/>' +
               '起始：' + params.data.start + '年<br/>' +
               '结束：' + params.data.end + '年<br/>' +
               '存续：' + params.data.duration + '年';
    }
"""
```

## 数据文件

- `china_full.geojson`：中国地图 GeoJSON 数据（35 个省级行政区）
- `data/` 目录下包含多个 Excel 数据文件

## 依赖

```
streamlit
pyecharts
pandas
jieba
requests
```

## 新增页面（v1.10.3+）

### Webhook 测试工具（pages/9_🔗_Webhook 测试.py）

**功能**：测试 webhook URL 的可用性和响应性能

**主要特性**：
- 支持 GET/POST/PUT/DELETE 四种 HTTP 方法
- 测量响应时间（毫秒级别）
- 显示响应状态码、headers 和 body
- 内置 httpbin 测试预设
- 可调节超时时间（1-60 秒）

**POST 请求默认 payload**：
```json
{
    "test": true,
    "timestamp": "2024-01-01 12:00:00",
    "message": "Webhook 测试消息"
}
```

**测试预设 URL**：
- `http://localhost:8000/` - 本地 API 服务
- `http://localhost:8501/` - 本地 Streamlit
- `https://httpbin.org/post` - HTTP 测试服务
- `https://httpbin.org/status/200` - 状态码测试
