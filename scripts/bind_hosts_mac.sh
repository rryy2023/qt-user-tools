#!/bin/bash
# 千图网 Hosts 绑定工具 (Mac)

echo "============================================================"
echo "千图网 Hosts 绑定工具 (Mac)"
echo "============================================================"
echo ""

# 检查是否有sudo权限
if [ "$(id -u)" -ne 0 ]; then 
    echo "错误: 需要管理员权限！"
    echo "请使用 sudo 运行此脚本: sudo $0"
    exit 1
fi

# 设置hosts文件路径
HOSTS_FILE="/etc/hosts"

# 备份hosts文件
echo "正在备份hosts文件..."
BACKUP_FILE="${HOSTS_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
cp "$HOSTS_FILE" "$BACKUP_FILE" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "备份成功: $BACKUP_FILE"
else
    echo "警告: 备份失败，但将继续执行"
fi
echo ""

# 提示用户输入IP地址
echo "请根据问题类型输入需要绑定的域名和IP地址"
echo ""
echo "常见绑定:"
echo "  1. preview.qiantucdn.com - 主站卡片预览图问题"
echo "  2. js.qiantucdn.com - 下载页面样式问题"
echo "  3. icon.qiantucdn.com - 主站样式问题"
echo "  4. dl.58pic.com - 下载页面无法访问 (IP: 47.104.5.133)"
echo "  5. y.58pic.com - 云设计首页无法访问 (IP: 118.190.104.146)"
echo "  6. proxy-rar.58pic.com, proxy-vip.58pic.com, proxy-vd.58pic.com - 下载失败"
echo ""
echo "注意: IP地址可能会变化，请使用最新IP(访问 https://17ce.com/ 选择ping输入域名查看最新IP)"
echo "常见问题处理方法文档: https://www.yuque.com/toujours-2nfpc/hdny3c/wnp4kg?#JM0n6"
echo ""

read -p "请输入域名 (例如: preview.qiantucdn.com): " DOMAIN
if [ -z "$DOMAIN" ]; then
    echo "错误: 域名不能为空"
    exit 1
fi

read -p "请输入IP地址: " IP
if [ -z "$IP" ]; then
    echo "错误: IP地址不能为空"
    exit 1
fi

# 验证IP格式（简单验证）
if ! [[ $IP =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
    echo "警告: IP地址格式可能不正确，但将继续执行"
fi

# 检查是否已存在该域名的绑定
if grep -q "$DOMAIN" "$HOSTS_FILE"; then
    echo ""
    echo "发现已存在的绑定，将更新为新的IP地址"
    echo "正在移除旧的绑定..."
    
    # 创建临时文件
    TEMP_FILE=$(mktemp)
    
    # 移除旧绑定
    grep -v "$DOMAIN" "$HOSTS_FILE" > "$TEMP_FILE"
    
    # 添加新绑定
    echo "$IP    $DOMAIN" >> "$TEMP_FILE"
    
    # 替换原文件
    mv "$TEMP_FILE" "$HOSTS_FILE"
    
    echo "已更新绑定: $IP    $DOMAIN"
else
    # 添加新绑定
    echo "$IP    $DOMAIN" >> "$HOSTS_FILE"
    echo "已添加绑定: $IP    $DOMAIN"
fi

echo ""
echo "============================================================"
echo "操作完成！"
echo "============================================================"
echo ""
echo "提示:"
echo "  1. 请刷新浏览器或重启浏览器以使更改生效"
echo "  2. 如果问题仍然存在，可以运行以下命令清除DNS缓存:"
echo "     sudo dscacheutil -flushcache"
echo "     sudo killall -HUP mDNSResponder"
echo "  3. 备份文件保存在: $BACKUP_FILE"
echo ""
