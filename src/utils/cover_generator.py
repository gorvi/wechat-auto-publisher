"""
Cover Generator Module
封面图生成模块

支持两种方式：
1. AI生成（DALL-E）- 根据文章主题生成
2. 本地模板（Pillow）- 精美渐变背景
"""

import os
from typing import Optional
from datetime import datetime


class CoverGenerator:
    """
    封面图生成器
    
    支持AI生成和本地模板两种方式
    """
    
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
    
    def generate(self, title: str, style: str = "auto") -> str:
        """
        生成封面图
        
        Args:
            title: 文章标题
            style: 生成风格 (auto/ai/local)
                  - auto: 优先使用AI，没有API则用本地
                  - ai: 强制使用AI生成
                  - local: 使用本地模板
            
        Returns:
            图片本地路径
        """
        if style == "ai":
            return self._generate_ai(title)
        elif style == "local":
            return self._generate_local(title)
        else:  # auto
            if self.openai_api_key:
                try:
                    return self._generate_ai(title)
                except Exception as e:
                    print(f"⚠️ AI生成失败，使用本地模板: {e}")
                    return self._generate_local(title)
            else:
                return self._generate_local(title)
    
    def _generate_ai(self, title: str) -> str:
        """使用DALL-E生成封面"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)
            
            # 根据标题生成提示词
            prompt = self._create_prompt(title)
            
            print(f"🎨 使用AI生成封面...")
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1792x1024",
                quality="standard",
                n=1
            )
            
            # 下载图片
            import requests
            image_url = response.data[0].url
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            
            # 保存
            img_path = f'/tmp/cover_ai_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            with open(img_path, 'wb') as f:
                f.write(img_response.content)
            
            print(f"✅ AI封面生成成功")
            return img_path
            
        except ImportError:
            raise ImportError("请安装openai库: pip install openai")
    
    def _create_prompt(self, title: str) -> str:
        """根据标题创建DALL-E提示词"""
        # 提取主题关键词
        keywords = self._extract_keywords(title)
        
        base_prompt = f"""
Create a professional, modern WeChat article cover image.

Title: "{title}"
Theme: {keywords}

Style Requirements:
- Modern, minimalist design
- Professional business/tech aesthetic
- Gradient background (blue, purple, or teal tones)
- Clean typography area for title (center or left-aligned)
- Abstract geometric elements or subtle patterns
- No text in the image itself
- Wide banner format (16:9 ratio)
- High quality, suitable for professional blog

