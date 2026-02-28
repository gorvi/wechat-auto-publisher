# 贡献指南

感谢你对 WeChat Auto Publisher 感兴趣！我们欢迎各种形式的贡献。

---

## 🚀 快速开始

1. Fork 本仓库
2. 克隆你的 Fork
   ```bash
   git clone https://github.com/YOUR_USERNAME/wechat-auto-publisher.git
   cd wechat-auto-publisher
   ```
3. 安装依赖
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```
4. 创建分支
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## 📋 贡献类型

### 🐛 报告 Bug

- 使用 [GitHub Issues](https://github.com/yourname/wechat-auto-publisher/issues)
- 描述清楚复现步骤
- 提供环境信息（Python版本、操作系统）
- 如果可以，提供错误日志

### 💡 建议新功能

- 先在 Discussions 中讨论
- 说明使用场景
- 如果可能，描述实现思路

### 📝 改进文档

- 修复 typo
- 添加示例代码
- 翻译文档

### 💻 提交代码

#### 代码规范

- 遵循 PEP 8
- 使用 Black 格式化
- 添加类型注解
- 写清晰的注释

#### 提交信息规范

```
<type>: <subject>

<body>

<footer>
```

**type 类型：**
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

**示例：**
```
feat: add support for multiple WeChat accounts

- Add WeChatAccountManager class
- Update configuration schema
- Add tests

Closes #123
```

---

## 🧪 测试

运行测试：
```bash
pytest
```

覆盖率检查：
```bash
pytest --cov=src tests/
```

---

## 🎯 开发路线

查看 [GitHub Projects](https://github.com/yourname/wechat-auto-publisher/projects) 了解当前开发计划。

---

## 🏆 贡献者荣誉

所有贡献者都会出现在：
- README 的贡献者列表
- 发布说明的致谢部分
- 网站上的贡献者页面

---

## 📞 联系方式

- 讨论区：[GitHub Discussions](https://github.com/yourname/wechat-auto-publisher/discussions)
- 邮件：contributors@yourwebsite.com

---

再次感谢你的贡献！🙏
