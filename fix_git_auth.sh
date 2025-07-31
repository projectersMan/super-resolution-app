#!/bin/bash

# fix_git_auth.sh - 修复Git认证问题

echo "=== Git认证问题修复工具 ==="
echo

# 检查当前Git配置
echo "1. 检查当前Git远程仓库配置:"
git remote -v
echo

# 检查Git用户配置
echo "2. 检查Git用户配置:"
echo "用户名: $(git config user.name)"
echo "邮箱: $(git config user.email)"
echo

echo "=== 问题分析 ==="
echo "❌ GitHub已不再支持密码认证 (自2021年8月13日起)"
echo "✅ 需要使用Personal Access Token (PAT)进行认证"
echo

echo "=== 解决方案 ==="
echo "方案1: 使用Personal Access Token"
echo "1. 访问 https://github.com/settings/tokens"
echo "2. 点击 'Generate new token (classic)'"
echo "3. 设置token名称和权限 (至少需要 'repo' 权限)"
echo "4. 复制生成的token"
echo "5. 在推送时使用token作为密码"
echo

echo "方案2: 配置Git凭据存储"
echo "执行以下命令配置凭据存储:"
echo "git config --global credential.helper store"
echo

echo "方案3: 使用SSH密钥 (推荐)"
echo "1. 生成SSH密钥: ssh-keygen -t ed25519 -C 'your_email@example.com'"
echo "2. 添加到ssh-agent: ssh-add ~/.ssh/id_ed25519"
echo "3. 复制公钥: cat ~/.ssh/id_ed25519.pub"
echo "4. 在GitHub添加SSH密钥: https://github.com/settings/keys"
echo "5. 更改远程仓库URL为SSH格式"
echo

echo "=== 快速修复 ==="
read -p "是否要配置Git凭据存储? (y/n): " configure_credentials

if [[ $configure_credentials == "y" || $configure_credentials == "Y" ]]; then
    echo "配置Git凭据存储..."
    git config --global credential.helper store
    echo "✅ 凭据存储已配置"
    echo "💡 下次推送时输入用户名和Personal Access Token，Git会自动保存"
else
    echo "跳过凭据存储配置"
fi

echo
read -p "是否要切换到SSH认证? (y/n): " switch_to_ssh

if [[ $switch_to_ssh == "y" || $switch_to_ssh == "Y" ]]; then
    echo "切换到SSH认证..."
    
    # 提取仓库信息
    REPO_URL=$(git remote get-url origin)
    if [[ $REPO_URL == https://github.com/* ]]; then
        # 转换HTTPS URL到SSH URL
        SSH_URL=$(echo $REPO_URL | sed 's|https://github.com/|git@github.com:|')
        echo "原URL: $REPO_URL"
        echo "新URL: $SSH_URL"
        
        read -p "确认切换到SSH URL? (y/n): " confirm_ssh
        if [[ $confirm_ssh == "y" || $confirm_ssh == "Y" ]]; then
            git remote set-url origin $SSH_URL
            echo "✅ 已切换到SSH认证"
            echo "💡 请确保已在GitHub添加SSH密钥"
            echo "🔗 SSH密钥管理: https://github.com/settings/keys"
        else
            echo "取消SSH切换"
        fi
    else
        echo "当前不是HTTPS URL，无需切换"
    fi
else
    echo "保持当前认证方式"
fi

echo
echo "=== 测试连接 ==="
read -p "是否要测试Git连接? (y/n): " test_connection

if [[ $test_connection == "y" || $test_connection == "Y" ]]; then
    echo "测试Git连接..."
    if git ls-remote origin > /dev/null 2>&1; then
        echo "✅ Git连接测试成功"
    else
        echo "❌ Git连接测试失败"
        echo "💡 请检查认证配置"
    fi
fi

echo
echo "=== 完成 ==="
echo "如果仍有问题，请参考GitHub官方文档:"
echo "🔗 https://docs.github.com/en/authentication"