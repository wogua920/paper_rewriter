// 全局变量
let processingInProgress = false;

// DOM元素
document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const inputText = document.getElementById('input-text');
    const processBtn = document.getElementById('process-btn');
    const intensitySlider = document.getElementById('intensity-slider');
    const intensityValue = document.getElementById('intensity-value');
    const loadingOverlay = document.getElementById('loading-overlay');
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    const copyBtn = document.getElementById('copy-btn');
    const downloadBtn = document.getElementById('download-btn');
    
    // 输出文本区域
    const finalText = document.getElementById('final-text');
    const rewrittenText = document.getElementById('rewritten-text');
    const cleanedText = document.getElementById('cleaned-text');
    const originalText = document.getElementById('original-text');
    
    // 初始化强度滑块
    intensitySlider.addEventListener('input', function() {
        intensityValue.textContent = this.value;
    });
    
    // 标签页切换
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // 移除所有标签页的active类
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            // 添加当前标签页的active类
            this.classList.add('active');
            const tabId = this.getAttribute('data-tab');
            document.getElementById(`${tabId}-tab`).classList.add('active');
        });
    });
    
    // 处理按钮点击事件
    processBtn.addEventListener('click', function() {
        if (processingInProgress) return;
        
        const text = inputText.value.trim();
        if (!text) {
            alert('请输入需要处理的文本');
            return;
        }
        
        // 获取选中的改写方法
        const rewriteMethods = [];
        document.querySelectorAll('input[name="rewrite-method"]:checked').forEach(checkbox => {
            rewriteMethods.push(checkbox.value);
        });
        
        // 获取选中的AI检测规避方法
        const avoidMethods = [];
        document.querySelectorAll('input[name="avoid-method"]:checked').forEach(checkbox => {
            avoidMethods.push(checkbox.value);
        });
        
        // 获取处理强度
        const intensity = intensitySlider.value;
        
        // 显示加载动画
        loadingOverlay.classList.remove('hidden');
        processingInProgress = true;
        
        // 发送API请求
        fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                rewrite_methods: rewriteMethods,
                avoid_methods: avoidMethods,
                intensity: intensity
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('处理请求失败');
            }
            return response.json();
        })
        .then(data => {
            // 更新结果
            originalText.value = data.original_text;
            cleanedText.value = data.cleaned_text;
            rewrittenText.value = data.rewritten_text;
            finalText.value = data.final_text;
            
            // 切换到最终结果标签页
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            document.querySelector('.tab-btn[data-tab="final"]').classList.add('active');
            document.getElementById('final-tab').classList.add('active');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('处理文本时出错: ' + error.message);
        })
        .finally(() => {
            // 隐藏加载动画
            loadingOverlay.classList.add('hidden');
            processingInProgress = false;
        });
    });
    
    // 复制结果按钮
    copyBtn.addEventListener('click', function() {
        const activeTab = document.querySelector('.tab-pane.active textarea');
        if (activeTab && activeTab.value) {
            navigator.clipboard.writeText(activeTab.value)
                .then(() => {
                    alert('已复制到剪贴板');
                })
                .catch(err => {
                    console.error('复制失败:', err);
                    // 备用复制方法
                    activeTab.select();
                    document.execCommand('copy');
                    alert('已复制到剪贴板');
                });
        } else {
            alert('没有可复制的内容');
        }
    });
    
    // 下载结果按钮
    downloadBtn.addEventListener('click', function() {
        const activeTab = document.querySelector('.tab-pane.active textarea');
        if (activeTab && activeTab.value) {
            const blob = new Blob([activeTab.value], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = '论文降重结果.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } else {
            alert('没有可下载的内容');
        }
    });
});
