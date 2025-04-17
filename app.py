from flask import Flask, render_template, request, jsonify
import os
import sys
from text_preprocessor import TextPreprocessor
from text_rewriter import TextRewriter
from ai_detection_avoider import AIDetectionAvoider
import nltk

app = Flask(__name__)

# 创建必要的目录
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

# 初始化处理器
preprocessor = TextPreprocessor()
rewriter = TextRewriter()
avoider = AIDetectionAvoider()

@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    """处理文本"""
    # 获取请求数据
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': '请提供文本'}), 400
    
    text = data['text']
    
    # 获取处理参数
    rewrite_methods = data.get('rewrite_methods', ['synonym', 'restructure', 'word_order'])
    avoid_methods = data.get('avoid_methods', ['human_features', 'sentence_diversity', 'reduce_patterns', 'adjust_perplexity'])
    intensity = float(data.get('intensity', 0.5))
    
    # 处理文本
    try:
        # 预处理
        cleaned_text = preprocessor.clean_text(text)
        
        # 改写
        rewritten_text = rewriter.rewrite_text(cleaned_text, methods=rewrite_methods, intensity=intensity)
        
        # 规避AI检测
        final_text = avoider.avoid_ai_detection(rewritten_text, methods=avoid_methods, intensity=intensity)
        
        # 返回结果
        return jsonify({
            'original_text': text,
            'cleaned_text': cleaned_text,
            'rewritten_text': rewritten_text,
            'final_text': final_text
        })
    except Exception as e:
        return jsonify({'error': f'处理文本时出错: {str(e)}'}), 500

if __name__ == '__main__':
    # 设置 NLTK 数据路径为项目目录中的 nltk_data
    nltk_data_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
    nltk.data.path.append(nltk_data_path)

    # 启动 Flask 应用
    app.run(host='0.0.0.0', port=5000, debug=True)