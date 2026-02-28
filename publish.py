#!/usr/bin/env python3
"""
命令行发布工具

Usage:
    python publish.py "文章标题" "content.md"
    python publish.py "标题" --content "# 正文内容"
    python publish.py --topic "AI编程" --ai-generate
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.publisher import WeChatAutoPublisher


def publish_from_file(title, file_path):
    """从Markdown文件发布"""
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    publisher = WeChatAutoPublisher()
    return publisher.publish_article(title, content)


def publish_from_text(title, content):
    """从文本发布"""
    publisher = WeChatAutoPublisher()
    return publisher.publish_article(title, content)


def main():
    parser = argparse.ArgumentParser(
        description='微信公众号文章发布工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "测试文章" article.md
  %(prog)s "测试文章" --content "# 标题\\n\\n正文"
  %(prog)s --topic "AI编程" --ai-generate
        """
    )
    
    parser.add_argument('title', nargs='?', help='文章标题')
    parser.add_argument('file', nargs='?', help='Markdown文件路径')
    parser.add_argument('--content', '-c', help='直接输入Markdown内容')
    parser.add_argument('--topic', '-t', help='文章主题（用于AI生成）')
    parser.add_argument('--ai-generate', action='store_true', help='使用AI生成内容（Pro功能）')
    parser.add_argument('--author', '-a', help='作者名')
    
    args = parser.parse_args()
    
    # 验证参数
    if not args.topic and not args.title:
        parser.print_help()
        return 1
    
    # AI生成模式
    if args.ai_generate or args.topic:
        print("🤖 AI生成模式（需要Pro授权）")
        print("   开源版请直接提供文章内容")
        return 0
    
    # 发布模式
    try:
        if args.file:
            # 从文件发布
            print(f"📄 从文件发布: {args.file}")
            success = publish_from_file(args.title, args.file)
        elif args.content:
            # 从文本发布
            print(f"📝 从文本发布")
            success = publish_from_text(args.title, args.content)
        else:
            print("❌ 请提供文件路径或内容")
            parser.print_help()
            return 1
        
        return 0 if success else 1
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
