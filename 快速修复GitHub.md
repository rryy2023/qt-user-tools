# 快速修复 GitHub 连接

## ✅ 已自动修复

已为您配置 GitHub 镜像地址，现在可以使用：

```bash
# 查看远程地址
git remote -v

# 测试连接
git fetch

# 推送代码
git push

# 拉取代码
git pull
```

## 🔧 如果仍有问题

### 方案 1：使用修复脚本

```bash
./fix_github_connection.sh
```

### 方案 2：手动切换镜像

```bash
# 使用 ghproxy 镜像
git remote set-url origin https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git

# 或使用其他镜像
git remote set-url origin https://mirror.ghproxy.com/https://github.com/rryy2023/qt-user-tools.git
```

### 方案 3：配置代理（如果有）

```bash
# HTTP 代理
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 查看配置
git config --global --get http.proxy
```

### 方案 4：使用 SSH（长期方案）

```bash
# 1. 生成 SSH 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. 添加公钥到 GitHub
cat ~/.ssh/id_ed25519.pub
# 复制到 GitHub: Settings -> SSH and GPG keys

# 3. 修改远程地址
git remote set-url origin git@github.com:rryy2023/qt-user-tools.git

# 4. 测试
ssh -T git@github.com
```

## 📋 当前配置

- **远程地址**: `https://ghproxy.com/https://github.com/rryy2023/qt-user-tools.git`
- **超时时间**: 300秒
- **缓冲区**: 500MB

## 🔗 详细文档

查看 `GitHub连接问题解决方案.md` 获取完整说明。
