# 使用指南 / Usage Guide

## 快速开始 / Quick Start

### 1. 安装依赖 / Install Dependencies

```bash
uv pip install pyyaml pydantic requests
```

### 2. 转换订阅 / Convert Subscription

#### 从 URL 转换 / From URL

```bash
uv run subscription_converter.py --url https://your-subscription-url -o clash.yaml
```

#### 从本地文件 / From Local File

```bash
uv run subscription_converter.py --file subscription.txt -o clash.yaml
```

## 详细示例 / Detailed Examples

### 示例 1: 基本转换 / Basic Conversion

```bash
# 从订阅 URL 转换并保存为 clash.yaml
uv run subscription_converter.py \
  --url "https://example.com/subscription" \
  -o clash.yaml
```

**输出 / Output:**
```
Fetching subscription from: https://example.com/subscription
Parsing subscription...
Found 10 proxies
Proxy types:
  - ss: 5
  - vmess: 3
  - trojan: 2
Generating Clash configuration...
✓ Configuration saved to: clash.yaml
✓ Conversion completed successfully!
```

### 示例 2: 使用自定义规则 / Custom Rules

```bash
# 使用自定义规则文件
uv run subscription_converter.py \
  --url "https://example.com/subscription" \
  --rules "https://raw.githubusercontent.com/user/rules/master/clash.txt" \
  -o clash.yaml
```

### 示例 3: 输出到标准输出 / Output to Stdout

```bash
# 直接查看生成的配置，不保存文件
uv run subscription_converter.py \
  --url "https://example.com/subscription" \
  --stdout
```

### 示例 4: 转换本地订阅文件 / Convert Local File

首先创建一个订阅文件 `my_subscription.txt`:

```
ss://YWVzLTI1Ni1nY206cGFzc3dvcmQxMjNAc3MxLmV4YW1wbGUuY29tOjgzODg=#Server1
ss://YWVzLTI1Ni1nY206cGFzc3dvcmQxMjNAc3MyLmV4YW1wbGUuY29tOjgzODk=#Server2
vmess://eyJ2IjoiMiIsInBzIjoi6K+m57uG5pyN5Yqh5ZmoIiwiYWRkIjoidm1lc3MuZXhhbXBsZS5jb20iLCJwb3J0IjoiNDQzIiwiaWQiOiIxMjM0NTY3OC0xMjM0LTEyMzQtMTIzNC0xMjM0NTY3ODkwMTIiLCJhaWQiOiIwIiwibmV0Ijoid3MiLCJ0eXBlIjoibm9uZSIsImhvc3QiOiJ2bWVzcy5leGFtcGxlLmNvbSIsInBhdGgiOiIvdm1lc3MiLCJ0bHMiOiJ0bHMifQ==
trojan://password@trojan.example.com:443?sni=trojan.example.com#Trojan
```

然后转换：

```bash
uv run subscription_converter.py --file my_subscription.txt -o clash.yaml
```

## Python API 使用 / Using Python API

### 方式 1: 使用 SubscriptionConverter

```python
from subscription_converter import SubscriptionConverter

# 创建转换器实例
converter = SubscriptionConverter()

# 从 URL 转换
converter.convert_from_url(
    subscription_url="https://example.com/subscription",
    output_file="clash.yaml"
)

# 从本地文件转换
converter.convert_from_file(
    input_file="subscription.txt",
    output_file="clash.yaml"
)
```

### 方式 2: 直接使用解析器和生成器

```python
from proxy_parser import parse_subscription
from clash_generator import ClashGenerator

# 读取订阅内容
with open("subscription.txt", "r") as f:
    subscription_content = f.read()

# 解析代理
proxies = parse_subscription(subscription_content)
print(f"Found {len(proxies)} proxies")

# 生成 Clash 配置
generator = ClashGenerator()
config = generator.generate_config(proxies)

# 保存配置
with open("clash.yaml", "w") as f:
    f.write(config)
```

### 方式 3: 解析单个代理 URL

```python
from proxy_parser import parse_proxy_url

# 解析 Shadowsocks
ss_proxy = parse_proxy_url("ss://YWVzLTI1Ni1nY206cGFzc3dvcmQ=@example.com:8388#MyServer")
print(f"Server: {ss_proxy.server}:{ss_proxy.port}")
print(f"Cipher: {ss_proxy.cipher}")

# 解析 VMess
vmess_proxy = parse_proxy_url("vmess://eyJ2IjoiMiIsInBzIjoi...")
print(f"UUID: {vmess_proxy.uuid}")
print(f"Network: {vmess_proxy.network}")

# 解析 Trojan
trojan_proxy = parse_proxy_url("trojan://password@example.com:443#MyTrojan")
print(f"Password: {trojan_proxy.password}")
```

## 自定义配置 / Custom Configuration

### 自定义代理组 / Custom Proxy Groups

```python
from clash_generator import ClashGenerator
from proxy_parser import parse_subscription

# 解析代理
proxies = parse_subscription(content)
proxy_names = [p.name for p in proxies]

# 自定义代理组
custom_groups = [
    {
        "name": "🚀 Proxy",
        "type": "select",
        "proxies": ["♻️ Auto", "🔄 Fallback", "DIRECT"] + proxy_names
    },
    {
        "name": "♻️ Auto",
        "type": "url-test",
        "proxies": proxy_names,
        "url": "http://www.gstatic.com/generate_204",
        "interval": 300
    },
    {
        "name": "🔄 Fallback",
        "type": "fallback",
        "proxies": proxy_names,
        "url": "http://www.gstatic.com/generate_204",
        "interval": 300
    },
    {
        "name": "🎬 Netflix",
        "type": "select",
        "proxies": ["🚀 Proxy"] + proxy_names
    }
]

# 生成配置
generator = ClashGenerator()
config = generator.generate_config(proxies, proxy_groups=custom_groups)
```

