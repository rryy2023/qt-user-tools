# 立即修复 GitHub 连接

## 🎯 问题

- 当前镜像：`gitclone.com` 返回 502 错误
- Git 命令修改失败（权限问题）

## ✅ 解决方案：直接编辑配置文件

### 步骤 1：打开配置文件

在终端执行：

```bash
cd /Users/xuwei/Downloads/happy/qt-user-tools
nano .git/config
```

### 步骤 2：修改远程地址

找到这一行（大约第 8 行）：
```
url = https://gitclone.com/github.com/rryy2023/qt-user-tools.git
```

**改为**：
```
url = https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git
```

### 步骤 3：保存并退出

- 按 `Ctrl+X`
- 按 `Y` 确认保存
- 按 `Enter` 退出

### 步骤 4：验证

```bash
# 查看远程地址
git remote -v

# 应该显示：
# origin  https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git (fetch)
# origin  https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git (push)

# 测试连接
git fetch --dry-run
```

## 🔄 如果 ghproxy 也失败

尝试其他镜像：

```bash
# 编辑配置文件
nano .git/config

# 改为镜像 1
url = https://mirror.ghproxy.com/https://github.com/rryy2023/qt-user-tools.git

# 或镜像 2
url = https://github.com/rryy2023/qt-user-tools.git
```

## 📋 完整配置文件示例

修改后的 `.git/config` 应该是：

```ini
[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
	logallrefupdates = true
	ignorecase = true
	precomposeunicode = true
[remote "origin"]
	url = https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git
	fetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
	gk-last-accessed = 2026-01-28T06:27:00.907Z
	gk-last-modified = 2026-01-28T06:27:00.907Z
	remote = origin
	merge = refs/heads/main
```

## ⚡ 一键命令（如果权限允许）

```bash
cd /Users/xuwei/Downloads/happy/qt-user-tools
sed -i '' 's|https://gitclone.com/github.com/rryy2023/qt-user-tools.git|https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git|g' .git/config
git remote -v
```

## 🎉 修复后

修复成功后，可以正常使用：

```bash
git push
git pull
git fetch
```

GitHub Actions 也会正常工作！
