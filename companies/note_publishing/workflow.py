import os
import json
import time
from datetime import datetime
from typing import Dict, Any, Generator
from core.ai_client import AIClient

CURRENT_DIR = os.path.dirname(__file__)
ARTICLES_DIR = os.path.join(CURRENT_DIR, "articles")
MEETINGS_DIR = os.path.join(CURRENT_DIR, "meetings")

class NotePublishingWorkflow:
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
        os.makedirs(ARTICLES_DIR, exist_ok=True)
        os.makedirs(MEETINGS_DIR, exist_ok=True)

    def run_creation_pipeline(self, topic: str, target_audience: str = "", price_preference: str = "自動提案") -> Generator[Dict[str, Any], None, Dict[str, Any]]:
        """
        AI社員たちが協力してnote有料記事を企画・会議・執筆・マーケティングするパイプライン。
        Generatorとして各ステップの進行状況と社員の発言をリアルタイムに返す。
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        meeting_logs = []

        # ==========================================
        # Step 1: リサーチ担当 風間 涼 の分析
        # ==========================================
        yield {"step": 1, "employee": "kazama", "status": "thinking", "message": f"テーマ「{topic}」の市場ニーズ・読者ターゲットを調査中..."}
        
        sys_kazama = (
            "あなたはNotePub AI株式会社のリサーチ担当『風間 涼』です。"
            "noteでの売れ筋トレンド、競合記事、読者の深い悩みを論理的に分析します。"
            "以下のフォーマットで簡潔かつ具体的に回答してください：\n"
            "【ターゲット読者ペルソナ】\n"
            "【読者が抱える強烈な悩み・願望】\n"
            "【無料エリアで提示すべきフック】\n"
            "【有料エリアで提供すべき独自価値（テンプレ・実践ノウハウ等）】"
        )
        prompt_kazama = f"記事テーマ: {topic}\n希望ターゲット層（あれば）: {target_audience}\nこのテーマでnote有料記事として売れるための分析を行ってください。"
        
        res_kazama = self.ai_client.generate_text(sys_kazama, prompt_kazama) if self.ai_client.is_configured() else None
        if not res_kazama:
            res_kazama = (
                f"【ターゲット読者ペルソナ】\n"
                f"・{topic}に関心はあるが、何から手をつけて良いか迷っている初心者〜中級者\n"
                f"・時間をかけずにすぐ結果・テンプレが欲しい忙しい社会人・クリエイター\n\n"
                f"【読者が抱える強烈な悩み・願望】\n"
                f"・独学だと時間がかかりすぎる、失敗したくない\n"
                f"・実務でそのまま使える具体的なフォーマットや手順書が今すぐ欲しい\n\n"
                f"【無料エリアで提示すべきフック】\n"
                f"・「なぜ多くの人が{topic}で挫折するのか」の理由と、解決の全体像（3ステップ）\n\n"
                f"【有料エリアで提供すべき独自価値】\n"
                f"・コピペで即使える実践テンプレート集＆失敗回避チェックリスト"
            )
        
        meeting_logs.append({
            "employee": "kazama",
            "name": "風間 涼",
            "role": "リサーチ担当",
            "icon": "🔍",
            "content": res_kazama
        })
        yield {"step": 1, "employee": "kazama", "status": "done", "log": meeting_logs[-1]}
        time.sleep(0.5)

        # ==========================================
        # Step 2: 財務アナリスト 白石 葵 の価格提案
        # ==========================================
        yield {"step": 2, "employee": "shiraishi", "status": "thinking", "message": "最適販売価格と売上シミュレーションを算出中..."}
        
        sys_shiraishi = (
            "あなたはNotePub AI株式会社の財務・プライシングアナリスト『白石 葵』です。"
            "提供価値とnote購入者の心理的ハードル（300円/500円/980円/1480円）を考慮し、最適な販売価格と売上予想を算出します。"
            "以下のフォーマットで回答してください：\n"
            "【推奨販売価格】〇〇円（税込）\n"
            "【価格設定の根拠】\n"
            "【売上シミュレーション（月間想定）】"
        )
        prompt_shiraishi = f"テーマ: {topic}\nリサーチ結果:\n{res_kazama}\n希望価格方針: {price_preference}"
        
        res_shiraishi = self.ai_client.generate_text(sys_shiraishi, prompt_shiraishi) if self.ai_client.is_configured() else None
        if not res_shiraishi:
            res_shiraishi = (
                f"【推奨販売価格】500円（税込）\n\n"
                f"【価格設定の根拠】\n"
                f"ワンコイン（500円）は『ランチ1回分未満で時短と成果が手に入る』ため最も成約率が高く、初速の売上と高評価レビューを集めやすいベストな価格帯です。\n\n"
                f"【売上シミュレーション（月間想定）】\n"
                f"・販売目標: 月30部（1日1部ペース）\n"
                f"・月間総売上: 15,000円\n"
                f"・note手数料控除後の想定利益: 約12,750円 / 本"
            )
        
        meeting_logs.append({
            "employee": "shiraishi",
            "name": "白石 葵",
            "role": "財務アナリスト",
            "icon": "📊",
            "content": res_shiraishi
        })
        yield {"step": 2, "employee": "shiraishi", "status": "done", "log": meeting_logs[-1]}
        time.sleep(0.5)

        # ==========================================
        # Step 3: CEO 一条 蓮 の企画承認
        # ==========================================
        yield {"step": 3, "employee": "ichijo", "status": "thinking", "message": "企画の最終レビューと執筆方針を決定中..."}
        
        sys_ichijo = (
            "あなたはNotePub AI株式会社のCEO『一条 蓮』です。"
            "風間と白石の提案を総括し、ライターの結城に向けて『読者満足度を最大化するための執筆指示』を簡潔に下してください。"
        )
        prompt_ichijo = f"テーマ: {topic}\nリサーチ:\n{res_kazama}\n財務分析:\n{res_shiraishi}"
        
        res_ichijo = self.ai_client.generate_text(sys_ichijo, prompt_ichijo) if self.ai_client.is_configured() else None
        if not res_ichijo:
            res_ichijo = (
                f"風間さん、白石さん、分析ありがとうございます。素晴らしい切り口ですね。\n"
                f"結城編集長、本企画を正式承認します！価格は500円を想定し、無料部分では読者の悩みに深く寄り添い、"
                f"有料部分では『これさえ見れば今すぐ実践できる具体的な型・テンプレ』を徹底的に分かりやすく執筆してください。よろしくお願いします！"
            )
        
        meeting_logs.append({
            "employee": "ichijo",
            "name": "一条 蓮",
            "role": "CEO / 統括リーダー",
            "icon": "👩‍💼",
            "content": res_ichijo
        })
        yield {"step": 3, "employee": "ichijo", "status": "done", "log": meeting_logs[-1]}
        time.sleep(0.5)

        # ==========================================
        # Step 4: 編集長 結城 紬 の記事執筆
        # ==========================================
        yield {"step": 4, "employee": "yuki", "status": "thinking", "message": "記事の無料エリア・有料エリア・タイトルを本格執筆中..."}
        
        sys_yuki = (
            "あなたはNotePub AI株式会社の編集長兼チーフライター『結城 紬』です。"
            "noteで高評価を獲得し、売れ続けるための本格的な有料記事を執筆します。"
            "マークダウン形式で以下の構成を必ず厳守して書いてください：\n"
            "# 【魅力的なメインタイトル】\n"
            "（読者が思わずクリックしたくなるキャッチーなタイトル）\n\n"
            "## はじめに（無料公開エリア）\n"
            "（読者の現状の悩みへの共感、なぜこの記事が必要なのか、この記事で学べる全体像）\n\n"
            "## 基礎知識・全体フレームワーク（無料公開エリア）\n"
            "（無料部分だけでも十分に有益だと感じられるロジック）\n\n"
            "---\n"
            "### 🔒 ここから先は有料エリアです\n"
            "（有料部分で手に入る具体的な価値の予告）\n"
            "---\n\n"
            "## 実践ステップ・具体的手順（有料エリア）\n"
            "（読者が迷わず行動できるステップ・バイ・ステップの解説）\n\n"
            "## そのまま使えるテンプレート＆チェックリスト（有料エリア）\n"
            "（コピペで使えるプロンプト、文章雛形、チェック表など）\n\n"
            "## よくある失敗と回避策・プロのコツ（有料エリア）\n"
            "\n"
            "## おわりに（有料エリア）"
        )
        prompt_yuki = f"テーマ: {topic}\nCEOの指示: {res_ichijo}\nリサーチ情報: {res_kazama}\n上記に基づき、3000文字相当の完成原稿を執筆してください。"
        
        article_content = self.ai_client.generate_text(sys_yuki, prompt_yuki, temperature=0.8) if self.ai_client.is_configured() else None
        if not article_content:
            article_content = f"""# 【完全保存版】{topic}で圧倒的に差をつける実践マニュアル：今日から使えるテンプレ付き

