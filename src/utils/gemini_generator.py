"""
Gemini AI Content Generator
使用 Google Gemini Pro 生成文章内容

API Key 格式：AIzaSy... (Generative Language API)
"""

import os
from typing import Optional


class GeminiContentGenerator:
    """
    Google Gemini 内容生成器
    
    模型：Gemini Pro / Gemini Pro Vision
    用途：生成文章内容、分析图片
    
    特点：
    - 免费额度较宽松
    - 支持长文本
    - 支持中文
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("请提供 Gemini API Key 或设置 GEMINI_API_KEY 环境变量")
    
    def generate_article(self, 
                        topic: str, 
                        style: str = "professional",
                        word_count: int = 1000,
                        language: str = "中文") -> str:
        """
        生成文章
        
        Args:
            topic: 文章主题
            style: 风格 (professional/casual/technical/storytelling)
            word_count: 字数
            language: 语言
            
        Returns:
            Markdown格式文章
        """
        try:
            import google.generativeai as genai
            
            # 配置 API Key
            genai.configure(api_key=self.api_key)
            
            # 选择模型
            model = genai.GenerativeModel('gemini-pro')
            
            # 构建提示词
            prompt = self._create_article_prompt(topic, style, word_count, language)
            
            print(f"🤖 使用 Gemini Pro 生成文章...")
            print(f"   主题: {topic}")
            
            # 生成
            response = model.generate_content(prompt)
            
            if response.text:
                print(f"✅ 文章生成成功 ({len(response.text)} 字符)")
                return response.text
            else:
                raise Exception("生成内容为空")
                
        except ImportError:
            raise ImportError("需要安装依赖: pip install google-generativeai")
        except Exception as e:
            print(f"❌ Gemini 生成失败: {e}")
            raise
    
    def _create_article_prompt(self, topic: str, style: str, word_count: int, language: str) -> str:
        """创建文章生成提示词"""
        
        style_descriptions = {
            "professional": "专业、严谨、有深度，适合商业和技术场景",
            "casual": "轻松、易懂、亲切，像和朋友聊天",
            "technical": "深入、详细、有代码和案例，适合技术人员",
            "storytelling": "故事化、生动、有情节，用故事讲观点"
        }
        
        style_desc = style_descriptions.get(style, style_descriptions["professional"])
        
        prompt = f"""请为一篇关于"{topic}"的微信公众号文章生成内容。

要求：
1. 使用Markdown格式
2. 语言风格：{style_desc}
3. 字数：{word_count}字左右
4. 语言：{language}
5. 结构包含：
   - 吸引人的标题（使用#）
   - 引言/导语（引起共鸣）
   - 3-5个核心观点（使用##）
   - 每个观点下有具体说明、案例或数据
   - 实用建议（可操作的行动指南）
   - 总结和互动引导

注意事项：
- 标题要吸引人，但不过度标题党
- 内容要有实用价值，读者能学到东西
- 适当使用列表、表格、引用等格式
- 语言自然流畅，避免机器感
- 如果是技术主题，可以包含代码示例

请直接输出完整的Markdown格式文章。
"""
        return prompt.strip()
    
    def generate_title_variations(self, topic: str, count: int = 3) -> list:
        """
        生成多个标题变体
        
        Args:
            topic: 主题
            count: 标题数量
            
        Returns:
            标题列表
        """
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""为"{topic}"这个主题生成{count}个吸引人的微信公众号文章标题。

要求：
1. 每个标题都要有吸引力
2. 适合目标读者（对AI工具感兴趣的职场人）
3. 不要夸张或误导
4. 多样化风格：有的专业、有的接地气、有的悬念

请只返回标题列表，每行一个，不要有其他内容。
"""
            
            response = model.generate_content(prompt)
            titles = [t.strip() for t in response.text.split('\n') if t.strip()]
            
            return titles[:count]
            
        except Exception as e:
            print(f"❌ 标题生成失败: {e}")
            return [f"{topic}实战指南", f"关于{topic}的深度解析", f"{topic}入门到精通"]
    
    def analyze_content(self, content: str) -> dict:
        """
        分析文章质量
        
        Args:
            content: 文章内容
            
        Returns:
            分析报告
        """
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""请分析以下微信公众号文章的质量：

文章内容：
{content[:2000]}...

请从以下维度分析：
1. 标题吸引力（1-10分）
2. 内容实用性（1-10分）
3. 结构清晰度（1-10分）
4. 语言流畅度（1-10分）
5. 主要优点
6. 改进建议

请以JSON格式返回分析结果。
"""
            
            response = model.generate_content(prompt)
            
            # 尝试解析JSON
            import json
            try:
                result = json.loads(response.text)
                return result
            except:
                return {"analysis": response.text}
                
        except Exception as e:
            print(f"❌ 分析失败: {e}")
            return {"error": str(e)}


class MultiAIContentGenerator:
    """
    多AI内容生成器
    
    自动选择：Gemini (免费) > OpenAI (付费)
    """
    
    def __init__(self, 
                 gemini_api_key: str = None,
                 openai_api_key: str = None):
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        
        self.available_providers = self._check_providers()
    
    def _check_providers(self) -> list:
        """检查可用的提供商"""
        providers = []
        
        if self.gemini_api_key:
            providers.append("gemini")
        
        if self.openai_api_key:
            providers.append("openai")
        
        return providers
    
    def generate(self, topic: str, provider: str = "auto", **kwargs) -> str:
        """
        生成内容
        
        Args:
            topic: 主题
            provider: gemini/openai/auto
            **kwargs: 其他参数
        """
        if provider == "auto":
            # 优先使用 Gemini（更便宜）
            provider = self.available_providers[0] if self.available_providers else None
        
        if provider == "gemini":
            generator = GeminiContentGenerator(self.gemini_api_key)
            return generator.generate_article(topic, **kwargs)
        
        elif provider == "openai":
            # 使用 OpenAI
            from ..ai.content_generator import ContentGenerator
            generator = ContentGenerator(self.openai_api_key)
            return generator.generate_article(topic, **kwargs)
        
        else:
            raise ValueError("没有可用的AI提供商，请配置 GEMINI_API_KEY 或 OPENAI_API_KEY")


# 快捷函数
def generate_with_gemini(topic: str, api_key: str = None, **kwargs) -> str:
    """使用 Gemini 快速生成文章"""
    generator = GeminiContentGenerator(api_key)
    return generator.generate_article(topic, **kwargs)
