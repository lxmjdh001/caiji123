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
        self.batch_size = 100  # 每批采集100篇
        self.rest_minutes = 5   # 休息5分钟
        self.current_batch_count = 0  # 当前批次计数
        
    def get_headers(self):
        """获取随机请求头"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Referer': 'https://www.baidu.com/',
            'Sec-Ch-Ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
        }
    
    def search_wechat_articles(self, keyword: str, max_pages: int = 3) -> List[str]:
        """搜索微信公众号文章链接"""
        print(f"🔍 搜索关键词: {keyword}")
        
        # 使用搜狗微信搜索
        search_sources = [
            f"https://weixin.sogou.com/weixin?type=2&query={keyword}&ie=utf8",
            f"https://weixin.sogou.com/weixin?type=2&query={keyword}&ie=utf8&page=2",
            f"https://weixin.sogou.com/weixin?type=2&query={keyword}&ie=utf8&page=3"
        ]
        
        article_urls = []
        
        for i, url in enumerate(search_sources[:max_pages]):
            try:
                print(f"📄 搜索页面 {i+1}: {url}")
                # 增加延迟
                delay = random.uniform(3, 6)
                print(f"⏳ 等待 {delay:.1f} 秒...")
                time.sleep(delay)
                
                # 发送请求
                headers = self.get_headers()
                response = requests.get(url, headers=headers, timeout=30)
                print(f"📄 页面响应状态: {response.status_code}")
                print(f"📄 页面内容长度: {len(response.content)} 字节")
                
                if response.status_code != 200:
                    print(f"❌ 请求失败，状态码: {response.status_code}")
                    continue
                
                # 检查是否有验证码
                if "验证码" in response.text or "VerifyCode" in response.text:
                    print("⚠️ 检测到验证码页面，等待2分钟后重试...")
                    time.sleep(120)
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 检查页面标题
                title = soup.title.string if soup.title else '无标题'
                print(f"📄 页面标题: {title}")
                
                # 查找所有链接
                links = soup.find_all('a', href=True)
                print(f"🔍 找到 {len(links)} 个链接")
                
                # 查找搜狗搜索结果中的微信文章链接
                wechat_links = []
                
                # 先打印前几个链接看看结构
                print(f"🔍 前5个链接示例:")
                for i, link in enumerate(links[:5]):
                    href = link.get('href', '')
                    print(f"  {i+1}. {href[:150]}...")
                
                for link in links:
                    href = link.get('href', '')
                    
                    # 处理搜狗的重定向链接
                    if 'weixin.sogou.com' in href and 'url=' in href:
                        try:
                            print(f"🔍 处理搜狗链接: {href[:100]}...")
                            
                            # 提取重定向的真实URL
                            import urllib.parse
                            parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                            if 'url' in parsed and parsed['url']:
                                real_url = parsed['url'][0]
                                print(f"🔍 提取的URL参数: {real_url[:100]}...")
                                
                                # URL解码
                                real_url = urllib.parse.unquote(real_url)
                                print(f"🔍 URL解码后: {real_url[:100]}...")
                                
                                # 尝试Base64解码
                                try:
                                    import base64
                                    # 补全Base64 padding
                                    missing_padding = len(real_url) % 4
                                    if missing_padding:
                                        real_url += '=' * (4 - missing_padding)
                                    
                                    decoded_bytes = base64.b64decode(real_url)
                                    decoded_url = decoded_bytes.decode('utf-8')
                                    print(f"🔍 Base64解码后: {decoded_url[:100]}...")
                                    
                                    # 检查是否是微信文章链接
                                    if 'mp.weixin.qq.com' in decoded_url and '/s?' in decoded_url:
                                        real_url = decoded_url
                                        print(f"✅ 找到微信文章链接: {real_url}")
                                    else:
                                        print(f"❌ Base64解码后也不是微信文章链接")
                                        continue
                                except Exception as e:
                                    print(f"❌ Base64解码失败: {e}")
                                    continue
                                
                                # 检查是否已经采集过这篇文章
                                if not self.db.is_article_exists(real_url):
                                    if real_url not in wechat_links:
                                        wechat_links.append(real_url)
                                        print(f"🔗 找到新文章链接: {real_url}")
                                else:
                                    print(f"⏭️ 跳过已采集文章: {real_url}")
                        except Exception as e:
                            print(f"解析链接失败: {e}")
                            continue
                    
                    # 直接包含微信链接的情况
                    elif 'mp.weixin.qq.com' in href and '/s?' in href:
                        if href.startswith('//'):
                            href = 'https:' + href
                        elif href.startswith('/'):
                            href = 'https://mp.weixin.qq.com' + href
                        
                        # 检查是否已经采集过
                        if not self.db.is_article_exists(href):
                            if href not in wechat_links:
                                wechat_links.append(href)
                                print(f"🔗 找到直接链接: {href}")
                        else:
                            print(f"⏭️ 跳过已采集文章: {href}")
                    
                    # 检查是否是搜狗的link链接（新的格式）
                    elif '/link?' in href and 'url=' in href:
                        try:
                            print(f"🔍 处理搜狗link链接: {href[:100]}...")
                            
                            # 提取重定向的真实URL
                            import urllib.parse
                            parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                            if 'url' in parsed and parsed['url']:
                                real_url = parsed['url'][0]
                                print(f"🔍 提取的URL参数: {real_url[:100]}...")
                                
                                # URL解码
                                real_url = urllib.parse.unquote(real_url)
                                print(f"🔍 URL解码后: {real_url[:100]}...")
                                
                                # 尝试Base64解码
                                try:
                                    import base64
                                    # 补全Base64 padding
                                    missing_padding = len(real_url) % 4
                                    if missing_padding:
                                        real_url += '=' * (4 - missing_padding)
                                    
                                    decoded_bytes = base64.b64decode(real_url)
                                    decoded_url = decoded_bytes.decode('utf-8')
                                    print(f"🔍 Base64解码后: {decoded_url[:100]}...")
                                    
                                    # 检查是否是微信文章链接
                                    if 'mp.weixin.qq.com' in decoded_url and '/s?' in decoded_url:
                                        real_url = decoded_url
                                        print(f"✅ 找到微信文章链接: {real_url}")
                                    else:
                                        print(f"❌ Base64解码后也不是微信文章链接")
                                        continue
                                except Exception as e:
                                    print(f"❌ Base64解码失败: {e}")
                                    continue
                                
                                # 检查是否已经采集过这篇文章
                                if not self.db.is_article_exists(real_url):
                                    if real_url not in wechat_links:
                                        wechat_links.append(real_url)
                                        print(f"🔗 找到新文章链接: {real_url}")
                                else:
                                    print(f"⏭️ 跳过已采集文章: {real_url}")
                        except Exception as e:
                            print(f"解析link链接失败: {e}")
                            continue
                
                article_urls.extend(wechat_links)
                print(f"✅ 本页面找到 {len(wechat_links)} 个新文章链接")
                
            except Exception as e:
                print(f"❌ 搜索页面失败: {e}")
                continue
        
        # 去重
        unique_urls = list(set(article_urls))
        print(f"🎯 总共找到 {len(unique_urls)} 个唯一文章链接")
        
        return unique_urls
    
    def search_wechat_articles_old(self, keyword: str, max_pages: int = 3) -> List[str]:
        """旧的搜索方法（已废弃）"""
        article_urls = []
        
        for i, url in enumerate([]):
            try:
                print(f"📄 搜索页面 {i+1}: {url}")
                # 增加更长的随机延迟，模拟人类行为
                delay = random.uniform(8, 15)  # 8-15秒延迟
                print(f"⏳ 等待 {delay:.1f} 秒...")
                time.sleep(delay)
                
                # 增强请求头
                headers = self.get_headers()
                headers.update({
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Upgrade-Insecure-Requests': '1'
                })
                
                response = self.session.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                
                print(f"📄 页面响应状态: {response.status_code}")
                print(f"📄 页面内容长度: {len(response.content)} 字节")
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 调试：检查页面是否包含搜索结果
                if "以下内容来自微信公众平台" in response.text:
                    print("✅ 页面包含微信搜索结果")
                else:
                    print("❌ 页面不包含微信搜索结果")
                    print(f"页面标题: {soup.title.string if soup.title else '无标题'}")
                
                # 调试：检查是否有反爬虫提示
                if "验证码" in response.text or "captcha" in response.text.lower() or "VerifyCode" in response.text:
                    print("⚠️ 检测到验证码页面，等待2分钟后重试...")
                    time.sleep(120)  # 等待2分钟
                    continue
                if "访问过于频繁" in response.text or "环境异常" in response.text:
                    print("⚠️ 检测到访问限制，等待更长时间...")
                    time.sleep(random.uniform(30, 60))  # 等待30-60秒
                    continue
                if "IP" in response.text and "访问时间" in response.text:
                    print("⚠️ 检测到IP限制页面，跳过")
                    continue
                
                # 多种方式查找文章链接
                found_links = set()
                
                # 方法0: 如果是Bing搜索，特殊处理
                if 'bing.com' in url:
                    print("🔍 处理Bing搜索结果...")
                    
                    # Bing搜索结果通常在特定的div中
                    all_links = soup.find_all('a', href=True)
                    wechat_links = []
                    
                    for link in all_links:
                        href = link.get('href', '')
                        if 'mp.weixin.qq.com' in href and '/s?' in href:
                            wechat_links.append(href)
                    
                    print(f"🔍 Bing找到 {len(wechat_links)} 个微信链接")
                    
                    for href in wechat_links:
                        if not self.db.is_article_exists(href):
                            if href not in found_links:
                                found_links.add(href)
                                article_urls.append(href)
                                print(f"🔗 Bing找到文章链接: {href}")
                        else:
                            print(f"⏭️ 跳过已采集文章: {href}")
                
                # 方法0.5: 如果是DuckDuckGo搜索，特殊处理
                elif 'duckduckgo.com' in url:
                    print("🔍 处理DuckDuckGo搜索结果...")
                    
                    # DuckDuckGo搜索结果通常在特定的div中
                    all_links = soup.find_all('a', href=True)
                    wechat_links = []
                    
                    for link in all_links:
                        href = link.get('href', '')
                        if 'mp.weixin.qq.com' in href and '/s?' in href:
                            wechat_links.append(href)
                    
                    print(f"🔍 DuckDuckGo找到 {len(wechat_links)} 个微信链接")
                    
                    for href in wechat_links:
                        if not self.db.is_article_exists(href):
                            if href not in found_links:
                                found_links.add(href)
                                article_urls.append(href)
                                print(f"🔗 DuckDuckGo找到文章链接: {href}")
                        else:
                            print(f"⏭️ 跳过已采集文章: {href}")
                
                # 方法0.7: 如果是百度搜索，特殊处理
                elif 'baidu.com' in url:
                    print("🔍 处理百度搜索结果...")
                    
                    # 百度搜索结果有多种结构，需要全面搜索
                    # 1. 查找所有包含微信链接的a标签
                    all_links = soup.find_all('a', href=True)
                    wechat_links = []
                    
                    for link in all_links:
                        href = link.get('href', '')
                        if 'mp.weixin.qq.com' in href and '/s?' in href:
                            wechat_links.append(href)
                    
                    print(f"🔍 找到 {len(wechat_links)} 个微信链接")
                    
                    # 2. 处理找到的微信链接
                    for href in wechat_links:
                        # 处理相对链接
                        if href.startswith('//'):
                            href = 'https:' + href
                        elif href.startswith('/'):
                            href = 'https://mp.weixin.qq.com' + href
                        
                        # 检查是否已经采集过
                        if not self.db.is_article_exists(href):
                            if href not in found_links:
                                found_links.add(href)
                                article_urls.append(href)
                                print(f"🔗 百度找到文章链接: {href}")
                        else:
                            print(f"⏭️ 跳过已采集文章: {href}")
                    
                    # 3. 额外查找百度搜索结果区域的链接
                    result_divs = soup.find_all('div', class_='result')
                    print(f"🔍 找到 {len(result_divs)} 个百度结果区域")
                    
                    for div in result_divs:
                        # 查找标题链接
                        title_link = div.find('h3').find('a', href=True) if div.find('h3') else None
                        if title_link:
                            href = title_link['href']
                            if 'mp.weixin.qq.com' in href and '/s?' in href:
                                if href.startswith('//'):
                                    href = 'https:' + href
                                elif href.startswith('/'):
                                    href = 'https://mp.weixin.qq.com' + href
                                
                                # 检查是否已经采集过
                                if not self.db.is_article_exists(href):
                                    if href not in found_links:
                                        found_links.add(href)
                                        article_urls.append(href)
                                        print(f"🔗 百度结果区域找到文章链接: {href}")
                                else:
                                    print(f"⏭️ 跳过已采集文章: {href}")
                
                # 方法1: 查找搜狗搜索结果中的链接
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link.get('href', '')
                    
                    # 处理搜狗的重定向链接
                    if 'weixin.sogou.com' in href and 'url=' in href:
                        import urllib.parse
                        try:
                            print(f"🔍 处理搜狗链接: {href[:100]}...")
                            
                            # 提取重定向的真实URL
                            parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                            if 'url' in parsed and parsed['url']:
                                real_url = parsed['url'][0]
                                print(f"🔍 提取的URL参数: {real_url[:100]}...")
                                
                                # URL解码
                                real_url = urllib.parse.unquote(real_url)
                                print(f"🔍 解码后的URL: {real_url[:100]}...")
                                
                                # 检查是否是微信文章链接
                                if 'mp.weixin.qq.com' in real_url:
                                    # 检查是否已经采集过这篇文章
                                    if not self.db.is_article_exists(real_url):
                                        if real_url not in found_links:
                                            found_links.add(real_url)
                                            article_urls.append(real_url)
                                            print(f"🔗 找到新文章链接: {real_url}")
                                    else:
                                        print(f"⏭️ 跳过已采集文章: {real_url}")
                                else:
                                    print(f"❌ 不是微信文章链接: {real_url}")
                        except Exception as e:
                            print(f"解析链接失败: {e}")
                            continue
                    
                    # 直接包含微信链接的情况
                    elif 'mp.weixin.qq.com' in href and '/s?' in href:
                        if href.startswith('//'):
                            href = 'https:' + href
                        elif href.startswith('/'):
                            href = 'https://mp.weixin.qq.com' + href
                        
                        if href not in found_links:
                            found_links.add(href)
                            article_urls.append(href)
                            print(f"🔗 找到直接链接: {href}")
                
                # 方法2: 查找搜索结果区域的链接
                result_divs = soup.find_all('div', class_=['result', 'news-item', 'txt-box'])
                print(f"🔍 找到 {len(result_divs)} 个结果区域")
                
                for i, div in enumerate(result_divs):
                    link = div.find('a', href=True)
                    if link:
                        href = link.get('href', '')
                        print(f"🔍 结果区域 {i+1} 的链接: {href[:100]}...")
                        
                        if 'weixin.sogou.com' in href and 'url=' in href:
                            import urllib.parse
                            try:
                                parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                                if 'url' in parsed and parsed['url']:
                                    real_url = urllib.parse.unquote(parsed['url'][0])
                                    print(f"🔍 结果区域解码URL: {real_url[:100]}...")
                                    
                                    if 'mp.weixin.qq.com' in real_url:
                                        if real_url not in found_links:
                                            found_links.add(real_url)
                                            article_urls.append(real_url)
                                            print(f"🔗 找到结果链接: {real_url}")
                                    else:
                                        print(f"❌ 结果区域不是微信链接: {real_url}")
                            except Exception as e:
                                print(f"❌ 结果区域解析失败: {e}")
                                continue
                
                # 方法3: 查找所有包含 sogou_vr 的链接（搜狗特有的ID）
                sogou_links = soup.find_all('a', id=lambda x: x and 'sogou_vr' in x)
                print(f"🔍 找到 {len(sogou_links)} 个搜狗VR链接")
                
                for i, link in enumerate(sogou_links):
                    href = link.get('href', '')
                    if href:
                        print(f"🔍 搜狗VR链接 {i+1}: {href[:100]}...")
                        
                        # 处理搜狗VR链接
                        if 'weixin.sogou.com' in href and 'url=' in href:
                            import urllib.parse
                            try:
                                print(f"🔍 处理VR链接: {href[:100]}...")
                                
                                # 提取重定向的真实URL
                                parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                                if 'url' in parsed and parsed['url']:
                                    real_url = parsed['url'][0]
                                    print(f"🔍 VR链接提取的URL参数: {real_url[:100]}...")
                                    
                                    # URL解码
                                    real_url = urllib.parse.unquote(real_url)
                                    print(f"🔍 VR链接解码后的URL: {real_url[:100]}...")
                                    
                                    # 检查是否是微信文章链接
                                    if 'mp.weixin.qq.com' in real_url:
                                        # 检查是否已经采集过这篇文章
                                        if not self.db.is_article_exists(real_url):
                                            if real_url not in found_links:
                                                found_links.add(real_url)
                                                article_urls.append(real_url)
                                                print(f"🔗 VR链接找到新文章: {real_url}")
                                        else:
                                            print(f"⏭️ VR链接跳过已采集文章: {real_url}")
                                    else:
                                        print(f"❌ VR链接不是微信文章: {real_url}")
                            except Exception as e:
                                print(f"❌ VR链接解析失败: {e}")
                                continue
                
                print(f"✅ 找到 {len(found_links)} 个新文章链接")
                
            except Exception as e:
                print(f"❌ 搜索失败: {str(e)}")
                continue
        
        # 去重并返回
        unique_urls = list(dict.fromkeys(article_urls))  # 保持顺序的去重
        print(f"🎯 总共找到 {len(unique_urls)} 个唯一文章链接")
        
        return unique_urls
    
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
                        self.current_batch_count += 1
                        
                        print(f"✅ 采集成功: {result['title']} (累计: {self.current_batch_count})")
                        
                        # 检查是否达到批量休息条件
                        if self.current_batch_count >= self.batch_size:
                            print(f"🛌 已采集 {self.current_batch_count} 篇文章，休息 {self.rest_minutes} 分钟...")
                            time.sleep(self.rest_minutes * 60)  # 休息5分钟
                            self.current_batch_count = 0  # 重置计数
                            print("⏰ 休息结束，继续采集...")
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
    
    def set_batch_settings(self, batch_size: int = 100, rest_minutes: int = 5):
        """设置批量采集参数"""
        self.batch_size = batch_size
        self.rest_minutes = rest_minutes
        self.current_batch_count = 0  # 重置计数
        print(f"📊 批量采集设置已更新: 每 {batch_size} 篇休息 {rest_minutes} 分钟")
    
    def get_scraping_status(self):
        """获取采集状态"""
        stats = self.db.get_stats()
        recent_tasks = self.db.get_tasks(limit=10)
        
        return {
            'is_running': self.is_running,
            'stats': stats,
            'recent_tasks': recent_tasks,
            'batch_settings': {
                'batch_size': self.batch_size,
                'rest_minutes': self.rest_minutes,
                'current_count': self.current_batch_count
            }
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
