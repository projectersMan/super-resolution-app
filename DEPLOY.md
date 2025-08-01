# AI图像超分辨率应用 - Render部署指南

## 📋 部署前检查清单

### ✅ 已完成的准备工作
- [x] Flask应用程序 (`app.py`)
- [x] 依赖文件 (`requirements.txt`)
- [x] Render配置 (`Procfile`)
- [x] Python版本配置 (`runtime.txt`)
- [x] 前端界面 (`templates/index.html`)
- [x] 静态资源 (`static/css/style.css`, `static/js/main.js`)
- [x] 环境变量示例 (`.env.example`)
- [x] 项目文档 (`README.md`, `prd.md`)
- [x] 测试脚本 (`test/` 目录)
- [x] 部署测试 (`deploy_test.py`)

## 🚀 Render平台部署步骤

### 1. 准备Hugging Face API Token

1. 访问 [Hugging Face](https://huggingface.co/)
2. 注册/登录账户
3. 进入 Settings → Access Tokens
4. 创建新的 Token (选择 "Read" 权限即可)
5. 复制生成的 Token

### 2. 在Render上创建Web Service

1. 登录 [Render](https://render.com/)
2. 点击 "New" → "Web Service"
3. 连接你的GitHub仓库
4. 选择包含此项目的仓库

### 3. 配置部署设置

#### 基本设置
- **Name**: `ai-image-upscaler` (或你喜欢的名称)
- **Environment**: `Python 3`
- **Region**: 选择离你最近的区域
- **Branch**: `main` (或你的主分支)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn -w 1 -b 0.0.0.0:$PORT app:app`

#### 环境变量配置
在 "Environment Variables" 部分添加:

| Key | Value | 说明 |
|-----|-------|------|
| `HF_API_TOKEN` | `你的Hugging Face Token` | **必需** - 用于调用AI模型 |
| `PORT` | `10000` | **可选** - Render会自动设置 |
| `FLASK_ENV` | `production` | **可选** - 生产环境标识 |

### 4. 高级配置 (可选)

#### 健康检查
- **Health Check Path**: `/health`
- **Health Check Timeout**: `30` 秒

#### 资源配置
- **Instance Type**: 选择合适的实例类型
  - 免费层: `Free` (512MB RAM)
  - 付费层: `Starter` (1GB RAM) 或更高

### 5. 部署验证

部署完成后，访问以下端点验证:

1. **健康检查**: `https://your-app.onrender.com/health`
   - 应返回: `{"status": "healthy", "hf_token_configured": true}`

2. **应用信息**: `https://your-app.onrender.com/info`
   - 应返回应用的基本信息

3. **主页面**: `https://your-app.onrender.com/`
   - 应显示图片上传界面

## 🔧 故障排除

### 常见问题

#### 1. 应用启动失败
**症状**: 部署失败或应用无法启动
**解决方案**:
- 检查 `requirements.txt` 中的依赖版本
- 确认 `Procfile` 配置正确
- 查看Render的部署日志

#### 2. HF_API_TOKEN 错误
**症状**: 图片处理失败，返回Token相关错误
**解决方案**:
- 确认在Render环境变量中正确设置了 `HF_API_TOKEN`
- 验证Token是否有效且有足够权限
- 检查Token是否已过期

#### 3. 图片处理超时
**症状**: 上传图片后长时间无响应
**解决方案**:
- 检查网络连接
- 尝试上传较小的图片
- 查看应用日志了解具体错误

#### 4. 静态文件加载失败
**症状**: 页面样式异常或JavaScript不工作
**解决方案**:
- 确认 `static/` 目录结构正确
- 检查文件路径是否正确
- 清除浏览器缓存

### 日志查看

在Render控制台中:
1. 进入你的Web Service
2. 点击 "Logs" 标签
3. 查看实时日志或历史日志

## 📊 性能优化建议

### 1. 实例配置
- 对于生产环境，建议使用至少 1GB RAM 的实例
- 考虑启用自动扩展功能

### 2. 缓存策略
- 静态文件会自动被CDN缓存
- 考虑实现结果缓存以提高响应速度

### 3. 监控设置
- 启用Render的监控功能
- 设置适当的健康检查
- 配置告警通知

## 🔒 安全注意事项

1. **API Token安全**
   - 永远不要在代码中硬编码Token
   - 定期轮换API Token
   - 使用最小权限原则

2. **文件上传安全**
   - 应用已实现文件类型验证
   - 限制文件大小 (当前限制5MB)
   - 验证图片内容

3. **CORS配置**
   - 已配置适当的CORS策略
   - 仅允许必要的跨域请求

## 📞 支持

如果遇到问题:
1. 查看本文档的故障排除部分
2. 检查Render的官方文档
3. 查看项目的GitHub Issues
4. 联系技术支持

---

**部署成功后，你的AI图像超分辨率应用就可以在线使用了！** 🎉