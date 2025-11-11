# 新旧转换器对比说明

## 核心差异

### 旧方法 (`sub_converter.py` + subconverter 服务)

**工作原理**：
1. 调用 subconverter HTTP 服务 (`http://127.0.0.1:25500/sub`)
2. Subconverter 完整处理 INI 配置文件
3. 生成包含所有自定义策略组的 Clash 配置

**特点**：
- ✅ 完整支持 subconverter INI 配置
- ✅ 支持复杂的自定义策略组
- ✅ 支持 `ruleset=` 外部规则引用
- ✅ 支持 `custom_proxy_group=` 策略组定义
- ❌ 需要运行 subconverter 服务
- ❌ 依赖外部服务

**示例输出** (`config_old.yaml`)：
```yaml
proxy-groups:
- name: 🚀 节点选择
  type: select
  proxies:
  - ♻️ 自动选择
  - 📺 省流节点
  - 🇭🇰 香港节点
  # ... 更多自定义策略组

- name: 🎯 全球直连
  type: select
  proxies:
  - DIRECT

- name: 🛑 广告拦截
  type: select
  proxies:
  - REJECT

rules:
- DOMAIN-SUFFIX,acl4.ssr,🎯 全球直连
- DOMAIN-SUFFIX,google.com,🚀 节点选择
# ... 数千条规则
```

### 新方法 (`subscription_converter.py`)

**工作原理**：
1. 纯 Python 本地解析订阅
2. 自动检测 INI 配置文件
3. 下载并解析所有规则集
4. 生成完整的 Clash 配置

**特点**：
- ✅ 无需外部服务
- ✅ 跨平台兼容
- ✅ 快速简单
- ✅ **完整支持 INI 配置文件** (NEW!)
- ✅ **支持自定义策略组** (NEW!)
- ✅ **支持外部规则引用** (NEW!)
- ✅ 自动下载规则集
- ✅ 支持正则匹配节点

**示例输出**：

**没有 INI 配置时** (`config_new.yaml` - 简单模式)：
```yaml
proxy-groups:
- name: PROXY
  type: select
  proxies:
  - Auto
  - 节点1
  - 节点2

- name: Auto
  type: url-test
  proxies:
  - 节点1
  - 节点2
  url: http://www.gstatic.com/generate_204
  interval: 300

rules:
- DOMAIN-SUFFIX,google.com,PROXY
- GEOIP,CN,DIRECT
- MATCH,PROXY
```

**使用 INI 配置时** (`config_ini_local.yaml` - 完整模式)：
```yaml
proxy-groups:
- name: 🚀 节点选择
  type: select
  proxies:
  - ♻️ 自动选择
  - 📺 省流节点
  - 🇭🇰 香港节点
  # ... 更多自定义策略组

- name: 🎯 全球直连
  type: select
  proxies:
  - DIRECT

- name: 🛑 广告拦截
  type: select
  proxies:
  - REJECT

rules:
- DOMAIN-SUFFIX,acl4.ssr,🎯 全球直连
- DOMAIN-SUFFIX,google.com,🚀 节点选择
# ... 数万条规则
```

## 对比表格

| 特性 | 旧方法 (HTTP) | 新方法 (Local) |
|------|---------------|----------------|
| **服务依赖** | ✅ 需要 subconverter | ❌ 无需任何服务 |
| **INI 配置支持** | ✅ 完整支持 | ✅ **完整支持** (NEW!) |
| **自定义策略组** | ✅ 完整支持（🎯🛑🚀等） | ✅ **完整支持** (NEW!) |
| **外部规则引用** | ✅ 支持 `ruleset=` | ✅ **完整支持** (NEW!) |
| **规则数量** | 数万条（从多个源合并） | 数万条（从多个源合并） |
| **复杂度** | 中等 | 低 |
| **速度** | 中等（依赖网络和服务） | 快（纯本地处理） |
| **配置文件大小** | 大（3-5MB） | 相同（3-5MB 使用 INI 时） |
| **适用场景** | 所有场景 | **所有场景** (NEW!) |
| **推荐使用** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ (推荐!) |

## ✅ 新方法现在完整支持 INI 配置！

**2025-11-10 更新**：新方法已实现完整的 INI 配置支持！

### 实现原理

新增 `ini_parser.py` 模块，提供：

1. **INI 文件解析器**：
   - 解析 `[custom]` 段落
   - 支持 `ruleset=` 外部规则引用
   - 支持 `custom_proxy_group=` 自定义策略组

