# 飞书多维表格配置指南

## 📋 表结构设计

已设计好以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 话题ID | 文本 | 唯一标识 |
| 标题 | 文本 | 话题标题 |
| 来源 | 单选 | 即刻/36氪/虎嗅/GitHub/微博 |
| 原文链接 | 文本 | URL链接 |
| 热度评分 | 数字 | 0-100分 |
| 摘要 | 多行文本 | 内容摘要 |
| 标签 | 文本 | 逗号分隔 |
| 状态 | 单选 | 待处理/处理中/已发布/已拒绝 |
| 推荐度 | 数字 | AI评分0-100 |
| 建议角度 | 多行文本 | 写作建议 |
| 创建时间 | 日期 | 自动填充 |
| 更新时间 | 日期 | 自动更新 |

---

## 🔧 配置步骤

### 步骤1：创建多维表格

1. 打开 [飞书多维表格](https://www.feishu.cn/product/base)
2. 创建新表格，命名为 **"话题库"**
3. 添加上面设计的字段

### 步骤2：获取表格信息

打开表格后，URL格式如下：
```
https://example.feishu.cn/base/APP_TOKEN?table=tblTABLE_ID
```

需要提取：
- **APP_TOKEN**: `base/` 后面的一串字符
- **TABLE_ID**: `table=` 后面的一串字符（以`tbl`开头）

### 步骤3：获取个人访问令牌

1. 打开 [飞书开放平台](https://open.feishu.cn/)
2. 登录 → 进入开发者后台
3. 创建企业自建应用（或使用已有应用）
4. 在 **"凭证与基础信息"** 中获取 **App ID** 和 **App Secret**
5. 或者创建 **个人访问令牌** (Personal Access Token)

### 步骤4：配置环境变量

在 `.env` 文件中添加：

```env
# 飞书多维表格配置
FEISHU_APP_TOKEN=你的APP_TOKEN
FEISHU_TABLE_ID=你的TABLE_ID
FEISHU_PERSONAL_TOKEN=你的个人访问令牌
```

---

## 🚀 使用方法

### 替换存储方式

修改 `test_collector.py` 或 `run_full_workflow.py`：

```python
# 原来使用本地存储
from collector import TopicDatabase
db = TopicDatabase()

# 改为使用飞书存储
from collector.feishu_storage import FeishuBitableStorage
db = FeishuBitableStorage()
```

### 基本操作

```python
from collector.feishu_storage import FeishuBitableStorage

# 初始化
storage = FeishuBitableStorage()

# 添加话题
record_id = storage.add_topic({
    'id': 'topic_001',
    'title': 'AI工作流实战',
    'source': '即刻',
    'url': 'https://...',
    'hot_score': 95,
    'summary': '分享AI工具在自动化工作流中的应用',
    'tags': ['AI', '效率'],
    'status': 'pending'
})

# 查询话题
pending_topics = storage.get_topics(status='pending', limit=10)

# 更新状态
storage.update_status(record_id, 'published')
```

---

## ⚠️ 注意事项

1. **权限**：确保个人访问令牌有读写多维表格的权限
2. **频率限制**：飞书API有调用频率限制，批量操作时注意间隔
3. **字段映射**：确保多维表格的字段名与代码中的完全一致
4. **网络**：确保服务器能访问飞书API（国内通常没问题）

---

## 📊 表结构示意图

```
┌─────────────────────────────────────────────────────────────┐
│                        话题库 (多维表格)                      │
├──────────┬────────┬────────┬────────┬────────┬─────────────┤
│ 话题ID    │ 标题   │ 来源   │ 热度   │ 状态   │ 建议角度    │
├──────────┼────────┼────────┼────────┼────────┼─────────────┤
│ topic_001 │ AI实战 │ 即刻   │ 95     │ 待处理 │ 1. 场景分析 │
│ topic_002 │ 创业   │ 36氪   │ 88     │ 处理中 │ 2. 经验分享 │
│ topic_003 │ 工具   │ GitHub │ 82     │ 已发布 │ 3. 对比评测 │
└──────────┴────────┴────────┴────────┴────────┴─────────────┘
```

---

请提供以下信息，我来帮你配置：
1. 飞书多维表格链接（我可以从中提取token）
2. 或者：APP_TOKEN 和 TABLE_ID
3. 个人访问令牌 (Personal Access Token)

**发了权限给我，那表格链接发我一下！**
