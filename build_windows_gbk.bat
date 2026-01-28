@echo off
chcp 936 >nul
echo ========================================
echo Windows EXE 打包脚本
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ 未找到Python，请先安装Python
    pause
    exit /b 1
)

echo ✓ 检测到Python
python --version

REM 检查PyInstaller
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ✗ 未安装PyInstaller
    echo 正在安装PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ✗ PyInstaller安装失败
        pause
        exit /b 1
    )
)

echo ✓ PyInstaller已安装

REM 检查依赖
echo.
echo 检查依赖...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo ⚠ 缺少依赖，正在安装...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ✗ 依赖安装失败
        pause
        exit /b 1
    )
)

echo ✓ 依赖检查完成

REM 运行打包脚本
echo.
echo 开始打包...
python build_windows.py

if errorlevel 1 (
    echo.
    echo ✗ 打包失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo.
echo 输出文件命名规范:
echo   EXE: QiantuTroubleshooter_v0.0.1_Windows-x64.exe
echo   ZIP: QiantuTroubleshooter_v0.0.1_Windows-x64.zip
echo.
pause
