# CLI 使用指南

## 🚀 快速开始

### 场景 1：只有订阅 URL（无需账户）★ 推荐

这是最简单的使用方式，不需要任何账户，只需要订阅链接：

```bash
# 最简单的用法
uv run cli.py --url https://example.com/subscription -o config.yaml

# 过滤特定节点
uv run cli.py --url https://example.com/sub --include "香港|HK" -o hk.yaml

# 使用外部规则
uv run cli.py --url https://example.com/sub \
  --config https://example.com/rules.ini -o config.yaml
```

### 场景 2：有 Dler Cloud 账户

如果你有 Dler Cloud 账户，可以自动获取订阅：

```bash
# 使用邮箱密码登录并转换
uv run cli.py --email your@email.com --password yourpass -o config.yaml

# 使用 Token
uv run cli.py --token YOUR_API_TOKEN -o config.yaml
```

### 使用 HTTP 服务（旧方法）

```bash
# 需要先启动 subconverter 服务
uv run cli.py --email your@email.com --password yourpass \
  -o config.yaml --method http
```

---

## 📚 详细参数说明

### 认证参数（可选，仅使用 Dler Cloud API 时需要）

| 参数 | 说明 | 示例 |
|------|------|------|
| `--email` | Dler Cloud 邮箱 | `--email user@example.com` |
| `--password` | Dler Cloud 密码 | `--password yourpassword` |
| `--token` | API Token（优先使用） | `--token xxx` |

**⚠️ 重要**：
- 如果提供了 `--url` 参数，则**不需要**认证参数
- 认证参数只在使用 Dler Cloud API 自动获取订阅时才需要
- 也可以在 `.env` 文件中配置：

```bash
DLER_EMAIL=your@email.com
DLER_PASSWORD=yourpassword
DLER_API_TOKEN=xxx
```

### 订阅参数

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `--url` | 订阅 URL（不使用 Dler API） | - | `--url https://...` |
| `--sub-type` | 订阅类型（Dler API） | `ss2022` | `--sub-type vmess` |

支持的订阅类型：
- `ss2022` - Shadowsocks 2022
- `vmess` - VMess
- `trojan` - Trojan

### 转换方法

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--method` | 转换方法 | `local` |

可选值：
- `local` - **本地转换（推荐）**：纯 Python 实现，无需服务器
- `http` - HTTP 服务转换：需要 subconverter 服务

### HTTP 服务参数（仅 `--method http` 时使用）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--host` | subconverter 服务地址 | `http://127.0.0.1:25500/sub` |
| `--target` | 目标格式 | `clash` |

### 配置参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--config` | 外部配置/规则文件 URL | `--config https://...` |
| `--exclude` | 排除的节点（正则） | `--exclude "过期\|expire"` |
| `--include` | 包含的节点（正则） | `--include "香港\|HK\|台湾\|TW"` |

### 功能开关

| 参数 | 说明 | 默认 |
|------|------|------|
| `--no-insert` | 不插入节点 | 插入 |
| `--no-new-name` | 不使用新节点名称 | 使用新名称 |
| `--no-udp` | 禁用 UDP | 启用 |
| `--no-emoji` | 移除 emoji | 保留 |
| `--scv` | 跳过证书验证 | 启用 |
| `--tfo` | 启用 TCP Fast Open | 禁用 |
| `--sort` | 排序节点 | 不排序 |
| `--append-type` | 添加类型后缀 | 不添加 |

### 其他参数

| 参数 | 说明 |
|------|------|
| `-o, --output` | 输出文件路径（默认：config.yaml） |
| `-v, --verbose` | 详细输出 |
| `-h, --help` | 显示帮助信息 |

---

## 💡 使用示例

### 示例 1：基本使用（本地转换）

```bash
uv run cli.py --email user@example.com --password pass123 -o config.yaml
```

**输出**：
```
✓ 登录成功
✓ 获取到订阅地址
使用本地转换 (新方法)
✓ 订阅大小: 18428 字节
✓ 发现 44 个节点
✓ 配置已保存: config.yaml
✓ 转换完成!
```

### 示例 2：使用 HTTP 服务（旧方法）

```bash
uv run cli.py --email user@example.com --password pass123 \
  -o config.yaml --method http
```

**前提**：需要先启动 subconverter 服务
```bash
# 假设 subconverter 运行在 http://127.0.0.1:25500
```

### 示例 3：从 URL 直接转换

```bash
uv run cli.py --url https://example.com/subscription -o config.yaml
```

### 示例 4：使用自定义规则

```bash
uv run cli.py --email user@example.com --password pass123 \
  -o config.yaml \
  --config https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online.ini
```

### 示例 5：过滤香港和台湾节点

```bash
uv run cli.py --email user@example.com --password pass123 \
  -o config.yaml \
  --include "香港|HK|台湾|TW"
```

**输出**：
```
✓ 发现 44 个节点
  包含规则匹配: 6/44 个节点
过滤后: 6/44 个节点
```

### 示例 6：排除过期节点并排序

```bash
uv run cli.py --url https://example.com/subscription \
  -o config.yaml \
  --exclude "过期|expire|剩余" \
  --sort
```

### 示例 7：移除 emoji 并添加类型后缀

```bash
uv run cli.py --email user@example.com --password pass123 \
  -o config.yaml \
  --no-emoji \
  --append-type
```

**节点名称变化**：
- 原始：`🇭🇰 香港 IEPL [01]`
- 转换后：`香港 IEPL [01] [SS]`

### 示例 8：使用自定义 HTTP 服务

```bash
uv run cli.py --url https://example.com/subscription \
  -o config.yaml \
  --method http \
  --host http://localhost:8080/sub \
  --target surge
```

