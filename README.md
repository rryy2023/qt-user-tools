# 千图网客服问题解决工具集

根据客服教程文档开发的自动化脚本工具集，用于解决千图网使用过程中的常见问题。

## 功能特性

- ✅ **Hosts绑定/解绑**: 支持8种常见问题的hosts绑定场景
- ✅ **自动IP获取**: 从17ce.com获取域名最优IP地址
- ✅ **浏览器工具**: 清除缓存、检查版本、清除DNS缓存
- ✅ **下载问题诊断**: 检查第三方下载工具和浏览器设置
- ✅ **跨平台支持**: 支持Windows和Mac系统
- ✅ **交互式界面**: 友好的命令行交互菜单
- ✅ **安全备份**: 自动备份hosts文件，支持回滚

## 项目结构

```
tools/
├── diagnose.py              # 主诊断工具（交互式）
├── hosts/
│   ├── bind_hosts.py        # hosts绑定工具
│   ├── unbind_hosts.py      # hosts解绑工具
│   ├── check_hosts.py       # hosts检查工具
│   └── get_domain_ip.py     # 获取域名IP工具
├── browser/
│   ├── clear_cache.py       # 清除浏览器缓存
│   ├── clear_dns.py         # 清除DNS缓存
│   └── check_browser.py     # 检查浏览器版本
├── download/
│   └── check_download.py   # 检查下载问题
├── scripts/
│   ├── bind_hosts_windows.bat  # Windows hosts绑定脚本
│   └── bind_hosts_mac.sh       # Mac hosts绑定脚本
├── config/
│   └── domain_mappings.json    # 域名-IP映射配置
├── requirements.txt            # Python依赖
└── README.md                   # 使用说明
```

## 安装

### 1. 安装Python依赖

```bash
pip install -r requirements.txt
```

### 2. 设置执行权限（Mac/Linux）

```bash
chmod +x scripts/bind_hosts_mac.sh
chmod +x hosts/*.py
chmod +x browser/*.py
chmod +x download/*.py
chmod +x diagnose.py
```

## 使用方法

### 方式一：使用主诊断工具（推荐）

运行交互式诊断工具，根据菜单选择问题类型：

```bash
python diagnose.py
```

主菜单包含以下选项：

1. **主站卡片预览图无法显示、加载慢** - 绑定 preview.qiantucdn.com
2. **下载页面样式乱了** - 绑定 js.qiantucdn.com
3. **主站样式丢了** - 绑定 icon.qiantucdn.com
4. **下载页面显示无法访问网站** - 绑定 dl.58pic.com
5. **云设计首页显示无法访问** - 绑定 y.58pic.com
6. **千图首页面卡片无法加载但上面有标签文字** - 解绑 preview.qiantucdn.com
7. **下载失败-网络错误、下载中断** - 绑定下载代理域名
8. **检查hosts文件配置** - 查看当前绑定状态
9. **清除浏览器缓存** - 清除Chrome/Safari/Edge缓存
10. **清除DNS缓存** - 清除系统DNS缓存
11. **检查浏览器版本** - 检查浏览器兼容性
12. **诊断下载问题** - 检查下载工具和设置

### 方式二：使用独立工具

#### Hosts绑定

```bash
# 根据问题类型绑定
python hosts/bind_hosts.py --problem preview --auto-fix

# 绑定指定域名
python hosts/bind_hosts.py --domain preview.qiantucdn.com --auto-fix

# 预览模式（不实际修改）
python hosts/bind_hosts.py --problem preview
```

支持的问题类型：
- `preview` - 预览图问题
- `js` - 下载页面样式问题
- `icon` - 主站样式问题
- `download` - 下载页面无法访问
- `cloud` - 云设计首页无法访问
- `download_fail` - 下载失败

#### Hosts解绑

```bash
# 解绑指定域名
python hosts/unbind_hosts.py --domain preview.qiantucdn.com --auto-fix

# 解绑所有千图相关域名
python hosts/unbind_hosts.py --auto-fix
```

#### 检查Hosts配置

