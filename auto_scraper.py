#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动采集系统
"""

import requests
import json
import re
import time
import random
import threading
from datetime import datetime
from typing import List, Dict
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from database import Database
from scraper import WeChatScraper

class AutoScraper:
    def __init__(self, db_path: str = "articles.db"):
        self.db = Database(db_path)
        self.scraper = WeChatScraper()
        self.ua = UserAgent()
        self.session = requests.Session()
        self.is_running = False
        
    def get_headers(self):
        """获取随机请求头"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def search_wechat_articles(self, keyword: str, max_pages: int = 3) -> List[str]:
        """搜索微信公众号文章链接"""
        print(f"🔍 搜索关键词: {keyword}")
        
        # 这里使用搜狗微信搜索
        search_urls = [
            f"https://weixin.sogou.com/weixin?type=2&query={keyword}&ie=utf8",
            f"https://weixin.sogou.com/weixin?type=2&query={keyword}&ie=utf8&page=2",
            f"https://weixin.sogou.com/weixin?type=2&query={keyword}&ie=utf8&page=3"
        ]
        
        article_urls = []
        
        for url in search_urls[:max_pages]:
            try:
                print(f"📄 搜索页面: {url}")
                time.sleep(random.uniform(2, 4))  # 随机延迟
                
                response = self.session.get(url, headers=self.get_headers(), timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 查找文章链接
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link.get('href', '')
                    if 'mp.weixin.qq.com' in href and '/s?' in href:
                        # 清理链接
                        clean_url = href.split('&')[0] + '&' + '&'.join(href.split('&')[1:])
                        if clean_url not in article_urls:
                            article_urls.append(clean_url)
                
                print(f"✅ 找到 {len(article_urls)} 个文章链接")
                
            except Exception as e:
                print(f"❌ 搜索失败: {str(e)}")
                continue
        
        return article_urls
    
    def auto_scrape_keyword(self, keyword: str, max_articles: int = 10) -> Dict:
        """自动采集指定关键词的文章"""
        print(f"🚀 开始自动采集关键词: {keyword}")
        
        # 添加关键词到数据库
        keyword_id = self.db.add_keyword(keyword)
        
        # 创建任务
        task_id = self.db.add_task(keyword_id, 'auto_scrape')
        self.db.update_task_status(task_id, 'running')
        
        try:
            # 搜索文章链接
            article_urls = self.search_wechat_articles(keyword, max_pages=3)
            
            if not article_urls:
                self.db.update_task_status(task_id, 'failed', error='未找到文章链接')
                return {'success': False, 'message': '未找到文章链接'}
            
            # 限制采集数量
            article_urls = article_urls[:max_articles]
            
            scraped_count = 0
            failed_count = 0
            
            for i, url in enumerate(article_urls, 1):
                try:
                    print(f"📰 采集第 {i}/{len(article_urls)} 篇文章")
                    
                    # 采集文章
                    result = self.scraper.scrape_article(url)
                    
                    if result:
                        # 获取下一个URL编号
                        url_number = self.db.get_next_url_number()
                        
                        # 生成HTML文件名
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        safe_title = re.sub(r'[^\w\s-]', '', result['title'])[:50]
                        html_filename = f"{safe_title}_{timestamp}.html"
                        
                        result['html_file'] = html_filename
                        result['url_number'] = url_number
                        
                        # 保存到数据库
                        self.db.add_article(result, keyword_id)
                        
                        # 生成HTML文件
                        self.scraper.save_html(result, html_filename, self.db, url_number)
                        scraped_count += 1
                        
                        print(f"✅ 采集成功: {result['title']}")
                    else:
                        failed_count += 1
                        print(f"❌ 采集失败: {url}")
                    
                    # 随机延迟，避免被封
                    time.sleep(random.uniform(3, 6))
                    
                except Exception as e:
                    failed_count += 1
                    print(f"❌ 采集异常: {str(e)}")
                    continue
            
            # 更新任务状态
            result_data = {
                'scraped_count': scraped_count,
                'failed_count': failed_count,
                'total_urls': len(article_urls)
            }
            
            self.db.update_task_status(task_id, 'completed', json.dumps(result_data))
            
            return {
                'success': True,
                'message': f'采集完成: 成功 {scraped_count} 篇，失败 {failed_count} 篇',
                'data': result_data
            }
            
        except Exception as e:
            self.db.update_task_status(task_id, 'failed', error=str(e))
            return {'success': False, 'message': str(e)}
    
    def batch_scrape_keywords(self, keywords: List[str], max_articles_per_keyword: int = 5):
        """批量采集多个关键词"""
        print(f"🔄 开始批量采集 {len(keywords)} 个关键词")
        
        results = []
        for i, keyword in enumerate(keywords, 1):
            print(f"\n📝 处理关键词 {i}/{len(keywords)}: {keyword}")
            
            result = self.auto_scrape_keyword(keyword, max_articles_per_keyword)
            results.append({
                'keyword': keyword,
                'result': result
            })
            
            # 关键词间延迟
            if i < len(keywords):
                delay = random.uniform(10, 20)
                print(f"⏳ 等待 {delay:.1f} 秒后处理下一个关键词...")
                time.sleep(delay)
        
        return results
    
    def start_auto_scraper(self, keywords: List[str], interval_hours: int = 6, max_articles_per_keyword: int = 5):
        """启动自动采集服务"""
        if self.is_running:
            return {'success': False, 'message': '自动采集服务已在运行'}
        
        self.is_running = True
        
        def auto_scrape_loop():
            while self.is_running:
                try:
                    print(f"\n🔄 开始新一轮自动采集 - {datetime.now()}")
                    
                    # 批量采集
                    results = self.batch_scrape_keywords(keywords, max_articles_per_keyword)
                    
                    # 统计结果
                    total_success = sum(1 for r in results if r['result']['success'])
                    total_failed = len(results) - total_success
                    
                    print(f"\n📊 本轮采集完成: 成功 {total_success} 个关键词，失败 {total_failed} 个")
                    
                    # 等待下次采集
                    if self.is_running:
                        wait_seconds = interval_hours * 3600
                        print(f"⏰ 等待 {interval_hours} 小时后进行下一轮采集...")
                        time.sleep(wait_seconds)
                    
                except Exception as e:
                    print(f"❌ 自动采集异常: {str(e)}")
                    time.sleep(300)  # 异常后等待5分钟
        
        # 启动后台线程
        thread = threading.Thread(target=auto_scrape_loop)
        thread.daemon = True
        thread.start()
        
        return {'success': True, 'message': f'自动采集服务已启动，每 {interval_hours} 小时采集一次'}
    
    def stop_auto_scraper(self):
        """停止自动采集服务"""
        self.is_running = False
        return {'success': True, 'message': '自动采集服务已停止'}
    
    def get_scraping_status(self):
        """获取采集状态"""
        stats = self.db.get_stats()
        recent_tasks = self.db.get_tasks(limit=10)
        
        return {
            'is_running': self.is_running,
            'stats': stats,
            'recent_tasks': recent_tasks
        }


def main():
    """测试自动采集功能"""
    auto_scraper = AutoScraper()
    
    # 测试关键词
    test_keywords = ['加拿大移民', '留学']
    
    print("🧪 测试自动采集功能")
    print("=" * 50)
    
    # 测试单个关键词采集
    result = auto_scraper.auto_scrape_keyword(test_keywords[0], max_articles=3)
    print(f"采集结果: {result}")
    
    # 查看统计信息
    stats = auto_scraper.get_scraping_status()
    print(f"\n📊 统计信息: {stats}")


if __name__ == "__main__":
    main()
