# GitHub 连接问题解决方案

## 🔍 问题描述

```
fatal: unable to access 'https://github.com/rryy2023/qt-user-tools.git/': 
Failed to connect to github.com port 443 after 75028 ms: Couldn't connect to server
```

这是网络连接问题，无法访问 GitHub。

## ✅ 解决方案

### 方案 1：使用 GitHub 镜像（推荐，最简单）

使用 `ghproxy.com` 镜像加速：

```bash
# 查看当前远程地址
git remote -v

# 修改为镜像地址
git remote set-url origin https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git

# 验证
git remote -v

# 测试连接
git fetch
```

### 方案 2：使用 SSH 代替 HTTPS

```bash
# 1. 生成 SSH 密钥（如果还没有）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. 添加 SSH 密钥到 ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 3. 复制公钥到 GitHub
cat ~/.ssh/id_ed25519.pub
# 在 GitHub: Settings -> SSH and GPG keys -> New SSH key

# 4. 修改远程地址为 SSH
git remote set-url origin git@github.com:rryy2023/qt-user-tools.git

# 5. 测试连接
ssh -T git@github.com
```

### 方案 3：配置代理（如果有代理）

```bash
# HTTP/HTTPS 代理
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# SOCKS5 代理
git config --global http.proxy socks5://127.0.0.1:7890
git config --global https.proxy socks5://127.0.0.1:7890

# 查看配置
git config --global --get http.proxy
git config --global --get https.proxy

# 取消代理
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### 方案 4：使用其他 GitHub 镜像

#### 镜像列表

1. **ghproxy.com**（推荐）
   ```bash
   git remote set-url origin https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git
   ```

2. **mirror.ghproxy.com**
   ```bash
   git remote set-url origin https://mirror.ghproxy.com/https://github.com/rryy2023/qt-user-tools.git
   ```

3. **gitclone.com**
   ```bash
   git remote set-url origin https://gitclone.com/github.com/rryy2023/qt-user-tools.git
   ```

### 方案 5：检查网络和 DNS

```bash
# 1. 检查网络连接
ping github.com

# 2. 检查 DNS
nslookup github.com

# 3. 尝试使用其他 DNS（如 8.8.8.8）
# macOS: 系统设置 -> 网络 -> DNS

# 4. 清除 DNS 缓存（macOS）
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

### 方案 6：增加超时时间

```bash
# 增加 Git 超时时间
git config --global http.timeout 300
git config --global http.postBuffer 524288000
```

## 🚀 快速修复脚本

创建并运行以下脚本：

```bash
#!/bin/bash
# 快速修复 GitHub 连接问题

echo "正在修复 GitHub 连接..."

# 方案 1: 使用 ghproxy 镜像
echo "尝试使用 ghproxy 镜像..."
git remote set-url origin https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git

# 测试连接
echo "测试连接..."
if git fetch --dry-run 2>&1 | grep -q "fatal"; then
    echo "镜像连接失败，尝试其他方案..."
    
    # 方案 2: 使用 SSH
    echo "尝试使用 SSH..."
    git remote set-url origin git@github.com:rryy2023/qt-user-tools.git
    
    if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
        echo "✓ SSH 连接成功"
    else
        echo "✗ SSH 连接失败，请检查 SSH 密钥配置"
    fi
else
    echo "✓ 镜像连接成功"
fi
```

## 📋 推荐工作流

### 日常使用（推荐配置）

```bash
# 1. 使用镜像地址（最快）
git remote set-url origin https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git

# 2. 增加超时时间
git config --global http.timeout 300

# 3. 测试
git fetch
```

### 长期使用（推荐 SSH）

```bash
# 1. 配置 SSH 密钥（一次性）
ssh-keygen -t ed25519 -C "your_email@example.com"
# 添加公钥到 GitHub

# 2. 使用 SSH 地址
git remote set-url origin git@github.com:rryy2023/qt-user-tools.git

# 3. 测试
ssh -T git@github.com
```

## 🔧 故障排除

### 问题 1：镜像也连接失败

**解决**：
- 尝试其他镜像
- 检查网络连接
- 使用代理

### 问题 2：SSH 连接失败

**检查**：
```bash
# 测试 SSH 连接
ssh -T git@github.com

# 查看 SSH 配置
cat ~/.ssh/config

# 检查密钥
ls -la ~/.ssh/
```

### 问题 3：代理配置错误

**解决**：
```bash
# 查看当前代理配置
git config --global --get http.proxy

# 取消代理
git config --global --unset http.proxy
git config --global --unset https.proxy
```

## 📝 注意事项

1. **镜像地址**：某些镜像可能不稳定，建议多试几个
2. **SSH 密钥**：需要添加到 GitHub 账户
3. **代理设置**：确保代理服务器正常运行
4. **网络环境**：某些网络环境可能限制 GitHub 访问

## 🎯 最佳实践

1. **开发环境**：使用 SSH（稳定、快速）
2. **临时访问**：使用镜像（简单、快速）
3. **企业网络**：配置代理（安全、合规）

## 🔗 相关资源

- [GitHub SSH 设置指南](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [Git 代理配置](https://git-scm.com/docs/git-config#Documentation/git-config.txt-httpproxy)
- [GitHub 镜像列表](https://github.com/XIU2/TrackersListCollection)
