class SuperResolutionApp {
    constructor() {
        this.originalImage = document.getElementById('originalImage');
        this.resultImage = document.getElementById('resultImage');
        this.originalPlaceholder = document.getElementById('originalPlaceholder');
        this.resultPlaceholder = document.getElementById('resultPlaceholder');
        this.imageInput = document.getElementById('imageInput');
        this.upscaleBtn = document.getElementById('upscaleBtn');
        this.loading = document.getElementById('loading');
        this.message = document.getElementById('message');
        this.fileInfo = document.getElementById('fileInfo');
        this.originalSize = document.getElementById('originalSize');
        this.resultSize = document.getElementById('resultSize');
        
        this.currentFile = null;
        this.initEventListeners();
        this.checkHealth();
    }
    
    initEventListeners() {
        this.imageInput.addEventListener('change', (e) => this.handleImageUpload(e));
        this.upscaleBtn.addEventListener('click', () => this.handleUpscale());
    }
    
    handleImageUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        this.currentFile = file;
        
        // 验证文件类型
        if (!file.type.startsWith('image/')) {
            this.showMessage('请选择有效的图片文件 (JPG, PNG)', 'error');
            this.resetFileInput();
            return;
        }
        
        // 验证文件大小 (限制为5MB)
        if (file.size > 5 * 1024 * 1024) {
            this.showMessage('图片大小不能超过5MB', 'error');
            this.resetFileInput();
            return;
        }
        
        // 显示文件信息
        const fileSize = (file.size / 1024 / 1024).toFixed(2);
        this.fileInfo.textContent = `${file.name} (${fileSize} MB)`;
        
        const reader = new FileReader();
        reader.onload = (e) => {
            this.originalImage.src = e.target.result;
            this.originalImage.style.display = 'block';
            this.originalPlaceholder.style.display = 'none';
            this.upscaleBtn.disabled = false;
            this.resultImage.style.display = 'none';
            this.resultPlaceholder.style.display = 'flex';
            this.resultSize.textContent = '';
            this.clearMessage();
            
            // 显示原始图片尺寸
            const img = new Image();
            img.onload = () => {
                this.originalSize.textContent = `${img.width}×${img.height}`;
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
    
    async handleUpscale() {
        if (!this.currentFile) {
            this.showMessage('请先选择图片', 'error');
            return;
        }
        
        this.showLoading(true);
        this.upscaleBtn.disabled = true;
        this.upscaleBtn.querySelector('.btn-text').textContent = '⏳ 处理中...';
        
        try {
            const formData = new FormData();
            formData.append('image', this.currentFile);
            
            const response = await fetch('/upscale', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.resultImage.src = data.upscaled_image;
                this.resultImage.style.display = 'block';
                this.resultPlaceholder.style.display = 'none';
                
                // 显示处理时间和结果尺寸
                if (data.processing_time) {
                    this.showMessage(`✅ 超分处理完成！耗时 ${data.processing_time} 秒`, 'success');
                } else {
                    this.showMessage('✅ 超分处理完成！', 'success');
                }
                
                // 显示结果图片尺寸
                const img = new Image();
                img.onload = () => {
                    this.resultSize.textContent = `${img.width}×${img.height}`;
                };
                img.src = data.upscaled_image;
                
            } else {
                throw new Error(data.error || '处理失败');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showMessage(`❌ 处理失败: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
            this.upscaleBtn.disabled = false;
            this.upscaleBtn.querySelector('.btn-text').textContent = '✨ 开始超分';
        }
    }
    
    showLoading(show) {
        this.loading.style.display = show ? 'block' : 'none';
    }
    
    showMessage(text, type) {
        this.message.textContent = text;
        this.message.className = `message ${type}`;
        setTimeout(() => this.clearMessage(), 5000);
    }
    
    clearMessage() {
        this.message.textContent = '';
        this.message.className = 'message';
    }
    
    resetFileInput() {
        this.imageInput.value = '';
        this.fileInfo.textContent = '支持 JPG, PNG 格式 (最大5MB)';
        this.currentFile = null;
    }
    
    async checkHealth() {
        try {
            const response = await fetch('/health');
            const data = await response.json();
            if (data.status === 'healthy') {
                console.log('✅ Application is healthy');
            }
        } catch (error) {
            console.warn('⚠️ Health check failed:', error);
        }
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new SuperResolutionApp();
});

// 添加拖拽上传支持
document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.querySelector('.upload-btn');
    const fileInput = document.getElementById('imageInput');
    
    // 防止默认拖拽行为
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    // 高亮拖拽区域
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        uploadArea.style.borderColor = '#667eea';
        uploadArea.style.backgroundColor = 'rgba(102, 126, 234, 0.1)';
    }
    
    function unhighlight() {
        uploadArea.style.borderColor = '#ddd';
        uploadArea.style.backgroundColor = 'white';
    }
    
    // 处理文件拖拽
    uploadArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length) {
            // 创建一个新的FileList事件
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(files[0]);
            fileInput.files = dataTransfer.files;
            
            // 触发change事件
            const event = new Event('change', { bubbles: true });
            fileInput.dispatchEvent(event);
        }
    }
});

// 页面可见性API - 当页面重新获得焦点时检查健康状态
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        // 页面重新可见时检查健康状态
        if (typeof app !== 'undefined' && app.checkHealth) {
            app.checkHealth();
        }
    }
});