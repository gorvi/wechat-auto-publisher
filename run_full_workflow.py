#!/usr/bin/env python3
"""
完整工作流：采集话题 → AI生成文章 → 发布到微信

一键完成：
1. 采集热门话题
2. 选择最佳话题
3. AI生成文章内容
4. 生成封面图
5. 发布到微信草稿箱
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from collector import TopicCollector, TopicDatabase, TopicSelector
from core.publisher import WeChatAutoPublisher


def full_workflow():
    """
    完整工作流
    
    自动化内容生产流水线
    """
    print("🚀 启动完整工作流")
    print("=" * 70)
    print("流程：采集 → 选择 → 生成 → 封面 → 发布")
    print("=" * 70)
    
    # ========== 步骤1: 采集话题 ==========
    print("\n📡 步骤1: 采集热门话题")
    print("-" * 70)
    
    collector = TopicCollector()
    items = collector.collect_all(limit_per_source=3)
    
    if not items:
        print("❌ 未采集到话题，流程终止")
        return False
    
    print(f"✅ 采集到 {len(items)} 条话题")
    
    # 保存到数据库
    db = TopicDatabase()
    db.add_topics([item.to_dict() for item in items])
    
    # ========== 步骤2: 选择话题 ==========
    print("\n🎯 步骤2: 选择最佳话题")
    print("-" * 70)
    
    selector = TopicSelector(db)
    best_topic = selector.select_best(count=1, strategy='hot')[0]
    
    print(f"✅ 选中话题: {best_topic['title']}")
    print(f"   来源: {best_topic['source']}")
    print(f"   热度: {best_topic['hot_score']}")
    
    # 分析话题
    analysis = selector.analyze_topic(best_topic)
    print(f"\n💡 分析结果:")
    print(f"   推荐度: {analysis['score']}/100")
    print(f"   建议角度: {analysis['angles'][0]}")
    
    # 标记为处理中
    db.update_status(best_topic['id'], 'processing')
    
    # ========== 步骤3: AI生成文章 ==========
    print("\n🤖 步骤3: AI生成文章内容")
    print("-" * 70)
    
    # 检查是否有AI API Key
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if gemini_key:
        try:
            from utils.gemini_generator import GeminiContentGenerator
            
            generator = GeminiContentGenerator(api_key=gemini_key)
            
            print(f"   正在生成文章...")
            content = generator.generate_article(
                topic=best_topic['title'],
                style='professional',
                word_count=1000
            )
            
            print(f"✅ 文章生成成功 ({len(content)} 字符)")
            
        except Exception as e:
            print(f"⚠️ AI生成失败: {e}")
            print(f"   使用模板内容...")
            content = generate_template_content(best_topic)
    else:
        print(f"⚠️ 未配置AI API Key")
        print(f"   使用模板内容...")
        content = generate_template_content(best_topic)
    
    # ========== 步骤4: 准备发布 ==========
    print("\n📝 步骤4: 准备发布")
    print("-" * 70)
    
    # 检查微信配置
    wechat_app_id = os.getenv('WECHAT_APP_ID')
    wechat_secret = os.getenv('WECHAT_APP_SECRET')
    
    if not wechat_app_id or not wechat_secret:
        print("❌ 未配置微信公众号")
        print("   请设置 WECHAT_APP_ID 和 WECHAT_APP_SECRET")
        return False
    
    print(f"✅ 微信公众号已配置")
    
    # ========== 步骤5: 发布到微信 ==========
    print("\n📤 步骤5: 发布到微信草稿箱")
    print("-" * 70)
    
    try:
        publisher = WeChatAutoPublisher()
        
        success, media_id, _ = publisher.publish_article(
            title=best_topic['title'],
            markdown_content=content,
            publish=False,  # 保存到草稿箱
            verbose=True
        )
        
        if success:
            print(f"\n🎉 发布成功！")
            print(f"   文章已保存到微信草稿箱")
            
            # 更新话题状态
            db.update_status(best_topic['id'], 'published')
            
            print(f"\n📋 下一步:")
            print(f"   1. 登录微信公众平台")
            print(f"   2. 进入"内容与互动" → "草稿箱"")
            print(f"   3. 查看并发布文章")
            
            return True
        else:
            print(f"\n❌ 发布失败")
            db.update_status(best_topic['id'], 'rejected')
            return False
            
    except Exception as e:
        print(f"\n❌ 发布出错: {e}")
        db.update_status(best_topic['id'], 'rejected')
        return False


def generate_template_content(topic: dict) -> str:
    """
    生成模板内容（当AI不可用时）
    """
    title = topic['title']
    source = topic['source']
    summary = topic.get('summary', '')
    
    content = f"""# {title}

> 来源：{source}

## 引言

{summary if summary else '今天我们来聊聊这个话题。'}

## 核心观点

### 1. 背景分析

这个话题反映了当前行业的一个重要趋势。

### 2. 深度解读

从技术、商业、用户等多个维度分析：

- **技术层面**：新技术的应用带来的变革
- **商业层面**：商业模式的创新和演变  
- **用户层面**：用户需求的变化和升级

### 3. 实践建议

基于以上分析，建议：

1. 持续关注行业动态
2. 积极尝试新工具和方法
3. 保持学习和迭代

## 总结

{title}是一个值得关注的话题，希望这篇文章对你有所帮助。

---

*本文由 WeChat Auto Publisher 自动生成*
*数据来源：{source}*
"""
    
    return content


if __name__ == "__main__":
    try:
        success = full_workflow()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 流程出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
