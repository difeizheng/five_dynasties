# 五代十国历史信息可视化系统 - 项目记忆

## 项目概览

基于 Streamlit + Pyecharts 的五代十国历史信息可视化系统，提供时间轴、政权地图、人物关系、藩镇分析等多维度可视化功能。

**当前版本**: v1.4.0 | **更新时间**: 2026-03-20 | **Git 标签**: v1.4.0

## 已完成功能

### P0 核心优化 ✅
- **统一配置管理**: `src/config.py` 集中管理政权、颜色、地理、人物、事件配置
- **数据驱动改造**: 从 Excel 读取人物、藩镇、事件数据
- **错误处理优化**: `src/streamlit_utils.py` 提供统一错误处理组件和装饰器

### P1 功能增强 ✅
- **人物详情页**: 点击人物节点显示详细信息（庙号、谥号、生平事迹）
- **时间轴交互优化**: 添加时间范围、政权类型、事件类型筛选器
- **地图下钻功能**: 省份选择器查看历史沿革（涉及政权、都城、重大事件）
- **藩镇编年史**: 按时间线展示藩镇兴衰、节度使更迭

### P2 进阶功能 ✅
- **对比分析工具**: `pages/7_🔍_对比分析.py` 支持政权、人物、藩镇多维度对比 + 数据导出
- **导出功能**: `src/streamlit_utils.py` 提供 CSV/Excel/HTML 导出工具函数

## 核心文件结构

```
five_dynasties/
├── app.py                          # 主页
├── pages/
│   ├── 1_📅_时间轴.py              # 时间轴页面
│   ├── 2_🗺️_政权地图.py            # 政权地图页面
│   ├── 3_👥_人物关系.py            # 人物关系页面
│   ├── 4_🏰_藩镇分析.py            # 藩镇分析页面
│   ├── 5_📊_数据统计.py            # 数据统计页面
│   ├── 6_📖_文献检索.py            # 文献检索页面
│   └── 7_🔍_对比分析.py            # 对比分析页面（新增）
├── src/
│   ├── config.py                   # 统一配置管理
│   ├── data_loader.py              # 数据加载
│   ├── data_processor.py           # 数据处理
│   └── streamlit_utils.py          # Streamlit 工具函数
├── TODO.md                         # 开发任务清单
└── MEMORY.md                       # 项目记忆（本文件）
```

## 配置说明

### 政权配置 (`src/config.py`)
- `WUDAI_REGIMES`: 五代政权（后梁、后唐、后晋、后汉、后周）
- `SHIGUO_REGIMES`: 十国政权（吴越、南唐、前后蜀、闽国、南汉、楚、荆南、北汉）
- `REGIME_COLORS`: 政权颜色映射
- `WUDAI_SUCCESSION` / `SHIGUO_SUCCESSION`: 帝王世系数据
- `FANZHEN_CHRONICLES`: 藩镇编年史数据

### 地理配置
- `PROVINCE_MAPPING`: 古今省份名称映射
- `REGIME_TO_PROVINCE`: 政权与现代省份对照
- `CAPITAL_COORDS`: 都城坐标

## 开发规范

1. **配置集中**: 所有硬编码配置应放入 `src/config.py`
2. **错误处理**: 数据加载使用 `safe_load_data()` 装饰器
3. **UI 组件**: 使用 `src/streamlit_utils.py` 中的统一组件
4. **导出功能**: 使用 `export_dataframe_to_csv()` 等工具函数
5. **地图渲染**: 使用 `src/streamlit_utils.py` 中的 `build_choropleth_map_html` 和 `build_simple_highlight_map_html` 公共组件
6. **数据验证**: 使用 `src/data_loader.py` 中的验证函数确保数据质量

## 公共组件 (`src/streamlit_utils.py`)

### 地图渲染组件
- `build_choropleth_map_html()`: 构建 choropleth 地图（多区域不同颜色）
- `build_simple_highlight_map_html()`: 构建简单高亮地图（二分颜色）

### 错误处理组件
- `render_error_message()`: 渲染错误信息
- `render_warning_message()`: 渲染警告信息
- `render_success_message()`: 渲染成功信息
- `render_info_message()`: 渲染提示信息

### 数据加载组件
- `safe_load_data()`: 安全加载数据
- `render_empty_state()`: 渲染空状态

### 导出功能组件
- `export_dataframe_to_csv()`: 导出 CSV
- `export_to_excel()`: 导出 Excel
- `export_chart_as_html()`: 导出 HTML 图表

## 数据验证 (`src/data_loader.py`)

### 验证函数
- `validate_dataframe_schema()`: 验证 DataFrame 列结构
- `validate_year_column()`: 验证年份列范围
- `validate_regime_data()`: 验证政权数据
- `validate_character_data()`: 验证人物数据
- `validate_fanzhen_data()`: 验证藩镇数据

### 验证结果类
- `DataValidationResult`: 封装验证结果（错误、警告）

## 运行方式

```bash
# 启动开发服务器
streamlit run app.py --server.port=8502
```

## 技术栈
- Streamlit (Web 框架)
- Pyecharts (可视化)
- Pandas (数据处理)
- Jieba (文本分析)

## 待办任务 (P3 可选功能)
- [ ] 任务 12: 用户收藏系统
- [ ] 任务 13: 历史模拟器
- [ ] 任务 14: API 接口
- [ ] 任务 15: 数据可视化大屏

## 版本历史
| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.6.0 | 2026-03-23 | 技术债务处理 + 数据可视化大屏 |
| v1.5.0 | 2026-03-23 | 技术债务处理：抽取公共地图渲染组件、添加数据验证机制 |
| v1.4.0 | 2026-03-20 | 完成 P0-P2 全部任务，新增对比分析页面和导出功能 |
| v1.3.0 | 2026-03-20 | 完成 P1 任务（地图下钻、藩镇编年史） |
| v1.2.0 | 2026-03-20 | 完成 P0 任务（配置管理、数据驱动、错误处理） |
| v1.1.0 | 2026-03-20 | 创建任务清单，基础功能完成 |