## はじめに（無料公開エリア）
「{topic}に興味はあるけれど、何から手をつければいいかわからない…」
「色々調べて試してみたものの、いまいち成果に繋がらない…」

そんな悩みを抱えていませんか？

現代において、{topic}は非常に注目を集めていますが、正しい順序と実践的な型を知らずに独学で挑戦すると、膨大な時間を浪費してしまうことになります。

この記事では、忙しいあなたが最短最速で成果を出すための「具体的な手順」と「即戦力テンプレート」を余すところなくまとめました。

---

## なぜ多くの人が{topic}でつまずいてしまうのか？（無料公開エリア）
つまずいてしまう最大の理由は**「最初から完璧を目指し、自己流で始めてしまうから」**です。

成功している人は、例外なく「すでに検証された型（テンプレート）」をベースにしています。
ゼロから悩む時間をなくし、型に沿って進めるだけで、誰でも同じクオリティのアウトプットが出せるようになります。

本記事の構成は以下の通りです：
1. **全体像の把握（無料エリア）**
2. **最短で成果を出す3つのステップ（有料エリア）**
3. **コピペでそのまま使える実践テンプレート集（有料エリア）**
4. **失敗を防ぐチェックリスト（有料エリア）**

---
### 🔒 ここから先は有料エリアです
ここから先では、実際に現場で使われている**「実践テンプレート集」**と**「具体的なステップ・バイ・ステップの手順」**をすべて公開します。

