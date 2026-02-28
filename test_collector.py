#!/usr/bin/env python3
"""
测试话题采集功能
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from collector import TopicCollector, TopicDatabase, TopicSelector


def test_collection():
    """测试话题采集"""
    print("🧪 测试话题采集")
    print("=" * 60)
    
    # 创建采集器
    collector = TopicCollector()
    
    # 采集话题
    items = collector.collect_all(limit_per_source=3)
    
    print(f"\n📊 采集结果:")
    print(f"   共采集到 {len(items)} 条话题")
    
    # 保存到文件
    filepath = collector.save_to_file(items)
    print(f"   已保存到: {filepath}")
    
    return items


def test_database(items):
    """测试话题库"""
    print("\n\n🧪 测试话题库管理")
    print("=" * 60)
    
    # 创建数据库
    db = TopicDatabase()
    
    # 添加话题
    print("\n💾 添加话题到数据库...")
    topics_data = [item.to_dict() for item in items]
    db.add_topics(topics_data)
    
    print(f"   数据库统计: {db.get_stats()}")
    
    # 查询待处理话题
    print("\n📋 待处理话题:")
    pending = db.get_topics(status='pending', limit=5)
    for i, topic in enumerate(pending, 1):
        print(f"   {i}. [{topic['source']}] {topic['title'][:30]}... (热度: {topic['hot_score']})")
    
    return db


def test_selector(db):
    """测试话题选择器"""
    print("\n\n🧪 测试话题选择")
    print("=" * 60)
    
    selector = TopicSelector(db)
    
    # 选择最佳话题
    print("\n🎯 推荐话题 (热度优先):")
    best_topics = selector.select_best(count=3, strategy='hot')
    
    for i, topic in enumerate(best_topics, 1):
        print(f"\n   {i}. {topic['title']}")
        print(f"      来源: {topic['source']} | 热度: {topic['hot_score']}")
        
        # 分析话题
        analysis = selector.analyze_topic(topic)
        print(f"      推荐度: {analysis['score']}/100")
        print(f"      推荐理由: {', '.join(analysis['reasons'])}")
        print(f"      建议角度:")
        for angle in analysis['angles']:
            print(f"         - {angle}")


def test_full_pipeline():
    """测试完整流程"""
    print("\n\n🚀 完整流程测试")
    print("=" * 60)
    
    # 1. 采集
    print("\n1️⃣ 采集话题...")
    collector = TopicCollector()
    items = collector.collect_all(limit_per_source=2)
    
    # 2. 存储
    print("\n2️⃣ 存储到数据库...")
    db = TopicDatabase()
    db.add_topics([item.to_dict() for item in items])
    
    # 3. 选择
    print("\n3️⃣ 选择最佳话题...")
    selector = TopicSelector(db)
    best = selector.select_best(count=1)[0]
    
    print(f"\n   ✅ 选中话题: {best['title']}")
    print(f"      建议立即创作文章！")
    
    # 4. 更新状态
    db.update_status(best['id'], 'processing')
    print(f"\n4️⃣ 已标记为处理中")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='测试话题采集系统')
    parser.add_argument('--collection', '-c', action='store_true', help='测试采集')
    parser.add_argument('--database', '-d', action='store_true', help='测试数据库')
    parser.add_argument('--selector', '-s', action='store_true', help='测试选择器')
    parser.add_argument('--full', '-f', action='store_true', help='完整流程测试')
    parser.add_argument('--all', '-a', action='store_true', help='测试全部')
    args = parser.parse_args()
    
    # 如果没有参数，默认测试全部
    if not any([args.collection, args.database, args.selector, args.full, args.all]):
        args.all = True
    
    items = None
    db = None
    
    if args.collection or args.all:
        items = test_collection()
    
    if args.database or args.all:
        if items is None:
            # 加载已有数据
            collector = TopicCollector()
            items = collector.collect_all(limit_per_source=2)
        db = test_database(items)
    
    if args.selector or args.all:
        if db is None:
            db = TopicDatabase()
        test_selector(db)
    
    if args.full:
        test_full_pipeline()
    
    print("\n" + "=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)
