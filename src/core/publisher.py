"""
WeChat Auto Publisher - Core Module
微信公众号自动发布工具 - 核心模块
"""

import requests
import json
import os
import re
import time
from datetime import datetime
from typing import Optional, Dict, Any


class WeChatAPIError(Exception):
    """微信API错误"""
    pass


class WeChatAutoPublisher:
    """
    微信公众号自动发布器

    功能：
    - 获取Access Token
    - 上传封面图和图文素材
    - 发布文章
    - Markdown转HTML
    """

    def __init__(self, app_id: str = None, app_secret: str = None):
        """
        初始化发布器

        Args:
            app_id: 微信公众号AppID，默认从环境变量读取
            app_secret: 微信公众号AppSecret，默认从环境变量读取
        """
        self.app_id = app_id or os.getenv("WECHAT_APP_ID")
        self.app_secret = app_secret or os.getenv("WECHAT_APP_SECRET")

        if not self.app_id or not self.app_secret:
            raise ValueError(
                "请提供app_id和app_secret，或设置环境变量 "
                "WECHAT_APP_ID 和 WECHAT_APP_SECRET"
            )

        self.access_token: Optional[str] = None
        self.token_expires: int = 0

    def _ensure_token(self) -> str:
        """确保Access Token有效"""
        if not self.access_token or time.time() > self.token_expires - 300:
            self._refresh_token()
        return self.access_token

    def _refresh_token(self) -> str:
        """
        刷新Access Token

        Returns:
            新的Access Token

        Raises:
            WeChatAPIError: 获取Token失败
        """
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret
        }

        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            if "access_token" in data:
                self.access_token = data["access_token"]
                expires_in = data.get("expires_in", 7200)
                self.token_expires = time.time() + expires_in
                return self.access_token
            else:
                error_msg = data.get("errmsg", "Unknown error")
                raise WeChatAPIError(f"获取Access Token失败: {error_msg}")

        except requests.RequestException as e:
            raise WeChatAPIError(f"请求失败: {e}")

    def create_default_cover(self, title: str = "Article") -> str:
        """
        创建默认封面图

        优先级：
        1. 本地封面库（推荐，国内访问快）
        2. Unsplash/Picsum（备用）
        3. 本地模板（兜底）

        Args:
            title: 文章标题

        Returns:
            图片本地路径
        """
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

        # 1. 优先使用本地封面库（国内用户推荐）
        try:
            from utils.local_gallery import LocalCoverGallery
            gallery = LocalCoverGallery("covers")
            if gallery.get_count() > 0:
                return gallery.generate(topic="tech")
            else:
                print("⚠️ 本地封面库为空，尝试其他方案...")
        except Exception as e:
            print(f"⚠️ 本地封面库不可用: {e}")

        # 2. 尝试 Unsplash（国外图库）
        try:
            from utils.unsplash_generator import UnsplashCoverGenerator
            generator = UnsplashCoverGenerator()
            return generator.generate(title, topic="tech")
        except Exception as e:
            print(f"⚠️ Unsplash 不可用: {e}")

        # 3. 兜底：使用本地模板生成
        print("🎨 使用本地模板生成封面...")
        from utils.cover_generator import AdvancedCoverGenerator
        generator = AdvancedCoverGenerator()
        return generator.generate(title, style="local")

    def upload_image(self, image_path: str) -> str:
        """
        上传图片到微信素材库

        Args:
            image_path: 图片本地路径

        Returns:
            图片的media_id

        Raises:
            WeChatAPIError: 上传失败
            FileNotFoundError: 文件不存在
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片不存在: {image_path}")

        token = self._ensure_token()
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"

        with open(image_path, 'rb') as f:
            files = {'media': f}
            resp = requests.post(url, files=files, timeout=30)

        data = resp.json()
        if "media_id" in data:
            return data["media_id"]
        else:
            error_msg = data.get("errmsg", "Unknown error")
            raise WeChatAPIError(f"上传图片失败: {error_msg}")

    def markdown_to_html(self, markdown_content: str) -> str:
        """
        Markdown转微信HTML

        Args:
            markdown_content: Markdown格式内容

        Returns:
            微信格式的HTML
        """
        try:
            import markdown
            html = markdown.markdown(
                markdown_content,
                extensions=['tables', 'fenced_code', 'toc']
            )
        except ImportError:
            # 简单转换（如果没有markdown库）
            html = self._simple_markdown_to_html(markdown_content)

        return self._apply_wechat_style(html)

    def _simple_markdown_to_html(self, markdown_content: str) -> str:
        """简单的Markdown转HTML（备用）"""
        # 标题
        content = markdown_content
        content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)

        # 粗体、斜体
        content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)

        # 段落
        paragraphs = content.split('\n\n')
        content = '\n'.join(f'<p>{p}</p>' if not p.startswith('<') else p for p in paragraphs)

        return content

    def _apply_wechat_style(self, html: str) -> str:
        """应用微信文章样式"""
        style = """
        <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.8;
            color: #333;
            font-size: 16px;
            max-width: 100%;
        }
        h1 {
            font-size: 24px;
            font-weight: bold;
            margin: 24px 0 16px;
            color: #1a1a1a;
        }
        h2 {
            font-size: 20px;
            font-weight: bold;
            margin: 20px 0 12px;
            color: #2c2c2c;
        }
        h3 {
            font-size: 18px;
            font-weight: bold;
            margin: 16px 0 10px;
            color: #333;
        }
        p { margin: 12px 0; line-height: 1.8; }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
            font-size: 14px;
        }
        pre {
            background: #f8f8f8;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
        }
        blockquote {
            border-left: 4px solid #1890ff;
            padding: 12px 16px;
            background: #f0f7ff;
            margin: 16px 0;
            color: #555;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
        }
        th, td {
            border: 1px solid #e8e8e8;
            padding: 12px;
            text-align: left;
        }
        th { background: #fafafa; font-weight: bold; }
        img { max-width: 100%; height: auto; }
        </style>
        """

        return f"<!DOCTYPE html><html><head>{style}</head><body>{html}</body></html>"

    def upload_draft(
        self,
        title: str,
        html_content: str,
        thumb_media_id: str,
        author: str = None,
        content_source_url: str = ""
    ) -> str:
        """
        上传图文草稿

        Args:
            title: 文章标题
            html_content: HTML格式内容
            thumb_media_id: 封面图media_id（必需）
            author: 作者名
            content_source_url: 原文链接

        Returns:
            草稿的media_id

        Raises:
            WeChatAPIError: 上传失败
        """
        if not thumb_media_id:
            raise WeChatAPIError("封面图media_id是必需的，请先上传封面图")

        token = self._ensure_token()
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"

        # 生成摘要
        digest = re.sub(r'<[^>]+>', '', html_content)[:100] + "..."

        # 构建文章数据
        article = {
            "title": title,
            "thumb_media_id": thumb_media_id,
            "author": author or os.getenv("DEFAULT_AUTHOR", "AI助手"),
            "digest": digest,
            "content": html_content,
            "content_source_url": content_source_url,
            "need_open_comment": 1,
            "only_fans_can_comment": 0
        }

        articles = [article]

        # 使用 ensure_ascii=False 确保中文字符不被转义
        import json
        resp = requests.post(
            url,
            data=json.dumps({"articles": articles}, ensure_ascii=False).encode('utf-8'),
            headers={'Content-Type': 'application/json; charset=utf-8'},
            timeout=30
        )
        data = resp.json()

        if "media_id" in data:
            return data["media_id"]
        else:
            error_msg = data.get("errmsg", "Unknown error")
            raise WeChatAPIError(f"上传草稿失败: {error_msg}")

    def publish(self, media_id: str) -> str:
        """
        发布文章（freepublish，不通知用户）

        Args:
            media_id: 草稿的media_id

        Returns:
            publish_id

        Raises:
            WeChatAPIError: 发布失败
        """
        token = self._ensure_token()
        url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={token}"

        resp = requests.post(
            url,
            data=json.dumps({"media_id": media_id}, ensure_ascii=False).encode('utf-8'),
            headers={'Content-Type': 'application/json; charset=utf-8'},
            timeout=30
        )
        data = resp.json()

        if data.get("errcode") == 0:
            return data.get("publish_id")
        else:
            error_msg = data.get("errmsg", "Unknown error")
            raise WeChatAPIError(f"发布失败: {error_msg}")

    def get_publish_status(self, publish_id: str) -> Dict[str, Any]:
        """
        查询发布状态

        Args:
            publish_id: 发布ID

        Returns:
            发布状态信息
        """
        token = self._ensure_token()
        url = f"https://api.weixin.qq.com/cgi-bin/freepublish/get?access_token={token}"

        resp = requests.post(url, json={"publish_id": publish_id}, timeout=10)
        return resp.json()

    def publish_article(
        self,
        title: str,
        markdown_content: str,
        thumb_media_id: str = None,
        author: str = None,
        verbose: bool = True,
        auto_cover: bool = True,
        publish: bool = False  # 默认只存草稿箱，不发布
    ) -> tuple:
        """
        完整发布流程：创建封面 -> Markdown转HTML -> 上传草稿 -> [可选]发布

        Args:
            title: 文章标题
            markdown_content: Markdown内容
            thumb_media_id: 封面图media_id（可选，不提供则自动生成）
            author: 作者名
            verbose: 是否打印进度
            auto_cover: 是否自动生成封面图
            publish: 是否直接发布（False=只存草稿箱，True=直接发布）

        Returns:
            (是否成功, media_id, publish_id或None)
        """
        if verbose:
            print(f"\n{'='*60}")
            if publish:
                print(f"📝 开始发布: {title}")
            else:
                print(f"📝 保存到草稿箱: {title}")
            print(f"{'='*60}")

        try:
            # 1. 处理封面图
            if not thumb_media_id and auto_cover:
                if verbose:
                    print("🎨 生成封面图...")
                cover_path = self.create_default_cover(title)
                thumb_media_id = self.upload_image(cover_path)
                # 清理临时文件
                os.remove(cover_path)
                if verbose:
                    print(f"✅ 封面上传成功")
            elif not thumb_media_id and not auto_cover:
                raise WeChatAPIError("请提供封面图media_id，或设置auto_cover=True自动生成")

            # 2. Markdown转HTML
            html_content = self.markdown_to_html(markdown_content)
            if verbose:
                print("✅ Markdown转HTML完成")

            # 3. 上传草稿
            media_id = self.upload_draft(title, html_content, thumb_media_id, author)
            if verbose:
                print(f"✅ 草稿上传成功")
                print(f"   media_id: {media_id}")

            # 4. 可选：发布
            if publish:
                publish_id = self.publish(media_id)
                if verbose:
                    print(f"\n🎉 文章发布成功!")
                    print(f"   标题: {title}")
                    print(f"   publish_id: {publish_id}")
                    print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                return True, media_id, publish_id
            else:
                if verbose:
                    print(f"\n📋 文章已保存到草稿箱")
                    print(f"   标题: {title}")
                    print(f"   media_id: {media_id}")
                    print(f"   请登录微信公众平台审核后发布")
                return True, media_id, None

        except WeChatAPIError as e:
            if verbose:
                print(f"\n❌ 操作失败: {e}")
            return False, None, None
