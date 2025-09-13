#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简洁的微信公众号文章采集Web应用
"""

from flask import Flask, render_template, request, jsonify
import threading
import time
import os
from datetime import datetime
from scraper import WeChatScraper
from database import Database

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

# 全局状态
scraping_status = {
    'is_running': False,
    'progress': 0,
    'message': '等待开始',
    'result': None,
    'error': None
}

# 数据库实例
db = Database()

def scrape_article_async(url):
    """异步采集文章"""
    global scraping_status
    
    try:
        scraping_status['is_running'] = True
        scraping_status['progress'] = 10
        scraping_status['message'] = '正在连接...'
        scraping_status['error'] = None
        
        scraper = WeChatScraper()
        
        scraping_status['progress'] = 50
        scraping_status['message'] = '正在解析内容...'
        
        result = scraper.scrape_article(url)
        
        if result:
            scraping_status['progress'] = 100
            scraping_status['message'] = '采集完成'
            scraping_status['result'] = result
            
            # 获取下一个URL编号
            url_number = db.get_next_url_number()
            
            # 生成HTML文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            html_filename = f"article_{timestamp}.html"
            result['html_file'] = html_filename
            result['url_number'] = url_number
            
            # 保存到数据库
            db.add_article(result)
            
            # 生成HTML文件
            scraper.save_html(result, html_filename, db, url_number)
            scraping_status['html_file'] = html_filename
            scraping_status['url_number'] = url_number
        else:
            scraping_status['progress'] = 0
            scraping_status['message'] = '采集失败'
            scraping_status['error'] = '无法获取文章内容'
            
    except Exception as e:
        scraping_status['progress'] = 0
        scraping_status['message'] = '采集失败'
        scraping_status['error'] = str(e)
    finally:
        scraping_status['is_running'] = False

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/scrape', methods=['POST'])
def api_scrape():
    """开始采集API"""
    global scraping_status
    
    if scraping_status['is_running']:
        return jsonify({'success': False, 'message': '正在采集中，请稍候'})
    
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'success': False, 'message': '请输入URL'})
    
    if 'mp.weixin.qq.com' not in url:
        return jsonify({'success': False, 'message': '请输入有效的微信公众号文章链接'})
    
    # 重置状态
    scraping_status = {
        'is_running': True,
        'progress': 0,
        'message': '准备开始',
        'result': None,
        'error': None
    }
    
    # 启动异步任务
    thread = threading.Thread(target=scrape_article_async, args=(url,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'message': '开始采集'})

@app.route('/api/status')
def api_status():
    """获取状态API"""
    return jsonify(scraping_status)

@app.route('/api/result')
def api_result():
    """获取结果API"""
    return jsonify(scraping_status['result'])

@app.route('/api/download/<filename>')
def download_file(filename):
    """下载文件API"""
    try:
        from flask import send_file
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/view/<filename>')
def view_html(filename):
    """查看HTML文件API"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"文件读取失败: {str(e)}", 404

@app.route('/new/<int:url_number>')
def view_by_number(url_number):
    """通过URL编号查看文章"""
    try:
        # 从数据库查找对应的文章
        articles = db.get_articles()
        target_article = None
        
        for article in articles:
            if article.get('url_number') == url_number:
                target_article = article
                break
        
        if not target_article or not target_article.get('html_file'):
            return f"文章 {url_number} 不存在", 404
        
        # 读取HTML文件
        with open(target_article['html_file'], 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"文件读取失败: {str(e)}", 404

if __name__ == '__main__':
    print("🚀 启动微信公众号文章采集工具")
    print("🌐 访问地址: http://localhost:3000")
    app.run(host='0.0.0.0', port=3000, debug=False)