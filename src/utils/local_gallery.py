"""
Local Cover Gallery
本地封面库

解决国外图库访问慢/不稳定的问题
方案：用户自己准备封面图片，程序随机选择

使用方法：
1. 准备图片：从网上下载喜欢的封面图，放入 covers/ 目录
2. 程序自动从中随机选择作为文章封面
3. 完全免费，国内访问无障碍，质量可控
"""

import os
import random
import shutil
from datetime import datetime
from typing import List, Optional
from PIL import Image


class LocalCoverGallery:
    """
    本地封面库
    
    管理本地封面图片，支持随机选择和自动调整尺寸
    """
    
    # 微信封面推荐尺寸
    COVER_WIDTH = 900
    COVER_HEIGHT = 383
    
    def __init__(self, gallery_path: str = "covers"):
        """
        初始化封面库
        
        Args:
            gallery_path: 封面库目录路径（默认项目根目录下的 covers/）
        """
        self.gallery_path = gallery_path
        
        # 确保目录存在
        if not os.path.exists(self.gallery_path):
            os.makedirs(self.gallery_path)
            print(f"📁 创建封面库目录: {self.gallery_path}")
    
    def add_cover(self, image_path: str, title: str = None) -> str:
        """
        添加封面到库中
        
        Args:
            image_path: 图片路径
            title: 封面标题（用于命名）
            
        Returns:
            保存后的路径
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片不存在: {image_path}")
        
        # 生成文件名
        if title:
            # 清理标题中的特殊字符
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')[:30]  # 限制长度
            filename = f"{safe_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        else:
            filename = f"cover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        
        target_path = os.path.join(self.gallery_path, filename)
        
        # 复制并调整尺寸
        self._process_image(image_path, target_path)
        
        print(f"✅ 封面已添加到库中: {filename}")
        return target_path
    
    def _process_image(self, source_path: str, target_path: str):
        """
        处理图片：调整尺寸为微信封面尺寸
        
        Args:
            source_path: 源图片路径
            target_path: 目标保存路径
        """
        with Image.open(source_path) as img:
            # 转换为RGB（处理PNG等格式）
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # 获取原始尺寸
            width, height = img.size
            
            # 计算裁剪区域（保持比例，居中裁剪）
            target_ratio = self.COVER_WIDTH / self.COVER_HEIGHT
            current_ratio = width / height
            
            if current_ratio > target_ratio:
                # 图片太宽，裁剪左右
                new_width = int(height * target_ratio)
                left = (width - new_width) // 2
                img = img.crop((left, 0, left + new_width, height))
            else:
                # 图片太高，裁剪上下
                new_height = int(width / target_ratio)
                top = (height - new_height) // 2
                img = img.crop((0, top, width, top + new_height))
            
            # 调整尺寸
            img = img.resize((self.COVER_WIDTH, self.COVER_HEIGHT), Image.Resampling.LANCZOS)
            
            # 保存
            img.save(target_path, 'JPEG', quality=95)
    
    def get_random_cover(self, topic: str = None) -> Optional[str]:
        """
        随机获取一张封面
        
        Args:
            topic: 主题（可选，如果图片按主题分类）
            
        Returns:
            封面图片路径，如果没有则返回None
        """
        # 获取所有图片文件
        valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
        
        if topic:
            # 如果指定了主题，先查找主题目录
            topic_dir = os.path.join(self.gallery_path, topic)
            if os.path.exists(topic_dir):
                images = [f for f in os.listdir(topic_dir) 
                         if f.lower().endswith(valid_extensions)]
                if images:
                    return os.path.join(topic_dir, random.choice(images))
        
        # 从主目录随机选择
        images = [f for f in os.listdir(self.gallery_path) 
                 if f.lower().endswith(valid_extensions)]
        
        if not images:
            print(f"⚠️ 封面库为空，请先添加封面图片到 {self.gallery_path}/")
            return None
        
        return os.path.join(self.gallery_path, random.choice(images))
    
    def list_covers(self) -> List[str]:
        """
        列出所有封面
        
        Returns:
            封面文件列表
        """
        valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
        return [f for f in os.listdir(self.gallery_path) 
                if f.lower().endswith(valid_extensions)]
    
    def get_count(self) -> int:
        """获取封面数量"""
        return len(self.list_covers())
    
    def delete_cover(self, filename: str) -> bool:
        """
        删除封面
        
        Args:
            filename: 文件名
            
        Returns:
            是否成功
        """
        filepath = os.path.join(self.gallery_path, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"🗑️ 已删除: {filename}")
            return True
        return False
    
    def generate(self, title: str = None, topic: str = None) -> str:
        """
        生成封面（接口统一方法）
        
        从本地库中随机选择一张封面
        
        Args:
            title: 标题（忽略，仅保持接口一致）
            topic: 主题（可选）
            
        Returns:
            封面图片路径
        """
        cover_path = self.get_random_cover(topic)
        
        if cover_path:
            print(f"✅ 从本地封面库选择: {os.path.basename(cover_path)}")
            return cover_path
        else:
            raise ValueError(
                f"封面库为空！请先将图片放入 {self.gallery_path}/ 目录\n"
                f"建议：下载10-20张喜欢的图片作为封面库"
            )


def setup_default_covers(gallery_path: str = "covers"):
    """
    设置默认封面库
    
    创建示例封面库结构
    """
    gallery = LocalCoverGallery(gallery_path)
    
    # 创建主题子目录
    topics = ["tech", "business", "design", "nature", "abstract"]
    for topic in topics:
        topic_dir = os.path.join(gallery_path, topic)
        if not os.path.exists(topic_dir):
            os.makedirs(topic_dir)
    
    print("📁 封面库结构已创建")
    print(f"   主目录: {gallery_path}/")
    for topic in topics:
        print(f"   - {topic}/")
    
    print("\n💡 使用建议:")
    print("   1. 从以下网站下载免费可商用的图片:")
    print("      - 站酷 (zcool.com.cn)")
    print("      - 花瓣网 (huaban.com)")
    print("      - 视觉中国 (vcg.com) 免费专区")
    print("      - Pixabay (国内可访问)")
    print("   2. 将图片放入对应主题目录")
    print("   3. 程序会自动选择合适的封面")
    
    return gallery


# 快捷函数
def get_local_cover(gallery_path: str = "covers", topic: str = None) -> str:
    """快捷获取本地封面"""
    gallery = LocalCoverGallery(gallery_path)
    return gallery.generate(topic=topic)
