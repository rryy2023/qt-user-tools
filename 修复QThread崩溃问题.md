# 修复 QThread 崩溃问题

## 🐛 问题

应用关闭时崩溃：
```
QThread: Destroyed while thread '' is still running
zsh: abort
```

## 🔍 原因

1. **线程生命周期管理不当**：`HostsCheckWorker` 线程在窗口关闭时仍在运行
2. **缺少线程清理**：没有在窗口关闭时等待线程完成
3. **线程引用丢失**：创建线程后没有保存引用，无法清理

## ✅ 修复方案

### 1. 保存线程引用

```python
def __init__(self):
    super().__init__()
    self.hosts_worker = None  # 保存线程引用
    # ...
```

### 2. 实现 closeEvent

```python
def closeEvent(self, event):
    """窗口关闭事件：确保线程正确清理"""
    if self.hosts_worker and self.hosts_worker.isRunning():
        # 请求线程退出
        self.hosts_worker.quit()
        # 等待线程完成（最多等待2秒）
        if not self.hosts_worker.wait(2000):
            # 如果2秒内没有完成，强制终止
            self.hosts_worker.terminate()
            self.hosts_worker.wait(1000)
        # 清理线程对象
        self.hosts_worker.deleteLater()
        self.hosts_worker = None
    
    event.accept()
```

### 3. 线程完成时自动清理

```python
def update_status_async(self):
    # 如果之前的线程还在运行，先清理
    if self.hosts_worker and self.hosts_worker.isRunning():
        self.hosts_worker.quit()
        self.hosts_worker.wait(1000)
    
    self.hosts_worker = HostsCheckWorker()
    self.hosts_worker.result_ready.connect(self.on_hosts_check_result)
    self.hosts_worker.finished.connect(self.on_hosts_worker_finished)  # 自动清理
    self.hosts_worker.start()

def on_hosts_worker_finished(self):
    """线程完成时的清理"""
    if self.hosts_worker:
        self.hosts_worker.deleteLater()
        self.hosts_worker = None
```

### 4. 线程支持停止请求

```python
class HostsCheckWorker(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._stop_requested = False
    
    def stop(self):
        """请求停止线程"""
        self._stop_requested = True
    
    def run(self):
        # 在执行过程中检查停止请求
        if self._stop_requested:
            return
        # ...
```

## 🔧 修复内容

1. ✅ 添加 `self.hosts_worker` 引用保存
2. ✅ 实现 `closeEvent` 方法等待线程完成
3. ✅ 添加 `on_hosts_worker_finished` 自动清理
4. ✅ 线程支持停止请求
5. ✅ 添加 `QCloseEvent` 导入

## 📋 需要重新打包

代码已修复，需要重新打包应用：

### 本地打包

```bash
./build_all_platforms.sh --mac-arm64
```

### GitHub Actions

```bash
git add .
git commit -m "Fix: QThread lifecycle management"
git push origin main
```

## ✅ 验证

修复后，应用应该可以：
- ✅ 正常启动
- ✅ 正常关闭（不再崩溃）
- ✅ 线程正确清理

## 📝 技术细节

### QThread 生命周期最佳实践

1. **保存引用**：始终保存线程对象的引用
2. **等待完成**：在销毁前等待线程完成
3. **使用 quit()**：优雅地请求线程退出
4. **设置超时**：避免无限等待
5. **deleteLater()**：使用 Qt 的延迟删除机制

### 线程清理流程

```
窗口关闭 → closeEvent() → 
  检查线程运行状态 → 
  请求退出 (quit()) → 
  等待完成 (wait()) → 
  清理对象 (deleteLater()) → 
  接受关闭事件
```

## 🎯 总结

通过正确的线程生命周期管理，解决了应用关闭时的崩溃问题。现在应用可以安全地关闭，不会出现 QThread 警告或崩溃。
