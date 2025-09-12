#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简洁的微信公众号文章采集器
"""

import requests
import json
import re
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class WeChatScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        
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
    
    def clean_text(self, text):
        """清理文本内容"""
        if not text:
            return ""
        
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        # 移除文章结尾的推广内容
        unwanted_patterns = [
            r'跳转二维码.*',
            r'作者头像.*',
            r'长按识别.*',
            r'扫码关注.*',
            r'点击阅读.*',
        ]
        
        for pattern in unwanted_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def extract_content(self, soup):
        """提取文章内容"""
        # 尝试多种选择器
        content_selectors = [
            '#js_content',
            '.rich_media_content',
            '.content',
            'article',
            'main'
        ]
        
        content = ""
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                content = element.get_text()
                break
        
        return self.clean_text(content)
    
    def extract_title(self, soup):
        """提取文章标题"""
        title_selectors = [
            'h1#activity-name',
            'h1.rich_media_title',
            'title',
            'h1'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        
        return "未知标题"
    
    def extract_author(self, soup):
        """提取作者信息"""
        author_selectors = [
            '.rich_media_meta_text',
            '.author',
            '[data-author]'
        ]
        
        for selector in author_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        
        return "未知作者"
    
    def scrape_article(self, url):
        """采集文章"""
        try:
            print(f"开始采集: {url}")
            
            # 随机延迟
            time.sleep(random.uniform(1, 3))
            
            # 发送请求
            response = self.session.get(url, headers=self.get_headers(), timeout=30)
            response.raise_for_status()
            
            # 解析HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 提取信息
            title = self.extract_title(soup)
            author = self.extract_author(soup)
            content = self.extract_content(soup)
            
            # 构建结果
            result = {
                'title': title,
                'author': author,
                'content': content,
                'url': url,
                'scrape_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'word_count': len(content)
            }
            
            print(f"采集成功: {title}")
            return result
            
        except Exception as e:
            print(f"采集失败: {str(e)}")
            return None
    
    def save_to_file(self, data, filename):
        """保存到文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"已保存: {filename}")
        except Exception as e:
            print(f"保存失败: {str(e)}")
    
    def generate_html(self, data, recommended_articles=None, url_number=None):
        """生成HTML文件"""
        # 生成推荐阅读列表HTML
        recommend_html = ""
        if recommended_articles:
            recommend_html = """
        <div class="recommend-section">
            <h3 class="recommend-title">📚 推荐阅读</h3>
            <div class="recommend-list">
"""
            for article in recommended_articles:
                # 使用新的URL格式
                article_url = f"new/{article.get('url_number', '1')}" if article.get('url_number') else article.get('html_file', '#')
                recommend_html += f"""
                <div class="recommend-item">
                    <a href="{article_url}" class="recommend-link">
                        <span class="recommend-title-text">{article['title']}</span>
                        <span class="recommend-meta">{article['author']} · {article['scrape_time'][:10]}</span>
                    </a>
                </div>
"""
            recommend_html += """
            </div>
        </div>
"""
        
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['title']}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f8f9fa;
        }}
        .article-container {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .article-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .article-title {{
            font-size: 2em;
            margin-bottom: 10px;
            font-weight: 600;
        }}
        .article-meta {{
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .article-content {{
            padding: 40px;
        }}
        .content-text {{
            font-size: 16px;
            line-height: 1.8;
            color: #333;
            white-space: pre-wrap;
        }}
        .recommend-section {{
            background: #f8f9fa;
            padding: 30px;
            border-top: 1px solid #e9ecef;
        }}
        .recommend-title {{
            font-size: 1.3em;
            margin-bottom: 20px;
            color: #333;
            text-align: center;
            font-weight: 600;
        }}
        .recommend-list {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 12px;
        }}
        .recommend-item {{
            background: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .recommend-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .recommend-link {{
            text-decoration: none;
            color: inherit;
            display: block;
        }}
        .recommend-title-text {{
            font-size: 14px;
            font-weight: 600;
            color: #333;
            line-height: 1.4;
            display: block;
            margin-bottom: 6px;
        }}
        .recommend-meta {{
            font-size: 12px;
            color: #666;
            display: block;
        }}
        .article-footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e9ecef;
        }}
        .word-count {{
            font-size: 14px;
            margin-top: 10px;
        }}
        @media (max-width: 768px) {{
            .recommend-list {{
                grid-template-columns: 1fr;
            }}
            .article-content {{
                padding: 20px;
            }}
            .recommend-section {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="article-container">
        <div class="article-header">
            <h1 class="article-title">{data['title']}</h1>
            <div class="article-meta">
                <div>作者: {data['author']}</div>
                <div>时间: {data['scrape_time']}</div>
            </div>
        </div>
        
        <div class="article-content">
            <div class="content-text">{data['content']}</div>
        </div>
        
        {recommend_html}
        
        <div class="article-footer">
            <div>采集时间: {data['scrape_time']}</div>
            <div class="word-count">字数: {data['word_count']}</div>
        </div>
    </div>
</body>
</html>
"""
        return html_content
    
    def save_html(self, data, filename, db=None, url_number=None):
        """保存HTML文件"""
        try:
            # 获取推荐文章
            recommended_articles = None
            if db:
                try:
                    recommended_articles = db.get_random_articles(15)
                    # 过滤掉当前文章（使用URL编号）
                    if url_number:
                        recommended_articles = [article for article in recommended_articles if article.get('url_number') != url_number]
                    else:
                        # 如果没有URL编号，使用标题过滤
                        recommended_articles = [article for article in recommended_articles if article['title'] != data['title']]
                except Exception as e:
                    print(f"获取推荐文章失败: {str(e)}")
            
            html_content = self.generate_html(data, recommended_articles, url_number)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"已保存HTML: {filename}")
        except Exception as e:
            print(f"保存HTML失败: {str(e)}")


def main():
    """主函数"""
    scraper = WeChatScraper()
    
    # 测试URL
    test_url = "https://mp.weixin.qq.com/s?src=11&timestamp=1757648270&ver=6231&signature=joUe7cttth4-xe6-Tzaib4kd8AZOyO2SWEvBfhjAlCKJ80XR55A7dGf83gjGF603c40uL7-eWba50YV8*cAfYbhtpGTiLo20i8AfOjcYhCwaX7JtET2xg5RGQ*WMMFtZ&new=1"
    
    # 采集文章
    result = scraper.scrape_article(test_url)
    
    if result:
        # 保存结果
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_filename = f"article_{timestamp}.json"
        html_filename = f"article_{timestamp}.html"
        
        scraper.save_to_file(result, json_filename)
        scraper.save_html(result, html_filename)
        
        # 打印结果
        print("\n=== 采集结果 ===")
        print(f"标题: {result['title']}")
        print(f"作者: {result['author']}")
        print(f"字数: {result['word_count']}")
        print(f"时间: {result['scrape_time']}")
        print(f"JSON文件: {json_filename}")
        print(f"HTML文件: {html_filename}")
    else:
        print("采集失败")


if __name__ == "__main__":
    main()
