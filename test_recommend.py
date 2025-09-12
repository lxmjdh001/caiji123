#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试推荐阅读功能
"""

from database import Database
from scraper import WeChatScraper

def test_recommend_function():
    """测试推荐阅读功能"""
    print("🧪 测试推荐阅读功能")
    print("=" * 50)
    
    # 初始化数据库和采集器
    db = Database("test.db")
    scraper = WeChatScraper()
    
    # 添加一些测试文章到数据库
    test_articles = [
        {
            'title': '加拿大移民政策最新解读',
            'author': '移民专家',
            'content': '这是关于加拿大移民政策的详细解读...',
            'url': 'https://mp.weixin.qq.com/s/test1',
            'scrape_time': '2025-09-12 10:00:00',
            'word_count': 1500
        },
        {
            'title': '留学加拿大必知的10个要点',
            'author': '留学顾问',
            'content': '留学加拿大需要注意的要点...',
            'url': 'https://mp.weixin.qq.com/s/test2',
            'scrape_time': '2025-09-12 11:00:00',
            'word_count': 1200
        },
        {
            'title': '加拿大生活成本分析',
            'author': '生活达人',
            'content': '详细分析加拿大的生活成本...',
            'url': 'https://mp.weixin.qq.com/s/test3',
            'scrape_time': '2025-09-12 12:00:00',
            'word_count': 1800
        }
    ]
    
    # 添加测试文章到数据库
    for article in test_articles:
        db.add_article(article)
        print(f"✅ 添加测试文章: {article['title']}")
    
    # 测试获取推荐文章
    recommended_articles = db.get_random_articles(15)
    print(f"\n📚 获取到 {len(recommended_articles)} 篇推荐文章:")
    for article in recommended_articles:
        print(f"  - {article['title']} ({article['author']})")
    
    # 测试生成带推荐阅读的HTML
    test_data = {
        'title': '测试文章标题',
        'author': '测试作者',
        'content': '这是测试文章的内容...',
        'scrape_time': '2025-09-12 13:00:00',
        'word_count': 1000
    }
    
    html_content = scraper.generate_html(test_data, recommended_articles)
    
    # 保存测试HTML
    with open('test_recommend.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ 测试HTML已生成: test_recommend.html")
    print("🎉 推荐阅读功能测试完成！")

if __name__ == "__main__":
    test_recommend_function()
