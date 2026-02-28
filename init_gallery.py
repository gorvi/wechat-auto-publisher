#!/usr/bin/env python3
"""
初始化本地封面库

为中国用户设计的方案：
- 无需代理访问国外网站
- 完全免费
- 质量可控（自己选择喜欢的图片）
- 国内访问无障碍
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.local_gallery import setup_default_covers


def main():
    print("🏠 本地封面库初始化")
    print("=" * 70)
    
    gallery = setup_default_covers("covers")
    
    print("\n" + "=" * 70)
    print("📋 下一步操作")
    print("=" * 70)
    
    print("""
方式1：手动下载图片（推荐）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 访问以下国内可访问的网站下载图片：
   
   🔹 站酷 (zcool.com.cn)
      - 搜索"科技背景"、"商务背景"、"抽象背景"
      - 选择喜欢的作品下载
   
   🔹 花瓣网 (huaban.com)  
      - 搜索"封面背景"、"PPT背景"
      - 收藏并下载高清图片
   
   🔹 视觉中国 (vcg.com)
      - 免费专区有大量可商用图片
   
   🔹 Pixabay (pixabay.com)
      - 国内可以访问
      - 完全免费可商用

2. 将下载的图片放入对应目录：
   
   covers/
   ├── tech/          ← 科技/AI/编程类文章
   ├── business/      ← 商务/创业类文章  
   ├── design/        ← 设计/创意类文章
   ├── nature/        ← 自然/生活类文章
   └── abstract/      ← 抽象/通用类文章

3. 图片要求：
   - 格式：JPG、PNG
   - 建议尺寸：大于 900x383（程序会自动裁剪）
   - 数量：每个主题 5-10 张即可


方式2：使用现有图片
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
如果你已经有喜欢的图片，直接复制到 covers/ 目录即可


方式3：继续使用自动下载
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
如果不想准备图片，程序会自动使用：
- 备用图库（Picsum）- 国外但国内可访问
- 本地模板（程序生成）- 无需网络
""")
    
    print("=" * 70)
    print("✅ 封面库初始化完成！")
    print("=" * 70)
    
    # 检查当前封面数量
    count = gallery.get_count()
    if count == 0:
        print(f"\n⚠️ 当前封面库为空（{count} 张）")
        print("💡 建议：先下载 10-20 张喜欢的图片放入 covers/ 目录")
    else:
        print(f"\n📊 当前封面库：{count} 张图片")
        print("✅ 可以开始使用了！")
    
    print("\n📖 使用文档：docs/LOCAL_GALLERY.md")


if __name__ == "__main__":
    main()
