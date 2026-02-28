"""
Advanced Cover Generator
高级封面图生成器

版本：v2.0 - 精致优化版
"""

import os
import random
import math
from typing import Optional, Tuple
from datetime import datetime


class AdvancedCoverGenerator:
    """
    高级封面图生成器
    
    两种模式：
    1. 本地精致模板（Pillow）- 当前使用
    2. AI生成（DALL-E 3）- Pro功能
    """
    
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        
        # 专业配色方案
        self.color_schemes = {
            "tech_blue": {
                "name": "科技蓝",
                "gradient": [("#0f2027", "#203a43"), ("#2c5364", "#203a43")],
                "accent": "#00d2ff",
                "text": "#ffffff"
            },
            "purple_dream": {
                "name": "梦幻紫",
                "gradient": [("#1a1a2e", "#16213e"), ("#0f3460", "#533483")],
                "accent": "#e94560",
                "text": "#ffffff"
            },
            "green_energy": {
                "name": "活力绿",
                "gradient": [("#134e5e", "#71b280"), ("#56ab2f", "#a8e063")],
                "accent": "#f0f2f0",
                "text": "#ffffff"
            },
            "dark_elegant": {
                "name": "深邃黑",
                "gradient": [("#000000", "#434343"), ("#232526", "#414345")],
                "accent": "#ffd700",
                "text": "#ffffff"
            },
            "orange_warm": {
                "name": "暖阳橙",
                "gradient": [("#3a1c71", "#d76d77"), ("#ffaf7b", "#ff9068")],
                "accent": "#ffffff",
                "text": "#ffffff"
            }
        }
    
    def generate(self, title: str, style: str = "local", theme: str = None) -> str:
        """
        生成封面图
        
        Args:
            title: 文章标题
            style: local/ai/auto
            theme: 配色主题 (tech_blue/purple_dream/green_energy/dark_elegant/orange_warm)
            
        Returns:
            图片本地路径
        """
        if style == "ai" and self.openai_api_key:
            return self._generate_ai(title)
        else:
            return self._generate_local(title, theme)
    
    def _generate_local(self, title: str, theme: str = None) -> str:
        """
        本地生成精致封面
        
        优化点：
        1. 更精致的渐变背景
        2. 更克制的装饰元素
        3. 更好的文字排版
        4. 标题完整显示（自动缩放）
        """
        from PIL import Image, ImageDraw, ImageFont, ImageFilter
        
        # 画布尺寸
        width, height = 900, 383
        
        # 选择主题
        if theme and theme in self.color_schemes:
            scheme = self.color_schemes[theme]
        else:
            scheme = random.choice(list(self.color_schemes.values()))
        
        # 创建渐变背景
        img = Image.new('RGB', (width, height), color=scheme["gradient"][0][0])
        draw = ImageDraw.Draw(img)
        
        # 绘制平滑渐变
        for y in range(height):
            ratio = y / height
            
            # 多阶段渐变
            if ratio < 0.5:
                local_ratio = ratio * 2
                color1 = scheme["gradient"][0][0]
                color2 = scheme["gradient"][0][1]
            else:
                local_ratio = (ratio - 0.5) * 2
                color1 = scheme["gradient"][1][0]
                color2 = scheme["gradient"][1][1]
            
            r = int(int(color1[1:3], 16) * (1 - local_ratio) + int(color2[1:3], 16) * local_ratio)
            g = int(int(color1[3:5], 16) * (1 - local_ratio) + int(color2[3:5], 16) * local_ratio)
            b = int(int(color1[5:7], 16) * (1 - local_ratio) + int(color2[5:7], 16) * local_ratio)
            
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # 添加微妙的网格纹理
        for x in range(0, width, 50):
            draw.line([(x, 0), (x, height)], fill=(255, 255, 255, 8), width=1)
        for y in range(0, height, 50):
            draw.line([(0, y), (width, y)], fill=(255, 255, 255, 8), width=1)
        
        # 添加精致的装饰圆点（更少、更小、更透明）
        for _ in range(8):
            x = random.randint(50, width - 50)
            y = random.randint(50, height - 50)
            radius = random.randint(30, 80)
            
            # 创建圆形渐变效果
            for r in range(radius, 0, -5):
                alpha = int(15 * (r / radius))
                draw.ellipse([x-r, y-r, x+r, y+r], 
                           fill=(255, 255, 255, alpha))
        
        # 添加发光线条
        for _ in range(3):
            x1 = random.randint(0, width // 2)
            y1 = random.randint(0, height)
            x2 = x1 + random.randint(200, 400)
            y2 = y1 + random.randint(-100, 100)
            
            # 发光效果
            for offset in range(5, 0, -1):
                alpha = int(20 * (5 - offset) / 5)
                draw.line([(x1, y1), (x2, y2)], 
                         fill=(255, 255, 255, alpha), 
                         width=offset)
        
        # 添加几何形状装饰（右下角）
        # 六边形
        center_x, center_y = width - 150, height - 100
        size = 60
        points = []
        for i in range(6):
            angle = math.pi / 3 * i - math.pi / 6
            x = center_x + size * math.cos(angle)
            y = center_y + size * math.sin(angle)
            points.append((x, y))
        
        draw.polygon(points, outline=scheme["accent"], width=2)
        draw.polygon(points, fill=(255, 255, 255, 20))
        
        # 加载字体
        title_font, subtitle_font = self._load_fonts()
        
        # 处理标题文字
        display_title = self._format_title(title)
        
        # 计算标题位置（左侧，垂直居中）
        margin_left = 80
        margin_top = 120
        
        # 绘制标题光晕背景
        title_bbox = draw.textbbox((0, 0), display_title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_height = title_bbox[3] - title_bbox[1]
        
        # 光晕效果
        for offset in range(30, 0, -5):
            alpha = int(10 * (30 - offset) / 30)
            draw.rounded_rectangle(
                [margin_left - offset, margin_top - offset,
                 margin_left + title_width + offset, margin_top + title_height + offset],
                radius=10,
                fill=(255, 255, 255, alpha)
            )
        
        # 绘制主标题
        draw.text((margin_left, margin_top), display_title, 
                 font=title_font, fill=scheme["text"])
        
        # 添加副标题
        date_text = datetime.now().strftime("%Y年%m月%d日")
        subtitle_y = margin_top + title_height + 25
        draw.text((margin_left, subtitle_y), date_text, 
                 font=subtitle_font, fill=(255, 255, 255, 200))
        
        # 添加装饰线
        line_y = subtitle_y + 40
        draw.line([(margin_left, line_y), (margin_left + 60, line_y)], 
                 fill=scheme["accent"], width=3)
        
        # 添加分类标签（右下角）
        tag_text = "AI生成"
        tag_bbox = draw.textbbox((0, 0), tag_text, font=subtitle_font)
        tag_width = tag_bbox[2] - tag_bbox[0]
        tag_height = tag_bbox[3] - tag_bbox[1]
        
        tag_x = width - tag_width - 100
        tag_y = height - 80
        padding = 12
        
        # 标签背景
        draw.rounded_rectangle(
            [tag_x - padding, tag_y - padding,
             tag_x + tag_width + padding, tag_y + tag_height + padding],
            radius=15,
            fill=(255, 255, 255, 30),
            outline=scheme["accent"],
            width=1
        )
        
        draw.text((tag_x, tag_y), tag_text, 
                 font=subtitle_font, fill='white')
        
        # 应用轻微模糊使整体更柔和
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # 保存
        img_path = f'/tmp/cover_v2_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        img.save(img_path, quality=95)
        
        return img_path
    
    def _load_fonts(self) -> Tuple:
        """加载中文字体"""
        from PIL import ImageFont
        
        # 尝试加载中文字体
        font_paths = [
            # macOS
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
            # Linux
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            # Windows
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simsun.ttc",
        ]
        
        title_font = None
        subtitle_font = None
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    title_font = ImageFont.truetype(font_path, 42)
                    subtitle_font = ImageFont.truetype(font_path, 20)
                    break
                except:
                    continue
        
        # 回退到默认字体
        if title_font is None:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        return title_font, subtitle_font
    
    def _format_title(self, title: str, max_length: int = 16) -> str:
        """
        格式化标题，确保完整显示
        
        Args:
            title: 原始标题
            max_length: 最大字符数
            
        Returns:
            格式化后的标题
        """
        # 移除多余空格
        title = title.strip()
        
        # 如果标题太长，截取并添加省略号
        if len(title) > max_length:
            return title[:max_length] + "..."
        
        return title
    
    def _generate_ai(self, title: str) -> str:
        """
        使用DALL-E 3生成AI封面
        
        模型：DALL-E 3
        尺寸：1792x1024（横向）
        质量：标准
        
        特点：
        - 根据标题智能生成相关图像
        - 专业级视觉设计
        - 与文章内容高度相关
        """
        try:
            from openai import OpenAI
            import requests
            
            client = OpenAI(api_key=self.openai_api_key)
            
            # 构建提示词
            prompt = self._create_ai_prompt(title)
            
            print(f"🎨 使用 DALL-E 3 生成封面...")
            print(f"   标题: {title}")
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1792x1024",
                quality="standard",
                n=1
            )
            
            # 下载图片
            image_url = response.data[0].url
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            
            # 保存
            img_path = f'/tmp/cover_ai_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            with open(img_path, 'wb') as f:
                f.write(img_response.content)
            
            print(f"✅ AI封面生成成功 (DALL-E 3)")
            return img_path
            
        except ImportError:
            print("⚠️ 未安装openai库，使用本地模板")
            return self._generate_local(title)
        except Exception as e:
            print(f"⚠️ AI生成失败: {e}，使用本地模板")
            return self._generate_local(title)
    
    def _create_ai_prompt(self, title: str) -> str:
        """创建DALL-E提示词"""
        # 提取主题
        keywords = self._extract_keywords(title)
        
        prompt = f"""Create a professional, modern WeChat article cover image.

Article Title: "{title}"
Key Themes: {keywords}

Design Requirements:
- Modern, minimalist professional style
- Wide banner format (16:9 aspect ratio)
- Suitable for tech/business blog
- Clean composition with space for text overlay
- Abstract or conceptual representation of the theme
- NO text in the image
- High quality, polished look

Visual Style:
- Contemporary flat design with subtle gradients
- Professional color palette (blues, purples, or modern tech colors)
- Clean geometric elements or abstract illustrations
- Balanced composition

Mood: Professional, innovative, trustworthy, engaging.
"""
        return prompt.strip()
    
    def _extract_keywords(self, title: str) -> str:
        """从标题提取关键词"""
        tech_keywords = ["AI", "人工智能", "自动化", "编程", "代码", "开发", 
                        "技术", "工具", "效率", "工作流", "产品", "创业"]
        
        found = [kw for kw in tech_keywords if kw in title]
        
        if not found:
            return "technology, innovation"
        
        return ", ".join(found[:3])


# 快捷函数
def generate_cover(title: str, style: str = "local", theme: str = None, 
                   openai_api_key: str = None) -> str:
    """
    快捷生成封面图
    
    Args:
        title: 文章标题
        style: local/ai
        theme: 配色主题
        openai_api_key: OpenAI API Key（AI模式需要）
        
    Returns:
        图片路径
    """
    generator = AdvancedCoverGenerator(openai_api_key)
    return generator.generate(title, style, theme)
