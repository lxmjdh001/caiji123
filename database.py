#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库模型和操作
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path: str = "articles.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建关键词表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT UNIQUE NOT NULL,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建文章表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                content TEXT,
                url TEXT UNIQUE NOT NULL,
                keyword_id INTEGER,
                scrape_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                word_count INTEGER DEFAULT 0,
                html_file TEXT,
                url_number INTEGER,
                status TEXT DEFAULT 'scraped',
                FOREIGN KEY (keyword_id) REFERENCES keywords (id)
            )
        ''')
        
        # 检查是否需要添加url_number字段
        cursor.execute("PRAGMA table_info(articles)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'url_number' not in columns:
            cursor.execute('ALTER TABLE articles ADD COLUMN url_number INTEGER')
        
        # 创建采集任务表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword_id INTEGER,
                task_type TEXT DEFAULT 'search',
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                result TEXT,
                error_message TEXT,
                FOREIGN KEY (keyword_id) REFERENCES keywords (id)
            )
        ''')
        
        # 创建URL计数器表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS url_counter (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                current_count INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 初始化计数器
        cursor.execute('SELECT COUNT(*) FROM url_counter')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO url_counter (current_count) VALUES (0)')
        
        conn.commit()
        conn.close()
    
    def add_keyword(self, keyword: str) -> int:
        """添加关键词"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO keywords (keyword) VALUES (?)
            ''', (keyword,))
            
            cursor.execute('''
                SELECT id FROM keywords WHERE keyword = ?
            ''', (keyword,))
            
            result = cursor.fetchone()
            conn.commit()
            return result[0] if result else None
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_keywords(self, status: str = 'active') -> List[Dict]:
        """获取关键词列表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, keyword, status, created_at FROM keywords 
            WHERE status = ? ORDER BY created_at DESC
        ''', (status,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'keyword': row[1],
                'status': row[2],
                'created_at': row[3]
            }
            for row in results
        ]
    
    def add_article(self, article_data: Dict, keyword_id: Optional[int] = None) -> int:
        """添加文章"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO articles 
                (title, author, content, url, keyword_id, word_count, html_file, url_number, scrape_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                article_data['title'],
                article_data['author'],
                article_data['content'],
                article_data['url'],
                keyword_id,
                article_data['word_count'],
                article_data.get('html_file'),
                article_data.get('url_number'),
                article_data['scrape_time']
            ))
            
            article_id = cursor.lastrowid
            conn.commit()
            return article_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_articles(self, keyword_id: Optional[int] = None, limit: int = 50) -> List[Dict]:
        """获取文章列表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if keyword_id:
            cursor.execute('''
                SELECT a.*, k.keyword FROM articles a
                LEFT JOIN keywords k ON a.keyword_id = k.id
                WHERE a.keyword_id = ? ORDER BY a.scrape_time DESC LIMIT ?
            ''', (keyword_id, limit))
        else:
            cursor.execute('''
                SELECT a.*, k.keyword FROM articles a
                LEFT JOIN keywords k ON a.keyword_id = k.id
                ORDER BY a.scrape_time DESC LIMIT ?
            ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'content': row[3],
                'url': row[4],
                'keyword_id': row[5],
                'scrape_time': row[6],
                'word_count': row[7],
                'html_file': row[8],
                'status': row[9],
                'url_number': row[10],
                'keyword': row[11]
            }
            for row in results
        ]
    
    def add_task(self, keyword_id: int, task_type: str = 'search') -> int:
        """添加任务"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO tasks (keyword_id, task_type) VALUES (?, ?)
            ''', (keyword_id, task_type))
            
            task_id = cursor.lastrowid
            conn.commit()
            return task_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def update_task_status(self, task_id: int, status: str, result: str = None, error: str = None):
        """更新任务状态"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            now = datetime.now().isoformat()
            
            if status == 'running':
                cursor.execute('''
                    UPDATE tasks SET status = ?, started_at = ? WHERE id = ?
                ''', (status, now, task_id))
            elif status in ['completed', 'failed']:
                cursor.execute('''
                    UPDATE tasks SET status = ?, completed_at = ?, result = ?, error_message = ? WHERE id = ?
                ''', (status, now, result, error, task_id))
            else:
                cursor.execute('''
                    UPDATE tasks SET status = ? WHERE id = ?
                ''', (status, task_id))
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_tasks(self, status: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """获取任务列表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status:
            cursor.execute('''
                SELECT t.*, k.keyword FROM tasks t
                LEFT JOIN keywords k ON t.keyword_id = k.id
                WHERE t.status = ? ORDER BY t.created_at DESC LIMIT ?
            ''', (status, limit))
        else:
            cursor.execute('''
                SELECT t.*, k.keyword FROM tasks t
                LEFT JOIN keywords k ON t.keyword_id = k.id
                ORDER BY t.created_at DESC LIMIT ?
            ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'keyword_id': row[1],
                'task_type': row[2],
                'status': row[3],
                'created_at': row[4],
                'started_at': row[5],
                'completed_at': row[6],
                'result': row[7],
                'error_message': row[8],
                'keyword': row[9]
            }
            for row in results
        ]
    
    def get_random_articles(self, limit: int = 15) -> List[Dict]:
        """获取随机文章列表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, author, scrape_time, html_file, url_number FROM articles 
            ORDER BY RANDOM() LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'scrape_time': row[3],
                'html_file': row[4],
                'url_number': row[5]
            }
            for row in results
        ]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 关键词数量
        cursor.execute('SELECT COUNT(*) FROM keywords WHERE status = "active"')
        keyword_count = cursor.fetchone()[0]
        
        # 文章数量
        cursor.execute('SELECT COUNT(*) FROM articles')
        article_count = cursor.fetchone()[0]
        
        # 今日文章数量
        cursor.execute('''
            SELECT COUNT(*) FROM articles 
            WHERE DATE(scrape_time) = DATE('now')
        ''')
        today_articles = cursor.fetchone()[0]
        
        # 任务统计
        cursor.execute('SELECT status, COUNT(*) FROM tasks GROUP BY status')
        task_stats = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'keyword_count': keyword_count,
            'article_count': article_count,
            'today_articles': today_articles,
            'task_stats': task_stats
        }
    
    def get_next_url_number(self) -> int:
        """获取下一个URL编号"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 获取当前计数并递增
            cursor.execute('SELECT current_count FROM url_counter ORDER BY id DESC LIMIT 1')
            result = cursor.fetchone()
            
            if result:
                current_count = result[0]
                next_count = current_count + 1
            else:
                next_count = 1
            
            # 更新计数器
            cursor.execute('UPDATE url_counter SET current_count = ?, updated_at = CURRENT_TIMESTAMP WHERE id = (SELECT id FROM url_counter ORDER BY id DESC LIMIT 1)', (next_count,))
            
            conn.commit()
            return next_count
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
