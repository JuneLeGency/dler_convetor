# 发布前检查清单

## ✅ 已完成项目

- [x] 项目结构重组为标准 Python 包
- [x] 创建 pyproject.toml 配置文件
- [x] 创建 README.md 和 LICENSE
- [x] 配置 CLI 入口点 (py-sub-conv)
- [x] 构建并测试本地安装
- [x] 清理重复文件
- [x] 整理文档到 docs/ 目录
- [x] 更新 main.py 使用新包

## 📋 发布前检查

### 1. 包完整性检查

```bash
# 检查包内容
uv run twine check dist/*

# 查看包含的文件
tar -tzf dist/py_subconverter-0.1.0.tar.gz | grep -v "/$" | head -20
```

### 2. 功能测试

```bash
# 测试 CLI 命令
uv run py-sub-conv --help

# 测试 Python 导入
uv run python -c "from py_subconverter import SubscriptionConverter, DlerAPIClient; print('✓ Import OK')"

# 运行单元测试
uv run pytest tests/ -v

# 测试完整转换流程
uv run python main.py
```

### 3. 文档检查

- [x] README.md 包含安装说明
- [x] README.md 包含使用示例
- [x] README.md 包含功能特性列表
- [x] LICENSE 文件存在
- [x] pyproject.toml 信息完整

### 4. 版本信息

- [x] pyproject.toml version: 0.1.0
- [x] py_subconverter/__init__.py __version__: 0.1.0
- [ ] 创建 git tag: v0.1.0

### 5. PyPI 元数据

检查 pyproject.toml 中的信息：
- [x] name: py-subconverter
- [x] description: 简短描述
- [x] readme: README.md
- [x] license: MIT
- [x] authors: 作者信息
- [x] keywords: 关键词列表
- [x] classifiers: 分类器
- [x] dependencies: 依赖列表
- [x] urls: 项目链接

## 🚀 发布步骤

### 步骤 1: 最终验证

```bash
# 1. 检查包
uv run twine check dist/*

# 2. 测试本地安装
uv pip install dist/py_subconverter-0.1.0-py3-none-any.whl --force-reinstall
uv run py-sub-conv --help
```

### 步骤 2: 配置 PyPI 认证

```bash
# 选项 1: 使用 .pypirc 文件（推荐）
cat > ~/.pypirc << 'PYPIRC'
[pypi]
username = __token__
password = pypi-你的token
PYPIRC

# 选项 2: 使用环境变量
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-你的token
```

### 步骤 3: 发布到 TestPyPI（可选）

```bash
# 发布到测试环境
uv run twine upload --repository testpypi dist/*

# 从测试环境安装验证
pip install --index-url https://test.pypi.org/simple/ py-subconverter
py-sub-conv --help
```

### 步骤 4: 发布到正式 PyPI

```bash
# 发布到正式 PyPI
uv run twine upload dist/*

# 等待 5-10 分钟让 PyPI 同步

# 验证安装
pip install py-subconverter
py-sub-conv --help
```

### 步骤 5: 创建 Git Tag

```bash
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

## 📊 发布后验证

### 1. PyPI 页面检查

访问 https://pypi.org/project/py-subconverter/ 检查：
- [ ] 项目描述正确显示
- [ ] README 正确渲染
- [ ] 版本号正确
- [ ] 依赖列表正确
- [ ] 下载链接可用

### 2. 安装测试

在全新环境中测试：
```bash
# 创建新虚拟环境
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# 安装包
pip install py-subconverter

# 测试 CLI
py-sub-conv --help

# 测试 Python API
python -c "from py_subconverter import SubscriptionConverter; print('✓ OK')"

# 清理
deactivate
rm -rf test_env
```

### 3. 功能验证

```bash
# 基本转换测试
py-sub-conv --url https://example.com/subscription -o test_config.yaml

# 带 INI 配置测试
py-sub-conv --url https://example.com/subscription \
  --config https://example.com/rules.ini \
  -o test_config.yaml
```

## 🔄 发布后任务

- [ ] 在 GitHub 创建 Release
- [ ] 更新 README.md 添加 PyPI badge
- [ ] 公告发布（Twitter, Reddit, etc.）
- [ ] 监控 PyPI 下载统计
- [ ] 收集用户反馈

## 📈 下一版本计划

### v0.1.1 (Bug修复)
- [ ] 修复已知问题
- [ ] 改进错误消息
- [ ] 更新文档

### v0.2.0 (新功能)
- [ ] 添加更多代理协议支持
- [ ] 性能优化
- [ ] 添加更多单元测试

### v1.0.0 (稳定版本)
- [ ] 完整的测试覆盖
- [ ] 完善的文档
- [ ] 稳定的 API

## 🆘 常见问题

### Q: 上传失败 - 包已存在
A: PyPI 不允许重复上传相同版本。需要增加版本号后重新构建。

### Q: README 渲染错误
A: 检查 README.md 格式是否符合 PyPI 的 Markdown 规范。

### Q: 依赖安装失败
A: 检查 pyproject.toml 中的依赖版本要求是否正确。

### Q: CLI 命令找不到
A: 确认 pyproject.toml 中的 scripts 配置正确，重新安装包。

## 📞 获取帮助

- GitHub Issues: https://github.com/gencylee/py-subconverter/issues
- PyPI 文档: https://packaging.python.org/
- Twine 文档: https://twine.readthedocs.io/