### 自定义规则 / Custom Rules

```python
custom_rules = [
    # Netflix
    "DOMAIN-SUFFIX,netflix.com,🎬 Netflix",
    "DOMAIN-SUFFIX,nflxvideo.net,🎬 Netflix",

    # Google
    "DOMAIN-SUFFIX,google.com,🚀 Proxy",
    "DOMAIN-SUFFIX,googleapis.com,🚀 Proxy",

    # 国内直连
    "DOMAIN-SUFFIX,cn,DIRECT",
    "DOMAIN-SUFFIX,baidu.com,DIRECT",
    "GEOIP,CN,DIRECT",

    # 默认规则
    "MATCH,🚀 Proxy"
]

config = generator.generate_config(proxies, rules=custom_rules)
```

## 支持的代理格式 / Supported Formats

### Shadowsocks (SS)

```
# SIP002 格式（明文）
ss://method:password@server:port#remark

# Base64 编码格式
ss://base64(method:password)@server:port#remark
ss://base64(method:password@server:port)#remark

# 带插件
ss://...?plugin=obfs-local;obfs=http#remark
```

### ShadowsocksR (SSR)

```
ssr://base64(server:port:protocol:method:obfs:base64(password)/?params)

# 参数包括:
# - remarks: base64(节点名称)
# - group: base64(分组名称)
# - obfsparam: base64(混淆参数)
# - protoparam: base64(协议参数)
```

### VMess

```
vmess://base64(json_config)

# JSON 配置示例:
{
  "v": "2",
  "ps": "节点名称",
  "add": "server.com",
  "port": "443",
  "id": "uuid",
  "aid": "0",
  "net": "ws",
  "type": "none",
  "host": "server.com",
  "path": "/path",
  "tls": "tls"
}
```

### Trojan

```
trojan://password@server:port?params#remark

# 常用参数:
# - sni: SNI 域名
# - type: 传输协议 (tcp, ws, grpc)
# - path: WebSocket 路径或 gRPC serviceName
# - host: WebSocket Host
# - allowInsecure: 跳过证书验证
```

### Hysteria2

```
hysteria2://password@server:port?params#remark
hy2://password@server:port?params#remark

# 常用参数:
# - sni: SNI 域名
# - obfs: 混淆方式
# - obfs-password: 混淆密码
# - up: 上传带宽
# - down: 下载带宽
```

## 常见问题 / FAQ

### Q1: 如何验证生成的配置是否正确？

```bash
# 使用 Clash 的验证工具
clash -t -f clash.yaml

# 或者在 Python 中验证 YAML 语法
uv run python -c "import yaml; yaml.safe_load(open('clash.yaml'))"
```

### Q2: 如何处理订阅中的无效节点？

转换器会自动跳过无法解析的节点，并在控制台输出警告信息。使用 `-v` 参数可以看到详细的错误信息。

### Q3: 如何更新订阅？

```bash
# 直接重新运行转换命令即可
uv run subscription_converter.py --url https://your-subscription-url -o clash.yaml
```

### Q4: 如何合并多个订阅？

```python
from proxy_parser import parse_subscription
from clash_generator import ClashGenerator

# 读取多个订阅
sub1 = parse_subscription(content1)
sub2 = parse_subscription(content2)
sub3 = parse_subscription(content3)

# 合并
all_proxies = sub1 + sub2 + sub3

# 生成配置
generator = ClashGenerator()
config = generator.generate_config(all_proxies)
```

### Q5: 生成的配置在哪些客户端上可用？

生成的 Clash 格式配置可用于：
- Clash for Windows
- Clash for Android (ClashA)
- Clash for Mac (ClashX)
- Clash Premium
- Clash Meta (Mihomo)

## 调试技巧 / Debugging Tips

### 查看详细输出

```bash
uv run subscription_converter.py --url https://... -v
```

### 测试单个代理解析

```python
from proxy_parser import parse_proxy_url

url = "ss://..."
proxy = parse_proxy_url(url)
if proxy:
    print(f"✓ Parsed: {proxy.name}")
    print(f"  Type: {proxy.type.value}")
    print(f"  Server: {proxy.server}:{proxy.port}")
else:
    print("✗ Failed to parse")
```

### 检查生成的 YAML

```python
import yaml

with open("clash.yaml") as f:
    config = yaml.safe_load(f)

print("Proxies:", len(config["proxies"]))
print("Groups:", len(config["proxy-groups"]))
print("Rules:", len(config["rules"]))
```

## 最佳实践 / Best Practices

1. **定期更新订阅**: 使用 cron 或计划任务定期运行转换命令
2. **备份配置**: 在更新前备份现有的 clash.yaml
3. **验证配置**: 生成后验证 YAML 格式是否正确
4. **自定义规则**: 根据实际需求调整代理组和规则
5. **使用版本控制**: 将配置文件纳入 git 管理（注意排除敏感信息）

## 许可证 / License

MIT License
