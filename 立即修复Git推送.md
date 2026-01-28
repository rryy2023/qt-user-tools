# 立即修复 Git Push HTTP 400 错误

## 🎯 问题

推送失败：HTTP 400 错误，数据包 2.79 MiB

## ✅ 解决方案（手动执行）

### 方法 1：直接编辑配置文件（推荐）

```bash
cd /Users/xuwei/Downloads/happy/qt-user-tools
nano .git/config
```

在 `[core]` 部分添加：

```ini
[core]
    # ... 其他配置 ...
    httpPostBuffer = 524288000
```

在文件末尾添加：

```ini
[http]
    postBuffer = 524288000
    maxRequestBuffer = 100M
```

保存退出（`Ctrl+X` → `Y` → `Enter`）

然后重试：
```bash
git push origin main
```

### 方法 2：使用 sed 命令（如果权限允许）

```bash
cd /Users/xuwei/Downloads/happy/qt-user-tools

# 添加 http 配置
if ! grep -q "\[http\]" .git/config; then
    echo "" >> .git/config
    echo "[http]" >> .git/config
    echo "    postBuffer = 524288000" >> .git/config
    echo "    maxRequestBuffer = 100M" >> .git/config
fi

# 验证
cat .git/config | grep -A 3 "\[http\]"

# 重试推送
git push origin main
```

### 方法 3：使用 SSH（最稳定，推荐）

```bash
# 1. 修改为 SSH 地址
git remote set-url origin git@github.com:rryy2023/qt-user-tools.git

# 2. 测试 SSH（如果还没配置）
ssh -T git@github.com

# 3. 推送
git push origin main
```

## 🔧 完整配置文件示例

修改后的 `.git/config` 应该包含：

```ini
[core]
    repositoryformatversion = 0
    filemode = true
    bare = false
    logallrefupdates = true
    ignorecase = true
    precomposeunicode = true
    httpPostBuffer = 524288000

[remote "origin"]
    url = https://github.com/rryy2023/qt-user-tools.git
    fetch = +refs/heads/*:refs/remotes/origin/*

[http]
    postBuffer = 524288000
    maxRequestBuffer = 100M
```

## 🚀 快速命令

```bash
cd /Users/xuwei/Downloads/happy/qt-user-tools

# 方法 A：编辑配置文件
nano .git/config
# 添加 [http] 部分

# 方法 B：使用 SSH（推荐）
git remote set-url origin git@github.com:rryy2023/qt-user-tools.git
git push origin main
```

## 📋 验证

```bash
# 查看配置
cat .git/config | grep -A 3 "\[http\]"

# 查看远程地址
git remote -v

# 测试推送
git push origin main
```

## ⚡ 最快方案

**使用 SSH**（不受 HTTP 限制）：

```bash
git remote set-url origin git@github.com:rryy2023/qt-user-tools.git
git push origin main
```

如果 SSH 还没配置，先配置 SSH 密钥（见 `修复Git推送400错误.md`）。
