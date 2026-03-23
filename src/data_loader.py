"""
数据加载模块
负责读取 Excel、Markdown、TXT 等原始数据文件
包含错误处理和降级方案
"""

import pandas as pd
import sqlite3
import os
from pathlib import Path
import chardet
import streamlit as st
import logging
from typing import List

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据文件路径
DATA_DIR = Path(__file__).parent.parent  # 项目根目录
DATA_FILES_DIR = DATA_DIR / 'data'  # 数据文件在 data 文件夹中


# ============================================
# 错误处理工具函数
# ============================================

def check_data_file_exists(filename: str) -> tuple[bool, str]:
    """
    检查数据文件是否存在

    Args:
        filename: 文件名

    Returns:
        (是否存在，错误消息)
    """
    file_path = DATA_FILES_DIR / filename
    if not file_path.exists():
        error_msg = f"数据文件不存在：{filename}"
        logger.error(error_msg)
        return False, error_msg
    return True, ""


def handle_load_error(filename: str, error: Exception, fallback_value: any = None) -> any:
    """
    处理加载错误，返回降级值

    Args:
        filename: 文件名
        error: 异常对象
        fallback_value: 降级返回值

    Returns:
        降级值
    """
    error_msg = f"加载文件失败 {filename}: {str(error)}"
    logger.error(error_msg)
    return fallback_value


def get_data_file_path(filename: str) -> Path:
    """获取数据文件路径"""
    return DATA_FILES_DIR / filename


@st.cache_data
def load_excel_data(
    filename: str,
    sheet_name: str = 0,
    validate: bool = False,
    required_columns: List[str] = None,
    data_name: str = None
) -> pd.DataFrame:
    """加载 Excel 数据

    Args:
        filename: 文件名
        sheet_name: sheet 名称或索引
        validate: 是否进行数据验证
        required_columns: 必需的列名列表（验证时使用）
        data_name: 数据名称（验证时使用）

    Returns:
        加载的 DataFrame
    """
    try:
        exists, error_msg = check_data_file_exists(filename)
        if not exists:
            st.warning(f"⚠️ {error_msg}")
            return pd.DataFrame()

        file_path = get_data_file_path(filename)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        # 清理列名
        df.columns = df.columns.str.strip()

        # 数据验证
        if validate and required_columns:
            validation_result = validate_dataframe_schema(
                df, required_columns, data_name or filename
            )

            for error in validation_result.errors:
                st.error(f"❌ 数据验证错误：{error}")
            for warning in validation_result.warnings:
                st.warning(f"⚠️ 数据验证警告：{warning}")

            if not validation_result.is_valid:
                st.warning(f"数据验证未通过，请检查数据质量")

        return df
    except FileNotFoundError as e:
        st.error(f"❌ 文件未找到：{filename}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ 加载 Excel 失败 {filename}: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_all_sheets(filename: str) -> dict:
    """加载 Excel 所有 sheet"""
    try:
        exists, error_msg = check_data_file_exists(filename)
        if not exists:
            st.warning(f"⚠️ {error_msg}")
            return {}

        file_path = get_data_file_path(filename)
        xls = pd.ExcelFile(file_path)
        result = {}
        for sheet in xls.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet)
            df.columns = df.columns.str.strip()
            result[sheet] = df
        return result
    except FileNotFoundError as e:
        st.error(f"❌ 文件未找到：{filename}")
        return {}
    except Exception as e:
        st.error(f"❌ 加载 Excel 所有 sheet 失败 {filename}: {str(e)}")
        return {}


def detect_encoding(file_path: Path) -> str:
    """检测文件编码"""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))
    return result.get('encoding', 'utf-8')


# ============================================
# 数据验证模块
# ============================================

class DataValidationResult:
    """数据验证结果"""
    def __init__(self, is_valid: bool, errors: List[str] = None, warnings: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []

    def add_error(self, error: str):
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, warning: str):
        self.warnings.append(warning)

    def merge(self, other: 'DataValidationResult'):
        """合并另一个验证结果"""
        if not other.is_valid:
            self.is_valid = False
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        return self


