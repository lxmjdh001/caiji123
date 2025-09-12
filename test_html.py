#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试HTML生成功能
"""

from scraper import WeChatScraper
from datetime import datetime

def test_html_generation():
    """测试HTML生成功能"""
    print("🧪 测试HTML生成功能")
    print("=" * 50)
    
    scraper = WeChatScraper()
    
    # 测试数据
    test_data = {
        'title': '测试文章标题',
        'author': '测试作者',
        'content': '这是测试文章内容。\n\n包含多行文本。\n\n测试换行和格式。',
        'scrape_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'word_count': 25,
        'url': 'https://test.example.com'
    }
    
    # 生成HTML
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    html_filename = f"test_article_{timestamp}.html"
    
    try:
        scraper.save_html(test_data, html_filename)
        print(f"✅ HTML文件生成成功: {html_filename}")
        
        # 读取并显示部分内容
        with open(html_filename, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"📄 文件大小: {len(content)} 字符")
            print(f"📝 包含标题: {'测试文章标题' in content}")
            print(f"👤 包含作者: {'测试作者' in content}")
            print(f"📊 包含字数: {'25' in content}")
            
    except Exception as e:
        print(f"❌ HTML生成失败: {str(e)}")

if __name__ == "__main__":
    test_html_generation()
