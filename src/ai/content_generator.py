"""
AI Content Generator (Pro Feature)
AI内容生成器（Pro功能）

需要商业许可才能使用
"""

import os
from typing import Optional


class ContentGenerator:
    """
    AI文章生成器
    
    Pro功能：使用GPT-4自动生成高质量文章内容
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("请提供OpenAI API Key")
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("请安装openai库: pip install openai")
    
    def generate_article(
        self,
        topic: str,
        style: str = "professional",
        word_count: int = 1000,
        language: str = "中文"
    ) -> str:
        """
        生成文章
        
        Args:
            topic: 文章主题
            style: 风格 (professional/casual/technical/storytelling)
            word_count: 字数要求
            language: 语言
            
        Returns:
            Markdown格式文章
        """
        style_prompts = {
            "professional": "专业、严谨、适合商业场景",
            "casual": "轻松、易懂、适合大众阅读",
            "technical": "深入、详细、适合技术人员",
            "storytelling": "故事化、生动、有感染力"
        }
        
        style_desc = style_prompts.get(style, style_prompts["professional"])
        
        prompt = f"""
请为一篇关于"{topic}"的微信公众号文章生成内容。

要求：
1. 使用Markdown格式
2. 语言风格：{style_desc}
3. 字数：{word_count}字左右
4. 语言：{language}
5. 结构包含：
   - 吸引人的标题（使用#）
   - 引言/导语
   - 3-5个核心观点（使用##）
   - 每个观点下有具体说明和例子
   - 总结和行动建议
   - 文末可以带一句轻松的结束语

注意事项：
- 标题要吸引人，但不要标题党
- 内容要有实用价值，不能太空泛
- 适当使用列表、表格、引用等格式
- 语言自然流畅，不要太生硬

请直接输出Markdown内容，不要有任何其他说明。
"""
        
        model = os.getenv("OPENAI_MODEL", "gpt-4")
        
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2500
        )
        
        return response.choices[0].message.content
    
    def generate_cover_prompt(self, title: str) -> str:
        """
        生成封面图提示词
        
        Args:
            title: 文章标题
            
        Returns:
            DALL-E提示词
        """
        prompt = f"""
根据文章标题"{title}"，生成一个适合微信公众号封面的DALL-E提示词。

要求：
- 风格：专业、现代、简洁
- 配色：蓝色、白色为主，适合商务/技术类文章
- 构图：宽屏比例(16:9)，主体在左侧或中央
- 元素：不要文字，使用图标、几何图形、渐变等抽象元素
- 氛围：积极向上、科技感、专业感

请直接输出英文提示词，用于DALL-E生成。
"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()


class CoverGenerator:
    """
    AI封面图生成器（Pro功能）
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("请提供OpenAI API Key")
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("请安装openai库: pip install openai")
    
    def generate_cover(self, title: str, save_path: str = None) -> str:
        """
        生成封面图
        
        Args:
            title: 文章标题
            save_path: 保存路径（可选）
            
        Returns:
            图片本地路径
        """
        # 生成提示词
        content_gen = ContentGenerator(self.api_key)
        prompt = content_gen.generate_cover_prompt(title)
        
        # 调用DALL-E生成
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",
            quality="standard",
            n=1
        )
        
        image_url = response.data[0].url
        
        # 下载图片
        import requests
        img_response = requests.get(image_url, timeout=30)
        img_response.raise_for_status()
        
        # 保存
        if not save_path:
            from datetime import datetime
            save_path = f"/tmp/cover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        with open(save_path, 'wb') as f:
            f.write(img_response.content)
        
        return save_path


class SEOOptimizer:
    """
    SEO优化器（Pro功能）
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("请提供OpenAI API Key")
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("请安装openai库: pip install openai")
    
    def optimize_title(self, title: str) -> dict:
        """
        优化标题
        
        Returns:
            {
                "original": 原标题,
                "optimized": 优化后的标题,
                "alternatives": [备选标题],
                "reason": 优化理由
            }
        """
        prompt = f"""
请优化以下微信公众号文章标题，使其更吸引人但不过分标题党：

原标题：{title}

要求：
1. 优化后的标题要更有吸引力
2. 提供3个备选标题
3. 说明优化理由
4. 避免夸张、误导性词汇

请按以下格式输出：
优化后：xxx
备选1：xxx
备选2：xxx
备选3：xxx
理由：xxx
"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        
        # 解析结果
        lines = result.split('\n')
        optimized = ""
        alternatives = []
        reason = ""
        
        for line in lines:
            if line.startswith("优化后："):
                optimized = line.replace("优化后：", "").strip()
            elif line.startswith("备选"):
                alternatives.append(line.split("：", 1)[1].strip())
            elif line.startswith("理由："):
                reason = line.replace("理由：", "").strip()
        
        return {
            "original": title,
            "optimized": optimized or title,
            "alternatives": alternatives,
            "reason": reason
        }
    
    def extract_keywords(self, content: str) -> list:
        """提取关键词"""
        prompt = f"""
从以下文章中提取5-8个关键词，用于SEO优化：

{content[:2000]}...

请直接输出关键词列表，每行一个。
"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        keywords = response.choices[0].message.content.strip().split('\n')
        return [k.strip() for k in keywords if k.strip()]