コーヒー1杯分の価格（500円）で、数十時間の試行錯誤をショートカットできます。ぜひ手元に置いてご活用ください。
---

## 最短で成果を出す実践3ステップ（有料エリア）

### ステップ1: ゴールから逆算したセットアップ
まずは最初の20%の力で80%の成果を出すための基盤を整えます。
- 目的の明確化（誰に何を届けるか）
- 最低限必要なツールの準備

### ステップ2: テンプレートを活用した高速実行
自己流を捨て、以下のフォーマットに当てはめて作成します。

### ステップ3: 検証と改善サイクルの確立
一度作って終わりにせず、読者の反応やデータを見ながら微調整を行います。

---

## そのまま使える実践テンプレート集（有料エリア）

```markdown
【コピペ用フォーマット】
1. ターゲット: [具体的な対象者]
2. 課題: [解決したい問題]
3. 提示する解決策: [3行で要約]
4. 行動への誘導: [今すぐ行うべき1つのアクション]
```

---

## 失敗を防ぐチェックリスト（有料エリア）
- [ ] 読者の目線で専門用語を噛み砕いているか？
- [ ] タイトルと本文の内容に乖離がないか？
- [ ] スマホ画面で読みやすい改行・文字量になっているか？

---

## おわりに
ここまでお読みいただきありがとうございました！
このテンプレートを早速ご自身の作業に当てはめて、一歩を踏み出してみてください。
"""
        
        meeting_logs.append({
            "employee": "yuki",
            "name": "結城 紬",
            "role": "編集長 / ライター",
            "icon": "✍️",
            "content": "記事の執筆が完了しました！読者がすぐに行動に移せるよう、無料・有料の境界線とテンプレートを精緻に仕上げています。"
        })
        yield {"step": 4, "employee": "yuki", "status": "done", "log": meeting_logs[-1]}
        time.sleep(0.5)

        # ==========================================
        # Step 5: マーケター 佐々木 翼 のSNS・導線設計
        # ==========================================
        yield {"step": 5, "employee": "sasaki", "status": "thinking", "message": "X（Twitter）用告知ポストとnote用アイキャッチ案を作成中..."}
        
        sys_sasaki = (
            "あなたはNotePub AI株式会社のマーケター『佐々木 翼』です。"
            "完成したnote有料記事をSNS（X/Twitter）で拡散・集客するための投稿文（3パターン）とアイキャッチのコピー案を作成してください。"
            "以下のフォーマットで出力してください：\n"
            "【アイキャッチ画像コピー案】\n"
            "【X告知ポスト 案1（ノウハウ要約型）】\n"
            "【X告知ポスト 案2（共感・悩み訴求型）】\n"
            "【X告知ポスト 案3（特典・テンプレ強調型）】\n"
            "【おすすめハッシュタグ】"
        )
        prompt_sasaki = f"テーマ: {topic}\n完成記事冒頭:\n{article_content[:500]}"
        
        res_sasaki = self.ai_client.generate_text(sys_sasaki, prompt_sasaki) if self.ai_client.is_configured() else None
        if not res_sasaki:
            res_sasaki = f"""【アイキャッチ画像コピー案】