### 示例 9：完整参数示例

```bash
uv run cli.py \
  --email user@example.com \
  --password pass123 \
  -o clash_config.yaml \
  --method local \
  --config https://example.com/rules.ini \
  --include "香港|HK|新加坡|SG" \
  --exclude "过期" \
  --sort \
  --tfo \
  --verbose
```

### 示例 10：使用环境变量

```bash
# 在 .env 文件中配置
echo "DLER_EMAIL=user@example.com" > .env
echo "DLER_PASSWORD=pass123" >> .env

# 直接运行（自动读取 .env）
uv run cli.py -o config.yaml
```

---

## 🆚 两种方法对比

### 本地转换（`--method local`，推荐）

**优点**：
- ✅ 无需额外服务
- ✅ 跨平台兼容
- ✅ 安装简单
- ✅ 资源占用低

**缺点**：
- ⚠️ 规则相对简单（可通过 --config 自定义）

**适用场景**：
- 个人使用
- 自动化脚本
- 无服务器环境
- 快速转换

### HTTP 服务（`--method http`）

**优点**：
- ✅ 功能完整
- ✅ 规则丰富
- ✅ 与 subconverter 完全兼容

**缺点**：
- ❌ 需要运行服务
- ❌ 依赖外部进程
- ❌ 部署复杂

**适用场景**：
- 已有 subconverter 服务
- 需要复杂规则
- 多人共享使用

---

## 🔧 高级用法

### 1. 批量转换多个订阅

```bash
#!/bin/bash
# batch_convert.sh

URLS=(
  "https://example1.com/sub"
  "https://example2.com/sub"
  "https://example3.com/sub"
)

for i in "${!URLS[@]}"; do
  uv run cli.py --url "${URLS[$i]}" -o "config_$i.yaml"
done
```

### 2. 定时更新订阅（cron）

```bash
# crontab -e
# 每天凌晨 3 点更新
0 3 * * * cd /path/to/convertor && uv run cli.py --email user@example.com --password pass123 -o config.yaml
```

### 3. 结合 Git 管理配置

```bash
#!/bin/bash
# update_and_commit.sh

uv run cli.py --email $EMAIL --password $PASS -o config.yaml

if git diff --quiet config.yaml; then
  echo "No changes"
else
  git add config.yaml
  git commit -m "Update subscription: $(date)"
  git push
fi
```

### 4. 按地区分组导出

```bash
# 导出香港节点
uv run cli.py --url $URL --include "香港|HK" -o hk.yaml

# 导出美国节点
uv run cli.py --url $URL --include "美国|US" -o us.yaml

# 导出日本节点
uv run cli.py --url $URL --include "日本|JP" -o jp.yaml
```

---

## 📝 正则表达式示例

### 包含规则（`--include`）

```bash
# 香港或台湾
--include "香港|HK|台湾|TW"

# 所有 IEPL 线路
--include "IEPL"

# 编号 01-05
--include "\[0[1-5]\]"

# 以特定前缀开头
--include "^🇭🇰"
```

### 排除规则（`--exclude`）

```bash
# 排除过期节点
--exclude "过期|expire|剩余"

# 排除高倍率节点
--exclude "x[2-9]|倍"

# 排除特定地区
--exclude "印度|土耳其"

# 排除包含特定字符
--exclude "测试|test"
```

### 组合使用

```bash
# 只要香港的 Air 线路，排除过期的
uv run cli.py --url $URL \
  --include "香港.*Air" \
  --exclude "过期" \
  -o hk_air.yaml
```

---

## 🐛 故障排除

### 问题 1：登录失败

```bash
✗ 获取订阅失败: Login failed
```

**解决**：
1. 检查邮箱密码是否正确
2. 检查网络连接
3. 使用 `-v` 查看详细错误

### 问题 2：HTTP 服务无法连接

```bash
✗ 下载失败: Connection refused
```

**解决**：
1. 确认 subconverter 服务是否运行
2. 检查端口是否正确（默认 25500）
3. 使用 `--host` 指定正确的地址

### 问题 3：未找到有效节点

```bash
✗ 未找到有效的代理节点
```

**解决**：
1. 检查订阅 URL 是否有效
2. 使用 `-v` 查看解析详情
3. 尝试使用 `--method http`

### 问题 4：过滤后无节点

```bash
过滤后: 0/44 个节点
```

**解决**：
1. 检查正则表达式是否正确
2. 使用 `-v` 查看过滤过程
3. 放宽过滤条件

---

## 💻 环境变量

支持从环境变量或 `.env` 文件读取配置：

```bash
# .env 文件示例
DLER_EMAIL=user@example.com
DLER_PASSWORD=yourpassword
DLER_API_TOKEN=xxx
```

优先级：
1. 命令行参数（最高）
2. 环境变量
3. .env 文件
4. 默认值（最低）

---

## 🎯 最佳实践

1. **推荐使用本地转换**
   ```bash
   uv run cli.py --email $EMAIL --password $PASS -o config.yaml
   ```

2. **敏感信息使用环境变量**
   ```bash
   # 不要在命令行直接输入密码
   # 使用 .env 文件
   ```

3. **使用过滤优化节点**
   ```bash
   # 只保留需要的节点
   --include "香港|新加坡|日本"
   ```

4. **定期更新配置**
   ```bash
   # 使用 cron 定时任务
   ```

5. **备份重要配置**
   ```bash
   # 使用 Git 管理
   git add config.yaml
   git commit -m "Update config"
   ```

---

## 📖 参考链接

- [项目 README](README.md)
- [详细使用指南](USAGE.md)
- [对比报告](COMPARISON_REPORT.md)
- [subconverter 文档](https://github.com/tindy2013/subconverter)
