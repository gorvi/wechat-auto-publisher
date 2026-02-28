#!/usr/bin/env python3
"""
测试 Unsplash 封面生成
展示不同主题的真实图片效果
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.unsplash_generator import UnsplashCoverGenerator


def test_unsplash_covers():
    """测试不同主题的 Unsplash 封面"""
    print("🎨 Unsplash 封面生成测试")
    print("=" * 70)
    print("特点：")
    print("  ✅ 免费使用")
    print("  ✅ 高质量真实照片")
    print("  ✅ 比本地模板更美观")
    print("  ✅ 自动裁剪为微信封面尺寸 (900x383)")
    print("=" * 70)
    
    generator = UnsplashCoverGenerator()
    
    # 测试不同主题
    topics = [
        ("tech", "科技/AI/编程"),
        ("business", "商务/办公/创业"),
        ("design", "设计/创意/艺术"),
    ]
    
    results = []
    
    for topic, description in topics:
        print(f"\n📸 生成 {description} 主题封面...")
        print(f"   主题: {topic}")
        
        try:
            img_path = generator.generate(
                title="AI工作流实战指南",
                topic=topic
            )
            
            # 检查文件是否存在和大小
            if os.path.exists(img_path):
                size = os.path.getsize(img_path) / 1024  # KB
                print(f"   ✅ 成功: {img_path}")
                print(f"   📁 文件大小: {size:.1f} KB")
                results.append((topic, img_path, "成功"))
            else:
                print(f"   ❌ 文件未生成")
                results.append((topic, None, "失败"))
                
        except Exception as e:
            print(f"   ❌ 失败: {e}")
            results.append((topic, None, "失败"))
    
    # 总结
    print("\n" + "=" * 70)
    print("📊 测试结果汇总")
    print("=" * 70)
    
    success_count = sum(1 for _, _, status in results if status == "成功")
    print(f"成功: {success_count}/{len(results)}")
    
    for topic, img_path, status in results:
        icon = "✅" if status == "成功" else "❌"
        print(f"{icon} {topic}: {status}")
        if img_path:
            print(f"   文件: {img_path}")
    
    print("\n💡 提示:")
    print("   封面图片保存在 /tmp/ 目录下")
    print("   可以打开查看效果")
    print("   如果 Unsplash 不可用，会自动使用备用图库")
    
    return success_count > 0


def test_smart_generator():
    """测试智能封面生成器"""
    print("\n\n🎨 智能封面生成器测试")
    print("=" * 70)
    print("自动选择最佳封面来源：")
    print("  1. Unsplash（高质量真实图片）")
    print("  2. 本地模板（无需网络）")
    print("=" * 70)
    
    from utils.unsplash_generator import SmartCoverGenerator
    
    generator = SmartCoverGenerator()
    
    print("\n📸 生成封面...")
    try:
        img_path = generator.generate(
            title="AI自动化实战",
            topic="tech",
            prefer="unsplash"
        )
        
        print(f"✅ 成功: {img_path}")
        
        # 显示图片信息
        from PIL import Image
        with Image.open(img_path) as img:
            print(f"   尺寸: {img.size[0]}x{img.size[1]}")
            print(f"   格式: {img.format}")
        
        return True
        
    except Exception as e:
        print(f"❌ 失败: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='测试 Unsplash 封面生成')
    parser.add_argument('--all', '-a', action='store_true', help='测试全部功能')
    parser.add_argument('--smart', '-s', action='store_true', help='测试智能生成器')
    args = parser.parse_args()
    
    success = True
    
    if not args.smart or args.all:
        success = test_unsplash_covers() and success
    
    if args.smart or args.all:
        success = test_smart_generator() and success
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 测试完成！封面图片已生成")
        print("💡 建议：查看生成的图片，确认效果满意")
    else:
        print("⚠️ 部分测试失败，但备用方案可用")
    print("=" * 70)
    
    sys.exit(0 if success else 1)
