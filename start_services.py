#!/usr/bin/env python3
"""
PandaFactor 服务启动脚本
同时启动 panda_web 和 panda_factor_server 服务
"""

import os
import sys
import subprocess
import signal
import time
from multiprocessing import Process

def start_panda_factor_server():
    """启动 panda_factor_server 服务"""
    print("🚀 启动 panda_factor_server 服务...")
    os.chdir(os.path.join(os.path.dirname(__file__), 'panda_factor_server'))
    subprocess.run([sys.executable, '-m', 'panda_factor_server'])

def start_panda_web():
    """启动 panda_web 服务"""
    print("🌐 启动 panda_web 服务...")
    os.chdir(os.path.join(os.path.dirname(__file__), 'panda_web'))
    subprocess.run([sys.executable, 'panda_web/main.py'])

def signal_handler(signum, frame):
    """信号处理器，用于优雅关闭服务"""
    print("\n🛑 接收到停止信号，正在关闭服务...")
    sys.exit(0)

def main():
    """主函数"""
    print("="*60)
    print("🐼 PandaFactor 服务启动器")
    print("="*60)
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 创建进程
    server_process = Process(target=start_panda_factor_server, name="PandaFactorServer")
    web_process = Process(target=start_panda_web, name="PandaWeb")
    
    try:
        # 启动服务
        print("📡 启动后端服务 (panda_factor_server)...")
        server_process.start()
        time.sleep(2)  # 等待服务器启动
        
        print("🖥️  启动前端服务 (panda_web)...")
        web_process.start()
        time.sleep(2)  # 等待 Web 服务启动
        
        print("\n✅ 所有服务已启动!")
        print("📊 后端 API 服务: http://localhost:8111")
        print("🌐 前端 Web 界面: http://localhost:8080")
        print("\n按 Ctrl+C 停止所有服务")
        print("="*60)
        
        # 等待进程结束
        server_process.join()
        web_process.join()
        
    except KeyboardInterrupt:
        print("\n🛑 用户中断，正在停止服务...")
    except Exception as e:
        print(f"❌ 启动服务时出错: {e}")
    finally:
        # 确保所有进程都被终止
        if server_process.is_alive():
            print("🔄 停止后端服务...")
            server_process.terminate()
            server_process.join(timeout=5)
            if server_process.is_alive():
                server_process.kill()
        
        if web_process.is_alive():
            print("🔄 停止前端服务...")
            web_process.terminate()
            web_process.join(timeout=5)
            if web_process.is_alive():
                web_process.kill()
        
        print("✅ 所有服务已停止")

if __name__ == "__main__":
    main()