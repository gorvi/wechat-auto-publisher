#!/bin/bash
# setup_github.sh - GitHub仓库设置脚本

echo "🚀 WeChat Auto Publisher - GitHub Setup"
echo "========================================"
echo ""

# 检查git
if ! command -v git &> /dev/null; then
    echo "❌ 请先安装git"
    exit 1
fi

# 检查GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "⚠️  建议安装GitHub CLI (gh) 以便自动创建仓库"
    echo "   Mac: brew install gh"
    echo "   其他: https://cli.github.com/"
    echo ""
fi

# 获取GitHub用户名
echo "请输入你的GitHub用户名:"
read GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ 用户名不能为空"
    exit 1
fi

REPO_NAME="wechat-auto-publisher"

echo ""
echo "📦 即将创建仓库: $GITHUB_USERNAME/$REPO_NAME"
echo ""

# 检查是否已登录GitHub
if command -v gh &> /dev/null; then
    echo "🔐 检查GitHub登录状态..."
    if ! gh auth status &> /dev/null; then
        echo "请先登录GitHub:"
        gh auth login
    fi
    
    # 创建仓库
    echo "📁 创建GitHub仓库..."
    gh repo create "$REPO_NAME" --public --source=. --remote=origin --push
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ 仓库创建成功！"
        echo ""
        echo "🌐 访问: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    else
        echo "❌ 创建失败，请手动创建"
    fi
else
    # 手动方式
    echo ""
    echo "📋 请按以下步骤手动设置:"
    echo ""
    echo "1. 在GitHub上创建仓库:"
    echo "   https://github.com/new"
    echo ""
    echo "2. 设置仓库名: $REPO_NAME"
    echo "   选择 Public (开源)"
    echo ""
    echo "3. 运行以下命令:"
    echo ""
    echo "   git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
fi

echo ""
echo "🎉 设置完成后:"
echo ""
echo "   1. 添加项目描述和标签"
echo "   2. 开启GitHub Discussions"
echo "   3. 设置GitHub Pages (可选)"
echo "   4. 添加贡献者指南链接"
echo ""
echo "💰 商业化准备:"
echo ""
echo "   1. 创建Stripe账户用于收款"
echo "   2. 设置Gumroad用于销售"
echo "   3. 创建官网 landing page"
echo "   4. 准备宣传材料"
echo ""
