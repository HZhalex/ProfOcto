#!/bin/bash
set -e

echo ""
echo "=== Academic Debate Arena — Setup ==="
echo ""

echo "[1/3] Tạo virtual environment..."
python3 -m venv .venv

echo "[2/3] Cài dependencies..."
.venv/bin/pip install --upgrade pip -q
.venv/bin/pip install -r requirements.txt -q

if [ ! -f .env ]; then
    echo "[3/3] Tạo file .env mẫu..."
    cp .env.example .env
    echo ""
    echo ">>> Mở file .env và điền GEMINI_API_KEY của bạn vào <<<"
else
    echo "[3/3] File .env đã tồn tại, bỏ qua."
fi

echo ""
echo "=== Setup xong! ==="
echo ""
echo "Bước tiếp theo:"
echo "  1. Điền API key vào file .env"
echo "  2. source .venv/bin/activate"
echo "  3. python main.py"
echo ""
~