import random
import re
import math
import jieba
import nltk
from text_preprocessor import TextPreprocessor
from text_rewriter import TextRewriter

class AIDetectionAvoider:
    """
    AI检测规避类，提供规避AI检测的功能
    """
    
    def __init__(self):
        """初始化AI检测规避器"""
        self.preprocessor = TextPreprocessor()
        self.rewriter = TextRewriter()
        self.load_human_writing_features()
        self.load_ai_patterns()
    
    def load_human_writing_features(self):
        """
        加载人类写作特征
        """
        # 口语化表达
        self.colloquial_expressions = [
            "说实话", "坦白讲", "老实说", "实际上", "说白了", "简单来说",
            "换句话说", "打个比方", "举个例子", "不得不说", "值得一提的是",
            "有意思的是", "令人惊讶的是", "不可思议的是", "说来也怪",
            "说来话长", "说起来容易做起来难", "说到这里", "说到底"
        ]
        
        # 习语和成语
        self.idioms = [
            "一目了然", "不言而喻", "深入浅出", "循序渐进", "举一反三",
            "触类旁通", "融会贯通", "学无止境", "集思广益", "博采众长",
            "推陈出新", "精益求精", "锲而不舍", "孜孜不倦", "日新月异",
            "与时俱进", "不断创新", "开拓进取", "百家争鸣", "百花齐放"
        ]
        
        # 转折连接词
        self.transition_words = [
            "然而", "不过", "但是", "尽管如此", "话虽如此", "相反",
            "与此相反", "另一方面", "从另一个角度看", "尽管", "虽然",
            "固然", "诚然", "的确", "确实", "无可否认", "不可否认",
            "可是", "只是", "不仅如此", "更重要的是", "此外", "除此之外",
            "不仅仅是", "更为关键的是", "值得注意的是", "需要强调的是"
        ]
        
        # 个人观点表达
        self.personal_opinions = [
            "我认为", "在我看来", "依我之见", "以我之见", "我个人认为",
            "我的观点是", "我的看法是", "据我所知", "就我所知", "我的理解是",
            "我的体会是", "我的经验是", "我的感受是", "我的判断是", "我的分析是"
        ]
        
        # 修辞手法
        self.rhetorical_devices = [
            "难道不是吗？", "这不正是...吗？", "谁能否认...呢？", "怎能不...呢？",
            "为什么不...呢？", "难道我们不应该...吗？", "试问...",
            "想一想...", "设想一下...", "假如...", "如果...", "倘若..."
        ]
    
    def load_ai_patterns(self):
        """
        加载AI生成文本的特征模式
        """
        # AI常用的模式化表达
        self.ai_patterns = [
            r"首先.*其次.*最后",
            r"一方面.*另一方面",
            r"不仅.*而且",
            r"因此.*所以",
            r"总的来说",
            r"总而言之",
            r"综上所述",
            r"值得注意的是",
            r"需要指出的是",
            r"有必要强调",
            r"毫无疑问",
            r"显而易见",
            r"不言而喻"
        ]
        
        # AI偏好使用的词汇
        self.ai_preferred_words = [
            "delve into", "plethora", "myriad", "plethora", "paradigm",
            "robust", "leverage", "synergy", "holistic", "innovative",
            "unprecedented", "revolutionary", "transformative", "cutting-edge",
            "state-of-the-art", "groundbreaking", "disruptive", "game-changing"
        ]
    
    def add_human_writing_features(self, text, intensity=0.5):
        """
        添加人类写作特征
        
        参数:
        text (str): 输入文本
        intensity (float): 添加强度，范围0-1
        
        返回:
        str: 处理后的文本
        """
        if not text:
            return ""
            
        # 分句
        sentences = self.preprocessor.split_sentences(text)
        
        # 处理每个句子
        new_sentences = []
        for i, sentence in enumerate(sentences):
            new_sentence = sentence
            
            # 根据强度决定是否添加人类写作特征
            if random.random() < intensity:
                # 随机选择一种人类写作特征添加
                feature_type = random.choice(['colloquial', 'idiom', 'transition', 'personal', 'rhetorical'])
                
                if feature_type == 'colloquial' and len(sentence) > 10:
                    # 添加口语化表达
                    expression = random.choice(self.colloquial_expressions)
                    if random.random() < 0.5:
                        new_sentence = expression + "，" + new_sentence
                    else:
                        new_sentence = new_sentence.rstrip("。！？") + "，" + expression + "。"
                
                elif feature_type == 'idiom' and len(sentence) > 15:
                    # 添加习语和成语
                    idiom = random.choice(self.idioms)
                    if "，" in new_sentence:
                        parts = new_sentence.split("，", 1)
                        new_sentence = parts[0] + "，" + idiom + "，" + parts[1]
                    else:
                        new_sentence = new_sentence.rstrip("。！？") + "，" + idiom + "。"
                
                elif feature_type == 'transition' and i > 0 and len(sentence) > 10:
                    # 添加转折连接词
                    transition = random.choice(self.transition_words)
                    new_sentence = transition + "，" + new_sentence
                
                elif feature_type == 'personal' and random.random() < 0.3:
                    # 添加个人观点表达（使用较低概率，避免过度使用）
                    opinion = random.choice(self.personal_opinions)
                    new_sentence = opinion + "，" + new_sentence
                
                elif feature_type == 'rhetorical' and len(sentence) > 15:
                    # 添加修辞手法
                    rhetorical = random.choice(self.rhetorical_devices)
                    if new_sentence.endswith("。"):
                        new_sentence = new_sentence[:-1] + rhetorical
                    else:
                        new_sentence = new_sentence + rhetorical
            
            new_sentences.append(new_sentence)
        
        # 合并句子
        return ''.join(new_sentences)
    
    def diversify_sentence_length(self, text, intensity=0.5):
        """
        增加句子长度的多样性
        
        参数:
        text (str): 输入文本
        intensity (float): 处理强度，范围0-1
        
        返回:
        str: 处理后的文本
        """
        if not text:
            return ""
            
        # 分句
        sentences = self.preprocessor.split_sentences(text)
        
        if len(sentences) <= 1:
            return text
            
        # 计算当前句子长度的标准差
        lengths = [len(s) for s in sentences]
        mean_length = sum(lengths) / len(lengths)
        variance = sum((l - mean_length) ** 2 for l in lengths) / len(lengths)
        std_dev = math.sqrt(variance)
        
        # 如果标准差已经足够大，不需要进一步处理
        if std_dev > 10:
            return text
            
        # 处理句子
        new_sentences = []
        for i, sentence in enumerate(sentences):
            if random.random() < intensity:
                # 根据句子在序列中的位置决定处理方式
                if i % 3 == 0 and len(sentence) < 30:
                    # 扩展短句
                    words = self.preprocessor.segment(sentence)
                    expanded_words = []
                    for word in words:
                        expanded_words.append(word)
                        # 随机添加修饰词
                        if len(word) > 1 and random.random() < 0.3:
                            if word in self.rewriter.synonym_dict:
                                expanded_words.append("或者说" + random.choice(self.rewriter.synonym_dict[word]))
                    new_sentence = ''.join(expanded_words)
                    new_sentences.append(new_sentence)
                elif i % 3 == 1 and len(sentence) > 20:
                    # 分割长句
                    mid = len(sentence) // 2
                    # 寻找合适的分割点
                    while mid < len(sentence) - 1 and sentence[mid] not in "，、；":
                        mid += 1
                    if sentence[mid] in "，、；":
                        first_part = sentence[:mid+1]
                        second_part = sentence[mid+1:]
                        if not second_part.endswith(("。", "！", "？")):
                            second_part += "。"
                        new_sentences.append(first_part)
                        new_sentences.append(second_part)
                    else:
                        new_sentences.append(sentence)
                else:
                    new_sentences.append(sentence)
            else:
                new_sentences.append(sentence)
        
        # 合并句子
        return ''.join(new_sentences)
    
    def reduce_ai_patterns(self, text):
        """
        减少AI生成文本的特征模式
        
        参数:
        text (str): 输入文本
        
        返回:
        str: 处理后的文本
        """
        if not text:
            return ""
            
        new_text = text
        
        # 替换AI常用的模式化表达
        for pattern in self.ai_patterns:
            if re.search(pattern, new_text):
                # 找到匹配的模式
                matches = re.finditer(pattern, new_text)
                for match in matches:
                    # 获取匹配的文本
                    matched_text = match.group(0)
                    # 使用改写器重写这部分文本
                    rewritten_text = self.rewriter.rewrite_text(matched_text, methods=['synonym', 'word_order'], intensity=0.8)
                    # 替换原文中的模式
                    new_text = new_text.replace(matched_text, rewritten_text)
        
        # 替换AI偏好使用的词汇
        for word in self.ai_preferred_words:
            if word in new_text.lower():
                # 使用同义词替换
                new_text = new_text.replace(word, self.rewriter.get_synonym(word))
        
        return new_text
    
    def adjust_perplexity(self, text, intensity=0.5):
        """
        调整文本的困惑度，使其更接近人类写作
        
        参数:
        text (str): 输入文本
        intensity (float): 处理强度，范围0-1
        
        返回:
        str: 处理后的文本
        """
        if not text:
            return ""
            
        # 分句
        sentences = self.preprocessor.split_sentences(text)
        
        # 处理每个句子
        new_sentences = []
        for sentence in sentences:
            if random.random() < intensity and len(sentence) > 15:
                # 增加文本的不可预测性
                words = self.preprocessor.segment(sentence)
                
                # 随机插入语气词或填充词
                filler_words = ["其实", "说实话", "确实", "的确", "当然", "无疑", "或许", "可能", "大概", "也许"]
                
                if len(words) > 5:
                    insert_pos = random.randint(1, len(words) - 1)
                    filler = random.choice(filler_words)
                    words.insert(insert_pos, filler)
                
                # 随机替换一些常用词为不太常用的同义词
                for i, word in enumerate(words):
                    if len(word) > 1 and random.random() < 0.2:
                        synonym = self.rewriter.get_synonym(word)
                        if synonym != word:
                            words[i] = synonym
                
                new_sentence = ''.join(words)
                new_sentences.append(new_sentence)
            else:
                new_sentences.append(sentence)
        
        # 合并句子
        return ''.join(new_sentences)
    
    def avoid_ai_detection(self, text, methods=None, intensity=0.5):
        """
        综合使用多种方法规避AI检测
        
        参数:
        text (str): 输入文本
        methods (list): 使用的规避方法列表，可选值：'human_features', 'sentence_diversity', 'reduce_patterns', 'adjust_perplexity'
        intensity (float): 处理强度，范围0-1
        
        返回:
        str: 处理后的文本
        """
        if not text:
            return ""
            
        if methods is None:
            methods = ['human_features', 'sentence_diversity', 'reduce_patterns', 'adjust_perplexity']
        
        new_text = text
        
        # 添加人类写作特征
        if 'human_features' in methods:
            new_text = self.add_human_writing_features(new_text, intensity)
        
        # 增加句子长度的多样性
        if 'sentence_diversity' in methods:
            new_text = self.diversify_sentence_length(new_text, intensity)
        
        # 减少AI生成文本的特征模式
        if 'reduce_patterns' in methods:
            new_text = self.reduce_ai_patterns(new_text)
        
        # 调整文本的困惑度
        if 'adjust_perplexity' in methods:
            new_text = self.adjust_perplexity(new_text, intensity)
        
        return new_text

