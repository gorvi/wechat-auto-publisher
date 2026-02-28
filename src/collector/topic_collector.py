"""
Topic Collector Module
话题采集模块

自动从多个来源采集热门话题和资讯
"""

import requests
import json
import re
import os
from datetime import datetime
from typing import List, Dict, Optional
from abc import ABC, abstractmethod
import feedparser


class TopicItem:
    """话题项数据结构"""
    
    def __init__(self, title: str, url: str, source: str, **kwargs):
        self.title = title
        self.url = url
        self.source = source
        self.created_at = datetime.now().isoformat()
        self.hot_score = kwargs.get('hot_score', 0)
        self.summary = kwargs.get('summary', '')
        self.tags = kwargs.get('tags', [])
        self.content = kwargs.get('content', '')
        self.status = 'pending'  # pending/processing/published/rejected
        
    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'url': self.url,
            'source': self.source,
            'created_at': self.created_at,
            'hot_score': self.hot_score,
            'summary': self.summary,
            'tags': self.tags,
            'content': self.content,
            'status': self.status
        }


class BaseCollector(ABC):
    """采集器基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
    
    @abstractmethod
    def collect(self, limit: int = 10) -> List[TopicItem]:
        """采集话题"""
        pass
    
    def fetch(self, url: str, **kwargs) -> requests.Response:
        """发送HTTP请求"""
        return requests.get(url, headers=self.headers, timeout=30, **kwargs)


class JikeCollector(BaseCollector):
    """
    即刻话题采集器
    
    采集即刻App的热门圈子内容
    """
    
    def __init__(self):
        super().__init__("即刻")
        self.topics = [
            "AI",
            "独立开发",
            "效率工具",
            "产品经理",
            "编程"
        ]
    
    def collect(self, limit: int = 10) -> List[TopicItem]:
        """
        采集即刻热门内容
        
        注：即刻有反爬机制，这里使用模拟数据作为示例
        实际使用时需要接入即刻API或解决反爬
        """
        items = []
        
        # 模拟即刻热门话题（实际应调用API）
        mock_topics = [
            {
                'title': '我用AI自动化了工作流，每天节省3小时',
                'url': 'https://web.okjike.com/topic/xxx',
                'hot_score': 95,
                'summary': '分享AI工具在自动化工作流中的应用案例',
                'tags': ['AI', '效率', '自动化']
            },
            {
                'title': '独立开发者月入10万的经验分享',
                'url': 'https://web.okjike.com/topic/yyy',
                'hot_score': 88,
                'summary': '独立开发者的产品、营销、变现经验',
                'tags': ['独立开发', '创业', '变现']
            },
            {
                'title': 'ChatGPT Plus值得买吗？使用3个月后的真实体验',
                'url': 'https://web.okjike.com/topic/zzz',
                'hot_score': 82,
                'summary': '详细分析ChatGPT Plus的功能和价值',
                'tags': ['AI', 'ChatGPT', '工具']
            }
        ]
        
        for topic in mock_topics[:limit]:
            items.append(TopicItem(
                title=topic['title'],
                url=topic['url'],
                source='即刻',
                hot_score=topic['hot_score'],
                summary=topic['summary'],
                tags=topic['tags']
            ))
        
        return items


class RSSCollector(BaseCollector):
    """
    RSS采集器
    
    支持RSS订阅源
    """
    
    def __init__(self):
        super().__init__("RSS")
        self.feeds = {
            '36氪': 'https://36kr.com/feed',
            '虎嗅': 'https://www.huxiu.com/rss/0.xml',
            '极客公园': 'https://www.geekpark.net/rss',
        }
    
    def collect(self, limit: int = 10) -> List[TopicItem]:
        """采集RSS订阅"""
        items = []
        
        for source_name, feed_url in self.feeds.items():
            try:
                print(f"   采集 {source_name}...", end=" ")
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:limit//len(self.feeds) + 1]:
                    item = TopicItem(
                        title=entry.get('title', ''),
                        url=entry.get('link', ''),
                        source=source_name,
                        summary=self._extract_summary(entry.get('summary', '')),
                        hot_score=50  # RSS默认分数
                    )
                    items.append(item)
                
                print(f"✅ ({len(items)}条)")
                
            except Exception as e:
                print(f"❌ {e}")
                continue
        
        return items[:limit]
    
    def _extract_summary(self, html_content: str) -> str:
        """从HTML提取纯文本摘要"""
        # 简单去除HTML标签
        text = re.sub(r'<[^\u003e]+>', '', html_content)
        return text[:200] + '...' if len(text) > 200 else text


class GitHubTrendingCollector(BaseCollector):
    """
    GitHub Trending采集器
    
    采集GitHub热门项目
    """
    
    def __init__(self):
        super().__init__("GitHub Trending")
    
    def collect(self, limit: int = 10) -> List[TopicItem]:
        """采集GitHub热门项目"""
        items = []
        
        try:
            # GitHub Trending API（使用模拟数据，实际应解析网页或调用API）
            url = "https://github.com/trending/python?since=daily"
            response = self.fetch(url)
            
            # 简单解析（实际应使用BeautifulSoup等解析库）
            # 这里使用模拟数据
            mock_projects = [
                {
                    'name': 'openai/openai-python',
                    'description': 'OpenAI Python SDK',
                    'stars': '5000+'
                },
                {
                    'name': 'microsoft/autogen',
                    'description': 'AI Agent框架',
                    'stars': '3000+'
                },
                {
                    'name': 'langchain-ai/langchain',
                    'description': 'LLM应用开发框架',
                    'stars': '10000+'
                }
            ]
            
            for project in mock_projects[:limit]:
                items.append(TopicItem(
                    title=f"GitHub热门: {project['name']}",
                    url=f"https://github.com/{project['name']}",
                    source='GitHub Trending',
                    hot_score=85,
                    summary=project['description'],
                    tags=['开源', 'GitHub', '技术']
                ))
                
        except Exception as e:
            print(f"   GitHub采集失败: {e}")
        
        return items


class WeiboHotCollector(BaseCollector):
    """
    微博热搜采集器
    
    采集微博热门话题
    """
    
    def __init__(self):
        super().__init__("微博热搜")
    
    def collect(self, limit: int = 10) -> List[TopicItem]:
        """采集微博热搜"""
        items = []
        
        # 模拟微博热搜数据（实际应调用API或解析网页）
        mock_hot = [
            {'title': 'AI取代程序员', 'hot': '爆', 'score': 100},
            {'title': 'ChatGPT新功能', 'hot': '热', 'score': 90},
            {'title': '独立开发者月入过万', 'hot': '新', 'score': 80},
        ]
        
        for topic in mock_hot[:limit]:
            items.append(TopicItem(
                title=topic['title'],
                url=f"https://s.weibo.com/weibo?q={topic['title']}",
                source='微博热搜',
                hot_score=topic['score'],
                tags=['热点', '社交']
            ))
        
        return items


class TopicCollector:
    """
    话题采集主类
    
    统一管理多个采集器
    """
    
    def __init__(self, data_dir: str = "data/topics"):
        self.data_dir = data_dir
        self.collectors = [
            JikeCollector(),
            RSSCollector(),
            GitHubTrendingCollector(),
            WeiboHotCollector()
        ]
        
        # 确保数据目录存在
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def collect_all(self, limit_per_source: int = 5) -> List[TopicItem]:
        """
        从所有来源采集话题
        
        Args:
            limit_per_source: 每个来源采集数量
            
        Returns:
            采集到的话题列表
        """
        all_items = []
        
        print("🚀 开始采集话题...")
        print("=" * 60)
        
        for collector in self.collectors:
            try:
                print(f"\n📡 {collector.name}")
                items = collector.collect(limit_per_source)
                all_items.extend(items)
                print(f"   ✅ 采集到 {len(items)} 条")
            except Exception as e:
                print(f"   ❌ 失败: {e}")
                continue
        
        print("\n" + "=" * 60)
        print(f"📊 总计采集: {len(all_items)} 条话题")
        
        return all_items
    
    def save_to_file(self, items: List[TopicItem], filename: str = None):
        """
        保存话题到文件
        
        Args:
            items: 话题列表
            filename: 文件名（默认使用日期）
        """
        if filename is None:
            filename = f"topics_{datetime.now().strftime('%Y%m%d')}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        # 转换为字典列表
        data = [item.to_dict() for item in items]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 已保存到: {filepath}")
        return filepath
    
    def load_topics(self, filename: str = None) -> List[Dict]:
        """
        加载话题
        
        Args:
            filename: 文件名（默认加载最新的）
            
        Returns:
            话题列表
        """
        if filename:
            filepath = os.path.join(self.data_dir, filename)
        else:
            # 找最新的文件
            files = [f for f in os.listdir(self.data_dir) if f.endswith('.json')]
            if not files:
                return []
            files.sort(reverse=True)
            filepath = os.path.join(self.data_dir, files[0])
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)


# 快捷函数
def collect_topics(limit: int = 5) -> List[TopicItem]:
    """快捷采集话题"""
    collector = TopicCollector()
    items = collector.collect_all(limit)
    collector.save_to_file(items)
    return items
