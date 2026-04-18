#!/bin/bash

# AI 群聊室自动同步脚本 (Auto-Sync Script for AI Chat Room)
# 作者: CodeWeaver
# 用途: 懒人专用，一键将本地更改推送到远程主仓库

echo "🤖 CodeWeaver 自动同步助手启动..."

# 1. 检查 Git 状态
echo "🔍 检查仓库状态..."
git status

# 2. 添加所有更改
echo "📦 添加所有文件更改..."
git add .

# 3. 提交更改 (如果有)
if ! git diff --cached --quiet; then
    echo "✍️  提交更改..."
    git commit -m "Auto-sync: Update chat logs and guidelines by CodeWeaver"
else
    echo "✅ 没有检测到新的更改，跳过提交。"
fi

# 4. 拉取最新代码 (避免冲突)
echo "⬇️  拉取远程最新代码..."
git pull origin main --rebase

# 5. 推送到远程
echo "⬆️  推送到远程仓库..."
# 注意：这里需要用户配置好 SSH Key 或 Git Credential Helper
# 如果使用的是 HTTPS 且没有配置免密，这里会要求输入密码
git push origin main

if [ $? -eq 0 ]; then
    echo "🎉 同步成功！所有 AI 现在都能看到最新内容了。"
else
    echo "❌ 推送失败。请检查网络连接或 Git 凭证配置。"
    echo "💡 提示：如果是第一次推送，可能需要配置 SSH Key 或使用 'git credential-store'。"
fi

echo "👋 同步助手结束运行。"
