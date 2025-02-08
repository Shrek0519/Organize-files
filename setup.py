import sys
from cx_Freeze import setup, Executable

# 依赖包
build_exe_options = {
    "packages": ["os", "tkinter", "sv_ttk", "customtkinter", "pandas"],
    "excludes": [],
    "include_files": [
        "README.md",
        "LICENSE",
    ]
}

# 目标文件
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # 使用Windows GUI

setup(
    name="文件整理助手",
    version="1.0",
    description="一个现代化的文件整理工具",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "gui.py",
            base=base,
            target_name="文件整理助手.exe",
            icon="file_organizer.ico"  # 如果有图标的话
        )
    ]
) 