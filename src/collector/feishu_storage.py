"""
Feishu Bitable Topic Storage (Simplified)
飞书多维表格话题存储（简化版）

表结构：
- 话题ID, 标题, 来源, 原文链接
- 热度评分, 摘要, 标签
- 状态, 推荐度, 建议角度
"""

import os
import requests
from typing import List, Dict, Optional


class FeishuBitableStorage:
    """飞书多维表格存储"""
    
    def __init__(self, app_token: str = None, table_id: str = None, token: str = None):
        self.app_token = app_token or os.getenv("FEISHU_APP_TOKEN")
        self.table_id = table_id or os.getenv("FEISHU_TABLE_ID")
        self.token = token or os.getenv("FEISHU_PERSONAL_TOKEN")
        
        self.base_url = "https://open.feishu.cn/open-apis/bitable/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def add_topic(self, topic: dict) -> str:
        """添加话题"""
        url = f"{self.base_url}/apps/{self.app_token}/tables/{self.table_id}/records"
        
        # 只使用表格中存在的字段
        fields = {
            "话题ID": topic.get('id', ''),
            "标题": topic.get('title', ''),
            "来源": topic.get('source', '其他'),
            "热度评分": topic.get('hot_score', 0),
            "摘要": str(topic.get('summary', ''))[:500],
            "标签": ", ".join(topic.get('tags', [])),
            "状态": self._map_status(topic.get('status', 'pending')),
            "推荐度": topic.get('analysis', {}).get('score', 0),
            "建议角度": "\n".join(topic.get('analysis', {}).get('angles', [])[:3]),
        }
        
        # URL字段需要特殊格式
        if topic.get('url'):
            fields["原文链接"] = {"text": topic['url'], "link": topic['url']}
        
        response = requests.post(url, headers=self.headers, json={"fields": fields}, timeout=30)
        result = response.json()
        
        if result.get('code') == 0:
            record_id = result['data']['record']['record_id']
            print(f"✅ 已添加: {topic['title'][:30]}...")
            return record_id
        else:
            raise Exception(f"添加失败: {result.get('msg', '未知错误')}")
    
    def _map_status(self, status: str) -> str:
        """映射状态"""
        status_map = {
            'pending': '待处理',
            'processing': '处理中',
            'published': '已发布',
            'rejected': '已拒绝'
        }
        return status_map.get(status, '待处理')
    
    def get_topics(self, limit: int = 50) -> List[Dict]:
        """获取话题列表"""
        url = f"{self.base_url}/apps/{self.app_token}/tables/{self.table_id}/records?page_size={limit}"
        
        response = requests.get(url, headers=self.headers, timeout=30)
        result = response.json()
        
        if result.get('code') != 0:
            print(f"⚠️  获取失败: {result.get('msg')}")
            return []
        
        topics = []
        items = result.get('data', {}).get('items', [])
        
        for item in items:
            fields = item.get('fields', {})
            topics.append({
                'record_id': item.get('record_id', ''),
                'id': fields.get('话题ID', ''),
                'title': fields.get('标题', ''),
                'source': fields.get('来源', ''),
                'url': fields.get('原文链接', ''),
                'hot_score': fields.get('热度评分', 0),
                'summary': fields.get('摘要', ''),
                'tags': fields.get('标签', '').split(', ') if fields.get('标签') else [],
                'status': self._unmap_status(fields.get('状态', '待处理')),
            })
        
        return topics
    
    def _unmap_status(self, status: str) -> str:
        """反向映射状态"""
        status_map = {
            '待处理': 'pending',
            '处理中': 'processing',
            '已发布': 'published',
            '已拒绝': 'rejected'
        }
        return status_map.get(status, 'pending')
    
    def update_status(self, record_id: str, status: str) -> bool:
        """更新状态"""
        url = f"{self.base_url}/apps/{self.app_token}/tables/{self.table_id}/records/{record_id}"
        
        data = {
            "fields": {
                "状态": self._map_status(status)
            }
        }
        
        response = requests.put(url, headers=self.headers, json=data, timeout=30)
        return response.json().get('code') == 0
