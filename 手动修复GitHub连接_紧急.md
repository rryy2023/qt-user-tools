# 手动修复 GitHub 连接（紧急）

## ⚠️ 当前问题

1. Git 配置文件权限问题
2. 当前镜像 `gitclone.com` 返回 502 错误

## 🚀 快速修复（手动执行）

### 方法 1：直接编辑配置文件（推荐）

```bash
# 1. 编辑配置文件
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

保存并退出：
- `nano`: `Ctrl+X` → `Y` → `Enter`
- `vim`: `Esc` → `:wq` → `Enter`

### 方法 2：使用 sudo（如果有权限）

```bash
sudo git remote set-url origin https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git
```

### 方法 3：修复文件权限后修改

```bash
# 检查权限
ls -la .git/config

# 如果需要，修复权限
chmod 644 .git/config

# 然后修改远程地址
git remote set-url origin https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git
```

## 🔧 验证修复

```bash
# 1. 查看远程地址
git remote -v

# 应该显示：
# origin  https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git (fetch)
# origin  https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git (push)

# 2. 测试连接
git fetch --dry-run

# 3. 如果成功，可以正常使用
git push
git pull
```

## 🔄 如果 ghproxy 也失败

尝试其他镜像：

```bash
# 镜像 1
git remote set-url origin https://mirror.ghproxy.com/https://github.com/rryy2023/qt-user-tools.git

# 镜像 2（如果上面都失败）
git remote set-url origin https://github.com/rryy2023/qt-user-tools.git
```

## 📝 完整命令列表

```bash
cd /Users/xuwei/Downloads/happy/qt-user-tools

# 方法 1：直接编辑（推荐）
nano .git/config
# 修改 url 为: https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git

# 方法 2：修复权限后修改
chmod 644 .git/config
git remote set-url origin https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git

# 验证
git remote -v
git fetch --dry-run
```

## ⚡ 最快方案

**直接编辑配置文件**：

```bash
cd /Users/xuwei/Downloads/happy/qt-user-tools
nano .git/config
```

找到这一行：
```
url = https://gitclone.com/github.com/rryy2023/qt-user-tools.git
```

改为：
```
url = https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git
```

保存退出即可。
