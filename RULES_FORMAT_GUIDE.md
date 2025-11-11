# 规则文件格式说明

## 问题描述

当使用新的本地转换器（`--method local`）并指定自定义规则文件时，如果规则文件是 **subconverter INI 格式**，会导致 Clash 报错：

```
error msg="rules[0] [[custom]] error: format invalid"
```

## 原因分析

新的本地转换器与旧的 HTTP 服务转换器（subconverter）对规则文件的处理方式不同：

### Subconverter INI 格式（❌ 本地转换器不支持）

```ini
[custom]
ruleset=🎯 全球直连,https://raw.githubusercontent.com/.../LocalAreaNetwork.list
ruleset=🛑 广告拦截,https://raw.githubusercontent.com/.../BanAD.list
custom_proxy_group=🚀 节点选择`select`[]♻️ 自动选择
```

**特点**：
- 包含 `[custom]` 段
- 使用 `ruleset=` 引用外部规则列表
- 使用 `custom_proxy_group=` 定义策略组
- 这是 **subconverter 的配置文件**，不是 Clash 规则列表

### Clash 规则列表格式（✅ 本地转换器支持）

```
# 注释
DOMAIN-SUFFIX,google.com,PROXY
DOMAIN-SUFFIX,youtube.com,PROXY
DOMAIN-KEYWORD,google,PROXY
GEOIP,CN,DIRECT
MATCH,PROXY
```

**特点**：
- 每行一条规则
- 使用逗号分隔字段
- 支持注释（# 或 ;）
- 这是 **纯 Clash 规则列表**

## 解决方案

### 方案 1：使用 HTTP 服务转换（推荐，适用于复杂配置）

如果你需要使用 subconverter INI 格式的配置文件，请使用 `--method http`：

```bash
uv run cli.py \
  --url https://example.com/subscription \
  --method http \
  --config https://raw.githubusercontent.com/.../config.ini \
  -o config.yaml
```

**优点**：
- ✅ 完全兼容 subconverter 配置
- ✅ 支持复杂的策略组配置
- ✅ 支持 ruleset 引用

**缺点**：
- ❌ 需要运行 subconverter 服务

### 方案 2：使用简单规则列表（推荐，适用于本地转换）

使用纯 Clash 规则列表：

```bash
uv run cli.py \
  --url https://example.com/subscription \
  --config https://example.com/simple-rules.txt \
  -o config.yaml
```

**simple-rules.txt** 示例：
```
DOMAIN-SUFFIX,google.com,PROXY
DOMAIN-SUFFIX,youtube.com,PROXY
GEOIP,CN,DIRECT
MATCH,PROXY
```

**优点**：
- ✅ 无需外部服务
- ✅ 速度快
- ✅ 跨平台

**缺点**：
- ⚠️ 不支持复杂的策略组配置

### 方案 3：不使用自定义规则

本地转换器会使用内置的默认规则：

```bash
uv run cli.py \
  --url https://example.com/subscription \
  -o config.yaml
```

## 自动检测

新版本的转换器会自动检测规则文件格式：

```bash
$ uv run cli.py --url $URL --config https://.../config.ini -o config.yaml

正在加载自定义规则...
⚠️  Warning: This appears to be a subconverter INI config file.
⚠️  The local converter only supports plain Clash rule lists.
⚠️  For complex subconverter configs, please use '--method http'
⚠️  使用默认规则
```

## 规则格式对比

| 特性 | Clash 规则列表 | Subconverter INI |
|------|----------------|------------------|
| 格式 | 纯文本规则 | INI 配置文件 |
| 策略组 | 简单（PROXY/DIRECT/AUTO） | 复杂（自定义策略组） |
| 本地转换 | ✅ 支持 | ❌ 不支持 |
| HTTP 转换 | ✅ 支持 | ✅ 支持 |
| 外部引用 | ❌ 不支持 | ✅ 支持 |
| 难度 | 简单 | 复杂 |

## 常见问题

### Q: 我一直用的规则文件突然不能用了？

**A**: 如果你之前用的是 `--method http`（或旧的 `sub_converter.py`），现在改用 `--method local`，并且你的规则文件是 subconverter INI 格式，那么确实不能用。

**解决方法**：继续使用 `--method http`，或者改用简单的 Clash 规则列表。

### Q: 如何将 INI 格式转换为简单规则列表？

**A**: 你需要：
1. 手动下载 INI 中所有 `ruleset=` 引用的规则文件
2. 合并所有规则
3. 去掉策略组名称（或替换为 PROXY/DIRECT）
4. 保存为纯文本文件

或者直接使用 `--method http` 更简单。

### Q: 什么时候使用哪种方法？

| 场景 | 推荐方法 |
|------|----------|
| 简单使用，只需要基本规则 | `--method local`（默认） |
| 已有 subconverter INI 配置 | `--method http` |
| 需要复杂策略组 | `--method http` |
| 无服务器环境，快速转换 | `--method local` |
| 完全兼容 subconverter | `--method http` |

## 示例

### 示例 1：使用默认规则（最简单）

```bash
uv run cli.py --url $URL -o config.yaml
```

### 示例 2：使用简单自定义规则

```bash
# 创建规则文件
cat > my_rules.txt << 'EOF'
DOMAIN-SUFFIX,google.com,PROXY
DOMAIN-SUFFIX,github.com,PROXY
GEOIP,CN,DIRECT
MATCH,PROXY
EOF

# 转换
uv run cli.py --url $URL --config my_rules.txt -o config.yaml
```

### 示例 3：使用复杂 INI 配置（HTTP 方法）

```bash
uv run cli.py \
  --url $URL \
  --method http \
  --config https://raw.githubusercontent.com/.../complex_config.ini \
  -o config.yaml
```

## 总结

- ✅ **本地转换** (`--method local`) 只支持简单的 Clash 规则列表
- ✅ **HTTP 转换** (`--method http`) 支持完整的 subconverter INI 配置
- ✅ 转换器会自动检测并提示你使用正确的方法
- ✅ 大多数场景下，使用默认规则就足够了

如果不确定，建议：
1. 先尝试不带 `--config` 参数（使用默认规则）
2. 如果需要自定义，使用简单规则列表
3. 如果需要复杂配置，使用 `--method http`