「もう悩まない！{topic}の黄金テンプレート」
「独学で挫折した人へ。今すぐ使える実践マニュアル」

【X告知ポスト 案1（ノウハウ要約型）】
{topic}で成果が出ない人に共通する「3つの落とし穴」をまとめました。
正直、型を知っているかどうかだけで作業効率は10倍変わります。
忙しい人向けにコピペで使えるテンプレ付きでnoteに全ノウハウを公開しました👇
[ここにnote記事のURL]

【X告知ポスト 案2（共感・悩み訴求型）】
「{topic}って難しそう…」と思っていた過去の自分に向けて書きました。
自己流で何十時間も溶かす前に、この手順だけ押さえておけばOKです。ワンコインで手に入る時短パックです💡
[ここにnote記事のURL]

【X告知ポスト 案3（特典・テンプレ強調型）】
{topic}の実践テンプレートをnoteで配布開始しました！
読んだその日からそのまま使えるチェックリスト付き。
限定価格500円で公開中なので、必要な方はお早めにどうぞ✨
[ここにnote記事のURL]

【おすすめハッシュタグ】
#{topic.replace(' ', '')} #業務効率化 #note販売 #副業初心者 #テンプレート
"""
        
        meeting_logs.append({
            "employee": "sasaki",
            "name": "佐々木 翼",
            "role": "マーケティング担当",
            "icon": "📢",
            "content": "noteの告知用SNSポスト（3パターン）とアイキャッチコピーを作成しました！公開と同時にXに投稿すれば初速の流入を作れます。"
        })
        yield {"step": 5, "employee": "sasaki", "status": "done", "log": meeting_logs[-1]}

        # タイトル抽出
        title = topic
        for line in article_content.split("\n"):
            if line.startswith("# "):
                title = line.replace("# ", "").strip()
                break

        # 最終データの保存
        article_data = {
            "id": f"art_{timestamp}",
            "topic": topic,
            "title": title,
            "price": 500,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "content": article_content,
            "marketing": res_sasaki,
            "pricing_analysis": res_shiraishi,
            "research": res_kazama,
            "meeting_logs": meeting_logs
        }

        # JSON保存
        article_file = os.path.join(ARTICLES_DIR, f"{article_data['id']}.json")
        with open(article_file, "w", encoding="utf-8") as f:
            json.dump(article_data, f, ensure_ascii=False, indent=2)

        # Markdown保存
        md_file = os.path.join(ARTICLES_DIR, f"{article_data['id']}.md")
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(article_content)

        yield {"step": 6, "status": "completed", "article": article_data}
        return article_data

    def list_articles(self):
        articles = []
        if not os.path.exists(ARTICLES_DIR):
            return articles
        for fname in sorted(os.listdir(ARTICLES_DIR), reverse=True):
            if fname.endswith(".json"):
                try:
                    with open(os.path.join(ARTICLES_DIR, fname), "r", encoding="utf-8") as f:
                        articles.append(json.load(f))
                except Exception:
                    pass
        return articles