Color palette: Deep blue to cyan gradient, with white and light blue accents.
Mood: Professional, innovative, trustworthy.
"""
        return base_prompt.strip()
    
    def _extract_keywords(self, title: str) -> str:
        """从标题提取关键词"""
        # 简单的关键词提取
        tech_keywords = ["AI", "人工智能", "自动化", "编程", "代码", "开发", "技术", "工具", "效率", "工作流"]
        business_keywords = ["商业", "创业", "营销", "增长", "盈利", "收入", "客户", "产品"]
        
        found_keywords = []
        for kw in tech_keywords + business_keywords:
            if kw in title:
                found_keywords.append(kw)
        
        if not found_keywords:
            # 从标题提取前10个字符作为主题
            return title[:10] if len(title) > 10 else title
        
        return ", ".join(found_keywords[:3])
    
    def _generate_local(self, title: str) -> str:
        """使用本地模板生成精美封面"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import random
            
            # 创建图片 (900x383 是微信封面推荐尺寸)
            width, height = 900, 383
            
            # 选择配色方案
            color_schemes = [
                # 蓝色渐变
                [("#1e3c72", "#2a5298"), ("#667eea", "#764ba2")],
                # 紫色渐变
                [("#667eea", "#764ba2"), ("#f093fb", "#f5576c")],
                # 青色渐变
                [("#11998e", "#38ef7d"), ("#00b09b", "#96c93d")],
                # 深色科技感
                [("#0f2027", "#203a43"), ("#2c5364", "#203a43")],
                # 橙色活力
                [("#f12711", "#f5af19"), ("#ff6b6b", "#feca57")],
            ]
            
            # 随机选择一个配色
            bg_colors, accent_colors = random.choice(color_schemes)
            
            # 创建渐变背景
            img = Image.new('RGB', (width, height), color=bg_colors[0])
            draw = ImageDraw.Draw(img)
            
            # 绘制渐变
            for y in range(height):
                r = int(int(bg_colors[0][1:3], 16) * (1 - y/height) + int(bg_colors[1][1:3], 16) * (y/height))
                g = int(int(bg_colors[0][3:5], 16) * (1 - y/height) + int(bg_colors[1][3:5], 16) * (y/height))
                b = int(int(bg_colors[0][5:7], 16) * (1 - y/height) + int(bg_colors[1][5:7], 16) * (y/height))
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # 添加装饰元素 - 圆点
            for _ in range(20):
                x = random.randint(0, width)
                y = random.randint(0, height)
                r = random.randint(20, 100)
                opacity = random.randint(20, 60)
                draw.ellipse([x-r, y-r, x+r, y+r], fill=(255, 255, 255, opacity))
            
            # 添加装饰元素 - 线条
            for _ in range(5):
                x1 = random.randint(0, width)
                y1 = random.randint(0, height)
                x2 = x1 + random.randint(-200, 200)
                y2 = y1 + random.randint(-200, 200)
                draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, 30), width=2)
            
            # 尝试加载字体
            try:
                # macOS系统字体
                title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
                subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
            except:
                try:
                    # Linux系统字体
                    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
                    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
                except:
                    title_font = ImageFont.load_default()
                    subtitle_font = ImageFont.load_default()
            
            # 准备标题文字（自动换行）
            display_title = title[:20] + "..." if len(title) > 20 else title
            
            # 计算标题位置（居中偏左）
            bbox = draw.textbbox((0, 0), display_title, font=title_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # 标题位置：左侧 80px，垂直居中偏上
            x = 80
            y = (height - text_height) // 2 - 20
            
            # 绘制标题背景光晕
            for offset in range(20, 0, -5):
                alpha = int(30 * (20 - offset) / 20)
                draw.text((x, y), display_title, font=title_font, 
                         fill=(255, 255, 255, alpha))
            
            # 绘制主标题
            draw.text((x, y), display_title, font=title_font, fill='white')
            
            # 添加副标题
            date_text = datetime.now().strftime("%Y年%m月%d日")
            bbox2 = draw.textbbox((0, 0), date_text, font=subtitle_font)
            date_y = y + text_height + 20
            draw.text((x, date_y), date_text, font=subtitle_font, fill=(255, 255, 255, 200))
            
            # 添加装饰性图标/标志（右下角）
            icon_text = "AI生成"
            bbox3 = draw.textbbox((0, 0), icon_text, font=subtitle_font)
            icon_x = width - bbox3[2] - 40
            icon_y = height - 60
            
            # 绘制圆角矩形背景
            padding = 15
            draw.rounded_rectangle(
                [icon_x - padding, icon_y - padding, 
                 icon_x + bbox3[2] + padding, icon_y + bbox3[3] + padding],
                radius=20,
                fill=(255, 255, 255, 50)
            )
            draw.text((icon_x, icon_y), icon_text, font=subtitle_font, fill='white')
            
            # 保存
            img_path = f'/tmp/cover_local_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            img.save(img_path, quality=95)
            
            return img_path
            
        except ImportError:
            raise ImportError("需要安装Pillow库: pip install Pillow")


# 快捷函数
def generate_cover(title: str, style: str = "auto", openai_api_key: str = None) -> str:
    """
    快捷生成封面图
    
    Args:
        title: 文章标题
        style: auto/ai/local
        openai_api_key: OpenAI API Key（可选）
        
    Returns:
        图片路径
    """
    generator = CoverGenerator(openai_api_key)
    return generator.generate(title, style)
