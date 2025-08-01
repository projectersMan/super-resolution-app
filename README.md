# 超分辨率图像处理应用

这是一个基于 Flask 和 Hugging Face 的图像超分辨率处理 Web 应用。

## 功能特性

- 🖼️ 图像上传和预览
- 🚀 AI 驱动的图像超分辨率处理
- 📱 响应式 Web 界面
- ⚡ 实时处理状态显示
- 💾 处理结果下载

## 技术栈

- **后端**: Flask (Python)
- **前端**: HTML5, CSS3, JavaScript
- **AI 模型**: Hugging Face Stable Diffusion x4 Upscaler
- **部署**: Render (生产环境)

## 本地运行

### 环境要求
- Python 3.8+
- pip
- Hugging Face API Token

### 安装步骤

1. 克隆项目
```bash
git clone <repository-url>
cd super-resolution-app
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，填入您的Hugging Face Token
# 获取Token: https://huggingface.co/settings/tokens
export HF_API_TOKEN=your_huggingface_token_here
```

4. 启动应用
```bash
python app.py
```

访问 http://localhost:5001

### 快速启动

使用提供的启动脚本:
```bash
./run.sh
```

## Render 部署

1. Fork 此仓库到您的 GitHub 账户
2. 在 Render 创建新的 Web Service
3. 连接您的 GitHub 仓库
4. 设置环境变量:
   - `HF_API_TOKEN`: 您的 Hugging Face API Token
5. 部署完成后即可访问

## 环境变量

### 必需配置

1. **复制环境变量模板**
   ```bash
   cp .env.example .env
   ```

2. **获取 Hugging Face API Token**
   - 访问：https://huggingface.co/settings/tokens
   - 创建新的 Token（选择 Read 权限）
   - 复制生成的 Token

3. **编辑 .env 文件**
   ```bash
   # 编辑 .env 文件，填入您的实际 Token
   HF_API_TOKEN=hf_your_actual_token_here
   PORT=5001
   FLASK_ENV=development
   ```

⚠️ **重要提醒**：
- 如果遇到 "HF_API_TOKEN环境变量未设置" 错误，请查看 [Token设置指南](SETUP_TOKEN.md)
- 请确保 .env 文件不要提交到 Git 仓库

### 环境变量说明

| 变量名 | 描述 | 必需 |
|--------|------|------|
| `HF_API_TOKEN` | Hugging Face API Token | 是 |
| `PORT` | 应用端口 (默认: 5001) | 否 |

## API 接口

- `GET /` - 主页面
- `POST /upload` - 图像上传和处理
- `GET /health` - 健康检查
- `GET /info` - 应用信息

## 测试

项目包含完整的测试套件，位于 `test/` 目录下：

### 运行所有测试
```bash
cd test
./run_tests.sh
```

### 单独运行测试
```bash
cd test
python3 test_api_connection.py    # 测试API连接
python3 test_hf_api.py           # 测试Hugging Face API
python3 test_real_esrgan.py      # 测试Real-ESRGAN模型
python3 test_stable_diffusion_upscaler.py  # 测试Stable Diffusion放大器
```

### 测试说明
- `test_api_connection.py`: 验证Hugging Face API连接和Token有效性
- `test_hf_api.py`: 测试超分辨率模型的可用性
- `test_real_esrgan.py`: 测试Real-ESRGAN模型的图像处理功能
- `test_stable_diffusion_upscaler.py`: 测试Stable Diffusion放大器

## 故障排除

### 端口占用问题
如果遇到端口占用错误，运行:
```bash
./run.sh
```
脚本会自动检测并释放被占用的端口。

### API Token 问题
1. 确保已设置 `HF_API_TOKEN` 环境变量
2. 验证 Token 有效性: https://huggingface.co/settings/tokens
3. 确保 Token 有足够的权限
4. 运行测试验证配置: `cd test && ./run_tests.sh`

### 网络连接问题
如果本地网络无法访问 Hugging Face API，建议部署到 Render 获得更稳定的网络环境。

## 许可证

MIT License