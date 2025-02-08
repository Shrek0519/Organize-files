import os
import sys
import tkinter as tk
from tkinter import messagebox
import subprocess

def check_dependencies():
    try:
        import sv_ttk
        import pandas
        return True
    except ImportError as e:
        return str(e)

def install_dependencies():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "sv-ttk", "pandas"])
        return True
    except Exception as e:
        return str(e)

def main():
    # 检查是否存在必要的文件
    required_files = ['gui.py', 'file_classifier.py', 'file_scanner.py', 'tag_generator.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        messagebox.showerror("错误", f"缺少必要文件：\n{', '.join(missing_files)}\n\n请确保所有程序文件都在同一目录下。")
        return

    # 检查依赖
    deps_check = check_dependencies()
    if deps_check is not True:
        if messagebox.askyesno("缺少依赖", f"缺少必要的依赖包。\n是否要自动安装？"):
            result = install_dependencies()
            if result is not True:
                messagebox.showerror("安装失败", f"依赖安装失败：\n{result}")
                return
        else:
            return

    # 运行主程序
    try:
        import gui
        app = gui.FileOrganizerGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("错误", f"程序运行出错：\n{str(e)}")

if __name__ == "__main__":
    main() 