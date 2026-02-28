"""
Unsplash Cover Generator
Unsplash 免费图库封面生成器

使用 Unsplash 高质量免费图片作为封面
特点：
- 完全免费
- 高质量真实图片
- 自动裁剪为微信封面尺寸（900x383）
- 无需 API Key（使用随机图片 URL）
"""

import os
import requests
import random
from typing import Optional
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


class UnsplashCoverGenerator:
    """
    Unsplash 封面生成器
    
    两种方式：
    1. 直接下载随机图片（无需API Key）
    2. 使用 Unsplash API 搜索特定主题（需要 Access Key）
    """
    
    # Unsplash 图片主题关键词映射
    TOPIC_KEYWORDS = {
        "tech": ["technology", "computer", "code", "digital", "innovation", "ai", "robot"],
        "business": ["business", "office", "meeting", "workspace", "startup", "entrepreneur"],
        "design": ["design", "creative", "art", "graphic", "minimal", "aesthetic"],
        "nature": ["nature", "landscape", "mountain", "ocean", "forest", "sky"],
        "city": ["city", "architecture", "building", "urban", "skyline", "street"],
        "people": ["people", "working", "team", "collaboration", "thinking", "creative"],
        "abstract": ["abstract", "geometric", "pattern", "texture", "gradient", "colorful"]
    }
    
    def __init__(self, access_key: str = None):
        """
        初始化
        
        Args:
            access_key: Unsplash Access Key（可选，用于搜索API）
        """
        self.access_key = access_key or os.getenv("UNSPLASH_ACCESS_KEY")
    
    def generate(self, title: str, topic: str = "tech", style: str = "random") -> str:
        """
        生成封面
        
        Args:
            title: 文章标题（用于选择相关主题）
            topic: 主题类别 (tech/business/design/nature/city/people/abstract)
            style: random/featured/search
            
        Returns:
            图片本地路径
        """
        if style == "search" and self.access_key:
            return self._generate_by_search(title, topic)
        else:
            return self._generate_random(topic)
    
    def _generate_random(self, topic: str = "tech") -> str:
        """
        使用 Unsplash 随机图片
        
        无需 API Key，直接下载随机图片
        """
        # 选择关键词
        keywords = self.TOPIC_KEYWORDS.get(topic, self.TOPIC_KEYWORDS["tech"])
        keyword = random.choice(keywords)
        
        print(f"🎨 从 Unsplash 获取图片...")
        print(f"   主题: {topic}")
        print(f"   关键词: {keyword}")
        
        # Unsplash 随机图片 URL
        # 参数：
        # - w=900, h=383: 微信封面尺寸
        # - fit=crop: 裁剪填充
        # - q=80: 图片质量
        unsplash_url = f"https://source.unsplash.com/900x383/?{keyword}"
        
        # 备用方案：使用 picsum.photos（如果 Unsplash source 不可用）
        # unsplash_url = f"https://picsum.photos/900/383?random={random.randint(1, 1000)}"
        
        try:
            # 下载图片
            response = requests.get(unsplash_url, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            # 保存临时文件
            img_path = f'/tmp/cover_unsplash_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
            with open(img_path, 'wb') as f:
                f.write(response.content)
            
            # 验证图片尺寸
            with Image.open(img_path) as img:
                width, height = img.size
                print(f"   下载尺寸: {width}x{height}")
                
                # 如果尺寸不对，调整尺寸
                if width != 900 or height != 383:
                    img = img.resize((900, 383), Image.Resampling.LANCZOS)
                    img.save(img_path, quality=95)
                    print(f"   已调整至: 900x383")
            
            print(f"✅ Unsplash 封面下载成功")
            return img_path
            
        except Exception as e:
            print(f"⚠️ Unsplash 下载失败: {e}")
            print(f"   使用备用方案...")
            return self._generate_fallback(topic)
    
    def _generate_by_search(self, title: str, topic: str) -> str:
        """
        使用 Unsplash API 搜索特定图片
        
        需要 Access Key
        """
        if not self.access_key:
            raise ValueError("使用搜索功能需要提供 Unsplash Access Key")
        
        # 选择关键词
        keywords = self.TOPIC_KEYWORDS.get(topic, self.TOPIC_KEYWORDS["tech"])
        query = random.choice(keywords)
        
        print(f"🔍 使用 Unsplash API 搜索...")
        print(f"   关键词: {query}")
        
        # Unsplash API 搜索
        url = "https://api.unsplash.com/search/photos"
        params = {
            "query": query,
            "per_page": 10,
            "orientation": "landscape",  # 横向图片
            "client_id": self.access_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data["results"]:
                # 随机选择一张图片
                photo = random.choice(data["results"])
                photo_url = photo["urls"]["regular"]  # 或 "small", "full"
                
                print(f"   选择图片: {photo['alt_description'] or 'No description'}")
                
                # 下载图片
                img_response = requests.get(photo_url, timeout=30)
                img_response.raise_for_status()
                
                # 保存
                img_path = f'/tmp/cover_unsplash_api_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
                with open(img_path, 'wb') as f:
                    f.write(img_response.content)
                
                # 调整尺寸
                with Image.open(img_path) as img:
                    img = img.resize((900, 383), Image.Resampling.LANCZOS)
                    img.save(img_path, quality=95)
                
                print(f"✅ Unsplash API 封面生成成功")
                return img_path
            else:
                raise Exception("未找到相关图片")
                
        except Exception as e:
            print(f"⚠️ API 搜索失败: {e}")
            return self._generate_random(topic)
    
    def _generate_fallback(self, topic: str) -> str:
        """
        备用方案：使用 Lorem Picsum
        
        另一个免费图库服务
        """
        print(f"🔄 使用备用图库...")
        
        seed = random.randint(1, 10000)
        url = f"https://picsum.photos/seed/{seed}/900/383"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            img_path = f'/tmp/cover_fallback_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
            with open(img_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ 备用封面下载成功")
            return img_path
            
        except Exception as e:
            print(f"❌ 备用方案也失败了: {e}")
            # 最后 fallback：使用本地模板
            from .cover_generator import AdvancedCoverGenerator
            generator = AdvancedCoverGenerator()
            return generator.generate("封面", style="local")
    
    def download_specific(self, unsplash_id: str) -> str:
        """
        下载特定的 Unsplash 图片
        
        Args:
            unsplash_id: 图片ID（从 Unsplash 网站 URL 获取）
            
        Returns:
            图片路径
        """
        # 例如：https://unsplash.com/photos/abc123 -> abc123
        url = f"https://source.unsplash.com/{unsplash_id}/900x383"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        img_path = f'/tmp/cover_unsplash_id_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
        with open(img_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ 特定图片下载成功: {unsplash_id}")
        return img_path


class SmartCoverGenerator:
    """
    智能封面生成器
    
    自动选择最佳封面来源：
    1. Unsplash（免费高质量图片）
    2. 本地高级模板（无需网络）
    """
    
    def __init__(self, unsplash_key: str = None):
        self.unsplash_gen = UnsplashCoverGenerator(unsplash_key)
    
    def generate(self, title: str, topic: str = "tech", prefer: str = "unsplash") -> str:
        """
        生成封面
        
        Args:
            title: 文章标题
            topic: 主题
            prefer: 首选来源 (unsplash/local)
            
        Returns:
            图片路径
        """
        if prefer == "unsplash":
            try:
                return self.unsplash_gen.generate(title, topic, style="random")
            except Exception as e:
                print(f"⚠️ Unsplash 失败，使用本地模板: {e}")
                from .cover_generator import AdvancedCoverGenerator
                generator = AdvancedCoverGenerator()
                return generator.generate(title, style="local")
        else:
            from .cover_generator import AdvancedCoverGenerator
            generator = AdvancedCoverGenerator()
            return generator.generate(title, style="local")


# 快捷函数
def generate_cover_unsplash(title: str, topic: str = "tech", access_key: str = None) -> str:
    """
    快捷生成 Unsplash 封面
    
    Args:
        title: 标题
        topic: 主题 (tech/business/design/nature/city/people/abstract)
        access_key: 可选的 Unsplash Access Key
        
    Returns:
        图片路径
    """
    generator = UnsplashCoverGenerator(access_key)
    return generator.generate(title, topic)
