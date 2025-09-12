#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动管理界面
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
    print("🚀 启动微信公众号自动采集管理系统")
    print("=" * 60)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 启动管理应用
    print("📱 正在启动管理界面...")
    print("🌐 管理界面: http://localhost:5001")
    print("🌐 采集界面: http://localhost:3000")
    print("⏹️  按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    try:
        from admin_app import app
        app.run(host='0.0.0.0', port=5001, debug=False)
    except KeyboardInterrupt:
        print("\n👋 管理界面已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()
