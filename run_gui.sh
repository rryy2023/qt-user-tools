#!/bin/bash
# GUI应用启动脚本 (Mac/Linux)

cd "$(dirname "$0")"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3"
    exit 1
fi

# 检查是否以root权限运行
if [ "$EUID" -ne 0 ]; then 
    echo "提示: 未以管理员权限运行"
    echo "某些功能（如修改hosts文件）需要管理员权限"
    echo "如需完整功能，请使用: sudo $0"
    echo ""
fi

# 运行应用
python3 gui/main.py
