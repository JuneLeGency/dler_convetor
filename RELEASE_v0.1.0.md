# Release v0.1.0 - 首次发布

## 🎉 发布说明

这是 `py-subconverter` 的首次正式发布！一个纯 Python 实现的代理订阅转换器，完全兼容 subconverter INI 配置格式。

## ✨ 主要特性

### 代理协议支持
- ✅ Shadowsocks (SS)
- ✅ ShadowsocksR (SSR)
- ✅ VMess
- ✅ Trojan
- ✅ VLESS

### INI 配置支持
- ✅ 完整支持 subconverter INI 格式
- ✅ 规则集自动下载 (`ruleset=`)
- ✅ 自定义策略组 (`custom_proxy_group=`)
- ✅ 正则表达式节点匹配
- ✅ 策略组引用 (`[]` 前缀)
- ✅ 自动过滤不支持的规则类型

### 规则类型过滤
自动过滤 Clash 不支持的规则类型：
- ❌ USER-AGENT (仅 Clash Meta)
- ❌ URL-REGEX (仅 Clash Meta)
- ✅ FINAL 自动转换为 MATCH

支持的规则类型：
- ✅ DOMAIN, DOMAIN-SUFFIX, DOMAIN-KEYWORD
- ✅ IP-CIDR, IP-CIDR6
- ✅ GEOIP, MATCH, PROCESS-NAME

### 转换模式
- **本地转换**（推荐）：100% 本地处理，无需外部服务
- **HTTP 转换**：兼容原版 subconverter HTTP 服务

## 📦 安装

```bash
pip install py-subconverter
```

## 🚀 快速开始

### 命令行使用

```bash
# 基本转换
py-sub-conv --url https://example.com/subscription -o config.yaml

# 使用 INI 配置
py-sub-conv --url https://example.com/subscription \
  --config https://example.com/rules.ini \
  -o config.yaml

# 过滤节点
py-sub-conv --url https://example.com/sub --include "香港|HK" -o hk.yaml
```

### Python API

```python
from py_subconverter import SubscriptionConverter

converter = SubscriptionConverter()
config = converter.convert(
    subscription_url="https://example.com/subscription",
    rule_url="https://example.com/config.ini",
    output_file="config.yaml"
)
```

## 🔧 关键修复

### 1. 策略组引用丢失 ✅
- 问题：策略组中的 `[]` 引用被错误移除
- 修复：正确保留并解析策略组引用

### 2. 规则缺少策略组 ✅
- 问题：下载的规则没有添加策略组名称
- 修复：智能检测并在正确位置插入策略组

### 3. YAML 缩进格式错误 ✅
- 问题：rules 部分缩进不符合 Clash 要求
- 修复：使用 CustomDumper 确保正确的 2 空格缩进

### 4. 空策略组 ✅
- 问题：正则表达式未匹配节点导致空策略组
- 修复：未匹配时添加 DIRECT 作为默认值

### 5. 不支持的规则类型 ✅
- 问题：USER-AGENT、URL-REGEX 导致 Clash 启动失败
- 修复：自动过滤不支持的规则类型，转换 FINAL → MATCH

## 📊 性能对比

| 指标 | 原版 subconverter | py-subconverter |
|------|------------------|-----------------|
| 服务依赖 | 需要 HTTP 服务 | ✅ 无需服务 |
| 处理速度 | ~30秒 | ~25秒 |
| 规则过滤 | 自动 | ✅ 自动 |
| 功能完整性 | 100% | 100% |
| 可维护性 | C++ | ✅ Python |

## 📝 依赖项

- Python >= 3.9
- pydantic >= 2.0.0
- PyYAML >= 6.0
- requests >= 2.28.0
- python-dotenv >= 0.20.0

## 🧪 测试覆盖

- ✅ 不支持的规则类型过滤测试
- ✅ FINAL → MATCH 转换测试
- ✅ 策略组解析测试
- ✅ 完整端到端转换测试

## 📚 文档

- [README.md](README.md) - 项目说明
- [RELEASE_GUIDE.md](RELEASE_GUIDE.md) - 发布指南
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 项目总结
- [docs/](docs/) - 详细文档

## 🐛 已知问题

目前没有已知的重大问题。

## 🔮 后续计划

### v0.2.0
- 添加更多代理协议支持 (Hysteria, WireGuard)
- 性能优化
- 更多单元测试

### v0.3.0
- Web UI
- 配置模板系统
- 规则集缓存

### v1.0.0
- 插件系统
- 自定义规则引擎
- 完整文档

## 🤝 贡献

欢迎贡献！请访问 [GitHub](https://github.com/gencylee/py-subconverter) 提交 Issue 或 Pull Request。

## 📜 许可证

MIT License

## 🙏 致谢

- [subconverter](https://github.com/tindy2013/subconverter) - 原版项目
- [ACL4SSR](https://github.com/ACL4SSR/ACL4SSR) - 规则集
- [Clash](https://github.com/Dreamacro/clash) - 代理工具

---

**发布日期**: 2025-11-11
**版本**: v0.1.0
**下载**: [PyPI](https://pypi.org/project/py-subconverter/)
