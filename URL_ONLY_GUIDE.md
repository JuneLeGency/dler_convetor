# 无需账户使用指南

## ✨ 好消息

**你不需要任何账户就能使用这个工具！**

只要你有一个订阅链接（URL），就可以立即开始使用。

## 🚀 最简单的使用方式

```bash
# 1. 基本转换
uv run cli.py --url https://你的订阅地址 -o config.yaml

# 2. 过滤节点
uv run cli.py --url https://你的订阅地址 --include "香港|HK" -o hk.yaml

# 3. 使用自定义规则
uv run cli.py --url https://你的订阅地址 \
  --config https://example.com/rules.ini \
  -o config.yaml
```

## 📝 常见问题

### Q: 我需要注册 Dler Cloud 账户吗？
**A: 不需要！** 只要你有订阅链接，就可以直接使用 `--url` 参数。

### Q: 什么是订阅链接？
**A:** 订阅链接是你的代理服务商提供的 URL，通常以 `https://` 开头，包含你的节点信息。

### Q: 支持哪些订阅格式？
**A:** 支持以下格式：
- Shadowsocks (ss://)
- ShadowsocksR (ssr://)
- VMess (vmess://)
- Trojan (trojan://)
- Hysteria2 (hy2://)
- Clash YAML

### Q: 我可以过滤节点吗？
**A:** 可以！使用 `--include` 或 `--exclude` 参数：

```bash
# 只要香港节点
uv run cli.py --url 订阅地址 --include "香港|HK" -o hk.yaml

# 排除过期节点
uv run cli.py --url 订阅地址 --exclude "过期|expire" -o config.yaml
```

### Q: 认证参数是什么时候需要的？
**A:** 认证参数（`--email`, `--password`, `--token`）**只在**你想使用 Dler Cloud API 自动获取订阅时才需要。

如果你提供了 `--url` 参数，就**完全不需要**认证。

## 🎯 使用场景对比

### 场景 1: 只有订阅 URL ★ 推荐
```bash
uv run cli.py --url https://example.com/sub -o config.yaml
```
- ✅ 无需账户
- ✅ 最简单
- ✅ 适合所有人

### 场景 2: 有 Dler Cloud 账户
```bash
uv run cli.py --email user@email.com --password pass -o config.yaml
```
- ✅ 自动获取订阅
- ✅ 无需手动复制链接
- ⚠️ 需要 Dler Cloud 账户

## 💡 更多示例

### 本地转换（默认）
```bash
uv run cli.py --url https://example.com/sub -o config.yaml
```

### 使用 HTTP 服务
```bash
uv run cli.py --url https://example.com/sub --method http -o config.yaml
```

### 完整功能示例
```bash
uv run cli.py \
  --url https://example.com/sub \
  --include "香港|新加坡" \
  --exclude "过期" \
  --sort \
  --no-emoji \
  -o config.yaml \
  -v
```

## 🔍 命令参数说明

### 必需参数
- `--url URL` - 你的订阅链接

### 可选参数
- `-o, --output FILE` - 输出文件（默认: config.yaml）
- `--include PATTERN` - 包含匹配的节点（正则表达式）
- `--exclude PATTERN` - 排除匹配的节点（正则表达式）
- `--sort` - 按名称排序节点
- `--no-emoji` - 移除节点名称中的 emoji
- `--append-type` - 在节点名称后添加类型（如 [SS]）
- `--config URL` - 外部规则文件 URL
- `--method {local,http}` - 转换方法（默认: local）
- `-v, --verbose` - 显示详细输出

## 📖 更多帮助

```bash
# 查看完整帮助
uv run cli.py --help

# 查看详细文档
cat CLI_USAGE.md       # 完整使用指南
cat CLI_QUICKREF.md    # 快速参考
cat README.md          # 项目说明
```

## 🎓 实际例子

### 例子 1: 转换订阅并只保留香港节点
```bash
uv run cli.py \
  --url https://example.com/subscription \
  --include "香港|HK" \
  -o hk_only.yaml \
  -v
```

### 例子 2: 排除过期节点，按名称排序
```bash
uv run cli.py \
  --url https://example.com/subscription \
  --exclude "过期|expire|剩余" \
  --sort \
  -o sorted.yaml
```

### 例子 3: 使用 ACL4SSR 规则
```bash
uv run cli.py \
  --url https://example.com/subscription \
  --config https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online.ini \
  -o clash_acl4ssr.yaml
```

### 例子 4: 批量处理不同地区
```bash
# 香港节点
uv run cli.py --url $URL --include "香港|HK" -o hk.yaml

# 新加坡节点
uv run cli.py --url $URL --include "新加坡|SG" -o sg.yaml

# 日本节点
uv run cli.py --url $URL --include "日本|JP" -o jp.yaml
```

## ⚠️ 常见错误

### 错误 1: 未找到有效节点
```
✗ 未找到有效的代理节点
```
**解决方法**:
- 检查订阅 URL 是否正确
- 使用 `-v` 参数查看详细信息
- 确认订阅内容格式正确

### 错误 2: 连接超时
```
✗ 获取订阅失败: timeout
```
**解决方法**:
- 检查网络连接
- 确认订阅服务器是否可访问
- 尝试使用代理

### 错误 3: 过滤后无节点
```
过滤后: 0/44 个节点
```
**解决方法**:
- 检查正则表达式是否正确
- 使用 `-v` 查看所有节点名称
- 放宽过滤条件

## 💪 进阶技巧

### 1. 使用 Shell 脚本自动化
```bash
#!/bin/bash
URL="https://example.com/subscription"
DATE=$(date +%Y%m%d)

uv run cli.py --url $URL -o "config_${DATE}.yaml"
echo "订阅已更新: config_${DATE}.yaml"
```

### 2. 定时自动更新（cron）
```bash
# 添加到 crontab
0 3 * * * cd /path/to/convertor && uv run cli.py --url $URL -o config.yaml
```

### 3. 结合 Git 版本控制
```bash
#!/bin/bash
uv run cli.py --url $URL -o config.yaml

if git diff --quiet config.yaml; then
  echo "无更新"
else
  git add config.yaml
  git commit -m "Update subscription: $(date)"
  git push
fi
```

---

**记住：有订阅 URL 就能用，无需任何账户！**

如有问题，请查看 [完整文档](CLI_USAGE.md) 或运行 `uv run cli.py --help`
