"""
Topic Database Manager
话题库管理模块

管理采集到的话题：存储、查询、更新状态
支持JSON文件存储（无需数据库）
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class TopicDatabase:
    """
    话题数据库
    
    使用JSON文件存储，简单易用
    """
    
    def __init__(self, data_dir: str = "data/topics"):
        self.data_dir = data_dir
        self.db_file = os.path.join(data_dir, "topic_db.json")
        
        # 确保目录存在
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # 加载或创建数据库
        self.data = self._load_db()
    
    def _load_db(self) -> Dict:
        """加载数据库"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 初始化空数据库
            return {
                'version': '1.0',
                'created_at': datetime.now().isoformat(),
                'topics': [],
                'stats': {
                    'total': 0,
                    'published': 0,
                    'rejected': 0,
                    'pending': 0
                }
            }
    
    def _save_db(self):
        """保存数据库"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_topic(self, topic: Dict) -> str:
        """
        添加话题
        
        Args:
            topic: 话题字典
            
        Returns:
            话题ID
        """
        # 生成唯一ID
        topic_id = f"topic_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.data['topics'])}"
        
        topic['id'] = topic_id
        topic['created_at'] = datetime.now().isoformat()
        topic['status'] = 'pending'  # pending/processing/published/rejected
        
        self.data['topics'].append(topic)
        self.data['stats']['total'] += 1
        self.data['stats']['pending'] += 1
        
        self._save_db()
        
        return topic_id
    
    def add_topics(self, topics: List[Dict]):
        """批量添加话题"""
        for topic in topics:
            # 检查是否已存在（根据URL去重）
            if not self._exists(topic.get('url', '')):
                self.add_topic(topic)
    
    def _exists(self, url: str) -> bool:
        """检查话题是否已存在"""
        for topic in self.data['topics']:
            if topic.get('url') == url:
                return True
        return False
    
    def get_topic(self, topic_id: str) -> Optional[Dict]:
        """获取单个话题"""
        for topic in self.data['topics']:
            if topic.get('id') == topic_id:
                return topic
        return None
    
    def get_topics(self, status: str = None, limit: int = None) -> List[Dict]:
        """
        获取话题列表
        
        Args:
            status: 筛选状态 (pending/processing/published/rejected)
            limit: 限制数量
            
        Returns:
            话题列表
        """
        topics = self.data['topics']
        
        if status:
            topics = [t for t in topics if t.get('status') == status]
        
        # 按热度排序
        topics.sort(key=lambda x: x.get('hot_score', 0), reverse=True)
        
        if limit:
            topics = topics[:limit]
        
        return topics
    
    def update_status(self, topic_id: str, status: str):
        """
        更新话题状态
        
        Args:
            topic_id: 话题ID
            status: 新状态
        """
        for topic in self.data['topics']:
            if topic.get('id') == topic_id:
                old_status = topic.get('status')
                topic['status'] = status
                topic['updated_at'] = datetime.now().isoformat()
                
                # 更新统计
                if old_status in self.data['stats']:
                    self.data['stats'][old_status] -= 1
                if status in self.data['stats']:
                    self.data['stats'][status] += 1
                
                self._save_db()
                return True
        
        return False
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.data['stats'].copy()
    
    def delete_topic(self, topic_id: str) -> bool:
        """删除话题"""
        for i, topic in enumerate(self.data['topics']):
            if topic.get('id') == topic_id:
                status = topic.get('status')
                self.data['topics'].pop(i)
                
                # 更新统计
                self.data['stats']['total'] -= 1
                if status in self.data['stats']:
                    self.data['stats'][status] -= 1
                
                self._save_db()
                return True
        
        return False
    
    def search(self, keyword: str) -> List[Dict]:
        """搜索话题"""
        results = []
        keyword = keyword.lower()
        
        for topic in self.data['topics']:
            title = topic.get('title', '').lower()
            summary = topic.get('summary', '').lower()
            tags = [t.lower() for t in topic.get('tags', [])]
            
            if keyword in title or keyword in summary or keyword in tags:
                results.append(topic)
        
        return results
    
    def export_to_file(self, filename: str = None, status: str = None):
        """导出话题到文件"""
        if filename is None:
            filename = f"topics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        topics = self.get_topics(status=status)
        
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(topics, f, ensure_ascii=False, indent=2)
        
        return filepath


class TopicSelector:
    """
    话题选择器
    
    基于AI分析选择最适合的话题
    """
    
    def __init__(self, db: TopicDatabase = None):
        self.db = db or TopicDatabase()
    
    def select_best(self, count: int = 3, strategy: str = 'hot') -> List[Dict]:
        """
        选择最佳话题
        
        Args:
            count: 选择数量
            strategy: 选择策略 (hot/random/diverse)
            
        Returns:
            话题列表
        """
        pending_topics = self.db.get_topics(status='pending')
        
        if not pending_topics:
            return []
        
        if strategy == 'hot':
            # 按热度排序
            topics = sorted(pending_topics, key=lambda x: x.get('hot_score', 0), reverse=True)
            return topics[:count]
        
        elif strategy == 'random':
            # 随机选择
            import random
            return random.sample(pending_topics, min(count, len(pending_topics)))
        
        elif strategy == 'diverse':
            # 多样化选择（不同来源）
            sources = {}
            for topic in pending_topics:
                source = topic.get('source', 'unknown')
                if source not in sources:
                    sources[source] = []
                sources[source].append(topic)
            
            selected = []
            for _ in range(count):
                for source, topics in sources.items():
                    if topics:
                        selected.append(topics.pop(0))
                        if len(selected) >= count:
                            break
                if len(selected) >= count:
                    break
            
            return selected
        
        else:
            return pending_topics[:count]
    
    def analyze_topic(self, topic: Dict) -> Dict:
        """
        分析话题潜力
        
        返回分析结果：
        - 推荐度 (0-100)
        - 推荐理由
        - 建议角度
        """
        score = 0
        reasons = []
        
        # 基于热度
        hot_score = topic.get('hot_score', 0)
        if hot_score > 80:
            score += 30
            reasons.append("热度很高")
        elif hot_score > 60:
            score += 20
            reasons.append("热度中等")
        
        # 基于来源权威性
        source = topic.get('source', '')
        if source in ['36氪', '虎嗅', '即刻']:
            score += 20
            reasons.append("来源可靠")
        
        # 基于标题质量
        title = topic.get('title', '')
        if len(title) > 10 and len(title) < 30:
            score += 10
            reasons.append("标题长度适中")
        
        # 基于是否有摘要
        if topic.get('summary'):
            score += 10
            reasons.append("有内容摘要")
        
        # 建议角度
        angles = self._suggest_angles(topic)
        
        return {
            'score': min(score, 100),
            'reasons': reasons,
            'angles': angles,
            'recommend': score >= 50
        }
    
    def _suggest_angles(self, topic: Dict) -> List[str]:
        """建议写作角度"""
        angles = []
        title = topic.get('title', '')
        
        if 'AI' in title or '人工智能' in title:
            angles.extend([
                'AI技术的实际应用场景',
                'AI对行业的影响分析',
                '普通人如何利用AI提升效率'
            ])
        
        if '独立开发' in title or '创业' in title:
            angles.extend([
                '独立开发者的实战经验',
                '从0到1的产品打造过程',
                '变现模式和收入分析'
            ])
        
        if '效率' in title or '工具' in title:
            angles.extend([
                '工具使用教程和技巧',
                '效率提升的前后对比',
                '同类工具横向对比'
            ])
        
        if not angles:
            angles = [
                '深度解读和分析',
                '结合个人经验的分享',
                '实用教程和步骤'
            ]
        
        return angles[:3]