# 示例用法
if __name__ == "__main__":
    # 创建AI检测规避器实例
    avoider = AIDetectionAvoider()
    
    # 示例文本
    sample_text = """
    首先，论文降重是指通过各种技术手段，降低论文与已有文献的相似度，提高论文的原创性。
    其次，常见的降重方法包括同义词替换、句式重构、语序调整等。
    最后，这些方法可以有效降低文本的重复率，同时保持原文的语义不变。
    总而言之，论文降重技术对于学术写作具有重要意义。
    """
    
    # 使用不同方法规避AI检测
    print("原文:")
    print(sample_text)
    
    print("\n添加人类写作特征:")
    human_features_text = avoider.avoid_ai_detection(sample_text, methods=['human_features'])
    print(human_features_text)
    
    print("\n增加句子长度多样性:")
    sentence_diversity_text = avoider.avoid_ai_detection(sample_text, methods=['sentence_diversity'])
    print(sentence_diversity_text)
    
    print("\n减少AI模式:")
    reduce_patterns_text = avoider.avoid_ai_detection(sample_text, methods=['reduce_patterns'])
    print(reduce_patterns_text)
    
    print("\n调整困惑度:")
    adjust_perplexity_text = avoider.avoid_ai_detection(sample_text, methods=['adjust_perplexity'])
    print(adjust_perplexity_text)
    
    print("\n综合规避:")
    combined_text = avoider.avoid_ai_detection(sample_text)
    print(combined_text)