def validate_dataframe_schema(
    df: pd.DataFrame,
    required_columns: List[str],
    data_name: str = "数据"
) -> DataValidationResult:
    """
    验证 DataFrame 的列结构

    Args:
        df: 要验证的 DataFrame
        required_columns: 必需的列名列表
        data_name: 数据名称

    Returns:
        验证结果
    """
    result = DataValidationResult(is_valid=True)

    if df.empty:
        result.add_warning(f"{data_name} 为空")
        return result

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        result.add_error(f"{data_name} 缺少列：{', '.join(missing_columns)}")

    # 检查空值
    for col in required_columns:
        if col in df.columns:
            null_count = df[col].isna().sum()
            if null_count > 0:
                result.add_warning(f"{data_name} 列 '{col}' 有 {null_count} 个空值")

    return result


def validate_year_column(
    df: pd.DataFrame,
    column_name: str,
    min_year: int = 600,
    max_year: int = 1000,
    data_name: str = "数据"
) -> DataValidationResult:
    """
    验证年份列是否在合理范围内

    Args:
        df: DataFrame
        column_name: 年份列名
        min_year: 最小允许年份
        max_year: 最大允许年份
        data_name: 数据名称

    Returns:
        验证结果
    """
    result = DataValidationResult(is_valid=True)

    if column_name not in df.columns:
        result.add_error(f"{data_name} 缺少年份列 '{column_name}'")
        return result

    invalid_years = df[
        ~df[column_name].between(min_year, max_year, na_option='keep')
    ][column_name]

    if len(invalid_years) > 0:
        result.add_warning(
            f"{data_name} 年份列 '{column_name}' 有 {len(invalid_years)} 个值超出范围 [{min_year}, {max_year}]"
        )

    return result


def validate_regime_data(df: pd.DataFrame) -> DataValidationResult:
    """
    验证政权数据的完整性

    Args:
        df: 政权数据 DataFrame

    Returns:
        验证结果
    """
    result = DataValidationResult(is_valid=True)

    # 验证必需列
    result.merge(validate_dataframe_schema(
        df,
        required_columns=['name', 'type', 'start', 'end', 'capital'],
        data_name="政权数据"
    ))

    if not result.is_valid:
        return result

    # 验证年份合理性
    for _, row in df.iterrows():
        if row['start'] >= row['end']:
            result.add_error(f"政权 '{row['name']}' 的起始年份 ({row['start']}) 不小于结束年份 ({row['end']})")

        if row['end'] - row['start'] > 200:
            result.add_warning(f"政权 '{row['name']}' 存续时间过长：{row['end'] - row['start']} 年")

    return result


def validate_character_data(df: pd.DataFrame) -> DataValidationResult:
    """
    验证人物数据的完整性

    Args:
        df: 人物数据 DataFrame

    Returns:
        验证结果
    """
    result = DataValidationResult(is_valid=True)

    result.merge(validate_dataframe_schema(
        df,
        required_columns=['name', 'regime'],
        data_name="人物数据"
    ))

    # 检查重复人物
    if 'name' in df.columns:
        duplicates = df[df.duplicated(subset=['name'], keep=False)]
        if len(duplicates) > 0:
            result.add_warning(f"发现 {len(duplicates)} 条重复人物记录")

    return result


def validate_fanzhen_data(df: pd.DataFrame) -> DataValidationResult:
    """
    验证藩镇数据的完整性

    Args:
        df: 藩镇数据 DataFrame

    Returns:
        验证结果
    """
    result = DataValidationResult(is_valid=True)

    result.merge(validate_dataframe_schema(
        df,
        required_columns=['name', 'province', 'power'],
        data_name="藩镇数据"
    ))

    if 'power' in df.columns:
        invalid_power = df[(df['power'] < 0) | (df['power'] > 100)]
        if len(invalid_power) > 0:
            result.add_warning(f"发现 {len(invalid_power)} 条藩镇实力值超出 [0, 100] 范围")

    return result


@st.cache_data
def load_txt_data(filename: str) -> str:
    """加载 TXT 数据"""
    try:
        exists, error_msg = check_data_file_exists(filename)
        if not exists:
            st.warning(f"⚠️ {error_msg}")
            return ""

        file_path = get_data_file_path(filename)
        encoding = detect_encoding(file_path)
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError as e:
        st.error(f"❌ 文件未找到：{filename}")
        return ""
    except Exception as e:
        st.error(f"❌ 加载 TXT 失败 {filename}: {str(e)}")
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
