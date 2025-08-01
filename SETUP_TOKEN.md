# 🔑 Hugging Face API Token 设置指南

## 问题描述
当您看到 "HF_API_TOKEN环境变量未设置" 错误时，说明应用程序无法找到必需的Hugging Face API Token。

## 解决步骤

### 1. 获取 Hugging Face API Token

1. **访问 Hugging Face 官网**
   - 打开浏览器，访问：https://huggingface.co/

2. **注册/登录账户**
   - 如果没有账户，点击 "Sign Up" 注册
   - 如果已有账户，点击 "Log In" 登录

3. **创建 API Token**
   - 登录后，点击右上角头像
   - 选择 "Settings"
   - 在左侧菜单中选择 "Access Tokens"
   - 点击 "New token" 按钮
   - 填写 Token 名称（如："AI-Image-Upscaler"）
   - 选择权限类型：**"Read"** （读取权限即可）
   - 点击 "Generate a token"
   - **重要：复制生成的 Token 并保存好**

### 2. 配置环境变量

#### 方法一：使用 .env 文件（推荐）

1. **编辑 .env 文件**
   ```bash
   # 在项目根目录下编辑 .env 文件
   nano .env
   ```

2. **填入您的 Token**
   ```bash
   # 将 your_token_here 替换为您实际的 Token
   HF_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   PORT=5001
   FLASK_ENV=development
   ```

3. **保存文件**
   - 按 `Ctrl+X`，然后按 `Y`，最后按 `Enter` 保存

#### 方法二：直接设置环境变量

**临时设置（当前终端会话）：**
```bash
export HF_API_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**永久设置（添加到 shell 配置文件）：**
```bash
# 对于 zsh 用户
echo 'export HF_API_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"' >> ~/.zshrc
source ~/.zshrc

# 对于 bash 用户
echo 'export HF_API_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"' >> ~/.bashrc
source ~/.bashrc
```

### 3. 验证配置

1. **重启应用程序**
   ```bash
   ./run.sh
   ```

2. **检查健康状态**
   - 访问：http://127.0.0.1:5001/health
   - 应该看到：`"hf_token_configured": true`

3. **运行测试**
   ```bash
   python deploy_test.py
   ```

## 常见问题

### Q: Token 格式是什么样的？
A: Hugging Face Token 通常以 `hf_` 开头，后跟一串字母和数字，总长度约40个字符。
例如：`hf_abcdefghijklmnopqrstuvwxyz1234567890`

### Q: 我的 Token 不工作怎么办？
A: 请检查：
- Token 是否正确复制（没有多余的空格）
- Token 是否已过期
- Token 是否有足够的权限（至少需要 Read 权限）

### Q: 如何检查 Token 是否有效？
A: 可以使用以下命令测试：
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-x4-upscaler
```

### Q: 在 Render 部署时如何设置？
A: 在 Render 控制台中：
1. 进入您的 Web Service
2. 点击 "Environment" 标签
3. 添加环境变量：
   - Key: `HF_API_TOKEN`
   - Value: 您的实际 Token
4. 点击 "Save Changes"

## 安全提醒

⚠️ **重要安全提示：**
- 永远不要在代码中硬编码 API Token
- 不要将包含真实 Token 的 .env 文件提交到 Git
- 定期轮换您的 API Token
- 只给 Token 必要的最小权限

## 需要帮助？

如果您仍然遇到问题：
1. 检查 Hugging Face 官方文档
2. 确认您的网络连接正常
3. 查看应用程序日志获取更多错误信息
4. 联系技术支持

---

配置完成后，您就可以正常使用 AI 图像超分辨率功能了！ 🎉