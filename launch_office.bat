@echo off
chcp 65001 >nul
title NoteOneSystems - AI Virtual Holdings
cd /d "%~dp0"

echo ==================================================
echo   NoteOneSystems バーチャルオフィスを起動中...
echo ==================================================
echo.
echo ブラウザでオフィス画面 (http://localhost:8501) が開きます。
echo アプリを終了するときは、このウィンドウを閉じるか Ctrl+C を押してください。
echo.

:: ブラウザをバックグラウンドで準備
start "" "http://localhost:8501"

:: Streamlit サーバー起動
".venv\Scripts\streamlit.exe" run app.py --server.headless=true

pause
