@echo off
REM GUI应用启动脚本 (Windows)

cd /d "%~dp0"

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python
    pause
    exit /b 1
)

REM 检查是否以管理员权限运行
net session >nul 2>&1
if errorlevel 1 (
    echo 提示: 未以管理员权限运行
    echo 某些功能（如修改hosts文件）需要管理员权限
    echo 如需完整功能，请右键点击此文件，选择"以管理员身份运行"
    echo.
)

REM 运行应用
python gui/main.py

pause
