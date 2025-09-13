#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
管理界面应用
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import threading
import time
import os
from datetime import datetime
from database import Database
from auto_scraper import AutoScraper

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

# 全局变量
auto_scraper = AutoScraper()
scraping_status = {
    'is_running': False,
    'keywords': [],
    'interval_hours': 6,
    'max_articles_per_keyword': 5
}

@app.route('/')
def index():
    """主页"""
    stats = auto_scraper.get_scraping_status()
    return render_template('admin.html', stats=stats)

@app.route('/api/keywords', methods=['GET'])
def get_keywords():
    """获取关键词列表"""
    keywords = auto_scraper.db.get_keywords()
    return jsonify(keywords)

@app.route('/api/keywords', methods=['POST'])
def add_keyword():
    """添加关键词"""
    data = request.get_json()
    keyword = data.get('keyword', '').strip()
    
    if not keyword:
        return jsonify({'success': False, 'message': '请输入关键词'})
    
    try:
        keyword_id = auto_scraper.db.add_keyword(keyword)
        return jsonify({'success': True, 'message': '关键词添加成功', 'id': keyword_id})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/keywords/<int:keyword_id>', methods=['DELETE'])
def delete_keyword(keyword_id):
    """删除关键词"""
    try:
        conn = auto_scraper.db.db_path
        # 这里可以添加删除逻辑
        return jsonify({'success': True, 'message': '关键词删除成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/articles')
def get_articles():
    """获取文章列表"""
    keyword_id = request.args.get('keyword_id', type=int)
    limit = request.args.get('limit', 50, type=int)
    
    articles = auto_scraper.db.get_articles(keyword_id, limit)
    return jsonify(articles)

@app.route('/api/tasks')
def get_tasks():
    """获取任务列表"""
    status = request.args.get('status')
    limit = request.args.get('limit', 50, type=int)
    
    tasks = auto_scraper.db.get_tasks(status, limit)
    return jsonify(tasks)

@app.route('/api/scrape', methods=['POST'])
def manual_scrape():
    """手动采集"""
    data = request.get_json()
    keyword = data.get('keyword', '').strip()
    max_articles = data.get('max_articles', 5)
    
    if not keyword:
        return jsonify({'success': False, 'message': '请输入关键词'})
    
    def scrape_async():
        result = auto_scraper.auto_scrape_keyword(keyword, max_articles)
        print(f"手动采集完成: {result}")
    
    # 启动异步任务
    thread = threading.Thread(target=scrape_async)
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'message': '开始采集，请稍后查看结果'})

@app.route('/api/auto-scraper/start', methods=['POST'])
def start_auto_scraper():
    """启动自动采集"""
    global scraping_status
    
    if scraping_status['is_running']:
        return jsonify({'success': False, 'message': '自动采集服务已在运行'})
    
    data = request.get_json()
    keywords = data.get('keywords', [])
    interval_hours = data.get('interval_hours', 6)
    max_articles_per_keyword = data.get('max_articles_per_keyword', 5)
    
    if not keywords:
        return jsonify({'success': False, 'message': '请至少添加一个关键词'})
    
    # 更新状态
    scraping_status.update({
        'is_running': True,
        'keywords': keywords,
        'interval_hours': interval_hours,
        'max_articles_per_keyword': max_articles_per_keyword
    })
    
    # 启动自动采集
    result = auto_scraper.start_auto_scraper(keywords, interval_hours, max_articles_per_keyword)
    
    return jsonify(result)

@app.route('/api/auto-scraper/stop', methods=['POST'])
def stop_auto_scraper():
    """停止自动采集"""
    global scraping_status
    
    result = auto_scraper.stop_auto_scraper()
    scraping_status['is_running'] = False
    
    return jsonify(result)

@app.route('/api/auto-scraper/settings', methods=['POST'])
def set_auto_scraper_settings():
    """设置自动采集参数"""
    data = request.get_json()
    batch_size = data.get('batch_size', 100)
    rest_minutes = data.get('rest_minutes', 5)
    
    try:
        auto_scraper.set_batch_settings(batch_size, rest_minutes)
        return jsonify({'success': True, 'message': f'批量采集设置已更新: 每{batch_size}篇休息{rest_minutes}分钟'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/auto-scraper/status')
def get_auto_scraper_status():
    """获取自动采集状态"""
    global scraping_status
    
    status_data = auto_scraper.get_scraping_status()
    status_data.update(scraping_status)
    
    return jsonify(status_data)

@app.route('/api/stats')
def get_stats():
    """获取统计信息"""
    stats = auto_scraper.db.get_stats()
    return jsonify(stats)

@app.route('/api/download/<filename>')
def download_file(filename):
    """下载文件"""
    try:
        from flask import send_file
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/view/<filename>')
def view_html(filename):
    """查看HTML文件"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"文件读取失败: {str(e)}", 404

if __name__ == '__main__':
    print("🚀 启动微信公众号自动采集管理系统")
    print("🌐 访问地址: http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=False)
