#!/usr/bin/env python3
"""
初始化飞书多维表格
创建标准的话题库表结构
"""

import requests
import json
import os

# 配置
APP_TOKEN = os.getenv('FEISHU_APP_TOKEN', 'GL7MbUZhkaPsnys9jQncDpr9nVb')
TABLE_ID = os.getenv('FEISHU_TABLE_ID', 'tblaMAbGnT3WqpYD')
TOKEN = os.getenv('FEISHU_PERSONAL_TOKEN', 't-g1043117LECPWC4UFPYAJLYPDHFFASETN4YHHCQM')

base_url = "https://open.feishu.cn/open-apis/bitable/v1"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# 需要创建的字段
fields_to_create = [
    {"field_name": "话题ID", "type": 1},  # 文本
    {"field_name": "标题", "type": 1},     # 文本
    {"field_name": "来源", "type": 3, "property": {"options": [
        {"name": "即刻", "color": 0},
        {"name": "36氪", "color": 1},
        {"name": "虎嗅", "color": 2},
        {"name": "极客公园", "color": 3},
        {"name": "GitHub", "color": 4},
        {"name": "微博", "color": 5},
        {"name": "RSS", "color": 6}
    ]}},  # 单选
    {"field_name": "原文链接", "type": 15},  # 链接
    {"field_name": "热度评分", "type": 2},   # 数字
    {"field_name": "摘要", "type": 1},       # 文本（多行）
    {"field_name": "标签", "type": 1},       # 文本
    {"field_name": "状态", "type": 3, "property": {"options": [
        {"name": "待处理", "color": 0},
        {"name": "处理中", "color": 1},
        {"name": "已发布", "color": 2},
        {"name": "已拒绝", "color": 3}
    ]}},  # 单选
    {"field_name": "推荐度", "type": 2},    # 数字
    {"field_name": "建议角度", "type": 1},   # 文本
]

print("🚀 初始化飞书多维表格")
print("=" * 60)

for field in fields_to_create:
    try:
        url = f"{base_url}/apps/{APP_TOKEN}/tables/{TABLE_ID}/fields"
        response = requests.post(url, headers=headers, json=field, timeout=30)
        
        if response.json().get('code') == 0:
            print(f"✅ 创建字段: {field['field_name']}")
        else:
            # 字段可能已存在
            print(f"⚠️  {field['field_name']}: {response.json().get('msg', '可能已存在')}")
    except Exception as e:
        print(f"❌ {field['field_name']}: {e}")

print("\n" + "=" * 60)
print("🎉 表格初始化完成！")
print("=" * 60)
print("\n📋 请手动调整:")
print("   1. 将'文本'字段重命名为'创建时间'")
print("   2. 添加'更新时间'字段（日期类型）")
print("   3. 调整字段顺序")
