"""
Collector Module
采集模块

包含：
- topic_collector: 话题采集器
- topic_database: 话题库管理
"""

from .topic_collector import (
    TopicCollector,
    TopicItem,
    BaseCollector,
    JikeCollector,
    RSSCollector,
    GitHubTrendingCollector,
    WeiboHotCollector,
    collect_topics
)

from .topic_database import (
    TopicDatabase,
    TopicSelector
)

__all__ = [
    'TopicCollector',
    'TopicItem',
    'BaseCollector',
    'JikeCollector',
    'RSSCollector',
    'GitHubTrendingCollector',
    'WeiboHotCollector',
    'collect_topics',
    'TopicDatabase',
    'TopicSelector'
]
