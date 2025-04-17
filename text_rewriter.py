import jieba
import random
import re
from text_preprocessor import TextPreprocessor

class TextRewriter:
    """
    文本改写类，提供同义词替换、句式重构、语序调整等功能
    """
    
    def __init__(self):
        """初始化文本改写器"""
        self.preprocessor = TextPreprocessor()
        self.load_synonym_dict()
        self.load_sentence_patterns()
    
    def load_synonym_dict(self):
        """
        加载同义词词典
        
        这里使用简化版的同义词词典，实际应用中可以使用更完整的词典
        """
        self.synonym_dict = {
            # 名词
            "论文": ["文章", "著作", "学术作品", "研究报告", "学术论文"],
            "研究": ["探究", "调查", "考察", "分析", "探索"],
            "方法": ["方式", "途径", "手段", "措施", "策略"],
            "结果": ["成果", "结论", "效果", "成效", "产物"],
            "分析": ["解析", "剖析", "研判", "评析", "解读"],
            "问题": ["议题", "课题", "难题", "疑难", "困境"],
            "数据": ["资料", "信息", "素材", "材料", "统计结果"],
            "特点": ["特征", "特性", "特质", "特色", "特别之处"],
            "影响": ["作用", "效应", "效果", "冲击", "感染力"],
            "意义": ["价值", "重要性", "作用", "功用", "效用"],
            
            # 动词
            "表明": ["显示", "证明", "说明", "阐明", "揭示"],
            "提高": ["增强", "增加", "提升", "加强", "促进"],
            "降低": ["减少", "减低", "削弱", "缩减", "减轻"],
            "分析": ["解析", "研究", "探讨", "考察", "剖析"],
            "发现": ["察觉", "觉察", "发觉", "查明", "找到"],
            "认为": ["以为", "觉得", "看作", "视为", "认定"],
            "表示": ["显示", "呈现", "展示", "体现", "反映"],
            "进行": ["开展", "实施", "执行", "展开", "推行"],
            "使用": ["采用", "运用", "应用", "利用", "使用"],
            "提出": ["提议", "建议", "倡导", "发起", "推荐"],
            
            # 形容词
            "重要": ["关键", "主要", "核心", "关键性", "至关重要"],
            "显著": ["明显", "突出", "卓著", "显著性", "明确"],
            "有效": ["高效", "有用", "实用", "有益", "有力"],
            "必要": ["必需", "必须", "不可或缺", "必备", "必不可少"],
            "可能": ["或许", "可能性", "潜在", "可能会", "或者会"],
            
            # 副词
            "非常": ["极其", "十分", "格外", "尤其", "特别"],
            "主要": ["主要地", "首要地", "重点地", "关键地", "核心地"],
            "明显": ["显著地", "明确地", "清晰地", "明白地", "可见地"],
            "基本": ["基本上", "大体上", "大致上", "根本上", "本质上"],
            "通常": ["一般", "常常", "往往", "经常", "普遍"],
        }
    
    def load_sentence_patterns(self):
        """
        加载句式重构模板
        
        这里定义了一些常用的句式转换模板，用于句式重构
        """
        self.sentence_patterns = {
            # 陈述句转换模板
            "陈述句": [
                "{主语}不仅{谓语}{宾语}，而且{谓语2}{宾语2}。",
                "就{主语}而言，{谓语}{宾语}是显而易见的。",
                "从{主语}的角度来看，{谓语}{宾语}具有重要意义。",
                "关于{主语}，{谓语}{宾语}的现象值得关注。",
                "{主语}之所以{谓语}{宾语}，是因为{原因}。",
                "尽管{主语}{谓语}{宾语}，但{转折}。",
                "与其说{主语}{谓语}{宾语}，不如说{主语}{谓语2}{宾语2}。",
                "{主语}通过{方式}{谓语}{宾语}，从而{结果}。",
                "在{条件}的情况下，{主语}{谓语}{宾语}。",
                "{主语}的{谓语}{宾语}表明了{结论}。"
            ],
            
            # 被动句转换模板
            "被动句": [
                "{宾语}被{主语}{谓语}，这表明{结论}。",
                "{宾语}受到{主语}的{谓语}，导致{结果}。",
                "由{主语}{谓语}的{宾语}显示出{特点}。",
                "{宾语}在{主语}的作用下{谓语}，呈现出{特征}。",
                "经过{主语}的{谓语}，{宾语}表现出{特性}。"
            ],
            
            # 复合句转换模板
            "复合句": [
                "如果{条件}，那么{主语}将{谓语}{宾语}。",
                "只有当{条件}时，{主语}才能{谓语}{宾语}。",
                "随着{变化}，{主语}{谓语}{宾语}的程度也在增加。",
                "由于{原因}，{主语}{谓语}{宾语}的现象越来越明显。",
                "尽管{让步}，{主语}仍然{谓语}{宾语}。"
            ]
        }
    
    def get_synonym(self, word, pos=None):
        """
        获取词语的同义词
        
        参数:
        word (str): 原词
        pos (str): 词性，可选
        
        返回:
        str: 同义词，如果没有找到则返回原词
        """
        if word in self.synonym_dict:
            synonyms = self.synonym_dict[word]
            if synonyms:
                return random.choice(synonyms)
        return word
    
    def synonym_replacement(self, text, replacement_rate=0.3):
        """
        使用同义词替换算法改写文本
        
        参数:
        text (str): 输入文本
        replacement_rate (float): 替换率，范围0-1
        
        返回:
        str: 改写后的文本
        """
        if not text:
            return ""
            
        # 使用jieba进行分词和词性标注
        words_pos = self.preprocessor.pos_tagging(text)
        
        # 替换同义词
        new_words = []
        for word, pos in words_pos:
            # 根据替换率决定是否替换该词
            if random.random() < replacement_rate and len(word) > 1:  # 只替换长度大于1的词
                new_word = self.get_synonym(word, pos)
                new_words.append(new_word)
            else:
                new_words.append(word)
        
        # 合并词语
        return ''.join(new_words)
    
    def extract_sentence_components(self, sentence):
        """
        提取句子的主要成分（主语、谓语、宾语等）
        
        参数:
        sentence (str): 输入句子
        
        返回:
        dict: 句子成分字典
        """
        # 这里使用简化的方法提取句子成分
        # 实际应用中可以使用更复杂的句法分析
        
        words_pos = self.preprocessor.pos_tagging(sentence)
        
        components = {
            "主语": "",
            "谓语": "",
            "宾语": "",
            "谓语2": "",
            "宾语2": "",
            "条件": "",
            "结果": "",
            "原因": "",
            "转折": "",
            "方式": "",
            "结论": "",
            "特点": "",
            "变化": "",
            "让步": ""
        }
        
        # 简单规则：假设第一个名词是主语，第一个动词是谓语，后面的名词是宾语
        for i, (word, pos) in enumerate(words_pos):
            if not components["主语"] and (pos.startswith('n') or pos == 'r'):
                components["主语"] = word
            elif not components["谓语"] and pos.startswith('v'):
                components["谓语"] = word
            elif not components["宾语"] and (pos.startswith('n') or pos == 'r') and components["谓语"]:
                components["宾语"] = word
            elif not components["谓语2"] and pos.startswith('v') and components["宾语"]:
                components["谓语2"] = word
            elif not components["宾语2"] and (pos.startswith('n') or pos == 'r') and components["谓语2"]:
                components["宾语2"] = word
        
        # 如果没有提取到某些成分，使用默认值
        if not components["谓语2"]:
            components["谓语2"] = components["谓语"]
        if not components["宾语2"]:
            components["宾语2"] = components["宾语"]
        
        # 填充其他成分
        components["条件"] = f"{components['主语']}{components['谓语']}"
        components["结果"] = f"产生了重要影响"
        components["原因"] = f"存在客观需求"
        components["转折"] = f"仍需进一步研究"
        components["方式"] = f"科学方法"
        components["结论"] = f"具有重要意义"
        components["特点"] = f"独特性质"
        components["变化"] = f"环境的变化"
        components["让步"] = f"面临诸多挑战"
        
        return components
    
    def sentence_restructuring(self, sentence):
        """
        使用句式重构算法改写句子
        
        参数:
        sentence (str): 输入句子
        
        返回:
        str: 改写后的句子
        """
        if not sentence or len(sentence) < 10:  # 忽略过短的句子
            return sentence
            
        # 提取句子成分
        components = self.extract_sentence_components(sentence)
        
        # 随机选择一种句式类型
        pattern_type = random.choice(list(self.sentence_patterns.keys()))
        
        # 随机选择该类型的一个模板
        pattern = random.choice(self.sentence_patterns[pattern_type])
        
        # 应用模板
        try:
            new_sentence = pattern.format(**components)
            return new_sentence
        except:
            # 如果格式化失败，返回原句
            return sentence
    
    def word_order_adjustment(self, sentence):
        """
        调整句子中的词序
        
        参数:
        sentence (str): 输入句子
        
        返回:
        str: 调整词序后的句子
        """
        if not sentence or len(sentence) < 10:  # 忽略过短的句子
            return sentence
            
        # 分词
        words = self.preprocessor.segment(sentence)
        
        # 找到句子中的短语并调整其位置
        if len(words) > 5:
            # 简单的调整方法：交换两个短语的位置
            mid = len(words) // 2
            
            # 确保不会在标点符号处分割
            while mid < len(words) and re.match(r'[，。！？、；：""''（）【】《》]', words[mid]):
                mid += 1
            
            if mid < len(words):
                # 交换前后两部分
                new_words = words[mid:] + words[:mid]
                
                # 确保句子以适当的标点符号结束
                if new_words[-1] not in ['。', '！', '？', '；', '…']:
                    # 找到原句中的结束标点
                    for i in range(len(words)-1, -1, -1):
                        if words[i] in ['。', '！', '？', '；', '…']:
                            new_words.append(words[i])
                            break
                
                return ''.join(new_words)
        
        return sentence
    
    def rewrite_text(self, text, methods=None, intensity=0.5):
        """
        综合使用多种方法改写文本
        
        参数:
        text (str): 输入文本
        methods (list): 使用的改写方法列表，可选值：'synonym', 'restructure', 'word_order'
        intensity (float): 改写强度，范围0-1
        
        返回:
        str: 改写后的文本
        """
        if not text:
            return ""
            
        if methods is None:
            methods = ['synonym', 'restructure', 'word_order']
        
        # 清洗文本
        cleaned_text = self.preprocessor.clean_text(text)
        
        # 分句
        sentences = self.preprocessor.split_sentences(cleaned_text)
        
        # 改写每个句子
        new_sentences = []
        for sentence in sentences:
            new_sentence = sentence
            
            # 根据改写强度决定是否改写该句
            if random.random() < intensity:
                # 同义词替换
                if 'synonym' in methods:
                    new_sentence = self.synonym_replacement(new_sentence, replacement_rate=intensity)
                
                # 句式重构
                if 'restructure' in methods and random.random() < intensity:
                    new_sentence = self.sentence_restructuring(new_sentence)
                
                # 词序调整
                if 'word_order' in methods and random.random() < intensity:
                    new_sentence = self.word_order_adjustment(new_sentence)
            
            new_sentences.append(new_sentence)
        
        # 合并句子
        return ''.join(new_sentences)

# 示例用法
if __name__ == "__main__":
    # 创建文本改写器实例
    rewriter = TextRewriter()
    
    # 示例文本
    sample_text = """
    论文降重是指通过各种技术手段，降低论文与已有文献的相似度，提高论文的原创性。
    常见的降重方法包括同义词替换、句式重构、语序调整等。
    这些方法可以有效降低文本的重复率，同时保持原文的语义不变。
    """
    
    # 使用不同方法改写文本
    print("原文:")
    print(sample_text)
    
    print("\n同义词替换:")
    synonym_text = rewriter.rewrite_text(sample_text, methods=['synonym'])
    print(synonym_text)
    
    print("\n句式重构:")
    restructure_text = rewriter.rewrite_text(sample_text, methods=['restructure'])
    print(restructure_text)
    
    print("\n词序调整:")
    word_order_text = rewriter.rewrite_text(sample_text, methods=['word_order'])
    print(word_order_text)
    
    print("\n综合改写:")
    combined_text = rewriter.rewrite_text(sample_text)
    print(combined_text)
