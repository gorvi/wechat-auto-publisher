#!/bin/bash
# create_github_repo.sh - 自动创建GitHub仓库并推送

REPO_NAME="wechat-auto-publisher"
GITHUB_USER="gorvi"

echo "🚀 自动创建GitHub仓库"
echo "======================"
echo ""

# 检查是否有GitHub Token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ 需要GitHub Personal Access Token"
    echo ""
    echo "获取方式："
    echo "1. 打开 https://github.com/settings/tokens"
    echo "2. 点击 'Generate new token (classic)'"
    echo "3. 勾选 'repo' 权限"
    echo "4. 生成后复制token"
    echo ""
    echo "然后运行："
    echo "   export GITHUB_TOKEN=你的token"
    echo "   ./create_github_repo.sh"
    exit 1
fi

echo "📦 创建仓库: $REPO_NAME"

# 使用GitHub API创建仓库
RESPONSE=$(curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{
    \"name\": \"$REPO_NAME\",
    \"description\": \"微信公众号自动发布工具 - AI生成内容 + 自动封面 + 一键发布\",
    \"private\": false,
    \"auto_init\": false
  }" 2>&1)

# 检查是否成功
if echo "$RESPONSE" | grep -q "\"message\": \"Repository creation is disabled\""; then
    echo "❌ 仓库创建被禁用，请手动创建"
    exit 1
elif echo "$RESPONSE" | grep -q "\"name\": \"$REPO_NAME\""; then
    echo "✅ 仓库创建成功!"
    echo "   https://github.com/$GITHUB_USER/$REPO_NAME"
    echo ""
    
    # 配置远程仓库并推送
    echo "📤 推送代码到GitHub..."
    cd /Users/ghw/.openclaw/workspace/wechat-auto-publisher
    
    # 移除旧的remote（如果有）
    git remote remove origin 2>/dev/null || true
    
    # 添加新的remote（使用token认证）
    git remote add origin "https://$GITHUB_USER:$GITHUB_TOKEN@github.com/$GITHUB_USER/$REPO_NAME.git"
    
    # 推送
    git branch -M main
    if git push -u origin main; then
        echo ""
        echo "🎉 推送成功!"
        echo "   仓库地址: https://github.com/$GITHUB_USER/$REPO_NAME"
        echo ""
        echo "📋 下一步："
        echo "   1. 访问 https://github.com/$GITHUB_USER/$REPO_NAME"
        echo "   2. 查看代码是否完整"
        echo "   3. 在README.md中添加项目介绍"
        echo "   4. 创建Release v1.0.0"
    else
        echo "❌ 推送失败"
        exit 1
    fi
else
    echo "❌ 创建失败"
    echo "响应: $RESPONSE"
    exit 1
fi
