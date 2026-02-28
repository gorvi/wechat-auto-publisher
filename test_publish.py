#!/usr/bin/env python3
"""
测试发布脚本 - 验证微信文章发布功能
"""

import sys
import os

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.publisher import WeChatAutoPublisher


def test_token_only():
    """仅测试获取Token（不发布）"""
    print("🧪 测试获取Access Token")
    print("=" * 60)
    
    try:
        publisher = WeChatAutoPublisher()
        token = publisher._refresh_token()
        print(f"✅ Token获取成功: {token[:20]}...")
        print(f"   有效期: 7200秒（2小时）")
        return True
    except Exception as e:
        print(f"❌ Token获取失败: {e}")
        return False


def test_basic_publish(publish_now=False):
    """测试基础发布功能"""
    action = "发布" if publish_now else "保存草稿"
    print(f"🧪 测试微信文章{action}功能")
    print("=" * 60)
    
    # 测试内容
    test_title = f"测试文章 - {__import__('datetime').datetime.now().strftime('%m月%d日 %H:%M')}"
    test_content = """# 欢迎使用 WeChat Auto Publisher

这是一篇测试文章，用于验证自动发布功能。

## 功能特性

- ✅ Markdown转HTML
- ✅ 自动排版
- ✅ 微信API集成

## 代码示例

```python
from wechat_auto_publisher import WeChatAutoPublisher

publisher = WeChatAutoPublisher()
publisher.publish_article(
    title="标题",
    markdown_content="# 内容",
    publish=False  # 只存草稿箱
)
```

## 下一步

1. 配置环境变量
2. 运行测试脚本
3. 登录微信公众平台审核发布

---

*本文由 WeChat Auto Publisher 自动生成*
"""
    
    try:
        # 初始化发布器
        print("📱 初始化发布器...")
        publisher = WeChatAutoPublisher()
        print("✅ 初始化成功\n")
        
        # 发布文章（默认只存草稿箱）
        print(f"📝 准备{action}: {test_title}")
        success, media_id, publish_id = publisher.publish_article(
            title=test_title,
            markdown_content=test_content,
            verbose=True,
            publish=publish_now  # False=存草稿, True=直接发布
        )
        
        if success:
            print("\n" + "=" * 60)
            if publish_now:
                print("🎉 测试通过！文章已发布")
            else:
                print("🎉 测试通过！文章已保存到草稿箱")
                print("请登录微信公众平台查看并发布")
            return True
        else:
            print("\n❌ 测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='测试微信文章发布')
    parser.add_argument('--token-only', action='store_true', help='仅测试获取Token')
    parser.add_argument('--publish', '-p', action='store_true', help='直接发布（默认只存草稿箱）')
    args = parser.parse_args()
    
    if args.token_only:
        success = test_token_only()
    else:
        success = test_basic_publish(publish_now=args.publish)
    
    sys.exit(0 if success else 1)
