#!/bin/bash
# 时空胶囊 - 快速启动脚本

cd "$(dirname "$0")"

echo "================================================"
echo "🚀 时空胶囊 - 启动脚本"
echo "================================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python"
    exit 1
fi

# 检查依赖
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 正在安装依赖..."
    pip3 install -r requirements.txt
fi

# 启动服务
echo ""
echo "🚀 正在启动服务..."
echo ""
python3 app.py
