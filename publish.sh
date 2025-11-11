#!/bin/bash
# PyPI 发布脚本

set -e

echo "========================================="
echo "py-subconverter 发布脚本"
echo "========================================="
echo

# 检查是否在正确的目录
if [ ! -f "pyproject.toml" ]; then
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
fi

# 1. 清理旧的构建
echo "1. 清理旧的构建文件..."
rm -rf dist/ build/ *.egg-info/
echo "   ✓ 清理完成"
echo

# 2. 构建包
echo "2. 构建包..."
uv run python -m build
echo "   ✓ 构建完成"
echo

# 3. 检查包
echo "3. 检查包完整性..."
uv run twine check dist/*
echo "   ✓ 检查通过"
echo

# 4. 测试本地安装
echo "4. 测试本地安装..."
uv pip install dist/*.whl --force-reinstall > /dev/null 2>&1
uv run py-sub-conv --help > /dev/null 2>&1
echo "   ✓ 本地安装测试通过"
echo

# 5. 询问发布目标
echo "选择发布目标:"
echo "  1) TestPyPI (测试环境)"
echo "  2) PyPI (正式环境)"
echo "  3) 取消"
read -p "请选择 [1-3]: " choice

case $choice in
    1)
        echo
        echo "发布到 TestPyPI..."
        uv run twine upload --repository testpypi dist/*
        echo
        echo "✓ 发布到 TestPyPI 完成！"
        echo
        echo "测试安装:"
        echo "  pip install --index-url https://test.pypi.org/simple/ py-subconverter"
        ;;
    2)
        echo
        echo "⚠️  即将发布到正式 PyPI！"
        read -p "确认继续？ [y/N]: " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            echo
            echo "发布到 PyPI..."
            uv run twine upload dist/*
            echo
            echo "✓ 发布到 PyPI 完成！"
            echo
            echo "安装命令:"
            echo "  pip install py-subconverter"
            echo
            echo "项目页面:"
            echo "  https://pypi.org/project/py-subconverter/"
        else
            echo "取消发布"
            exit 0
        fi
        ;;
    3)
        echo "取消发布"
        exit 0
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac

echo
echo "========================================="
echo "发布完成！"
echo "========================================="
