# 五代十国历史信息可视化系统 - 工作状态记录

**最后更新**: 2026-03-18

## 项目状态

✅ **所有页面已完成修复并正常运行**

**访问地址**: http://localhost:8502

---

## 项目结构

```
five_dynasties_viz/
├── app.py                          # 主应用入口
├── pages/
│   ├── 1_📅_时间轴.py              # 时间轴页面
│   ├── 2_🗺️_政权地图.py            # 政权地图页面
│   ├── 3_👥_人物关系.py            # 人物关系页面
│   ├── 4_🏰_藩镇分析.py            # 藩镇分析页面
│   ├── 5_📊_数据统计.py            # 数据统计页面
│   └── 6_📖_文献检索.py            # 文献检索页面
├── src/
│   ├── data_loader.py              # 数据加载模块
│   ├── data_processor.py           # 数据处理模块
│   └── text_analyzer.py            # 文本分析模块
└── WORK_STATE.md                   # 本文件
```

---

## 已修复的兼容性问题汇总

### 1. Streamlit API 问题
- **问题**: `st.pyecharts_chart()` 不存在
- **修复**: 使用 `html(chart.render_embed(), height=600, scrolling=False)` 替代

- **问题**: `st.html()` 不存在
- **修复**: 使用 `from streamlit.components.v1 import html`

- **问题**: 导入顺序导致 `set_page_config()` 报错
- **修复**: 确保 docstring 在导入语句之前

### 2. pyecharts API 兼容性问题

#### LineStyleOpts
- **问题**: `curveness` 参数不支持
- **修复**: 移除该参数
- **影响文件**:
  - `pages/3_👥_人物关系.py:234-237`
  - `pages/4_🏰_藩镇分析.py:131-135, 180-183`

#### Tree.add()
- **问题**: `leaves_label_opts` 参数不支持
- **修复**: 移除该参数
- **影响文件**: `pages/3_👥_人物关系.py:166-169`

#### Sankey.add()
- **问题**: `layout`, `focus_node`, `linestyle_opts` 参数不支持
- **修复**: 移除这些参数
- **影响文件**: `pages/4_🏰_藩镇分析.py:124-136`

#### Radar.add()
- **问题**: `indicator` 参数不支持
- **修复**: 手动设置 `radar.options['radar'] = {'indicator': [...]}`
- **影响文件**: `pages/5_📊_数据统计.py:169-211`

#### Map 组件
- **问题**: 省份名称格式不匹配
- **修复**: 更新 `PROVINCE_MAPPING` 使用不带"省"的格式
- **影响文件**: `pages/2_🗺️_政权地图.py:24-46`

#### Line 图表
- **问题**: 数据未对齐 x 轴年份
- **修复**: 动态计算所有年份并统一对齐
- **影响文件**: `pages/4_🏰_藩镇分析.py:229-261`

#### 数据统计
- **问题**: DataFrame 列数与数据不匹配
- **修复**: 根据实际类别自动构建 DataFrame
- **影响文件**: `pages/6_📖_文献检索.py:199-240`

---

## 运行命令

```bash
cd D:\project_room\workspace2024\mytest\five_dynasties\five_dynasties_viz
python -m streamlit run app.py --server.port 8502
```

---

## 环境信息

- **Python**: 3.12
- **Streamlit**: 1.32.0
- **pyecharts**: 需要兼容版本（移除了不支持的参数）
- **端口**: 8502 (8501 被占用)

---

## 页面功能清单

| 页面 | 功能 | 状态 |
|------|------|------|
| 主页 | 统计卡片、政权列表、基础图表 | ✅ |
| 时间轴 | 甘特图、五代/十国时间线、重大事件 | ✅ |
| 政权地图 | 疆域地图、都城分布、面积对比 | ✅ |
| 人物关系 | 关系网络图、世系树、人物列表 | ✅ |
| 藩镇分析 | 分布图、实力对比、演变流向、关系网络 | ✅ |
| 数据统计 | 饼图、柱状图、雷达图、词云、文本统计 | ✅ |
| 文献检索 | 全文搜索、词云、分类关键词、索引表 | ✅ |

---

## 注意事项

1. **网络依赖**: 地图组件需要从 `assets.pyecharts.org` 加载 geoJson 数据
2. **缓存**: 数据使用 `@st.cache_data` 装饰器缓存
3. **端口检查**: 运行前确认 8502 端口是否可用

---

## 待办事项（可选）

- [ ] 添加更多历史数据
- [ ] 优化地图渲染速度
- [ ] 添加导出功能
