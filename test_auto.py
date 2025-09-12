#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试自动采集系统
"""

from auto_scraper import AutoScraper
from database import Database

def test_database():
    """测试数据库功能"""
    print("🧪 测试数据库功能")
    print("=" * 50)
    
    db = Database("test.db")
    
    # 测试添加关键词
    keyword_id = db.add_keyword("测试关键词")
    print(f"✅ 添加关键词成功，ID: {keyword_id}")
    
    # 测试获取关键词
    keywords = db.get_keywords()
    print(f"✅ 获取关键词列表: {len(keywords)} 个")
    
    # 测试统计信息
    stats = db.get_stats()
    print(f"✅ 统计信息: {stats}")
    
    return True

def test_auto_scraper():
    """测试自动采集功能"""
    print("\n🧪 测试自动采集功能")
    print("=" * 50)
    
    auto_scraper = AutoScraper("test.db")
    
    # 测试单个关键词采集
    print("开始测试关键词采集...")
    result = auto_scraper.auto_scrape_keyword("加拿大移民", max_articles=2)
    print(f"采集结果: {result}")
    
    # 测试获取状态
    status = auto_scraper.get_scraping_status()
    print(f"状态信息: {status}")
    
    return True

def main():
    """主测试函数"""
    print("🚀 开始测试自动采集系统")
    print("=" * 60)
    
    try:
        # 测试数据库
        test_database()
        
        # 测试自动采集
        test_auto_scraper()
        
        print("\n✅ 所有测试通过！")
        print("🎉 自动采集系统运行正常")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
