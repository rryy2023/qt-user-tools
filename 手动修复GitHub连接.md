# 手动修复 GitHub 连接

## ⚠️ 权限问题

检测到 Git 配置文件权限问题，请手动执行以下命令：

## 🚀 快速修复（推荐）

### 步骤 1：修改远程地址为镜像

在终端中执行：

```bash
cd /Users/xuwei/Downloads/happy/qt-user-tools

# 修改为镜像地址
git remote set-url origin https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git

# 验证
git remote -v
```

### 步骤 2：测试连接

```bash
# 测试连接（只测试，不下载）
git fetch --dry-run

# 如果成功，可以正常使用
git push
git pull
```

## 🔧 如果仍有权限问题

### 方法 1：检查文件权限

```bash
# 检查权限
ls -la .git/config

# 如果需要，修复权限
chmod 644 .git/config
```

### 方法 2：直接编辑配置文件

```bash
# 编辑配置文件
nano .git/config
# 或
vim .git/config
```

找到 `[remote "origin"]` 部分，修改为：

```ini
[remote "origin"]
    url = https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git
    fetch = +refs/heads/*:refs/remotes/origin/*
```

保存并退出。

### 方法 3：使用其他镜像

如果 `ghproxy.com` 不可用，尝试：

```bash
# 镜像 1
git remote set-url origin https://mirror.ghproxy.com/https://github.com/rryy2023/qt-user-tools.git

# 镜像 2
git remote set-url origin https://gitclone.com/github.com/rryy2023/qt-user-tools.git
```

## 📋 完整命令列表

```bash
# 1. 进入项目目录
cd /Users/xuwei/Downloads/happy/qt-user-tools

# 2. 查看当前配置
git remote -v

# 3. 修改为镜像地址
git remote set-url origin https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git

# 4. 验证配置
git remote -v

# 5. 测试连接
git fetch --dry-run

# 6. 如果成功，可以正常使用
git push origin main
git pull origin main
```

## 🔍 故障排除

### 问题 1：仍然无法连接

**尝试**：
1. 检查网络：`ping ghproxy.com`
2. 尝试其他镜像
3. 配置代理（如果有）

### 问题 2：权限被拒绝

**解决**：
```bash
# 检查文件所有者
ls -la .git/config

# 如果需要，修改所有者
sudo chown $USER .git/config
```

### 问题 3：镜像也失败

**使用 SSH**：
```bash
# 修改为 SSH 地址
git remote set-url origin git@github.com:rryy2023/qt-user-tools.git

# 需要先配置 SSH 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"
# 然后添加公钥到 GitHub
```

## 📝 注意事项

1. **镜像地址**：某些镜像可能不稳定，多试几个
2. **网络环境**：确保网络连接正常
3. **DNS 解析**：如果 DNS 有问题，尝试更换 DNS 服务器

## 🎯 推荐配置

**日常使用**（最简单）：
```bash
git remote set-url origin https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git
```

**长期使用**（最稳定）：
```bash
# 配置 SSH 密钥后
git remote set-url origin git@github.com:rryy2023/qt-user-tools.git
```
