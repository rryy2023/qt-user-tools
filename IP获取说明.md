# IP地址获取说明

## 获取逻辑

当修复"主站卡片预览图无法显示、加载慢"等问题时，工具会按以下顺序获取IP地址：

### 1. 优先使用配置文件中的IP

**配置文件**: `config/domain_mappings.json`

如果配置文件中已有该域名的IP地址，直接使用配置文件中的IP。

**示例**:
```json
{
  "preview.qiantucdn.com": "124.166.238.87",  // 如果配置了IP，直接使用
  "dl.58pic.com": "47.104.5.133"              // 已配置的IP
}
```

### 2. 从第三方服务获取IP（优先）

如果配置文件中没有IP（为空字符串），工具会**优先使用第三方IP查询服务**。

**为什么使用第三方服务？**
- ⚠️ **重要**: 用户本地可能无法访问这些域名（preview.qiantucdn.com等）
- 本地ping测试和DNS查询可能失败
- 第三方服务可以从外部网络查询，不受用户本地网络限制

**使用的第三方服务（按优先级）**:

1. **17ce.com** - 中国专业的网站测速服务
   - 提供全国多线路（电信、联通、移动等）的PING测试
   - 可以找到对用户网络最快的CDN节点IP
   - 优先使用此服务获取最优IP

2. **ip-api.com** - 国际IP查询服务
   - 提供域名到IP的查询
   - 免费使用，响应快速
   - 作为17ce.com的备选

3. **ipapi.co** - 另一个IP查询服务
   - 提供域名解析服务
   - 作为最后的第三方备选

**注意**: 
- 所有第三方服务都会过滤IPv6地址，只返回IPv4地址（hosts文件需要IPv4）
- 如果所有第三方服务都失败，才会尝试DNS查询

### 3. DNS查询（最后备用方案）

如果所有第三方服务都失败，工具会尝试DNS查询。

**注意**: 
- ⚠️ 用户本地可能无法访问这些域名，DNS查询很可能失败
- 如果DNS查询也失败，建议手动在配置文件中设置IP地址

**DNS查询**:
- 使用Python的`socket.gethostbyname()`函数
- 返回域名解析的IP地址
- 这是最基础的获取方式，通常都能成功

## 当前配置

查看 `config/domain_mappings.json`:

```json
{
  "preview.qiantucdn.com": "",  // 空字符串 = 需要从17ce.com或DNS获取
  "js.qiantucdn.com": "",
  "icon.qiantucdn.com": "",
  "dl.58pic.com": "47.104.5.133",  // 已配置固定IP
  "y.58pic.com": "118.190.104.146", // 已配置固定IP
  "proxy-rar.58pic.com": "",
  "proxy-vip.58pic.com": "",
  "proxy-vd.58pic.com": ""
}
```

## 在GUI中显示

修复问题时，对话框会显示IP获取的来源：

- **"✓ 已从配置文件获取IP: xxx.xxx.xxx.xxx"** - 使用配置文件中的IP
- **"✓ 已从17ce.com获取最优IP: xxx.xxx.xxx.xxx"** - 从17ce.com获取的最快IP（推荐）
- **"✓ 已从ip-api.com获取IP: xxx.xxx.xxx.xxx"** - 从ip-api.com获取的IP
- **"✓ 已从ipapi.co获取IP: xxx.xxx.xxx.xxx"** - 从ipapi.co获取的IP
- **"✓ 已通过DNS查询获取IP: xxx.xxx.xxx.xxx"** - 通过DNS查询获取的IP（最后备用）

## 为什么使用17ce.com？

1. **最优节点**: 17ce.com可以测试全国多个节点，找到对用户网络最快的IP
2. **CDN加速**: 千图网使用CDN，不同地区访问的IP可能不同，17ce.com能找到最优节点
3. **自动更新**: IP地址可能会变化，从17ce.com获取可以自动获取最新最优IP

## 手动配置IP

如果不想使用17ce.com，可以手动在配置文件中设置IP：

1. 打开 `config/domain_mappings.json`
2. 找到对应域名
3. 填入IP地址
4. 保存文件

**示例**:
```json
{
  "preview.qiantucdn.com": "124.166.238.87"  // 手动设置IP
}
```

设置后，工具会优先使用配置文件中的IP，不再从17ce.com获取。

## 获取最新IP的方法

如果需要手动获取最新IP：

1. **访问17ce.com**: 
   - 打开 http://17ce.com
   - 选择"PING"测试
   - 输入域名（如 preview.qiantucdn.com）
   - 查看测试结果，找到最快的节点IP

2. **使用命令行工具**:
   ```bash
   python hosts/get_domain_ip.py preview.qiantucdn.com
   ```

3. **使用DNS查询**:
   ```bash
   nslookup preview.qiantucdn.com
   # 或
   dig preview.qiantucdn.com
   ```

## 总结

对于 `preview.qiantucdn.com` 等未配置IP的域名，工具会按以下顺序尝试获取：

1. ✅ **配置文件** - 如果配置了IP，直接使用（最高优先级）

2. ✅ **第三方服务**（按顺序尝试）：
   - **17ce.com** - 中国专业测速服务，获取最优IP（推荐）
   - **ip-api.com** - 国际IP查询服务（备选1）
   - **ipapi.co** - IP查询服务（备选2）

3. ⚠️ **DNS查询** - 最后备用方案（用户本地可能无法访问域名，很可能失败）

**重要说明**：
- ⚠️ **用户本地可能无法访问这些域名**，因此：
  - ❌ 不使用ping测试（本地无法访问域名）
  - ❌ 不主要依赖DNS查询（本地可能无法解析）
  - ✅ **优先使用第三方服务**（从外部网络查询，不受本地限制）

**优势**：
- 多层第三方服务备选，提高成功率
- 优先使用17ce.com获取最优IP（CDN加速）
- 所有服务都会过滤IPv6，只返回IPv4地址
- GUI中会显示IP来源，让用户知道IP是从哪里获取的

**如果所有方法都失败**：
- 建议在配置文件中手动设置IP地址
- 或联系技术支持获取最新IP
