# WeChat Auto Publisher

一个开源的微信公众号自动发布工具，支持AI内容生成、自动排版、定时发布。

**[在线演示](https://yourwebsite.com/demo)** | **[完整文档](https://docs.yourwebsite.com)** | **[Pro版](https://yourwebsite.com/pricing)**

---

## 🚀 30秒快速开始

```bash
# 安装
pip install wechat-auto-publisher

# 配置环境变量
export WECHAT_APP_ID=your_app_id
export WECHAT_APP_SECRET=your_app_secret

# 发布文章
wechat-publish "标题" "content.md"
```

---

## ✨ 功能特性

### 开源版（免费）
- ✅ Markdown转微信公众号HTML
- ✅ 微信图文素材上传
- ✅ 自动发布
- ✅ 定时任务
- ✅ OpenClaw Skill集成

### Pro版
- 🤖 AI自动生成文章内容
- 🎨 AI自动生成封面图
- 📊 数据分析报表
- 🔄 多账号管理
- 📅 内容日历

[了解更多 Pro 功能](./docs/PRO.md)

---

## 📦 安装

### 从 PyPI 安装（推荐）

```bash
pip install wechat-auto-publisher
```

### 从源码安装

```bash
git clone https://github.com/yourname/wechat-auto-publisher.git
cd wechat-auto-publisher
pip install -e .
```

---

## 🔧 配置

创建 `.env` 文件：

```env
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret

# Pro功能需要
OPENAI_API_KEY=sk-xxx
```

---

## 💡 使用示例

### Python API

```python
from wechat_auto_publisher import WeChatAutoPublisher

publisher = WeChatAutoPublisher()

# 发布Markdown文章
publisher.publish_article(
    title="AI工作流实战",
    markdown_content="# 标题\n\n正文..."
)
```

### 命令行

```bash
# 发布文件
wechat-publish article.md --title "标题"

# 定时发布
wechat-publish article.md --schedule "2026-03-01 08:00"

# AI生成并发布
wechat-publish --topic "AI编程" --ai-generate
```

### OpenClaw集成

```python
from wechat_auto_publisher.skills.openclaw import publish_from_topic

# 一句话自动生成并发布
publish_from_topic("AI编程最佳实践")
```

---

## 🏗️ 架构

```
wechat-auto-publisher/
├── src/
│   ├── core/           # 核心功能
│   ├── ai/             # AI功能（Pro）
│   └── skills/         # Skill集成
├── docs/               # 文档
├── examples/           # 示例
└── tests/              # 测试
```

---

## 🤝 贡献

欢迎贡献！请阅读 [贡献指南](./CONTRIBUTING.md)。

### 特别感谢

感谢所有贡献者让这个项目变得更好！

---

## 💰 支持项目

如果这个项目帮到了你，可以：

- ⭐ Star 这个项目
- 🐦 在社交媒体上分享
- 💵 [购买 Pro 版](https://yourwebsite.com/pricing)
- ☕ [请作者喝咖啡](https://www.buymeacoffee.com/yourname)

---

## 📄 许可

[MIT](./LICENSE) © 2026 Your Name

商业使用需要购买 [商业许可](./docs/COMMERCIAL.md)。

---

## 📞 联系

- 问题反馈：[GitHub Issues](https://github.com/yourname/wechat-auto-publisher/issues)
- 功能讨论：[GitHub Discussions](https://github.com/yourname/wechat-auto-publisher/discussions)
- 商务合作：[sales@yourwebsite.com](mailto:sales@yourwebsite.com)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/yourname">Your Name</a>
</p>
