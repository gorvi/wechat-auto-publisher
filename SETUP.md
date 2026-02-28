# 开发环境配置

## 1. 创建虚拟环境

```bash
cd /Users/ghw/.openclaw/workspace/wechat-auto-publisher

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 验证
which python
# 应该显示: .../wechat-auto-publisher/venv/bin/python
```

## 2. 安装依赖

```bash
pip install -r requirements.txt
```

## 3. 配置环境变量

```bash
# 创建 .env 文件
cat > .env << 'EOF'
# 微信配置（已提供）
WECHAT_APP_ID=wxf23a5cb0449eb83d
WECHAT_APP_SECRET=1e64cecf9b9d4b06fe6a2ef48ee06eeb

# OpenAI配置（可选，Pro功能需要）
# OPENAI_API_KEY=sk-xxx

# 默认作者
DEFAULT_AUTHOR=AI助手

# 日志级别
LOG_LEVEL=INFO
EOF
```

## 4. 验证配置

```bash
# 测试导入
python -c "from src.core.publisher import WeChatAutoPublisher; print('✅ 导入成功')"

# 测试环境变量
python -c "import os; print('AppID:', os.getenv('WECHAT_APP_ID')[:10]+'...')"
```

## 5. 项目结构确认

```
wechat-auto-publisher/
├── venv/               # 虚拟环境
├── src/                # 源代码
├── tests/              # 测试
├── logs/               # 日志
├── .env                # 环境变量
└── requirements.txt    # 依赖
```

## 下一步

环境配置完成后，运行：
```bash
python test_publish.py
```

开始测试发布功能。
