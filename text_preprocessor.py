import os  # 添加这行
import jieba
import jieba.posseg as pseg
import re
import nltk
from nltk.tokenize import sent_tokenize

# 下载NLTK必要的数据包
# 移除以下代码
# try:
#     nltk.data.find('tokenizers/punkt')
# except LookupError:
#     nltk.download('punkt')

# 添加以下代码
nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk_data'))

class TextPreprocessor:
    """
    文本预处理类，提供文本清洗、分词、词性标注和句子分割等功能
    """
    
    def __init__(self):
        """初始化文本预处理器"""
        # 加载自定义词典（如果有）
        # jieba.load_userdict("user_dict.txt")
        pass
    
    # 设置 NLTK 数据路径
    nltk_data_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
    nltk.data.path.append(nltk_data_path)

    # 修复正则表达式中的转义字符
    def clean_text(self, text):
        if not text:
            return ""
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9，。！？、；："'
                      r'"''（）【】《》\\s]', '', text)  # 修改为\\s
        return text
    
    def split_paragraphs(self, text):
        """
        将文本分割为段落
        
        参数:
        text (str): 输入文本
        
        返回:
        list: 段落列表
        """
        if not text:
            return []
            
        # 按照换行符分割段落
        paragraphs = re.split(r'\n+', text)
        
        # 过滤空段落
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        return paragraphs
    
    def split_sentences(self, text, language='chinese'):
        """
        将文本分割为句子
        
        参数:
        text (str): 输入文本
        language (str): 语言，'chinese'或'english'
        
        返回:
        list: 句子列表
        """
        if not text:
            return []
            
        if language == 'chinese':
            # 中文句子分割
            pattern = r'([^。！？\?!]+[。！？\?!])'
            sentences = re.findall(pattern, text)
            # 处理最后可能没有标点符号的句子
            if text and not text.endswith(('。', '！', '？', '?', '!')):
                last_part = text.split(sentences[-1])[-1] if sentences else text
                if last_part.strip():
                    sentences.append(last_part.strip())
        else:
            # 英文句子分割
            sentences = sent_tokenize(text)
        
        return sentences
    
    def segment(self, text):
        """
        对文本进行分词
        
        参数:
        text (str): 输入文本
        
        返回:
        list: 分词结果列表
        """
        if not text:
            return []
            
        # 使用jieba进行分词
        words = jieba.lcut(text)
        
        return words
    
    def pos_tagging(self, text):
        """
        对文本进行词性标注
        
        参数:
        text (str): 输入文本
        
        返回:
        list: 词性标注结果列表，每个元素为(词, 词性)的元组
        """
        if not text:
            return []
            
        # 使用jieba进行词性标注
        words_pos = pseg.cut(text)
        
        return list(words_pos)
    
    def process_text(self, text):
        """
        完整处理文本，包括清洗、分段、分句、分词和词性标注
        
        参数:
        text (str): 输入文本
        
        返回:
        dict: 处理结果字典，包含清洗后文本、段落列表、句子列表、分词结果和词性标注结果
        """
        if not text:
            return {
                'cleaned_text': '',
                'paragraphs': [],
                'sentences': [],
                'words': [],
                'pos_tags': []
            }
            
        # 清洗文本
        cleaned_text = self.clean_text(text)
        
        # 分段
        paragraphs = self.split_paragraphs(cleaned_text)
        
        # 分句
        sentences = self.split_sentences(cleaned_text)
        
        # 分词
        words = self.segment(cleaned_text)
        
        # 词性标注
        pos_tags = self.pos_tagging(cleaned_text)
        
        return {
            'cleaned_text': cleaned_text,
            'paragraphs': paragraphs,
            'sentences': sentences,
            'words': words,
            'pos_tags': pos_tags
        }

# 示例用法
if __name__ == "__main__":
    # 创建文本预处理器实例
    preprocessor = TextPreprocessor()
    
    # 示例文本
    sample_text = """
    论文降重是指通过各种技术手段，降低论文与已有文献的相似度，提高论文的原创性。
    常见的降重方法包括同义词替换、句式重构、语序调整等。
    这些方法可以有效降低文本的重复率，同时保持原文的语义不变。
    """
    
    # 处理文本
    result = preprocessor.process_text(sample_text)
    
    # 打印处理结果
    print("清洗后文本:")
    print(result['cleaned_text'])
    print("\n段落列表:")
    for i, para in enumerate(result['paragraphs']):
        print(f"段落{i+1}: {para}")
    print("\n句子列表:")
    for i, sent in enumerate(result['sentences']):
        print(f"句子{i+1}: {sent}")
    print("\n分词结果:")
    print(result['words'])
    print("\n词性标注结果:")
    for word, tag in result['pos_tags']:
        print(f"{word}/{tag}", end=" ")
