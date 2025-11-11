# PyPI 发布指南

## 准备工作

### 1. 检查包内容

```bash
# 查看将要打包的文件
tar -tzf dist/py_subconverter-0.1.0.tar.gz | head -20

# 验证wheel包内容
unzip -l dist/py_subconverter-0.1.0-py3-none-any.whl
```

### 2. 测试本地安装

```bash
# 安装并测试
uv pip install dist/py_subconverter-0.1.0-py3-none-any.whl --force-reinstall
uv run py-sub-conv --help

# 运行单元测试
uv run pytest tests/
```

## 发布到 PyPI

### 方式 1: 使用 twine (推荐)

```bash
# 1. 配置 PyPI 认证
# 创建 ~/.pypirc 文件:
cat > ~/.pypirc << 'PYPIRC'
[pypi]
username = __token__
password = pypi-你的token
PYPIRC

# 2. 检查包是否符合PyPI规范
uv run twine check dist/*

# 3. 先发布到 TestPyPI (可选，用于测试)
uv run twine upload --repository testpypi dist/*

# 4. 从 TestPyPI 测试安装
pip install --index-url https://test.pypi.org/simple/ py-subconverter

# 5. 发布到正式 PyPI
uv run twine upload dist/*
```

### 方式 2: 使用 uv publish

```bash
# 配置 PyPI token
export TWINE_PASSWORD=pypi-你的token

# 直接发布
uv publish
```

## 发布后验证

```bash
# 等待几分钟让PyPI同步

# 在新环境中安装测试
python -m venv test_env
source test_env/bin/activate
pip install py-subconverter

# 测试CLI命令
py-sub-conv --help

# 测试Python导入
python -c "from py_subconverter import SubscriptionConverter; print('OK')"
```

## 版本管理

### 更新版本号

1. 编辑 `pyproject.toml`:
   ```toml
   version = "0.1.1"  # 更新版本号
   ```

2. 编辑 `py_subconverter/__init__.py`:
   ```python
   __version__ = "0.1.1"
   ```

3. 创建 git tag:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```

4. 重新构建并发布:
   ```bash
   rm -rf dist build
   uv run python -m build
   uv run twine upload dist/*
   ```

## 版本号规范 (Semantic Versioning)

- **0.1.0** - 初始版本
- **0.1.1** - Bug修复
- **0.2.0** - 新功能
- **1.0.0** - 稳定版本

## 常见问题

### 1. 上传失败：包已存在

PyPI 不允许重复上传相同版本，需要更新版本号。

### 2. 认证失败

检查 PyPI token 是否正确，token 应该以 `pypi-` 开头。

### 3. 包描述渲染错误

检查 README.md 格式是否符合 PyPI 的 Markdown 规范。

## PyPI 项目页面

发布后可以在以下地址查看:
- 项目主页: https://pypi.org/project/py-subconverter/
- 下载统计: https://pypistats.org/packages/py-subconverter

## 更新 README.md 中的链接

发布后记得更新 README.md 中的 GitHub 链接为实际的仓库地址。
