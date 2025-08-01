# Render部署故障排除指南

## 常见部署错误及解决方案

### 1. Pillow依赖安装失败

#### 错误症状
```
KeyError: '__version__'
Getting requirements to build wheel did not run successfully
```

#### 原因分析
- Pillow 10.0.1版本与Python 3.13存在兼容性问题
- 旧版本的Pillow在新Python版本上构建失败

#### 解决方案
1. **更新Pillow版本**
   ```
   # requirements.txt
   Pillow>=10.2.0  # 而不是 Pillow==10.0.1
   ```

2. **指定兼容的Python版本**
   ```
   # runtime.txt
   python-3.11.9  # 而不是 python-3.9.18
   ```

3. **验证修复**
   - 重新提交代码到GitHub
   - 在Render中触发新的部署
   - 查看构建日志确认Pillow安装成功

### 2. Python版本兼容性问题

#### 推荐配置
- **开发环境**: Python 3.9+ (本地开发)
- **生产环境**: Python 3.11.9 (Render部署)
- **依赖管理**: 使用版本范围而非固定版本

#### 最佳实践
```
# requirements.txt 推荐格式
Flask>=2.3.0,<3.0.0
requests>=2.31.0
gunicorn>=21.0.0
Pillow>=10.2.0
flask-cors>=4.0.0
python-dotenv>=1.0.0
```

### 3. 环境变量配置问题

#### 常见错误
- `HF_API_TOKEN` 未在Render中配置
- 环境变量名称拼写错误
- Token权限不足

#### 解决步骤
1. 在Render Dashboard中设置环境变量
2. 确保变量名完全匹配代码中的引用
3. 验证Hugging Face Token有效性

### 4. 构建超时问题

#### 症状
- 构建过程中断
- 依赖安装时间过长

#### 解决方案
1. **优化依赖列表**
   - 移除不必要的依赖
   - 使用轻量级替代方案

2. **使用预编译包**
   - 避免从源码编译大型依赖
   - 选择有wheel包的版本

### 5. 内存不足问题

#### 症状
- 应用启动失败
- 处理大图片时崩溃

#### 解决方案
1. **升级Render实例**
   - 使用更大内存的实例类型
   - 考虑付费计划

2. **优化代码**
   - 实现图片压缩
   - 添加内存使用监控
   - 优化图片处理流程

## 部署检查清单

### 部署前检查
- [ ] `requirements.txt` 版本兼容性
- [ ] `runtime.txt` Python版本正确
- [ ] 环境变量在Render中配置
- [ ] 代码已推送到GitHub
- [ ] `Procfile` 配置正确

### 部署后验证
- [ ] 应用成功启动
- [ ] 健康检查端点响应正常
- [ ] 静态文件加载正常
- [ ] API功能测试通过
- [ ] 错误日志检查

## 调试技巧

### 1. 查看详细日志
```bash
# 在Render控制台查看实时日志
# 关注以下关键信息：
# - 构建过程日志
# - 应用启动日志
# - 运行时错误日志
```

### 2. 本地测试
```bash
# 使用相同的Python版本测试
pyenv install 3.11.9
pyenv local 3.11.9

# 安装依赖
pip install -r requirements.txt

# 本地运行
python app.py
```

### 3. 分步部署
1. 先部署基础版本（最小依赖）
2. 逐步添加功能模块
3. 每次部署后验证功能

## 联系支持

如果问题仍然存在：
1. 查看 [Render官方文档](https://render.com/docs)
2. 检查 [Render状态页面](https://status.render.com/)
3. 联系Render技术支持
4. 在项目GitHub仓库提交Issue

---

**记住**: 大多数部署问题都与依赖版本兼容性相关，仔细检查 `requirements.txt` 和 `runtime.txt` 通常能解决90%的问题。