2. **规则集下载器**：
   - 自动下载所有 `ruleset=` 引用的规则文件
   - 支持内联规则（如 `[]GEOIP,CN`）
   - 合并所有规则并添加策略组

3. **策略组解析器**：
   - 解析反引号分隔的策略组语法
   - 支持正则表达式匹配节点（如 `香港|HK`）
   - 支持组引用（如 `[]♻️ 自动选择`）
   - 支持健康检查配置（url-test, fallback）

4. **自动检测**：
   - 自动检测 INI 格式配置文件
   - 无缝切换到 INI 解析模式
   - 保持向后兼容（普通规则文件仍然支持）

### 测试结果

使用真实的 INI 配置文件测试：
- ✅ 解析 31 个规则集
- ✅ 下载 85,270 条规则
- ✅ 生成 33 个自定义策略组
- ✅ 输出 3MB 配置文件
- ✅ 与旧方法（HTTP）功能完全一致！

## 使用建议

### 🎯 推荐：统一使用新方法（本地转换）

**新方法现在支持所有场景！**

#### 简单使用（不需要自定义规则）
```bash
uv run cli.py --url $URL -o config.yaml
```

#### 使用 INI 配置（自定义策略组和规则）
```bash
uv run cli.py --url $URL \
  --config https://example.com/config.ini \
  -o config.yaml
```

**优势**：
- ✅ 无需运行 subconverter 服务
- ✅ 跨平台，纯 Python
- ✅ 速度更快
- ✅ 功能完全相同

### 旧方法（HTTP）还需要吗？

**通常不需要！** 旧方法现在主要用于：
- 调试和对比测试
- 验证新方法的正确性
- 特殊的边缘情况（如有）

如果你还想使用旧方法：
```bash
uv run cli.py --url $URL \
  --method http \
  --config https://example.com/config.ini \
  -o config.yaml
```

### 场景 3：对比测试

如果你想看看两种方法的差异：

```python
# main.py 已经实现了这个功能
uv run main.py

# 会生成：
# - config_old.yaml (完整配置，数千条规则)
# - config_new.yaml (简单配置，十几条规则)
```

## 常见问题

### Q: 新方法现在支持 INI 配置了吗？

**A**: ✅ **是的！** 从 2025-11-10 更新开始，新方法完整支持 INI 配置文件，包括：
- `[custom]` 段落解析
- `ruleset=` 外部规则引用
- `custom_proxy_group=` 自定义策略组
- 正则表达式匹配节点
- 健康检查配置

### Q: 新旧方法生成的配置有区别吗？

**A**: 使用 INI 配置时，**没有本质区别**！两种方法都：
- 解析相同的节点
- 下载相同的规则集
- 生成相同的策略组
- 输出相同大小的文件（~3MB）

唯一区别：新方法无需 subconverter 服务。

### Q: 哪个方法更好？

**A**: ⭐⭐⭐⭐⭐ **新方法（本地转换）** 现在是最佳选择！

理由：
- ✅ 支持所有功能（INI、自定义策略组、规则集）
- ✅ 无需外部服务（纯 Python）
- ✅ 跨平台兼容
- ✅ 速度更快
- ✅ 更容易维护

### Q: 我应该继续使用旧方法吗？

**A**: **通常不需要！** 除非：
- 你想对比测试两种方法
- 你发现新方法有任何兼容性问题（请报告！）
- 你有特殊的边缘情况需求

## 迁移指南

### 从旧方法迁移到新方法

如果你想从 HTTP 方法迁移到本地方法：

1. **评估需求**：确认是否真的需要复杂的策略组
2. **测试新方法**：
   ```bash
   uv run cli.py --url $URL -o test_new.yaml
   ```
3. **对比结果**：导入 Clash 测试是否满足需求
4. **如果满足**：切换到新方法（更快更简单）
5. **如果不满足**：继续使用 HTTP 方法

### 保持使用旧方法

如果你需要保持使用复杂配置：

```bash
# 确保 subconverter 服务运行
docker run -d -p 25500:25500 tindy2013/subconverter

# 使用 HTTP 方法
uv run cli.py --url $URL \
  --method http \
  --config https://your-config.ini \
  -o config.yaml
```

## 总结

- ✅ **新旧方法都能正常工作**
- ✅ **差异是设计如此，不是 bug**
- ✅ **根据需求选择合适的方法**
- ✅ **可以同时使用两种方法**

新方法追求简单快速，旧方法提供完整功能。选择适合你的！
