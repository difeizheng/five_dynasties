"""
文本分析模块
负责文本分词、关键词提取、词云生成
"""

import jieba
import re
from collections import Counter
from typing import List, Dict, Tuple
import streamlit as st

# 停用词表（简易版）
STOP_WORDS = set([
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
    '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
    '你', '会', '着', '没有', '看', '好', '自己', '这', '那',
    '之', '而', '其', '以', '为', '于', '从', '与', '及', '等',
    '者', '此', '所', '因', '由', '及', '或', '一个', '一些',
    '这个', '那个', '这样', '那样', '什么', '怎么', '如何',
    '我们', '你们', '他们', '她们', '它们', '咱们', '大家',
    '可以', '可能', '应该', '必须', '能够', '可是', '但是',
    '如果', '假如', '虽然', '尽管', '即使', '因为', '所以',
    '然后', '接着', '于是', '从而', '进而', '同时', '此外',
    '另外', '还有', '以及', '及其', '或是', '或是', '要么',
])

# 历史专有名词（保持完整）
HISTORICAL_TERMS = [
    '五代', '十国', '后梁', '后唐', '后晋', '后汉', '后周',
    '吴越', '南唐', '前蜀', '后蜀', '闽国', '南汉', '荆南',
    '北汉', '契丹', '北宋', '南宋', '唐朝', '隋朝', '汉朝',
    '朱温', '李存勖', '石敬瑭', '刘知远', '郭威', '柴荣',
    '钱镠', '李昪', '李煜', '王建', '孟知祥', '王审知',
    '马殷', '高季兴', '刘䶮', '刘崇',
    '节度使', '刺史', '知州', '知县', '尚书', '侍郎',
    '宰相', '丞相', '御史', '太尉', '大将军',
    '开封', '洛阳', '杭州', '南京', '成都', '福州', '广州',
    '长沙', '荆州', '太原', '长安',
    '藩镇', '藩王', '割据', '称帝', '即位', '禅让',
    '陈桥兵变', '安史之乱', '黄巢起义', '赤壁之战',
]


def add_historical_terms():
    """添加历史专有名词到 jieba"""
    for term in HISTORICAL_TERMS:
        jieba.add_word(term)


def preprocess_text(text: str) -> str:
    """预处理文本"""
    # 移除特殊字符
    text = re.sub(r'[#$%@*&+=~]', '', text)
    # 统一标点
    text = re.sub(r'[…]{2,}', '……', text)
    # 移除多余空格
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def segment_text(text: str, use_stopwords: bool = True) -> List[str]:
    """中文分词"""
    add_historical_terms()

    text = preprocess_text(text)
    words = jieba.lcut(text)

    if use_stopwords:
        words = [w for w in words if w.strip() and w not in STOP_WORDS]

    return words


def extract_keywords(text: str, top_n: int = 20) -> List[Tuple[str, int]]:
    """提取关键词"""
    words = segment_text(text, use_stopwords=True)

    # 过滤单字（除非是专有名词）
    words = [w for w in words if len(w) > 1 or w in HISTORICAL_TERMS]

    # 统计词频
    counter = Counter(words)

    return counter.most_common(top_n)


def extract_keywords_by_category(text: str) -> Dict[str, List[Tuple[str, int]]]:
    """按类别提取关键词"""
    words = segment_text(text, use_stopwords=True)

    # 分类
    categories = {
        '人名': [],
        '地名': [],
        '政权': [],
        '官职': [],
        '事件': [],
        '其他': [],
    }

    # 简单分类规则
    for word in words:
        if word in ['朱温', '李存勖', '石敬瑭', '刘知远', '郭威', '柴荣',
                    '钱镠', '李昪', '李煜', '王建', '孟知祥', '王审知',
                    '马殷', '高季兴', '刘䶮', '刘崇', '赵匡胤']:
            categories['人名'].append(word)
        elif word in ['开封', '洛阳', '杭州', '南京', '成都', '福州', '广州',
                      '长沙', '荆州', '太原', '长安', '浙江', '江苏', '河南']:
            categories['地名'].append(word)
        elif word in ['后梁', '后唐', '后晋', '后汉', '后周',
                      '吴越', '南唐', '前蜀', '后蜀', '闽国', '南汉',
                      '荆南', '北汉', '唐朝', '北宋', '契丹']:
            categories['政权'].append(word)
        elif word in ['节度使', '刺史', '知州', '知县', '尚书', '侍郎',
                      '宰相', '丞相', '御史', '太尉', '大将军']:
            categories['官职'].append(word)
        elif word in ['陈桥兵变', '安史之乱', '黄巢起义', '赤壁之战']:
            categories['事件'].append(word)
        else:
            if len(word) > 1:
                categories['其他'].append(word)

    # 统计每类词频
    result = {}
    for cat, words in categories.items():
        counter = Counter(words)
        result[cat] = counter.most_common(15)

    return result


