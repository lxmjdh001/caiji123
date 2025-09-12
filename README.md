# 微信公众号文章采集系统

一个简洁高效的微信公众号文章采集和发布系统，支持自动采集、HTML生成和推荐阅读功能。

## ✨ 功能特点

- 🚀 **简洁高效** - 基于Flask的轻量级Web应用
- 📱 **Web界面** - 友好的用户界面，支持URL输入和实时状态显示
- 🔄 **自动采集** - 支持微信公众号文章自动采集和解析
- 📄 **HTML生成** - 自动生成美观的HTML文章页面
- 🔗 **推荐阅读** - 智能推荐相关文章，提升用户体验
- 🎯 **URL管理** - 支持简洁的`new/1`递增URL格式
- 💾 **数据库支持** - SQLite数据库存储文章和关键词
- 🤖 **自动任务** - 支持基于关键词的自动采集任务

## 🛠️ 技术栈

- **后端**: Python 3.8+, Flask
- **数据库**: SQLite
- **前端**: HTML, CSS, JavaScript
- **采集**: requests, BeautifulSoup4
- **部署**: 支持服务器部署

## 📦 安装部署

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/wechat-article-scraper.git
cd wechat-article-scraper
```

### 2. 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 启动应用
```bash
# 启动采集界面
python start.py

# 启动管理界面
python start_admin.py
```

## 🚀 使用方法

### 基础采集
1. 访问 http://localhost:3000
2. 输入微信公众号文章URL
3. 点击"开始采集"
4. 等待采集完成
5. 查看生成的HTML文件

### 自动采集
1. 访问 http://localhost:5001 (管理界面)
2. 添加关键词
3. 启动自动采集任务
4. 系统会自动搜索和采集相关文章

## 📁 项目结构

```
├── app.py                 # 主Web应用
├── admin_app.py           # 管理界面应用
├── scraper.py             # 文章采集核心
├── auto_scraper.py        # 自动采集功能
├── database.py            # 数据库操作
├── start.py               # 启动脚本
├── start_admin.py         # 管理界面启动脚本
├── requirements.txt       # 依赖包
├── templates/             # HTML模板
│   ├── index.html         # 主界面
│   └── admin.html         # 管理界面
└── README.md              # 项目说明
```

## 🔧 配置说明

### 端口配置
- 采集界面: 3000
- 管理界面: 5001

### 数据库
- 默认使用SQLite数据库
- 自动创建表结构
- 支持文章、关键词、任务管理

## 📱 访问地址

- **采集界面**: http://localhost:3000
- **管理界面**: http://localhost:5001
- **文章访问**: http://localhost:3000/new/1

## 🎯 URL格式

系统支持简洁的URL格式：
- `new/1` - 第一篇文章
- `new/2` - 第二篇文章
- `new/3` - 第三篇文章
- ...

## 🤝 贡献

欢迎提交Issue和Pull Request来改进项目！

## 📄 许可证

MIT License

## ⚠️ 注意事项

- 请遵守相关法律法规和网站使用条款
- 建议合理使用采集功能，避免对目标网站造成压力
- 生成的HTML文件仅供学习和研究使用