```bash
# 检查所有千图相关域名绑定
python hosts/check_hosts.py

# 检查指定域名
python hosts/check_hosts.py --domain preview.qiantucdn.com
```

#### 获取域名IP

```bash
# 获取域名IP（优先使用配置文件）
python hosts/get_domain_ip.py preview.qiantucdn.com

# 不使用配置文件，从17ce.com获取
python hosts/get_domain_ip.py preview.qiantucdn.com --no-config
```

#### 清除浏览器缓存

```bash
# 清除所有浏览器缓存
python browser/clear_cache.py --auto-fix

# 清除指定浏览器缓存
python browser/clear_cache.py --browser Chrome --auto-fix
```

**注意**: 清除缓存前请先关闭浏览器！

#### 清除DNS缓存

```bash
python browser/clear_dns.py
```

#### 检查浏览器版本

```bash
# 检查所有浏览器
python browser/check_browser.py

# 检查指定浏览器
python browser/check_browser.py --browser Chrome
```

#### 诊断下载问题

```bash
# 诊断下载问题（不指定URL）
python download/check_download.py

# 诊断指定URL的下载问题
python download/check_download.py --url "https://proxy-rar.58pic.com/..."
```

### 方式三：使用批处理脚本

#### Windows系统

1. 右键点击 `tools/scripts/bind_hosts_windows.bat`
2. 选择"以管理员身份运行"
3. 按照提示输入域名和IP地址

#### Mac系统

```bash
sudo scripts/bind_hosts_mac.sh
```

## 配置文件

### domain_mappings.json

存储域名和默认IP映射，位于 `tools/config/domain_mappings.json`：

```json
{
  "preview.qiantucdn.com": "",
  "js.qiantucdn.com": "",
  "icon.qiantucdn.com": "",
  "dl.58pic.com": "47.104.5.133",
  "y.58pic.com": "118.190.104.146",
  "proxy-rar.58pic.com": "",
  "proxy-vip.58pic.com": "",
  "proxy-vd.58pic.com": ""
}
```

空字符串表示需要从17ce.com实时获取IP。

## 常见问题

### 1. 权限不足

**Windows**: 右键点击脚本，选择"以管理员身份运行"

**Mac/Linux**: 使用 `sudo` 运行脚本

```bash
sudo python diagnose.py
```

### 2. IP地址变化

IP地址可能会定期变化，工具会：
- 优先使用配置文件中的IP
- 如果配置文件中没有，从17ce.com获取最优IP
- 如果17ce.com获取失败，使用DNS查询

### 3. 修改hosts后不生效

1. 清除DNS缓存：`python browser/clear_dns.py`
2. 刷新浏览器或重启浏览器
3. 如果仍然不生效，尝试重启电脑

### 4. 备份文件位置

- **Windows**: `C:\Windows\System32\drivers\etc\hosts.backup.*`
- **Mac/Linux**: `/etc/hosts.backup.*`

## 安全说明

1. **自动备份**: 修改hosts文件前会自动备份原文件
2. **权限检查**: 工具会检查是否有足够权限修改hosts文件
3. **预览模式**: 默认使用预览模式，需要明确指定 `--auto-fix` 才会实际修改

## 注意事项

1. ⚠️ 修改hosts文件需要管理员/root权限
2. ⚠️ 清除浏览器缓存前请先关闭浏览器
3. ⚠️ IP地址可能会变化，建议定期更新配置文件
4. ⚠️ 修改hosts后需要刷新浏览器或清除DNS缓存才能生效

## 技术支持

如遇到问题，请：
1. 检查是否有足够的系统权限
2. 查看错误提示信息
3. 检查hosts文件备份是否正常
4. 联系技术支持

## 更新日志

### v1.0.0 (2026-01-22)
- 初始版本发布
- 支持8种hosts绑定场景
- 支持Windows和Mac系统
- 交互式诊断工具
- 浏览器工具集
- 下载问题诊断

## 许可证

本工具集仅供内部使用。
# qt-user-tools
# qt-user-tools
