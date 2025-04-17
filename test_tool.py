import sys
from text_preprocessor import TextPreprocessor
from text_rewriter import TextRewriter
from ai_detection_avoider import AIDetectionAvoider

def test_with_sample():
    """使用样本文本测试工具的有效性"""
    # 创建处理器实例
    preprocessor = TextPreprocessor()
    rewriter = TextRewriter()
    avoider = AIDetectionAvoider()
    
    # 样本论文文本
    sample_text = """
    人工智能技术在近年来取得了显著的发展，尤其是在自然语言处理领域。
    大型语言模型的出现使得机器能够生成高质量的文本内容，这为学术写作带来了新的挑战。
    一方面，AI可以帮助研究者提高写作效率；另一方面，过度依赖AI可能导致学术不端行为。
    本文探讨了AI生成内容的特点及其在学术领域的应用，并提出了相应的伦理规范和检测方法。
    首先，我们分析了当前主流大语言模型的工作原理和输出特征。
    其次，我们研究了AI生成文本的语言模式和统计特性。
    最后，我们提出了一种基于多维特征的AI内容检测方法，并通过实验验证了其有效性。
    实验结果表明，该方法能够有效区分人类创作和AI生成的学术文本，准确率达到95%以上。
    总而言之，随着AI技术的不断发展，学术界需要建立更完善的规范和技术手段来应对这一挑战。
    """
    
    print("原始文本:")
    print(sample_text)
    print("\n" + "="*50 + "\n")
    
    # 测试文本预处理
    cleaned_text = preprocessor.clean_text(sample_text)
    print("清洗后文本:")
    print(cleaned_text)
    print("\n" + "="*50 + "\n")
    
    # 测试改写算法
    rewritten_text = rewriter.rewrite_text(cleaned_text, methods=['synonym', 'restructure', 'word_order'], intensity=0.7)
    print("改写后文本:")
    print(rewritten_text)
    print("\n" + "="*50 + "\n")
    
    # 测试AI检测规避
    final_text = avoider.avoid_ai_detection(rewritten_text, methods=['human_features', 'sentence_diversity', 'reduce_patterns', 'adjust_perplexity'], intensity=0.7)
    print("规避AI检测后文本:")
    print(final_text)
    print("\n" + "="*50 + "\n")
    
    # 计算文本变化率
    def calculate_change_rate(original, modified):
        """计算文本变化率"""
        original_words = preprocessor.segment(original)
        modified_words = preprocessor.segment(modified)
        
        original_set = set(original_words)
        modified_set = set(modified_words)
        
        changed_words = len(original_set.symmetric_difference(modified_set))
        total_words = len(original_set.union(modified_set))
        
        return changed_words / total_words if total_words > 0 else 0
    
    # 计算各阶段的文本变化率
    rewrite_change_rate = calculate_change_rate(cleaned_text, rewritten_text)
    final_change_rate = calculate_change_rate(cleaned_text, final_text)
    
    print(f"改写阶段文本变化率: {rewrite_change_rate:.2%}")
    print(f"最终文本变化率: {final_change_rate:.2%}")
    
    # 评估结果
    print("\n评估结果:")
    if final_change_rate >= 0.5:
        print("✓ 文本变化显著，降重效果良好")
    else:
        print("✗ 文本变化不足，降重效果有限")
    
    # 检查AI特征
    ai_patterns = [
        r"首先.*其次.*最后",
        r"一方面.*另一方面",
        r"总而言之",
        r"总的来说"
    ]
    
    ai_pattern_count_original = sum(1 for pattern in ai_patterns if re.search(pattern, cleaned_text))
    ai_pattern_count_final = sum(1 for pattern in ai_patterns if re.search(pattern, final_text))
    
    print(f"原文AI特征模式数量: {ai_pattern_count_original}")
    print(f"处理后AI特征模式数量: {ai_pattern_count_final}")
    
    if ai_pattern_count_final < ai_pattern_count_original:
        print("✓ AI特征模式减少，规避AI检测效果良好")
    else:
        print("✗ AI特征模式未减少，规避AI检测效果有限")

if __name__ == "__main__":
    import re
    test_with_sample()
