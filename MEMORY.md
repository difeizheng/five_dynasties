# 五代十国历史信息可视化系统 - 项目记忆

## 项目概览

基于 Streamlit + Pyecharts 的五代十国历史信息可视化系统，提供时间轴、政权地图、人物关系、藩镇分析等多维度可视化功能。

**当前版本**: v1.4.0 | **更新时间**: 2026-03-20

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
