#!/bin/bash
# quickstart.sh - 快速启动开发环境

set -e

echo "🚀 WeChat Auto Publisher - 快速启动"
echo "====================================="
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装"
    exit 1
fi

echo "✅ Python3 已安装: $(python3 --version)"

# 检查是否在项目目录
if [ ! -f "requirements.txt" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
    echo "✅ 虚拟环境创建成功"
else
    echo "✅ 虚拟环境已存在"
fi

# 激活虚拟环境
echo ""
echo "🔌 激活虚拟环境..."
source venv/bin/activate
echo "✅ 虚拟环境已激活"

# 安装依赖
echo ""
echo "📥 安装依赖..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✅ 依赖安装完成"

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  未找到 .env 文件"
    echo ""
    echo "请创建 .env 文件："
    cat << 'EOF'
    
cat > .env << 'ENVFILE'
WECHAT_APP_ID=wxf23a5cb0449eb83d
WECHAT_APP_SECRET=1e64cecf9b9d4b06fe6a2ef48ee06eeb
DEFAULT_AUTHOR=AI助手
ENVFILE
    
    echo ""
    echo "已自动创建 .env 文件"
else
    echo "✅ .env 文件已存在"
fi

# 测试导入
echo ""
echo "🧪 测试导入..."
python3 -c "from src.core.publisher import WeChatAutoPublisher; print('✅ 模块导入成功')"

# 显示下一步
echo ""
echo "🎉 环境配置完成！"
echo ""
echo "下一步："
echo ""
echo "1️⃣  测试获取Token："
echo "   python3 test_publish.py --token-only"
echo ""
echo "2️⃣  测试发布文章："
echo "   python3 test_publish.py"
echo ""
echo "3️⃣  查看日志："
echo "   tail -f logs/wechat_publisher.log"
echo ""
