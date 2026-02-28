"""
OpenClaw Skill Integration
OpenClaw Skill集成模块

Usage in OpenClaw:
    from wechat_auto_publisher.skills.openclaw import WeChatSkill
    
    skill = WeChatSkill()
    skill.publish("AI工作流实战", "# 标题\n\n内容...")
"""

import os
from typing import Optional
from ..core.publisher import WeChatAutoPublisher


class WeChatSkill:
    """
    OpenClaw Skill for WeChat publishing
    
    Example:
        skill = WeChatSkill()
        
        # Simple publish
        skill.publish("标题", "# Markdown内容")
        
        # AI generate and publish
        skill.publish_from_topic("AI编程最佳实践")
    """
    
    def __init__(self):
        self.publisher = WeChatAutoPublisher()
    
    def publish(
        self,
        title: str,
        markdown_content: str,
        thumb_media_id: Optional[str] = None
    ) -> bool:
        """
        发布文章到微信公众号
        
        Args:
            title: 文章标题
            markdown_content: Markdown格式内容
            thumb_media_id: 封面图media_id（可选）
            
        Returns:
            是否发布成功
        """
        return self.publisher.publish_article(
            title=title,
            markdown_content=markdown_content,
            thumb_media_id=thumb_media_id
        )
    
    def publish_from_topic(
        self,
        topic: str,
        style: str = "professional",
        word_count: int = 1000
    ) -> bool:
        """
        根据主题自动生成并发布文章（Pro功能）
        
        Args:
            topic: 文章主题
            style: 文章风格 (professional/casual/technical)
            word_count: 字数要求
            
        Returns:
            是否发布成功
            
        Note:
            需要设置OPENAI_API_KEY环境变量
        """
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ 未设置OPENAI_API_KEY，无法使用AI生成功能")
            print("   开源版请手动提供文章内容")
            return False
        
        # 检查是否为Pro功能
        if not os.getenv("ENABLE_AI_CONTENT", "false").lower() == "true":
            print("⚠️ AI内容生成是Pro功能")
            print("   开源版请手动提供文章内容")
            print("   升级Pro: https://yourwebsite.com/pricing")
            return False
        
        from ..ai.content_generator import ContentGenerator
        
        # 生成内容
        generator = ContentGenerator()
        content = generator.generate_article(topic, style, word_count)
        
        # 提取标题（如果AI生成了）
        title = topic
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        # 发布
        return self.publish(title, content)
    
    def schedule_publish(
        self,
        title: str,
        markdown_content: str,
        schedule_time: str
    ) -> bool:
        """
        定时发布（需要配合定时任务使用）
        
        Args:
            title: 文章标题
            markdown_content: Markdown内容
            schedule_time: 发布时间 (格式: "HH:MM")
        """
        # 这里可以集成schedule库
        import schedule
        import time
        
        def job():
            self.publish(title, markdown_content)
        
        schedule.every().day.at(schedule_time).do(job)
        
        print(f"⏰ 已设置定时任务: 每天 {schedule_time}")
        print(f"   标题: {title}")
        
        return True


# 快捷函数（直接在OpenClaw中使用）

def publish_article(title: str, content: str) -> bool:
    """快捷发布函数"""
    skill = WeChatSkill()
    return skill.publish(title, content)


def publish_from_topic(topic: str) -> bool:
    """AI生成并发布（Pro功能）"""
    skill = WeChatSkill()
    return skill.publish_from_topic(topic)


# OpenClaw自动发现接口
SKILL_NAME = "wechat-publisher"
SKILL_DESCRIPTION = "微信公众号自动发布工具"
SKILL_VERSION = "1.0.0"
SKILL_FUNCTIONS = {
    "publish": publish_article,
    "publish_from_topic": publish_from_topic,
}
