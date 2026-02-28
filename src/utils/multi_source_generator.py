"""
Multi-Source Cover Generator
多源封面生成器

优先级（从高到低）：
1. 本地封面库（用户自己准备的图片）
2. Picsum（免费图库，国内可访问）
3. Unsplash Source（备用）
4. 本地模板生成（兜底）

特点：
- 多源随机选择
- 自动降级（失败自动换下一个）
- 完全免费
- 国内访问友好
"""

import os
import random
import requests
from datetime import datetime
from typing import Optional, List


class MultiSourceCoverGenerator:
    """
    多源封面生成器
    
    智能选择和降级机制
    """
    
    def __init__(self, gallery_path: str = "covers"):
        """
        初始化
        
        Args:
            gallery_path: 本地封面库路径
        """
        self.gallery_path = gallery_path
        
        # 定义所有图片来源（按优先级排序）
        self.sources = [
            ("local", self._generate_local),
            ("picsum", self._generate_picsum),
            ("unsplash", self._generate_unsplash),
            ("template", self._generate_template)
        ]
    
    def generate(self, title: str, topic: str = "tech", prefer_source: str = None) -> str:
        """
        生成封面
        
        策略：
        - 如果指定了 prefer_source，优先尝试
        - 否则按优先级顺序尝试
        - 每个源失败自动切换到下一个
        
        Args:
            title: 文章标题
            topic: 主题 (tech/business/design/abstract)
            prefer_source: 优先使用的源 (local/picsum/unsplash/template)
            
        Returns:
            图片本地路径
        """
        print(f"🎨 生成封面: {title[:20]}...")
        print(f"   主题: {topic}")
        
        # 如果指定了优先源，将其放到第一位
        sources = self.sources.copy()
        if prefer_source:
            for i, (name, func) in enumerate(sources):
                if name == prefer_source:
                    sources.insert(0, sources.pop(i))
                    break
        
        # 尝试每个源
        last_error = None
        for source_name, source_func in sources:
            try:
                print(f"   尝试 {source_name}...", end=" ")
                img_path = source_func(topic)
                if img_path and os.path.exists(img_path):
                    print(f"✅ 成功")
                    return img_path
            except Exception as e:
                print(f"❌ 失败")
                last_error = e
                continue
        
        # 所有源都失败了
        raise Exception(f"所有封面源都不可用。最后错误: {last_error}")
    
    def _generate_local(self, topic: str) -> Optional[str]:
        """从本地封面库生成"""
        from .local_gallery import LocalCoverGallery
        
        gallery = LocalCoverGallery(self.gallery_path)
        
        if gallery.get_count() > 0:
            return gallery.generate(topic=topic)
        else:
            raise ValueError("本地封面库为空")
    
    def _generate_picsum(self, topic: str) -> str:
        """
        从 Picsum 生成
        
        Picsum 特点：
        - 免费
        - 国内可访问
        - 质量较高
        """
        seed = random.randint(1, 10000)
        
        # 根据主题选择不同的种子范围（让同一主题图片风格相近）
        topic_seeds = {
            "tech": (1, 2000),
            "business": (2001, 4000),
            "design": (4001, 6000),
            "nature": (6001, 8000),
            "abstract": (8001, 10000)
        }
        
        if topic in topic_seeds:
            min_seed, max_seed = topic_seeds[topic]
            seed = random.randint(min_seed, max_seed)
        
        url = f"https://picsum.photos/seed/{seed}/900/383"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        img_path = f'/tmp/cover_picsum_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
        with open(img_path, 'wb') as f:
            f.write(response.content)
        
        return img_path
    
    def _generate_unsplash(self, topic: str) -> str:
        """
        从 Unsplash Source 生成
        
        注意：Unsplash Source 偶尔不稳定
        """
        keywords = {
            "tech": ["technology", "computer", "digital"],
            "business": ["business", "office", "meeting"],
            "design": ["design", "creative", "art"],
            "nature": ["nature", "landscape", "mountain"],
            "abstract": ["abstract", "geometric", "pattern"]
        }
        
        keyword = random.choice(keywords.get(topic, keywords["tech"]))
        url = f"https://source.unsplash.com/900x383/?{keyword}"
        
        response = requests.get(url, timeout=30, allow_redirects=True)
        response.raise_for_status()
        
        img_path = f'/tmp/cover_unsplash_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
        with open(img_path, 'wb') as f:
            f.write(response.content)
        
        return img_path
    
    def _generate_template(self, topic: str) -> str:
        """使用本地模板生成"""
        from .cover_generator import AdvancedCoverGenerator
        
        generator = AdvancedCoverGenerator()
        return generator.generate("封面", style="local")
    
    def test_all_sources(self) -> dict:
        """
        测试所有封面源
        
        Returns:
            各源状态报告
        """
        results = {}
        
        print("🧪 测试所有封面源")
        print("=" * 60)
        
        for source_name, source_func in self.sources:
            try:
                print(f"\n测试 {source_name}...", end=" ")
                img_path = source_func("tech")
                if img_path and os.path.exists(img_path):
                    size = os.path.getsize(img_path) / 1024
                    print(f"✅ 成功 ({size:.1f} KB)")
                    results[source_name] = {"status": "ok", "path": img_path}
                else:
                    print(f"❌ 失败")
                    results[source_name] = {"status": "failed", "error": "No image generated"}
            except Exception as e:
                print(f"❌ 失败: {str(e)[:50]}")
                results[source_name] = {"status": "failed", "error": str(e)}
        
        print("\n" + "=" * 60)
        print("📊 测试结果汇总")
        print("=" * 60)
        
        for name, result in results.items():
            icon = "✅" if result["status"] == "ok" else "❌"
            print(f"{icon} {name}")
        
        return results


# 快捷函数
def generate_cover(title: str, topic: str = "tech", prefer_source: str = None) -> str:
    """
    快捷生成封面
    
    多源智能选择，自动降级
    
    Args:
        title: 文章标题
        topic: 主题
        prefer_source: 优先源
        
    Returns:
        图片路径
    """
    generator = MultiSourceCoverGenerator()
    return generator.generate(title, topic, prefer_source)


def test_sources():
    """测试所有封面源"""
    generator = MultiSourceCoverGenerator()
    return generator.test_all_sources()