def generate_wordcloud_data(text: str, max_words: int = 100) -> List[Dict]:
    """生成词云数据"""
    keywords = extract_keywords(text, max_words)

    # 归一化词频用于词云大小
    if keywords:
        max_freq = keywords[0][1]
        min_freq = keywords[-1][1] if len(keywords) > 1 else 1

        wordcloud_data = []
        for word, freq in keywords:
            size = 1 + (freq - min_freq) / (max_freq - min_freq) * 2 if max_freq > min_freq else 1
            wordcloud_data.append({
                'name': word,
                'value': freq,
                'size': round(size, 2)
            })

        return wordcloud_data

    return []


def search_text(text: str, query: str, context_size: int = 50) -> List[Dict]:
    """搜索文本"""
    results = []

    # 简单关键词搜索
    query_lower = query.lower()
    text_lower = text.lower()

    start = 0
    while True:
        pos = text_lower.find(query_lower, start)
        if pos == -1:
            break

        # 获取上下文
        context_start = max(0, pos - context_size)
        context_end = min(len(text), pos + len(query) + context_size)

        context = text[context_start:context_end]

        # 查找所在章节（简单规则：查找前面的 # 标题）
        chapter = ""
        chapter_pos = text.rfind('#', 0, pos)
        if chapter_pos != -1:
            chapter_end = text.find('\n', chapter_pos)
            if chapter_end != -1:
                chapter = text[chapter_pos:chapter_end].strip('#').strip()

        results.append({
            'position': pos,
            'context': context,
            'chapter': chapter,
        })

        start = pos + 1

        # 限制结果数量
        if len(results) >= 50:
            break

    return results


def analyze_text_statistics(text: str) -> Dict:
    """分析文本统计信息"""
    chars = len(text)
    words = segment_text(text, use_stopwords=False)
    unique_words = len(set(words))

    # 句子数（按句号、问号、感叹号计算）
    sentences = len(re.findall(r'[.!?!.!.!]', text))

    # 段落数
    paragraphs = len([p for p in text.split('\n') if p.strip()])

    # 平均句长
    avg_sentence_len = chars / sentences if sentences > 0 else 0

    # 平均词频
    word_counts = Counter(words)
    avg_word_freq = sum(word_counts.values()) / len(word_counts) if word_counts else 0

    return {
        'total_chars': chars,
        'total_words': len(words),
        'unique_words': unique_words,
        'sentences': sentences,
        'paragraphs': paragraphs,
        'avg_sentence_len': round(avg_sentence_len, 1),
        'avg_word_freq': round(avg_word_freq, 1),
    }


def get_text_summary(text: str, max_length: int = 500) -> str:
    """获取文本摘要（简单版：取前 N 字）"""
    # 找到合适的截断点（段落结束）
    if len(text) <= max_length:
        return text

    # 尝试在段落结束处截断
    truncated = text[:max_length]
    last_newline = truncated.rfind('\n')

    if last_newline > max_length * 0.5:
        return truncated[:last_newline]

    return truncated + '......'


if __name__ == "__main__":
    # 测试文本分析
    test_text = """
    五代十国时期，朱温建立后梁，定都开封。
    李存勖建立后唐，定都洛阳。
    钱镠建立吴越国，定都杭州。
    """

    print("测试文本分析...")

    # 测试分词
    words = segment_text(test_text)
    print(f"分词结果：{words}")

    # 测试关键词
    keywords = extract_keywords(test_text, top_n=5)
    print(f"关键词：{keywords}")

    # 测试统计
    stats = analyze_text_statistics(test_text)
    print(f"统计：{stats}")
