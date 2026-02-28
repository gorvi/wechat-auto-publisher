# WeChat Auto Publisher

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![WeChat API](https://img.shields.io/badge/WeChat-Official%20API-brightgreen.svg)]()

🤖 **AI驱动的微信公众号自动发布工具**

基于OpenAI + 微信官方API，实现Markdown文章自动生成、AI封面图、自动发布到公众号。

[English](./README_EN.md) | [文档](https://github.com/yourname/wechat-auto-publisher/wiki) | [讨论区](https://github.com/yourname/wechat-auto-publisher/discussions)

---

## ✨ 核心功能

### 🆓 开源版（免费）

- ✅ Markdown转微信公众号HTML
- ✅ 微信图文草稿上传
- ✅ 自动发布（freepublish）
- ✅ 定时任务支持
- ✅ 基础封面图支持
- ✅ OpenClaw Skill集成

### 💎 Pro版（付费）

- 🤖 AI自动生成文章内容（GPT-4）
- 🎨 AI自动生成封面图（DALL-E）
- 📊 数据分析报表
- 🔄 多账号管理
- 📅 内容日历
- 🎯 SEO优化建议
- 💬 7×24技术支持

[了解更多 Pro 功能](./docs/PRO.md) | [购买 Pro 许可](https://yourwebsite.com/pricing)

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourname/wechat-auto-publisher.git
cd wechat-auto-publisher

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的配置
```

### 基础使用

```python
from wechat_auto_publisher import WeChatAutoPublisher

# 初始化
publisher = WeChatAutoPublisher()

# 发布Markdown文章
publisher.publish_article(
    title="AI工作流实战",
    markdown_content="# 标题\n\n正文内容...",
    generate_cover=False  # 开源版手动上传封面
)
```

### OpenClaw集成

```python
# 在OpenClaw中直接调用
from wechat_auto_publisher import publish_from_topic

# AI生成并发布
publish_from_topic("AI编程最佳实践")
```

---

## 📖 文档

- [快速开始指南](./docs/QUICKSTART.md)
- [API文档](./docs/API.md)
- [OpenClaw Skill集成](./docs/OPENCLAW.md)
- [常见问题](./docs/FAQ.md)
- [Pro版功能对比](./docs/PRO.md)

---

## 💰 商业授权

本项目采用 **双许可模式**：

### 开源许可（MIT）
- 个人使用 ✅
- 非商业项目 ✅
- 修改和分发 ✅
- **必须保留版权声明**

### 商业许可
- 企业内部使用
- SaaS服务
- 闭源衍生产品
- 去除品牌标识

[购买商业许可](https://yourwebsite.com/pricing) | [联系销售](mailto:sales@yourwebsite.com)

---

## 🏗️ 架构

```
wechat-auto-publisher/
├── src/                    # 核心代码
│   ├── core/              # 微信API封装
│   ├── ai/                # AI生成（Pro）
│   ├── skills/            # OpenClaw Skills
│   └── utils/             # 工具函数
├── docs/                  # 文档
├── examples/              # 示例代码
├── tests/                 # 测试
└── scripts/               # 部署脚本
```

---

## 🤝 贡献

欢迎贡献代码！请阅读 [贡献指南](./CONTRIBUTING.md)。

### 贡献者

<a href="https://github.com/yourname/wechat-auto-publisher/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yourname/wechat-auto-publisher" />
</a>

---

## 📝 更新日志

查看 [CHANGELOG.md](./CHANGELOG.md)

---

## 📄 许可

[MIT](./LICENSE) © 2026 Your Name

---

## ☕ 赞助

如果这个项目帮到了你，可以请作者喝杯咖啡：

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/yourname)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/yourname">Your Name</a>
</p>
