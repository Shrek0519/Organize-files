import os
import sys
import winshell
from win32com.client import Dispatch

def create_shortcut():
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Python解释器路径
    python_path = sys.executable
    
    # 创建快捷方式
    desktop = winshell.desktop()
    path = os.path.join(desktop, "文件整理助手.lnk")
    
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = python_path
    shortcut.Arguments = 'launcher.py'
    shortcut.WorkingDirectory = current_dir
    shortcut.IconLocation = os.path.join(current_dir, 'file_organizer.ico')
    shortcut.save()

if __name__ == '__main__':
    create_shortcut() 