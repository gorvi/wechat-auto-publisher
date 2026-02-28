# Google Vertex AI (Imagen) 封面生成配置指南

## 概述

本项目支持使用 **Google Vertex AI (Imagen)** 生成高质量封面图。

**Imagen 特点：**
- Google 企业级AI图像生成服务
- 高质量、高分辨率图像
- 更好的文本理解和遵循能力
- 适合专业商业场景

---

## 配置步骤

### 步骤1：创建 Google Cloud 项目

1. 访问 [Google Cloud Console](https://console.cloud.google.com)
2. 创建新项目或选择现有项目
3. 记录 **项目ID**（稍后会用到）

### 步骤2：启用 Vertex AI API

```bash
# 在 Cloud Console 中，转到 "API 和服务" > "库"
# 搜索并启用 "Vertex AI API"
```

或在终端使用 gcloud：
```bash
gcloud services enable aiplatform.googleapis.com --project=YOUR_PROJECT_ID
```

### 步骤3：创建 Service Account

1. 转到 [IAM 和管理](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. 点击 "创建服务账号"
3. 填写名称：wechat-publisher
4. 分配角色：**Vertex AI User** (`roles/aiplatform.user`)
5. 创建并下载 JSON 密钥文件

### 步骤4：配置环境变量

将下载的 JSON 文件放到项目目录，并配置 `.env`：

```bash
# .env

# Google Cloud配置
GOOGLE_SERVICE_ACCOUNT_PATH=/path/to/your/service-account-key.json
GOOGLE_PROJECT_ID=your-project-id
GOOGLE_LOCATION=us-central1
```

### 步骤5：安装依赖

```bash
pip install google-auth google-auth-oauthlib requests
```

---

## 使用方法

### 方式1：直接使用 Google Imagen

```python
from src.utils.google_cover_generator import GoogleAICoverGenerator

generator = GoogleAICoverGenerator(
    service_account_path="/path/to/key.json",
    project_id="your-project-id"
)

img_path = generator.generate("AI工作流实战指南", style="professional")
print(f"封面生成成功: {img_path}")
```

### 方式2：自动选择最佳提供商

```python
from src.utils.google_cover_generator import MultiProviderCoverGenerator

# 自动选择：Google > OpenAI > 本地模板
generator = MultiProviderCoverGenerator()

# 自动生成（自动选择最佳提供商）
img_path = generator.generate("AI工作流实战指南", provider="auto")

# 或指定提供商
img_path = generator.generate("AI工作流实战指南", provider="google")
```

### 方式3：在发布流程中使用

```python
from src.core.publisher import WeChatAutoPublisher
from src.utils.google_cover_generator import GoogleAICoverGenerator

publisher = WeChatAutoPublisher()

# 使用 Google Imagen 生成封面
cover_gen = GoogleAICoverGenerator()
img_path = cover_gen.generate("AI工作流实战")
thumb_media_id = publisher.upload_image(img_path)

# 发布文章
publisher.publish_article(
    title="AI工作流实战指南",
    markdown_content="# 内容...",
    thumb_media_id=thumb_media_id,
    publish=False
)
```

---

## 风格选项

| 风格 | 说明 | 适用场景 |
|------|------|----------|
| `professional` | 专业商务风 | 企业、B2B、技术 |
| `artistic` | 艺术创意风 | 设计、创意、文化 |
| `tech` | 科技未来风 | AI、编程、科技 |
| `minimal` | 极简优雅风 | 生活方式、个人品牌 |

---

## 多提供商优先级

`MultiProviderCoverGenerator` 自动选择最佳方案：

```
优先级：
1. Google Imagen (Vertex AI) - 企业级质量
2. OpenAI DALL-E 3 - 高质量创意
3. 本地高级模板 - 稳定可靠，无需API
```

**自动选择逻辑：**
- 如果配置了 Google Service Account → 使用 Google Imagen
- 否则如果有 OpenAI API Key → 使用 DALL-E 3
- 否则 → 使用本地精美模板

---

## 成本说明

| 服务 | 价格 | 备注 |
|------|------|------|
| **Google Imagen** | $0.02-0.05/张 | Vertex AI 计费 |
| **OpenAI DALL-E 3** | $0.04-0.08/张 | 标准质量 $0.04，高清 $0.08 |
| **本地模板** | 免费 | 无API调用成本 |

---

## 故障排除

### 错误：权限不足

```
PermissionDenied: 403 IAM permission
```

**解决：**
1. 确保 Service Account 有 `Vertex AI User` 角色
2. 检查项目ID是否正确

### 错误：API未启用

```
NotFound: 404 Vertex AI API has not been enabled
```

**解决：**
```bash
gcloud services enable aiplatform.googleapis.com --project=YOUR_PROJECT_ID
```

### 错误：密钥文件无效

```
ValueError: 请提供有效的 Service Account JSON 文件路径
```

**解决：**
1. 检查文件路径是否正确
2. 确保文件存在且有读取权限
3. 确认是 JSON 格式（不是 P12）

---

## 相关文档

- [Google Vertex AI 文档](https://cloud.google.com/vertex-ai)
- [Imagen 模型介绍](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview)
- [Service Account 管理](https://cloud.google.com/iam/docs/service-accounts)

---

## 下一步

1. 完成 Google Cloud 配置
2. 测试 Google Imagen 封面生成
3. 对比 OpenAI DALL-E 3 和本地模板效果
4. 选择最适合的提供商
