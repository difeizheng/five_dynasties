"""
数据加载模块
负责读取 Excel、Markdown、TXT 等原始数据文件
"""

import pandas as pd
import sqlite3
import os
from pathlib import Path
import chardet
import streamlit as st

# 数据文件路径
DATA_DIR = Path(__file__).parent.parent  # 项目根目录
DATA_FILES_DIR = DATA_DIR / 'data'  # 数据文件在 data 文件夹中


def get_data_file_path(filename: str) -> Path:
    """获取数据文件路径"""
    return DATA_FILES_DIR / filename


@st.cache_data
def load_excel_data(filename: str, sheet_name: str = 0) -> pd.DataFrame:
    """加载 Excel 数据"""
    try:
        file_path = get_data_file_path(filename)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        # 清理列名
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        print(f"加载 Excel 失败 {filename}: {e}")
        return pd.DataFrame()


@st.cache_data
def load_all_sheets(filename: str) -> dict:
    """加载 Excel 所有 sheet"""
    try:
        file_path = get_data_file_path(filename)
        xls = pd.ExcelFile(file_path)
        result = {}
        for sheet in xls.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet)
            df.columns = df.columns.str.strip()
            result[sheet] = df
        return result
    except Exception as e:
        print(f"加载 Excel 所有 sheet 失败 {filename}: {e}")
        return {}


def detect_encoding(file_path: Path) -> str:
    """检测文件编码"""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))
    return result.get('encoding', 'utf-8')


@st.cache_data
def load_txt_data(filename: str) -> str:
    """加载 TXT 数据"""
    try:
        file_path = get_data_file_path(filename)
        encoding = detect_encoding(file_path)
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        print(f"加载 TXT 失败 {filename}: {e}")
        return ""


@st.cache_data
def load_wudai_characters() -> pd.DataFrame:
    """加载五代十国人物数据"""
    return load_excel_data('XiaoYuer_Wudai_Shiguo_Characters.xlsx')


@st.cache_data
def load_wudai_detailed_characters() -> dict:
    """加载五代十国详细人物数据（按时期）"""
    return load_all_sheets('XiaoYuer_Wudai_Detailed_Characters.xlsx')


@st.cache_data
def load_fanzhen_relationships() -> pd.DataFrame:
    """加载藩镇关系数据"""
    return load_excel_data('XiaoYuer_Wudai_Fanzhen_Relationships.xlsx')


@st.cache_data
def load_fanzhen_complete() -> dict:
    """加载完整藩镇分析数据"""
    return load_all_sheets('XiaoYuer_Wudai_Fanzhen_Complete_Analysis.xlsx')


@st.cache_data
def load_tang_fanzhen() -> dict:
    """加载唐朝藩镇数据"""
    return load_all_sheets('XiaoYuer_Tang_Fanzhen_Complete.xlsx')


@st.cache_data
def load_tang_emperors() -> dict:
    """加载唐朝皇帝数据"""
    return load_all_sheets('XiaoYuer_Tang_Emperors.xlsx')


@st.cache_data
def load_history_timeline() -> dict:
    """加载历史时间线数据"""
    return load_all_sheets('XiaoYuer_China_History_Timeline.xlsx')


@st.cache_data
def load_wudai_history_text() -> str:
    """加载五代十国全史文本"""
    return load_txt_data('五代十国全史.txt')


def init_database():
    """初始化 SQLite 数据库"""
    db_path = Path(__file__).parent.parent / 'database' / 'wudai.db'
    db_path.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # 创建政权表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS regimes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT,
            start_year INTEGER,
            end_year INTEGER,
            capital TEXT,
            modern_area TEXT,
            founder TEXT,
            description TEXT
        )
    ''')

    # 创建人物表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            regime TEXT,
            position TEXT,
            start_year TEXT,
            end_year TEXT,
            relation_prev TEXT,
            relation_next TEXT,
            events TEXT,
            death_reason TEXT
        )
    ''')

    # 创建藩镇表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fanzhen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            period TEXT,
            type TEXT,
            location TEXT,
            area TEXT,
            jiedushi TEXT,
            succession TEXT,
            key_events TEXT,
            end_result TEXT
        )
    ''')

    # 创建事件表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER,
            title TEXT,
            regime TEXT,
            description TEXT,
            type TEXT
        )
    ''')

    conn.commit()
    conn.close()

    return str(db_path)


def get_db_path() -> str:
    """获取数据库路径"""
    return str(Path(__file__).parent.parent / 'database' / 'wudai.db')


if __name__ == "__main__":
    # 测试数据加载
    print("测试数据加载...")

    # 测试加载人物数据
    chars = load_wudai_characters()
    print(f"人物数据：{len(chars)} 条")

    # 测试加载详细人物
    detailed = load_wudai_detailed_characters()
    print(f"详细人物：{len(detailed)} 个 sheet")

    # 测试加载藩镇
    fanzhen = load_fanzhen_relationships()
    print(f"藩镇关系：{len(fanzhen)} 条")

    # 测试加载文本
    text = load_wudai_history_text()
    print(f"全史文本：{len(text)} 字符")
