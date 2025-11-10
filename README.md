# Proxy Subscription Converter

一个独立的、跨平台的代理订阅转换工具，使用纯 Python 实现。无需服务器依赖！

A standalone, cross-platform proxy subscription converter implemented in pure Python. No server dependencies required!

## ✨ 特性 Features

- ✅ **纯 Python 实现** - 无需外部服务 / Pure Python Implementation - No external services
- ✅ **跨平台** - 支持 Windows, macOS, Linux / Cross-Platform
- ✅ **完整的 CLI 工具** - 支持新旧两种转换方式 / Complete CLI tool with dual conversion methods
- ✅ **Dler Cloud 集成** - 自动获取订阅 / Dler Cloud integration
- ✅ **多种代理格式** / Multiple Proxy Formats:
  - Shadowsocks (ss://, SIP008)
  - ShadowsocksR (ssr://)
  - VMess (vmess://)
  - Trojan (trojan://)
  - Hysteria2 (hysteria2://, hy2://)
  - Clash YAML
- ✅ **输出格式**: Clash YAML
- ✅ **节点过滤** - 支持正则表达式 / Node filtering with regex
- ✅ **自定义规则支持** / Custom Rules Support
- ✅ **无需 Docker/服务器** / No Docker/Server Required

## 🚀 快速开始 Quick Start

### 推荐方式：使用 CLI 工具 Recommended: Use CLI Tool

#### 场景 1：只有订阅 URL（无需账户）★ 最简单

```bash
# 基本使用 - 只需要订阅 URL
uv run cli.py --url https://example.com/subscription -o config.yaml

# 过滤特定节点
uv run cli.py --url $URL --include "香港|HK" --sort -o hk.yaml

# 使用外部规则
uv run cli.py --url $URL --config https://example.com/rules.ini -o config.yaml
```

#### 场景 2：有 Dler Cloud 账户

```bash
# 使用邮箱密码
uv run cli.py --email your@email.com --password yourpass -o config.yaml

# 使用 Token
uv run cli.py --token YOUR_API_TOKEN -o config.yaml

# 使用 HTTP 服务（旧方法）
uv run cli.py --email user@email.com --password pass --method http -o config.yaml
```

**详细文档**：
- **[无需账户使用指南](URL_ONLY_GUIDE.md)** ⭐ 新手必读 - 只用订阅 URL 的完整指南
- [CLI 使用指南](CLI_USAGE.md) - 完整参数说明和使用示例
- [CLI 快速参考](CLI_QUICKREF.md) - 常用命令速查
- [CLI 完成总结](CLI_SUMMARY.md) - 功能清单和测试结果

## 📦 安装 Installation

### 使用 uv (推荐 Recommended)

```bash
# 克隆仓库
git clone <repository-url>
cd convertor

# 安装依赖
uv pip install -e .
```

### 使用 pip Using pip

```bash
pip install -r requirements.txt
# or
pip install pyyaml pydantic requests python-dotenv
```

## 🎯 两种转换方式 Two Conversion Methods

### 方式 1：本地转换（推荐 Recommended）

**优势**：
- ✅ 无需额外服务
- ✅ 跨平台兼容
- ✅ 资源占用低
- ✅ 快速便捷

```bash
uv run cli.py --email user@email.com --password pass -o config.yaml
```

### 方式 2：HTTP 服务

**优势**：
- ✅ 与 subconverter 完全兼容
- ✅ 功能完整，规则丰富

**前提**：需要运行 subconverter 服务

```bash
uv run cli.py --email user@email.com --password pass \
  --method http \
  --host http://127.0.0.1:25500/sub \
  -o config.yaml
```

## 💡 CLI 常用参数 Common CLI Parameters

### 认证 Authentication
```bash
--email EMAIL              # Dler Cloud 邮箱
--password PASSWORD        # Dler Cloud 密码
--token TOKEN              # API Token（优先）
```

### 转换方法 Conversion Method
```bash
--method local             # 本地转换（默认）
--method http              # HTTP 服务转换
--host URL                 # HTTP 服务地址
```

### 过滤 Filtering
```bash
--include "香港|HK"        # 包含规则（正则）
--exclude "过期|expire"    # 排除规则（正则）
--sort                     # 排序节点
```

### 配置 Configuration
```bash
--config URL               # 自定义规则文件
--no-emoji                 # 移除 emoji
--append-type              # 添加类型后缀
-o FILE                    # 输出文件
-v                         # 详细输出
```

完整参数列表请运行：
```bash
uv run cli.py --help
```

## 📚 使用场景示例 Usage Examples

### 场景 1：日常使用
```bash
# 使用 .env 文件存储凭据
echo "DLER_EMAIL=user@email.com" > .env
echo "DLER_PASSWORD=yourpass" >> .env

# 直接运行
uv run cli.py -o config.yaml
```

### 场景 2：只要特定地区
```bash
# 只要香港和新加坡节点
uv run cli.py --url $URL --include "香港|新加坡" -o asia.yaml
```

### 场景 3：使用外部规则
```bash
uv run cli.py --url $URL \
  --config https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online.ini \
  -o config.yaml
```

### 场景 4：批量处理
```bash
for region in 香港 新加坡 日本; do
  uv run cli.py --url $URL --include "$region" -o "${region}.yaml"
done
```

## 🔧 Python API 使用 Python API Usage

### 基本用法 Basic Usage

```python
from subscription_converter import SubscriptionConverter

# 初始化转换器
converter = SubscriptionConverter()

# 从 URL 转换
converter.convert_from_url(
    subscription_url="https://你的订阅地址",
    output_file="clash.yaml"
)

# 从文件转换
converter.convert_from_file(
    input_file="subscription.txt",
    output_file="clash.yaml"
)
```

### 高级用法 Advanced Usage

```python
from proxy_parser import parse_subscription
from clash_generator import ClashGenerator

# 解析订阅内容
proxies = parse_subscription(subscription_content)

# 过滤节点
import re
pattern = re.compile(r'香港|HK')
proxies = [p for p in proxies if pattern.search(p.name)]

# 生成 Clash 配置
generator = ClashGenerator()
config_yaml = generator.generate_config(proxies)
```

## 🏗️ 项目架构 Architecture

### 核心模块 Core Modules

```
convertor/
├── cli.py                       # CLI 工具（完整实现）
├── proxy_parser.py             # 代理解析器（支持多种格式）
├── clash_generator.py          # Clash 配置生成器
├── subscription_converter.py   # 转换核心库
├── dler_api_client.py          # Dler Cloud API 客户端
├── main.py                     # 使用示例
├── models.py                   # 数据模型
└── pyproject.toml              # 项目配置
```

### 工作流程 Workflow

```
订阅 URL → 解析器 → 过滤/排序 → 生成器 → Clash YAML
   ↓         ↓          ↓          ↓          ↓
fetch   parse     filter    generate    save
```

## 🆚 对比 subconverter Comparison

| 特性 Feature | 本项目 This Project | subconverter |
|---------|--------------|----------------------|
| 语言 Language | Pure Python | C++ |
| 需要服务器 Server | ❌ No | ✅ Yes |
| 跨平台 Cross-Platform | ✅ 原生 Native | ✅ 需编译 Via compilation |
| 安装 Installation | pip/uv | Docker/Build from source |
| 依赖 Dependency | 最小化 Minimal | 众多 C++ 库 Many libs |
| 自定义 Customization | 容易 Easy (Python) | 复杂 Complex (C++) |
| CLI 工具 | ✅ 完整 Complete | ✅ HTTP API only |
| 节点过滤 | ✅ 正则 Regex | ✅ 正则 Regex |
| Dler Cloud | ✅ 原生支持 Native | ❌ Manual |

## 📝 支持的格式 Supported Formats

### 输入格式 Input Formats

#### Shadowsocks (SIP002)
```
ss://base64(method:password)@server:port#remark
ss://method:password@server:port#remark
```

#### Shadowsocks (SIP008)
```
ss://base64(method:password)@server:port/?udp=1#remark
```

#### Clash YAML
```yaml
proxies:
- name: "节点名"
  type: ss
  server: example.com
  port: 443
  cipher: aes-256-gcm
  password: password
```

#### VMess
```
vmess://base64(json_config)
```

#### Trojan
```
trojan://password@server:port?params#remark
```

#### Hysteria2
```
hysteria2://password@server:port?params#remark
hy2://password@server:port?params#remark
```

### 输出格式 Output Format

**Clash YAML** - 包含：
- 完整的 proxies 配置
- 代理组 (PROXY, Auto, Fallback)
- 规则集（可自定义）

## 🐛 故障排除 Troubleshooting

### 问题 1：登录失败
```bash
✗ 获取订阅失败: Login failed
```
**解决**：检查邮箱密码，使用 `-v` 查看详细错误

### 问题 2：HTTP 服务无法连接
```bash
✗ 下载失败: Connection refused
```
**解决**：确认 subconverter 服务运行，检查 `--host` 地址

### 问题 3：未找到有效节点
```bash
✗ 未找到有效的代理节点
```
**解决**：检查订阅 URL，使用 `-v` 查看解析详情

### 问题 4：过滤后无节点
```bash
过滤后: 0/44 个节点
```
**解决**：检查正则表达式，使用 `-v` 查看过滤过程

## 🧪 测试 Testing

```bash
# 测试本地转换
uv run cli.py --url https://example.com/sub -o test.yaml -v

# 测试 HTTP 转换
uv run cli.py --url https://example.com/sub --method http -o test.yaml

# 测试过滤功能
uv run cli.py --url https://example.com/sub --include "香港" -o hk.yaml -v

# 运行完整测试套件
python test_converter.py
```

## 📖 文档 Documentation

### 新手入门
- **[无需账户使用指南](URL_ONLY_GUIDE.md)** ⭐ 推荐 - 最简单的使用方式

### CLI 工具文档
- [CLI 使用指南](CLI_USAGE.md) - 详细的 CLI 使用文档
- [CLI 快速参考](CLI_QUICKREF.md) - 常用命令速查表
- [CLI 完成总结](CLI_SUMMARY.md) - 功能清单和测试结果

### 其他文档
- [对比报告](COMPARISON_REPORT.md) - 新旧方法对比
- [项目总结](PROJECT_SUMMARY.md) - 项目概览
- [使用指南](USAGE.md) - API 使用文档

## ⚙️ 环境变量 Environment Variables

支持通过 `.env` 文件或环境变量配置：

```bash
# .env 文件
DLER_EMAIL=your@email.com
DLER_PASSWORD=yourpassword
DLER_API_TOKEN=your_token
```

**优先级**：命令行参数 > 环境变量 > .env 文件 > 默认值

## 🎯 最佳实践 Best Practices

1. **推荐使用本地转换** - 快速、无依赖
2. **敏感信息使用 .env** - 不要在命令行直接输入密码
3. **使用过滤优化节点** - 只保留需要的节点
4. **定期更新配置** - 使用 cron 定时任务
5. **备份重要配置** - 使用 Git 管理

## 🎓 进阶功能 Advanced Features

### 自定义规则文件
```bash
uv run cli.py --url $URL \
  --config https://example.com/custom-rules.ini \
  -o config.yaml
```

### 正则表达式过滤
```bash
# 只要香港的 IEPL 线路
uv run cli.py --url $URL --include "香港.*IEPL" -o config.yaml

# 排除高倍率节点
uv run cli.py --url $URL --exclude "x[2-9]|倍" -o config.yaml
```

### 节点名称自定义
```bash
# 移除 emoji 并添加类型后缀
uv run cli.py --url $URL --no-emoji --append-type -o config.yaml
# 结果: 香港 IEPL [01] [SS]
```

## 📄 许可 License

MIT License

## 🙏 致谢 Acknowledgments

- 灵感来自 [tindy2013/subconverter](https://github.com/tindy2013/subconverter)
- 感谢所有贡献者

## 🔗 相关链接 Links

- [Clash](https://github.com/Dreamacro/clash)
- [subconverter](https://github.com/tindy2013/subconverter)
- [Dler Cloud](https://dlercloud.com)

---

**项目状态**: ✅ 生产就绪 Production Ready

**最后更新**: 2025-11-10
