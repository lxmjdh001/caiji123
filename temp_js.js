        // 全局变量
        let currentResult = null;
        let statusInterval = null;

        // DOM元素
        const urlInput = document.getElementById('urlInput');
        const scrapeBtn = document.getElementById('scrapeBtn');
        const clearBtn = document.getElementById('clearBtn');
        const historyBtn = document.getElementById('historyBtn');
        const progressSection = document.getElementById('progressSection');
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        const resultSection = document.getElementById('resultSection');
        const resultContent = document.getElementById('resultContent');
        const historySection = document.getElementById('historySection');
        const historyList = document.getElementById('historyList');
        const downloadBtn = document.getElementById('downloadBtn');
        const downloadHtmlBtn = document.getElementById('downloadHtmlBtn');
        const viewHtmlBtn = document.getElementById('viewHtmlBtn');
        const copyBtn = document.getElementById('copyBtn');

        // 事件监听
        scrapeBtn.addEventListener('click', startScraping);
        clearBtn.addEventListener('click', clearAll);
        historyBtn.addEventListener('click', toggleHistory);
        downloadBtn.addEventListener('click', downloadResult);
        downloadHtmlBtn.addEventListener('click', downloadHtmlResult);
        viewHtmlBtn.addEventListener('click', viewHtmlResult);
        copyBtn.addEventListener('click', copyResult);

        // 开始采集
        async function startScraping() {
            const url = urlInput.value.trim();
            if (!url) {
                alert('请输入有效的URL');
                return;
            }

            // 重置状态
            scrapeBtn.disabled = true;
            scrapeBtn.innerHTML = '<span class="loading"></span> 采集中...';
            progressSection.style.display = 'block';
            resultSection.style.display = 'none';
            historySection.classList.add('hidden');

            try {
                // 发送采集请求
                const response = await fetch('/api/scrape', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url: url })
                });

                const data = await response.json();
                if (data.success) {
                    // 开始轮询状态
                    startStatusPolling();
                } else {
                    showError(data.message);
                    resetUI();
                }
            } catch (error) {
                showError('网络错误: ' + error.message);
                resetUI();
            }
        }

        // 开始状态轮询
        function startStatusPolling() {
            statusInterval = setInterval(async () => {
                try {
                    const response = await fetch('/api/status');
                    const status = await response.json();
                    
                    updateProgress(status);
                    
                    if (!status.is_running) {
                        clearInterval(statusInterval);
                        if (status.result) {
                            showResult(status.result);
                        } else {
                            showError(status.error || '采集失败');
                        }
                        resetUI();
                    }
                } catch (error) {
                    clearInterval(statusInterval);
                    showError('状态查询失败: ' + error.message);
                    resetUI();
                }
            }, 1000);
        }

        // 更新进度
        function updateProgress(status) {
            progressFill.style.width = status.progress + '%';
            progressText.textContent = status.message;
        }

        // 显示结果
        function showResult(result) {
            currentResult = result;
            resultSection.style.display = 'block';
            
            const html = `
                <div class="result-content">
                    <div class="result-item">
                        <strong>标题:</strong> ${result.title || '未知'}
                    </div>
                    <div class="result-item">
                        <strong>作者:</strong> ${result.author || '未知'}
                    </div>
                    <div class="result-item">
                        <strong>时间:</strong> ${new Date(result.scrape_time).toLocaleString()}
                    </div>
                </div>
                <div class="result-item">
                    <strong>JSON数据:</strong>
                    <div class="json-output">${JSON.stringify(result, null, 2)}</div>
                </div>
            `;
            
            resultContent.innerHTML = html;
        }

        // 显示错误
        function showError(message) {
            resultSection.style.display = 'block';
            resultContent.innerHTML = `
                <div class="error-message">
                    <strong>❌ 错误:</strong> ${message}
                </div>
            `;
        }

        // 重置UI
        function resetUI() {
            scrapeBtn.disabled = false;
            scrapeBtn.innerHTML = '🔍 开始采集';
        }

        // 清空所有
        function clearAll() {
            urlInput.value = '';
            progressSection.style.display = 'none';
            resultSection.style.display = 'none';
            historySection.classList.add('hidden');
            currentResult = null;
        }

        // 切换历史记录
        async function toggleHistory() {
            if (historySection.classList.contains('hidden')) {
                await loadHistory();
                historySection.classList.remove('hidden');
                historyBtn.innerHTML = '🔙 返回';
            } else {
                historySection.classList.add('hidden');
                historyBtn.innerHTML = '📚 采集历史';
            }
        }

        // 加载历史记录
        async function loadHistory() {
            try {
                const response = await fetch('/api/history');
                const data = await response.json();
                
                if (data.success) {
                    if (data.data.length === 0) {
                        historyList.innerHTML = '<p>暂无采集历史</p>';
                    } else {
                        const html = data.data.map(item => `
                            <div class="history-item">
                                <div class="history-info">
                                    <div class="history-filename">${item.filename}</div>
                                    <div class="history-meta">
                                        大小: ${(item.size / 1024).toFixed(1)} KB | 
                                        修改时间: ${new Date(item.modified).toLocaleString()}
                                    </div>
                                </div>
                                <div>
                                    <button class="btn" onclick="downloadFile('${item.filename}')">下载</button>
                                </div>
                            </div>
                        `).join('');
                        historyList.innerHTML = html;
                    }
                } else {
                    historyList.innerHTML = '<p>加载历史记录失败</p>';
                }
            } catch (error) {
                historyList.innerHTML = '<p>加载历史记录失败: ' + error.message + '</p>';
            }
        }

        // 下载文件
        function downloadFile(filename) {
            window.open(`/api/download/${filename}`, '_blank');
        }

        // 下载结果
        function downloadResult() {
            if (currentResult) {
                const blob = new Blob([JSON.stringify(currentResult, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `article_${new Date().getTime()}.json`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }
        }

        // 下载HTML结果
        function downloadHtmlResult() {
            if (currentResult) {
                // 生成HTML文件名
                const safeTitle = currentResult.title.replace(/[^\w\s-]/g, '').substring(0, 50);
                const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
                const filename = `${timestamp}_${safeTitle}.html`;
                
                // 创建HTML内容
                const htmlContent = generateHtmlContent(currentResult);
                
                // 下载文件
                const blob = new Blob([htmlContent], { type: 'text/html' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }
        }

        // 查看HTML结果
        function viewHtmlResult() {
            if (currentResult) {
                const htmlContent = generateHtmlContent(currentResult);
                const newWindow = window.open('', '_blank');
                newWindow.document.write(htmlContent);
                newWindow.document.close();
            }
        }

        // 生成SEO关键词
        function generateKeywords(articleData) {
            const title = articleData.title || '';
            const keywords = ['微信公众号', '文章', '新闻', '博客'];
            
            if (title) {
                // 按空格和标点符号分割标题
                const titleWords = title.split(/[\s,，。！？；：""''（）【】]/).filter(word => word.length > 1);
                keywords.push(...titleWords.slice(0, 5));
            }
            
            return keywords.slice(0, 10).join(',');
        }
        
        // 生成结构化数据
        function generateStructuredData(articleData, scrapeTimeIso) {
            const structuredData = {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": articleData.title || '未知标题',
                "description": articleData.summary || '',
                "author": {
                    "@type": "Person",
                    "name": articleData.author || '未知作者'
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "文章采集工具"
                },
                "datePublished": scrapeTimeIso,
                "dateModified": scrapeTimeIso,
                "mainEntityOfPage": {
                    "@type": "WebPage",
                    "@id": articleData.url || ''
                },
                "articleBody": (articleData.content || '').substring(0, 500) + '...'
            };
            
            return JSON.stringify(structuredData, null, 2);
        }
        
        // 生成规范URL
        function generateCanonicalUrl(articleData) {
            const title = articleData.title || 'unknown';
            const slug = title.replace(/[^\w\s-]/g, '').replace(/\s+/g, '-').toLowerCase();
            return `https://example.com/articles/${slug}`;
        }

        // 生成HTML内容
        function generateHtmlContent(articleData) {
            const scrapeTime = new Date().toLocaleString();
            const scrapeTimeIso = new Date().toISOString();
            
            // 格式化内容
            const contentHtml = formatContentHtml(articleData.content || '');
            
            // 生成封面图片
            const coverHtml = generateCoverImage(articleData);
            
            // 格式化图片
            const imagesHtml = formatImagesHtml(articleData.images || []);
            
            // 生成SEO相关数据
            const keywords = generateKeywords(articleData);
            const structuredData = generateStructuredData(articleData, scrapeTimeIso);
            const canonicalUrl = generateCanonicalUrl(articleData);
            
            return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${articleData.title || '未知标题'}</title>
    <meta name="description" content="${articleData.summary || ''}">
    <meta name="author" content="${articleData.author || '未知作者'}">
    <meta name="keywords" content="${keywords}">
    <meta name="robots" content="index, follow">
    <meta name="googlebot" content="index, follow">
    <link rel="canonical" href="${canonicalUrl}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="${articleData.title || '未知标题'}">
    <meta property="og:description" content="${articleData.summary || ''}">
    <meta property="og:author" content="${articleData.author || '未知作者'}">
    <meta property="og:site_name" content="文章采集工具">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:title" content="${articleData.title || '未知标题'}">
    <meta property="twitter:description" content="${articleData.summary || ''}">
    
    <!-- 结构化数据 -->
    <script type="application/ld+json">
    ${structuredData}
