#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动微信公众号文章采集工具
"""

import subprocess
import sys
import os

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import requests
        import flask
        import bs4
        import fake_useragent
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def main():
    """主函数"""
    print("🚀 启动微信公众号文章采集工具")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 启动应用
    print("📱 正在启动Web服务器...")
    print("🌐 访问地址: http://localhost:3000")
    print("⏹️  按 Ctrl+C 停止服务器")
    print("=" * 50)
    
    try:
        from app import app
        app.run(host='0.0.0.0', port=3000, debug=False)
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()
