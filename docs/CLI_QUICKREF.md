# CLI 快速参考

## 🚀 最常用命令

### 只有订阅 URL（无需账户）★ 推荐

```bash
# 1. 最简单：只用订阅 URL
uv run cli.py --url https://example.com/sub -o config.yaml

# 2. 过滤香港节点
uv run cli.py --url URL --include "香港|HK" -o hk.yaml

# 3. 使用自定义规则
uv run cli.py --url URL --config https://example.com/rules.ini -o config.yaml

# 4. 使用 HTTP 服务转换
uv run cli.py --url URL --method http -o config.yaml
```

### 有 Dler Cloud 账户

```bash
# 1. 本地转换
uv run cli.py --email USER --password PASS -o config.yaml

# 2. HTTP 服务转换
uv run cli.py --email USER --password PASS -o config.yaml --method http
```

## 📋 参数速查表

### 认证
```bash
--email EMAIL              # 邮箱
--password PASS            # 密码
--token TOKEN              # API Token
```

### 订阅
```bash
--url URL                  # 订阅 URL
--sub-type ss2022          # 订阅类型 (ss2022/vmess/trojan)
```

### 转换方法
```bash
--method local             # 本地转换（默认）
--method http              # HTTP 服务转换
--host http://...          # HTTP 服务地址
```

### 过滤
```bash
--include "香港|HK"        # 包含规则
--exclude "过期|expire"    # 排除规则
```

### 功能
```bash
--config URL               # 自定义规则
--sort                     # 排序节点
--no-emoji                 # 移除 emoji
--append-type              # 添加类型后缀
--tfo                      # 启用 TCP Fast Open
-v                         # 详细输出
```

### 输出
```bash
-o FILE                    # 输出文件（默认：config.yaml）
```

## 🎯 典型场景

### 场景 1：日常使用
```bash
uv run cli.py --email $EMAIL --password $PASS -o config.yaml
```

### 场景 2：只要特定地区
```bash
uv run cli.py --url $URL --include "香港|新加坡" -o asia.yaml
```

### 场景 3：使用外部规则
```bash
uv run cli.py --url $URL \
  --config https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online.ini \
  -o config.yaml
```

### 场景 4：调试问题
```bash
uv run cli.py --url $URL -o config.yaml -v
```

### 场景 5：兼容旧服务
```bash
uv run cli.py --url $URL -o config.yaml \
  --method http \
  --host http://127.0.0.1:25500/sub \
  --config https://example.com/rules.ini
```

## 🔄 对比

| 功能 | 本地转换 | HTTP 服务 |
|------|----------|-----------|
| 命令 | `--method local` | `--method http` |
| 服务依赖 | ❌ 无 | ✅ 需要 |
| 速度 | 快 | 中等 |
| 规则 | 基础（可自定义） | 完整 |
| 推荐度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

## 💡 Tips

1. **使用 .env 文件存储凭据**
   ```bash
   echo "DLER_EMAIL=user@email.com" > .env
   echo "DLER_PASSWORD=pass" >> .env
   uv run cli.py -o config.yaml  # 自动读取
   ```

2. **正则表达式测试**
   ```bash
   # 先用 -v 查看所有节点
   uv run cli.py --url $URL -v -o /dev/null

   # 再应用过滤
   uv run cli.py --url $URL --include "your-pattern" -o config.yaml
   ```

3. **批量处理**
   ```bash
   for region in 香港 新加坡 日本; do
     uv run cli.py --url $URL --include "$region" -o "${region}.yaml"
   done
   ```

4. **自动化更新**
   ```bash
   # 添加到 crontab
   0 3 * * * cd /path && uv run cli.py --email $E --password $P -o config.yaml
   ```

## 🆘 快速帮助

```bash
uv run cli.py --help          # 查看完整帮助
uv run cli.py -v              # 详细输出模式
```

完整文档：[CLI_USAGE.md](CLI_USAGE.md)
