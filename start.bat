@echo off
:start
cls
echo 文件整理助手正在启动...
python gui.py
echo.
echo 程序已退出
echo 按 R 重新启动程序
echo 按任意其他键退出
choice /c RQ /n /m "请选择："
if errorlevel 2 goto end
if errorlevel 1 goto start
:end 