#!/bin/bash

# 微信公众号自动采集管理系统 - 模板修复脚本
# 用于解决 TemplateNotFound 错误

echo "🔧 开始修复模板文件问题..."

# 检查当前目录
echo "📁 当前工作目录: $(pwd)"

# 检查是否存在 templates 目录
if [ ! -d "templates" ]; then
    echo "📂 创建 templates 目录..."
    mkdir -p templates
else
    echo "✅ templates 目录已存在"
fi

# 创建 admin.html 模板文件
echo "📝 创建 admin.html 模板文件..."
cat > templates/admin.html << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微信公众号自动采集管理系统</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .content {
            padding: 40px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border-left: 4px solid #4facfe;
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #4facfe;
        }
        
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        
        .section {
            margin-bottom: 40px;
        }
        
        .section-title {
            font-size: 1.5em;
            margin-bottom: 20px;
            color: #333;
            border-bottom: 2px solid #4facfe;
            padding-bottom: 10px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        
        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            outline: none;
            border-color: #4facfe;
        }
        
        .btn {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .btn.danger {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        }
        
        .btn.success {
            background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
        }
        
        .btn.warning {
            background: linear-gradient(135deg, #ffd43b 0%, #fab005 100%);
        }
        
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        
        .table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        .table th, .table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e1e5e9;
        }
        
        .table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
        }
        
        .table tr:hover {
            background: #f8f9fa;
        }
        
        .status-badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .status-active {
            background: #d4edda;
            color: #155724;
        }
        
        .status-running {
            background: #cce5ff;
            color: #004085;
        }
        
        .status-completed {
            background: #d1ecf1;
            color: #0c5460;
        }
        
        .status-failed {
            background: #f8d7da;
            color: #721c24;
        }
        
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .alert-info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #4facfe;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .grid-2 {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 微信公众号自动采集管理系统</h1>
            <p>智能关键词搜索 · 自动采集 · HTML生成 · 批量发布</p>
        </div>
        
        <div class="content">
            <!-- 统计信息 -->
            <div class="stats-grid" id="statsGrid">
                <div class="stat-card">
                    <div class="stat-number" id="keywordCount">-</div>
                    <div class="stat-label">活跃关键词</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="articleCount">-</div>
                    <div class="stat-label">总文章数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="todayArticles">-</div>
                    <div class="stat-label">今日采集</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="runningTasks">-</div>
                    <div class="stat-label">运行中任务</div>
                </div>
            </div>
            
            <div class="grid-2">
                <!-- 关键词管理 -->
                <div class="section">
                    <h2 class="section-title">📝 关键词管理</h2>
                    
                    <div class="form-group">
                        <label for="newKeyword">添加新关键词</label>
                        <input type="text" id="newKeyword" placeholder="输入关键词，如：加拿大移民">
                    </div>
                    
                    <button class="btn" onclick="addKeyword()">添加关键词</button>
                    <button class="btn success" onclick="refreshKeywords()">刷新列表</button>
                    
                    <div id="keywordsList">
                        <div class="loading">
                            <div class="spinner"></div>
                            <div>加载中...</div>
                        </div>
                    </div>
                </div>
                
                <!-- 自动采集设置 -->
                <div class="section">
                    <h2 class="section-title">⚙️ 自动采集设置</h2>
                    
                    <div class="form-group">
                        <label for="intervalHours">采集间隔（小时）</label>
                        <select id="intervalHours">
                            <option value="1">1小时</option>
                            <option value="3">3小时</option>
                            <option value="6" selected>6小时</option>
                            <option value="12">12小时</option>
                            <option value="24">24小时</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="maxArticles">每个关键词最大采集数</label>
                        <select id="maxArticles">
                            <option value="3">3篇</option>
                            <option value="5" selected>5篇</option>
                            <option value="10">10篇</option>
                            <option value="20">20篇</option>
                        </select>
                    </div>
                    
                    <button class="btn success" onclick="startAutoScraper()">启动自动采集</button>
                    <button class="btn danger" onclick="stopAutoScraper()">停止自动采集</button>
                    
                    <div id="autoScraperStatus" class="alert alert-info" style="margin-top: 20px;">
                        自动采集服务状态：<span id="statusText">检查中...</span>
                    </div>
                </div>
            </div>
            
            <!-- 手动采集 -->
            <div class="section">
                <h2 class="section-title">🎯 手动采集</h2>
                
                <div class="form-group">
                    <label for="manualKeyword">关键词</label>
                    <input type="text" id="manualKeyword" placeholder="输入要采集的关键词">
                </div>
                
                <div class="form-group">
                    <label for="manualMaxArticles">采集数量</label>
                    <select id="manualMaxArticles">
                        <option value="3">3篇</option>
                        <option value="5" selected>5篇</option>
                        <option value="10">10篇</option>
                    </select>
                </div>
                
                <button class="btn" onclick="manualScrape()">开始采集</button>
            </div>
            
            <!-- 最近任务 -->
            <div class="section">
                <h2 class="section-title">📋 最近任务</h2>
                <button class="btn" onclick="refreshTasks()">刷新任务列表</button>
                
                <div id="tasksList">
                    <div class="loading">
                        <div class="spinner"></div>
                        <div>加载中...</div>
                    </div>
                </div>
            </div>
            
            <!-- 最近文章 -->
            <div class="section">
                <h2 class="section-title">📰 最近文章</h2>
                <button class="btn" onclick="refreshArticles()">刷新文章列表</button>
                
                <div id="articlesList">
                    <div class="loading">
                        <div class="spinner"></div>
                        <div>加载中...</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 页面加载时初始化
        document.addEventListener('DOMContentLoaded', function() {
            loadStats();
            loadKeywords();
            loadTasks();
            loadArticles();
            checkAutoScraperStatus();
            
            // 每30秒刷新一次状态
            setInterval(function() {
                loadStats();
                checkAutoScraperStatus();
            }, 30000);
        });
        
        // 加载统计信息
        function loadStats() {
            fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                document.getElementById('keywordCount').textContent = data.keyword_count || 0;
                document.getElementById('articleCount').textContent = data.article_count || 0;
                document.getElementById('todayArticles').textContent = data.today_articles || 0;
                document.getElementById('runningTasks').textContent = data.task_stats?.running || 0;
            })
            .catch(error => {
                console.error('加载统计信息失败:', error);
            });
        }
        
        // 加载关键词列表
        function loadKeywords() {
            const container = document.getElementById('keywordsList');
            container.innerHTML = '<div class="loading"><div class="spinner"></div><div>加载中...</div></div>';
            
            fetch('/api/keywords')
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    container.innerHTML = '<div class="alert alert-info">暂无关键词</div>';
                    return;
                }
                
                let html = '<table class="table"><thead><tr><th>关键词</th><th>状态</th><th>添加时间</th><th>操作</th></tr></thead><tbody>';
                
                data.forEach(keyword => {
                    html += `
                        <tr>
                            <td>${keyword.keyword}</td>
                            <td><span class="status-badge status-active">活跃</span></td>
                            <td>${new Date(keyword.created_at).toLocaleString()}</td>
                            <td>
                                <button class="btn danger" onclick="deleteKeyword(${keyword.id})">删除</button>
                            </td>
                        </tr>
                    `;
                });
                
                html += '</tbody></table>';
                container.innerHTML = html;
            })
            .catch(error => {
                container.innerHTML = '<div class="alert alert-error">加载失败: ' + error.message + '</div>';
            });
        }
        
        // 添加关键词
        function addKeyword() {
            const keyword = document.getElementById('newKeyword').value.trim();
            
            if (!keyword) {
                alert('请输入关键词');
                return;
            }
            
            fetch('/api/keywords', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ keyword: keyword })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('newKeyword').value = '';
                    loadKeywords();
                    loadStats();
                    alert('关键词添加成功');
                } else {
                    alert('添加失败: ' + data.message);
                }
            })
            .catch(error => {
                alert('添加失败: ' + error.message);
            });
        }
        
        // 删除关键词
        function deleteKeyword(id) {
            if (!confirm('确定要删除这个关键词吗？')) {
                return;
            }
            
            fetch(`/api/keywords/${id}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    loadKeywords();
                    loadStats();
                    alert('关键词删除成功');
                } else {
                    alert('删除失败: ' + data.message);
                }
            })
            .catch(error => {
                alert('删除失败: ' + error.message);
            });
        }
        
        // 刷新关键词列表
        function refreshKeywords() {
            loadKeywords();
        }
        
        // 启动自动采集
        function startAutoScraper() {
            const intervalHours = parseInt(document.getElementById('intervalHours').value);
            const maxArticles = parseInt(document.getElementById('maxArticles').value);
            
            fetch('/api/keywords')
            .then(response => response.json())
            .then(keywords => {
                if (keywords.length === 0) {
                    alert('请先添加关键词');
                    return;
                }
                
                const keywordList = keywords.map(k => k.keyword);
                
                fetch('/api/auto-scraper/start', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        keywords: keywordList,
                        interval_hours: intervalHours,
                        max_articles_per_keyword: maxArticles
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('自动采集服务启动成功');
                        checkAutoScraperStatus();
                    } else {
                        alert('启动失败: ' + data.message);
                    }
                })
                .catch(error => {
                    alert('启动失败: ' + error.message);
                });
            });
        }
        
        // 停止自动采集
        function stopAutoScraper() {
            if (!confirm('确定要停止自动采集服务吗？')) {
                return;
            }
            
            fetch('/api/auto-scraper/stop', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('自动采集服务已停止');
                    checkAutoScraperStatus();
                } else {
                    alert('停止失败: ' + data.message);
                }
            })
            .catch(error => {
                alert('停止失败: ' + error.message);
            });
        }
        
        // 检查自动采集状态
        function checkAutoScraperStatus() {
            fetch('/api/auto-scraper/status')
            .then(response => response.json())
            .then(data => {
                const statusText = document.getElementById('statusText');
                const statusDiv = document.getElementById('autoScraperStatus');
                
                if (data.is_running) {
                    statusText.textContent = '运行中';
                    statusDiv.className = 'alert alert-success';
                } else {
                    statusText.textContent = '已停止';
                    statusDiv.className = 'alert alert-info';
                }
            })
            .catch(error => {
                console.error('检查状态失败:', error);
            });
        }
        
        // 手动采集
        function manualScrape() {
            const keyword = document.getElementById('manualKeyword').value.trim();
            const maxArticles = parseInt(document.getElementById('manualMaxArticles').value);
            
            if (!keyword) {
                alert('请输入关键词');
                return;
            }
            
            if (!confirm(`确定要采集关键词"${keyword}"的文章吗？`)) {
                return;
            }
            
            fetch('/api/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    keyword: keyword,
                    max_articles: maxArticles
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('开始采集，请稍后查看结果');
                    setTimeout(() => {
                        loadTasks();
                        loadArticles();
                        loadStats();
                    }, 5000);
                } else {
                    alert('采集失败: ' + data.message);
                }
            })
            .catch(error => {
                alert('采集失败: ' + error.message);
            });
        }
        
        // 加载任务列表
        function loadTasks() {
            const container = document.getElementById('tasksList');
            container.innerHTML = '<div class="loading"><div class="spinner"></div><div>加载中...</div></div>';
            
            fetch('/api/tasks')
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    container.innerHTML = '<div class="alert alert-info">暂无任务</div>';
                    return;
                }
                
                let html = '<table class="table"><thead><tr><th>关键词</th><th>任务类型</th><th>状态</th><th>创建时间</th><th>完成时间</th></tr></thead><tbody>';
                
                data.forEach(task => {
                    const statusClass = 'status-' + task.status;
                    html += `
                        <tr>
                            <td>${task.keyword || '-'}</td>
                            <td>${task.task_type}</td>
                            <td><span class="status-badge ${statusClass}">${task.status}</span></td>
                            <td>${new Date(task.created_at).toLocaleString()}</td>
                            <td>${task.completed_at ? new Date(task.completed_at).toLocaleString() : '-'}</td>
                        </tr>
                    `;
                });
                
                html += '</tbody></table>';
                container.innerHTML = html;
            })
            .catch(error => {
                container.innerHTML = '<div class="alert alert-error">加载失败: ' + error.message + '</div>';
            });
        }
        
        // 加载文章列表
        function loadArticles() {
            const container = document.getElementById('articlesList');
            container.innerHTML = '<div class="loading"><div class="spinner"></div><div>加载中...</div></div>';
            
            fetch('/api/articles')
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    container.innerHTML = '<div class="alert alert-info">暂无文章</div>';
                    return;
                }
                
                let html = '<table class="table"><thead><tr><th>标题</th><th>作者</th><th>关键词</th><th>字数</th><th>采集时间</th><th>操作</th></tr></thead><tbody>';
                
                data.forEach(article => {
                    html += `
                        <tr>
                            <td title="${article.title}">${article.title.length > 30 ? article.title.substring(0, 30) + '...' : article.title}</td>
                            <td>${article.author}</td>
                            <td>${article.keyword || '-'}</td>
                            <td>${article.word_count}</td>
                            <td>${new Date(article.scrape_time).toLocaleString()}</td>
                            <td>
                                ${article.html_file ? `<button class="btn" onclick="viewHtml('${article.html_file}')">查看HTML</button>` : ''}
                            </td>
                        </tr>
                    `;
                });
                
                html += '</tbody></table>';
                container.innerHTML = html;
            })
            .catch(error => {
                container.innerHTML = '<div class="alert alert-error">加载失败: ' + error.message + '</div>';
            });
        }
        
        // 查看HTML
        function viewHtml(filename) {
            window.open(`/api/view/${filename}`, '_blank');
        }
        
        // 刷新任务列表
        function refreshTasks() {
            loadTasks();
        }
        
        // 刷新文章列表
        function refreshArticles() {
            loadArticles();
        }
    </script>
</body>
</html>
EOF

# 检查文件是否创建成功
if [ -f "templates/admin.html" ]; then
    echo "✅ admin.html 模板文件创建成功"
    echo "📊 文件大小: $(wc -c < templates/admin.html) 字节"
else
    echo "❌ admin.html 模板文件创建失败"
    exit 1
fi

# 检查目录结构
echo "📁 当前目录结构:"
ls -la

echo "📁 templates 目录内容:"
ls -la templates/

echo ""
# 检查是否还需要创建 index.html（前台应用需要）
if [ ! -f "templates/index.html" ]; then
    echo "📝 创建 index.html 模板文件（前台应用需要）..."
    cat > templates/index.html << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微信公众号文章采集工具</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .content {
            padding: 40px;
        }
        
        .input-group {
            margin-bottom: 30px;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: #333;
        }
        
        .input-group input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        .input-group input:focus {
            outline: none;
            border-color: #4facfe;
        }
        
        .btn {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
            width: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .progress-container {
            margin: 20px 0;
            display: none;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e1e5e9;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            width: 0%;
            transition: width 0.3s;
        }
        
        .status {
            text-align: center;
            margin: 20px 0;
            font-weight: 600;
            color: #666;
        }
        
        .result {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            display: none;
        }
        
        .result h3 {
            color: #333;
            margin-bottom: 15px;
        }
        
        .result-item {
            margin-bottom: 10px;
            padding: 10px;
            background: white;
            border-radius: 5px;
            border-left: 4px solid #4facfe;
        }
        
        .result-item strong {
            color: #333;
        }
        
        .error {
            background: #ffe6e6;
            color: #d63031;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            display: none;
        }
        
        .actions {
            margin-top: 20px;
            display: flex;
            gap: 10px;
        }
        
        .actions .btn {
            flex: 1;
            background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        }
        
        .actions .btn.secondary {
            background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📰 微信公众号文章采集工具</h1>
            <p>简单、快速、高效的微信文章采集解决方案</p>
        </div>
        
        <div class="content">
            <div class="input-group">
                <label for="url">文章链接</label>
                <input type="url" id="url" placeholder="请输入微信公众号文章链接..." />
            </div>
            
            <button class="btn" id="scrapeBtn" onclick="startScraping()">开始采集</button>
            
            <div class="progress-container" id="progressContainer">
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div class="status" id="status">准备开始</div>
            </div>
            
            <div class="error" id="error"></div>
            
            <div class="result" id="result">
                <h3>📋 采集结果</h3>
                <div id="resultContent"></div>
                
                <div class="actions">
                    <button class="btn" onclick="downloadJSON()">下载JSON</button>
                    <button class="btn" onclick="downloadHTML()">下载HTML</button>
                    <button class="btn secondary" onclick="viewHTML()">查看HTML</button>
                    <button class="btn secondary" onclick="copyResult()">复制结果</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let scrapingInterval = null;
        
        function startScraping() {
            const url = document.getElementById('url').value.trim();
            
            if (!url) {
                showError('请输入文章链接');
                return;
            }
            
            if (!url.includes('mp.weixin.qq.com')) {
                showError('请输入有效的微信公众号文章链接');
                return;
            }
            
            // 重置UI
            resetUI();
            
            // 发送采集请求
            fetch('/api/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showProgress();
                    startPolling();
                } else {
                    showError(data.message);
                }
            })
            .catch(error => {
                showError('网络错误: ' + error.message);
            });
        }
        
        function startPolling() {
            scrapingInterval = setInterval(() => {
                fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    updateProgress(data);
                    
                    if (!data.is_running) {
                        clearInterval(scrapingInterval);
                        
                        if (data.error) {
                            showError(data.error);
                        } else if (data.result) {
                            showResult(data.result);
                        }
                    }
                })
                .catch(error => {
                    clearInterval(scrapingInterval);
                    showError('状态查询失败: ' + error.message);
                });
            }, 1000);
        }
        
        function updateProgress(data) {
            const progressFill = document.getElementById('progressFill');
            const status = document.getElementById('status');
            
            progressFill.style.width = data.progress + '%';
            status.textContent = data.message;
        }
        
        function showProgress() {
            document.getElementById('progressContainer').style.display = 'block';
            document.getElementById('scrapeBtn').disabled = true;
            document.getElementById('scrapeBtn').textContent = '采集中...';
        }
        
        function showResult(result) {
            const resultDiv = document.getElementById('result');
            const contentDiv = document.getElementById('resultContent');
            
            contentDiv.innerHTML = `
                <div class="result-item">
                    <strong>标题:</strong> ${result.title}
                </div>
                <div class="result-item">
                    <strong>作者:</strong> ${result.author}
                </div>
                <div class="result-item">
                    <strong>字数:</strong> ${result.word_count}
                </div>
                <div class="result-item">
                    <strong>时间:</strong> ${result.scrape_time}
                </div>
                <div class="result-item">
                    <strong>内容预览:</strong><br>
                    <div style="margin-top: 10px; max-height: 200px; overflow-y: auto; background: #f8f9fa; padding: 10px; border-radius: 5px;">
                        ${result.content.substring(0, 500)}${result.content.length > 500 ? '...' : ''}
                    </div>
                </div>
            `;
            
            resultDiv.style.display = 'block';
            resetUI();
        }
        
        function showError(message) {
            const errorDiv = document.getElementById('error');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            resetUI();
        }
        
        function resetUI() {
            document.getElementById('progressContainer').style.display = 'none';
            document.getElementById('scrapeBtn').disabled = false;
            document.getElementById('scrapeBtn').textContent = '开始采集';
            document.getElementById('error').style.display = 'none';
        }
        
        function downloadJSON() {
            fetch('/api/result')
            .then(response => response.json())
            .then(data => {
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `article_${data.scrape_time.replace(/[:\s]/g, '_')}.json`;
                a.click();
                URL.revokeObjectURL(url);
            });
        }
        
        function downloadHTML() {
            fetch('/api/status')
            .then(response => response.json())
            .then(data => {
                if (data.html_file) {
                    window.open(`/api/download/${data.html_file}`, '_blank');
                } else {
                    alert('HTML文件未生成');
                }
            });
        }
        
        function viewHTML() {
            fetch('/api/status')
            .then(response => response.json())
            .then(data => {
                if (data.html_file) {
                    window.open(`/api/view/${data.html_file}`, '_blank');
                } else {
                    alert('HTML文件未生成');
                }
            });
        }
        
        function copyResult() {
            fetch('/api/result')
            .then(response => response.json())
            .then(data => {
                navigator.clipboard.writeText(JSON.stringify(data, null, 2))
                .then(() => {
                    alert('结果已复制到剪贴板');
                })
                .catch(() => {
                    alert('复制失败，请手动复制');
                });
            });
        }
    </script>
</body>
</html>
EOF
    echo "✅ index.html 模板文件创建成功"
fi

echo "🎉 修复完成！现在可以重新启动应用了："
echo ""
echo "📱 前台应用（用户界面）:"
echo "   python app.py"
echo "   🌐 访问地址: http://localhost:3000"
echo "   🌐 外网访问: http://72.60.193.135:3000"
echo ""
echo "⚙️ 后台应用（管理界面）:"
echo "   python admin_app.py"
echo "   🌐 访问地址: http://localhost:5001"
echo "   🌐 外网访问: http://72.60.193.135:5001"
echo ""
echo "💡 提示：如果需要外网访问，请确保防火墙已开放相应端口："
echo "   sudo ufw allow 3000/tcp  # 前台应用端口"
echo "   sudo ufw allow 5001/tcp  # 后台应用端口"
