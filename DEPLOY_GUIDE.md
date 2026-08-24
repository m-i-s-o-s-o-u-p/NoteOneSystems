# ☁️ 24時間無料クラウドへの公開マニュアル（完全図解）

Macの電源を切っても、スマホや他のPCからいつでもAI会社にアクセスできるようにするための設定手順です。
**すべてのツールが完全無料（0円）**で利用できます。

---

## 準備するもの（すべて無料）
1. **GitHub アカウント**: [https://github.com/](https://github.com/) （無料）
2. **Streamlit Cloud アカウント**: [https://share.streamlit.io/](https://share.streamlit.io/) （無料・GitHubと連携）
3. **Google Gemini API Key**: [https://aistudio.google.com/](https://aistudio.google.com/) （無料枠）

---

## 🛠️ 3ステップ設定手順

### ステップ 1: GitHubにプログラムを保存する
1. [GitHub](https://github.com/) にログインし、画面右上の「+」ボタンから **「New repository」** をクリックします。
2. 設定項目：
   - **Repository name**: `ai-holdings-platform` （お好きな名前でOK）
   - **Public / Private**: `Private`（非公開）を選択（※あなただけが見られる安全な設定です）
   - 「Create repository」ボタンをクリックします。
3. このフォルダ内のファイルをアップロードまたはGit Pushします。

### ステップ 2: Streamlit Community Cloudでアプリを公開する
1. [Streamlit Community Cloud](https://share.streamlit.io/) にアクセスし、**「Sign in with GitHub」** を選択します。
2. ログイン後、**「Create app」** ボタンをクリックします。
3. 設定項目：
   - **Repository**: 先ほど作成した `ai-holdings-platform` を選択
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: （自動設定されます。お好きなサブドメインに変更も可能）
4. **「Deploy!」** ボタンをクリックします。
   - 数十秒で自動的にビルドが完了し、あなた専用のWebオフィスが開きます！

### ステップ 3: 無料のGemini APIキーを登録する
1. Streamlit Cloudのアプリ画面右下にある **「Settings」**（または画面右上のメニュー「App settings」）を開きます。
2. 左メニューの **「Secrets」** を選択します。
3. 以下の枠の中に、Google AI Studioで取得したAPIキーを貼り付けて保存します：
   ```toml
   GEMINI_API_KEY = "AIzaSy..."
   ```
4. これで完了です！

---

## 📱 スマホやタブレットからの利用方法
発行されたURL（例: `https://your-name-ai-holdings.streamlit.app`）をスマホのブラウザでお気に入りに登録すれば、
**通勤中や外出先でもワンタップでAI社員たちに記事作成を指示し、完成した記事をnoteに投稿**できます。
