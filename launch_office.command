#!/bin/bash

# NoteOneSystems バーチャルオフィス起動ランチャー
cd "/Users/mbp-m1-2020/.gemini/antigravity/scratch/ai_holdings_platform"

echo "=================================================="
echo "🏢 NoteOneSystems バーチャルオフィスを起動しています..."
echo "=================================================="

# 2秒後に自動でGoogle Chromeで開く（起動済みなら新規タブで開く）
(sleep 2 && open -a "Google Chrome" "http://localhost:8501") &

# Streamlitダッシュボードを起動
python3 -m streamlit run app.py --server.headless=true
