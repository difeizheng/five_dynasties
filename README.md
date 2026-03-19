# 五代十国历史信息可视化系统

📜 基于 Streamlit 构建的五代十国历史信息可视化系统

## 功能特性

- 📅 **时间轴** - 政权更迭甘特图 + 历史大事记
- 🗺️ **政权地图** - 疆域范围可视化 + 现代省份对照
- 👥 **人物关系** - 帝王世系图 + 人物关系网络
- 🏰 **藩镇分析** - 藩镇演变桑基图 + 势力关系图
- 📊 **数据统计** - 多维度数据图表看板
- 📖 **文献检索** - 全文搜索 + 关键词词云

## 快速开始

### 环境要求

- Python 3.12+
- Windows / macOS / Linux

### 安装依赖

```bash
cd five_dynasties_viz
pip install -r requirements.txt
```

### 运行系统

```bash
streamlit run app.py
```

系统将在浏览器中自动打开，默认地址：http://localhost:8501

### 注意事项

- 如果图表无法显示，请确保安装了 `pyecharts>=1.9.1`
- 文本检索功能需要加载大文件，首次运行可能较慢
- 使用 `streamlit run app.py --server.port 8502` 可更改端口号

## 项目结构

```
five_dynasties_viz/
├── app.py                   # 主应用入口
├── src/
│   ├── data_loader.py       # 数据加载模块
│   ├── data_processor.py    # 数据处理模块
│   └── text_analyzer.py     # 文本分析模块
├── pages/                   # 多页面应用
│   ├── 1_📅_时间轴.py
│   ├── 2_🗺️_政权地图.py
│   ├── 3_👥_人物关系.py
│   ├── 4_🏰_藩镇分析.py
│   ├── 5_📊_数据统计.py
│   └── 6_📖_文献检索.py
├── data/                    # 原始数据文件（符号链接）
├── database/                # SQLite 数据库
├── assets/                  # 静态资源
└── requirements.txt         # 依赖列表
```

## 数据来源

- 五代十国人物数据
- 唐朝藩镇数据
- 历史时间线数据
- 五代十国全史文本
- 行政区划对照资料

## 技术栈

| 模块 | 技术 |
|------|------|
| 框架 | Streamlit |
| 可视化 | Pyecharts + Plotly |
| 数据处理 | Pandas |
| 文本分析 | Jieba |
| 数据库 | SQLite |

## 部署

### 本地部署

```bash
streamlit run app.py --server.port 8501
```

### Docker 部署

```bash
docker build -t five-dynasties-viz .
docker run -p 8501:8501 five-dynasties-viz
```

### Streamlit Cloud

将项目推送到 GitHub 后，可在 [share.streamlit.io](https://share.streamlit.io) 免费部署

## 开发说明

### 添加新页面

在 `pages/` 目录下创建新的 `.py` 文件，命名格式：`序号_图标_页面名称.py`

```python
import streamlit as st

st.set_page_config(page_title="页面标题", page_icon="🔖")
st.title("页面标题")

# 页面内容
```

### 数据处理

所有数据处理逻辑在 `src/` 模块中实现，通过 `@st.cache_data` 缓存提高性能

## License

MIT License

## 致谢

本系统使用小鱼儿提供的历史数据资料构建

---

**版本**: v1.0
**创建时间**: 2026-03-18
