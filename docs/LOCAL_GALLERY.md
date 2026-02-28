# 本地封面库使用指南

**为中国用户设计的解决方案**

---

## 为什么需要本地封面库？

| 问题 | 国外图库 | 本地封面库 |
|------|---------|-----------|
| 访问速度 | 慢，需代理 | 快，本地读取 |
| 稳定性 | 偶尔不可用 | 100%稳定 |
| 费用 | 部分收费 | 完全免费 |
| 质量 | 随机 | 自己选择，质量可控 |
| 版权 | 需确认 | 自己选择可商用图片 |

---

## 快速开始

### 步骤1：初始化封面库

```bash
python3 init_gallery.py
```

这会创建以下目录结构：
```
covers/
├── tech/          # 科技/AI/编程
├── business/      # 商务/创业
├── design/        # 设计/创意
├── nature/        # 自然/生活
└── abstract/      # 抽象/通用
```

### 步骤2：下载封面图片

#### 推荐网站（国内可访问）

**1. 站酷 (zcool.com.cn)**
- 搜索关键词："科技背景"、"商务背景"、"PPT背景"
- 优点：中文，国内设计师作品
- 注意：查看版权说明，选择可商用的

**2. 花瓣网 (huaban.com)**
- 搜索关键词："封面背景"、"公众号封面"
- 优点：资源多，分类清晰
- 注意：个人收藏整理，商用需确认

**3. 视觉中国免费专区 (vcg.com)**
- 路径：首页 → 免费专区
- 优点：正版可商用
- 缺点：免费资源有限

**4. Pixabay (pixabay.com)**
- 优点：国内可访问，完全免费可商用
- 推荐：英文搜索"technology background"、"business abstract"

**5. Pexels (pexels.com)**
- 优点：国内可访问，免费可商用
- 推荐：搜索"tech"、"office"、"abstract"

### 步骤3：放入封面库

将下载的图片放入对应主题的目录：

```bash
covers/
├── tech/
│   ├── ai_robot.jpg
│   ├── coding_screen.jpg
│   └── digital_network.jpg
├── business/
│   ├── meeting_room.jpg
│   └── startup_office.jpg
└── ...
```

**图片要求**：
- 格式：JPG、PNG、GIF、BMP、WebP
- 建议尺寸：大于 900x383 像素
- 程序会自动裁剪为微信封面尺寸
- 每个主题建议 5-10 张图片

---

## 使用方法

### 方式1：自动使用本地封面库

```python
from src.core.publisher import WeChatAutoPublisher

publisher = WeChatAutoPublisher()

# 自动从本地封面库选择
publisher.publish_article(
    title="AI工作流实战",
    markdown_content="# 内容...",
    auto_cover=True  # 优先使用本地封面库
)
```

### 方式2：指定主题

```python
from src.utils.local_gallery import LocalCoverGallery

gallery = LocalCoverGallery("covers")

# 从 tech 主题选择封面
cover_path = gallery.generate(topic="tech")
```

### 方式3：查看封面库

```python
from src.utils.local_gallery import LocalCoverGallery

gallery = LocalCoverGallery("covers")

# 列出所有封面
print(f"封面总数: {gallery.get_count()}")
for cover in gallery.list_covers():
    print(f"  - {cover}")
```

### 方式4：添加新封面

```python
from src.utils.local_gallery import LocalCoverGallery

gallery = LocalCoverGallery("covers")

# 添加新封面（自动调整尺寸）
gallery.add_cover("/path/to/downloaded/image.jpg", title="AI背景")
```

---

## 封面选择建议

### 科技类文章 (covers/tech/)
- 蓝色调、科技感、代码、机器人、数据流
- 推荐色调：深蓝、青绿、紫色

### 商务类文章 (covers/business/)
- 办公室、会议室、握手、图表
- 推荐色调：深灰、蓝色、金色

### 设计类文章 (covers/design/)
- 创意几何、色彩渐变、艺术作品
- 推荐色调：多彩、鲜艳

### 通用/抽象 (covers/abstract/)
- 渐变背景、几何图形、模糊光斑
- 适用：不确定主题时使用

---

## 封面图片资源推荐

### 免费可商用图片（国内可访问）

**Pixabay**
```
搜索关键词：
- technology abstract
- business background  
- digital network
- gradient background
```

**Pexels**
```
搜索关键词：
- tech wallpaper
- office workspace
- creative design
- abstract colorful
```

### 国内设计平台

**站酷免费素材**
- 网址：https://www.zcool.com.cn
- 搜索："科技背景"、"商务PPT背景"

**千图网免费专区**
- 网址：https://www.58pic.com
- 注意：选择"免费"标签的素材

**摄图网免费专区**
- 网址：https://699pic.com

---

## 自动降级机制

如果本地封面库为空，程序会自动降级：

```
优先级：
1. 本地封面库（推荐）← 无网络依赖
2. 备用图库 Picsum ← 国外但国内可访问
3. 本地模板生成 ← 无需网络，自动生成
```

---

## 常见问题

### Q: 需要多少张封面图片？
A: 建议每个主题 5-10 张，总共 20-50 张即可。图片可以重复使用。

### Q: 图片版权怎么处理？
A: 请选择：
- 明确标注"免费可商用"的图片
- CC0 协议图片
- 自己拍摄或设计的图片
- 付费购买的正版图片

### Q: 封面图片尺寸不对怎么办？
A: 程序会自动裁剪为 900x383，只要原始图片大于这个尺寸即可。

### Q: 可以用自己的照片吗？
A: 当然可以！这是本地封面库的最大优势。

### Q: 不同文章可以用同一张封面吗？
A: 可以，封面图片会重复使用。

---

## 完整工作流示例

```python
from src.core.publisher import WeChatAutoPublisher
from src.utils.gemini_generator import GeminiContentGenerator

# 1. 使用 Gemini 生成文章内容
gemini = GeminiContentGenerator(api_key="你的Key")
content = gemini.generate_article("AI工作流实战")

# 2. 使用本地封面库
publisher = WeChatAutoPublisher()
publisher.publish_article(
    title="AI工作流实战",
    markdown_content=content,
    auto_cover=True  # 自动从本地库选择封面
)

# 3. 文章已保存到微信草稿箱，带精美封面！
```

---

## 总结

**本地封面库的优势：**
- ✅ 完全免费
- ✅ 无需代理
- ✅ 访问速度快
- ✅ 质量可控（自己选择）
- ✅ 无版权风险（自己选择可商用图片）
- ✅ 100%稳定可用

**适合人群：**
- 不想配置代理的用户
- 对封面质量有要求的用户
- 希望长期稳定使用的用户
- 愿意花10分钟准备封面库的用户

---

**现在运行 `python3 init_gallery.py` 开始设置你的封面库！** 🎨
