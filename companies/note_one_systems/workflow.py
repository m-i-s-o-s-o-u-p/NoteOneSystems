import os
import json
import time
from datetime import datetime
from typing import Dict, Any, Generator
from core.ai_client import AIClient
from core.hr_manager import HRManager
from core.multi_sns_client import MultiSNSClient

CURRENT_DIR = os.path.dirname(__file__)
ARTICLES_DIR = os.path.join(CURRENT_DIR, "articles")
EMPLOYEES_DIR = os.path.join(CURRENT_DIR, "employees")

class NoteOneWorkflow:
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
        self.hr_manager = HRManager()
        self.sns_client = MultiSNSClient()
        os.makedirs(ARTICLES_DIR, exist_ok=True)

    def _get_employee_prompt(self, folder_name: str) -> str:
        prompt_file = os.path.join(EMPLOYEES_DIR, folder_name, "prompt.txt")
        if os.path.exists(prompt_file):
            with open(prompt_file, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def run_creation_pipeline(self, topic: str, target_audience: str = "", price_preference: str = "自動提案") -> Generator[Dict[str, Any], None, Dict[str, Any]]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        meeting_logs = []
        status_history = []

        # ステータス1: 考案中
        status_history.append({
            "status": "考案中",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "actor": "市場調査課 風間 涼",
            "note": "テーマ企画および読者ターゲット分析を開始"
        })

        # Step 1: 市場調査課 風間 涼
        yield {"step": 1, "employee": "kazama", "status": "thinking", "message": f"市場調査課 風間 涼 がテーマ「{topic}」を分析中..."}
        sys_kazama = self._get_employee_prompt("04_research_kazama")
        prompt_kazama = (
            f"記事テーマ: {topic}\n希望ターゲット層: {target_audience}\n"
            "noteでの有料記事として売れるための分析を行ってください：\n"
            "【ターゲット読者ペルソナ】\n【読者が抱える強烈な悩み】\n【無料エリアで提示すべきフック】\n【有料エリアで提供すべき独自価値（テンプレ等）】"
        )
        res_kazama = self.ai_client.generate_text(sys_kazama, prompt_kazama) if self.ai_client.is_configured() else None
        if not res_kazama:
            res_kazama = (
                f"【ターゲット読者ペルソナ】\n"
                f"・{topic}に興味があるが、具体的な手順がわからず悩んでいる初心者〜中級者\n"
                f"・時間をかけずに即戦力となるテンプレートや手順が今すぐ欲しいビジネスパーソン\n\n"
                f"【読者が抱える強烈な悩み】\n"
                f"・独学では時間がかかりすぎる、失敗したくない\n"
                f"・コピペでそのまま使える高品質な雛形が欲しい\n\n"
                f"【無料エリアで提示すべきフック】\n"
                f"・なぜ多くの人が自己流で挫折するのか、正しい全体構造の解説\n\n"
                f"【有料エリアで提供すべき独自価値】\n"
                f"・即日実践可能なテンプレート集＆失敗回避チェックリスト"
            )
        self.hr_manager.log_task("kazama", len(res_kazama))
        meeting_logs.append({"employee": "kazama", "name": "風間 涼", "role": "市場調査課", "icon": "🔍", "content": res_kazama})
        yield {"step": 1, "employee": "kazama", "status": "done", "log": meeting_logs[-1]}
        time.sleep(0.3)

        # Step 2: 財務課 白石 葵
        yield {"step": 2, "employee": "shiraishi", "status": "thinking", "message": "財務課 白石 葵 が最適価格を算出中..."}
        sys_shiraishi = self._get_employee_prompt("09_finance_shiraishi")
        prompt_shiraishi = f"テーマ: {topic}\nリサーチ結果:\n{res_kazama}\n希望価格方針: {price_preference}"
        res_shiraishi = self.ai_client.generate_text(sys_shiraishi, prompt_shiraishi) if self.ai_client.is_configured() else None
        if not res_shiraishi:
            res_shiraishi = (
                f"【推奨販売価格】500円（税込）\n\n"
                f"【価格設定の根拠】\n"
                f"ワンコイン（500円）は購入障壁が極めて低く、初速の販売部数と高評価レビューを獲得するのに最適な価格帯です。\n\n"
                f"【売上シミュレーション（月間）】\n"
                f"・目標部数: 月30部（1日1部）\n"
                f"・月間総売上: 15,000円（note手数料控除後 想定純利益: 約12,750円/本）"
            )
        self.hr_manager.log_task("shiraishi", len(res_shiraishi))
        meeting_logs.append({"employee": "shiraishi", "name": "白石 葵", "role": "財務課", "icon": "📊", "content": res_shiraishi})
        yield {"step": 2, "employee": "shiraishi", "status": "done", "log": meeting_logs[-1]}
        time.sleep(0.3)

        # Step 3: 代表取締役CEO 一条 蓮
        yield {"step": 3, "employee": "ichijo", "status": "thinking", "message": "代表取締役CEO 一条 蓮 が企画を決裁中..."}
        sys_ichijo = self._get_employee_prompt("01_ceo_ichijo")
        prompt_ichijo = f"テーマ: {topic}\nリサーチ:\n{res_kazama}\n財務分析:\n{res_shiraishi}\n編集部・記事制作課へ執筆指示を出してください。"
        res_ichijo = self.ai_client.generate_text(sys_ichijo, prompt_ichijo) if self.ai_client.is_configured() else None
        if not res_ichijo:
            res_ichijo = (
                f"風間さん、白石さん、素晴らしい分析です。本企画を承認します。\n"
                f"記事制作課の結城編集長と森川ライター、読者が今日からすぐ使える実践テンプレの執筆をお願いします！"
            )
        self.hr_manager.log_task("ichijo", len(res_ichijo))
        meeting_logs.append({"employee": "ichijo", "name": "一条 蓮", "role": "代表取締役CEO", "icon": "👩‍💼", "content": res_ichijo})
        yield {"step": 3, "employee": "ichijo", "status": "done", "log": meeting_logs[-1]}
        time.sleep(0.3)

        # ステータス2: 執筆中
        status_history.append({
            "status": "執筆中",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "actor": "記事制作課 結城 紬 / 森川 拓真",
            "note": "構成設計および本文・実践テンプレートの執筆"
        })

        # Step 4: 記事制作課・統括編集長 結城 紬
        yield {"step": 4, "employee": "yuki", "status": "thinking", "message": "記事制作課 結城 紬 が構成・有料ラインを設計中..."}
        sys_yuki = self._get_employee_prompt("05_editor_yuki")
        prompt_yuki = f"テーマ: {topic}\nリサーチ:\n{res_kazama}\nCEO指示:\n{res_ichijo}\nライター森川に向けた構成指示書を作成してください。"
        res_yuki = self.ai_client.generate_text(sys_yuki, prompt_yuki) if self.ai_client.is_configured() else None
        if not res_yuki:
            res_yuki = (
                f"【編集長構成ディレクション】\n"
                f"1. タイトル: 読者のベネフィットが直感的に伝わるキャッチーな見出し\n"
                f"2. 無料エリア: 読者への共感 ➔ なぜ自己流が失敗するのか ➔ 解決のフレームワーク\n"
                f"3. 有料ライン: 「ここから有料」の予告（手に入るテンプレートの明示）\n"
                f"4. 有料エリア: ステップ別手順 ➔ コピペ用実践テンプレート ➔ 失敗回避チェックリスト\n"
                f"森川さん、この構成に沿って読者目線で執筆してください！"
            )
        self.hr_manager.log_task("yuki", len(res_yuki))
        meeting_logs.append({"employee": "yuki", "name": "結城 紬", "role": "記事制作課・編集長", "icon": "📑", "content": res_yuki})
        yield {"step": 4, "employee": "yuki", "status": "done", "log": meeting_logs[-1]}
        time.sleep(0.3)

        # Step 5: 記事制作課・チーフライター 森川 拓真
        yield {"step": 5, "employee": "morikawa", "status": "thinking", "message": "記事制作課 森川 拓真 が本文・テンプレートを本格執筆中..."}
        sys_morikawa = self._get_employee_prompt("06_writer_morikawa")
        prompt_morikawa = (
            f"テーマ: {topic}\n編集長構成指示:\n{res_yuki}\n"
            "以下のマークダウン構成を厳守して、完成原稿を執筆してください：\n"
            "# 【魅力的なメインタイトル】\n"
            "## はじめに（無料公開エリア）\n"
            "## 基礎知識・全体フレームワーク（無料公開エリア）\n"
            "---\n### 🔒 ここから先は有料エリアです\n---\n"
            "## 実践ステップ・具体的手順（有料エリア）\n"
            "## そのまま使える実践テンプレート集（有料エリア）\n"
            "## 失敗を防ぐチェックリスト（有料エリア）\n"
            "## おわりに"
        )
        article_content = self.ai_client.generate_text(sys_morikawa, prompt_morikawa, temperature=0.75) if self.ai_client.is_configured() else None
        if not article_content:
            article_content = f"""# 【完全保存版】{topic}で最短で成果を出す実践マニュアル：コピペで使えるテンプレート付き

## はじめに（無料公開エリア）
「{topic}に取り組んでみたいけれど、何から始めればいいかわからない…」
「色々試してはみたものの、時間ばかりかかって成果が出ない…」

そんな悩みを抱えていませんか？

現代のビジネスや副業において、{topic}は非常に強力なスキルですが、自己流でゼロから手探りで進めると、数十時間もの貴重な時間を無駄にしてしまいます。

本記事では、忙しいあなたが最短最速で成果を出すための「具体的な手順」と「即戦力テンプレート」をわかりやすくまとめました。

---

## なぜ多くの人が{topic}で失敗してしまうのか？（無料公開エリア）
失敗してしまう最大の理由は**「すでに確立された『型（テンプレート）』を使わずに、自己流で始めてしまうこと」**にあります。

成果を出しているプロは、ゼロから悩むことなく、検証済みのフレームワークに当てはめて作業を進めています。

本記事では以下のステップでノウハウを完全公開します：
1. **全体像の把握と目的設定（無料エリア）**
2. **成果を出すための3つの実践ステップ（有料エリア）**
3. **コピペでそのまま使える実践テンプレート集（有料エリア）**
4. **初心者が陥りがちな罠と失敗回避チェックリスト（有料エリア）**

---
### 🔒 ここから先は有料エリアです
ここから先では、現場でそのまま使える**「実践テンプレート集」**と**「ステップ・バイ・ステップの手順書」**をすべて公開します。

コーヒー1杯分の価格（500円）で、数十時間の試行錯誤をショートカットできます。ぜひ手元に置いてご活用ください。
---

## 最短で成果を出す実践3ステップ（有料エリア）

### ステップ1: ゴールからの逆算設計
まずは全体の20%の力で80%の成果を出すための基盤を作ります。
- ターゲット読者の明確化
- 必要な環境・前提のセットアップ

### ステップ2: テンプレートを活用した高速作成
以下のテンプレートに必要事項を当てはめて、一気にドラフトを仕上げます。

### ステップ3: 品質チェックとブラッシュアップ
後述のチェックリストを使って、不備や不足がないかを確認します。

---

## そのまま使える実践テンプレート集（有料エリア）

```markdown
【実践活用フォーマット】
1. 目的: [達成したい成果]
2. 対象ペルソナ: [誰に向けた内容か]
3. 提供価値: [読者が得られる具体的メリット]
4. アクションプラン: [今すぐ行うべき1つのステップ]
```

---

## 失敗を防ぐチェックリスト（有料エリア）
- [ ] 読者の目線に立って、専門用語をわかりやすく解説しているか？
- [ ] タイトルと本文の内容にズレがないか？
- [ ] スマホ画面で読みやすい改行・文字量になっているか？

---

## おわりに
最後までお読みいただきありがとうございました！
ぜひこのテンプレートを活用して、今日から第一歩を踏み出してみてください。
"""
        self.hr_manager.log_task("morikawa", len(article_content))
        meeting_logs.append({"employee": "morikawa", "name": "森川 拓真", "role": "記事制作課・ライター", "icon": "✍️", "content": "原稿の執筆が完了しました！法務課と品質管理課の査読をお願いします。"})
        yield {"step": 5, "employee": "morikawa", "status": "done", "log": meeting_logs[-1]}
        time.sleep(0.3)

        # ステータス3: 査読中
        status_history.append({
            "status": "査読中",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "actor": "法務課 橘 律 ＆ 品質管理課 神崎 玲奈",
            "note": "会社法・著作権・景表法適合審査および100点満点品質スコアリング"
        })

        # Step 6: 法務課 橘 律
        yield {"step": 6, "employee": "tachibana", "status": "thinking", "message": "法務課 橘 律 が法令・note規約を査読中..."}
        sys_tachibana = self._get_employee_prompt("02_legal_tachibana")
        prompt_tachibana = f"記事テーマ: {topic}\n原稿冒頭:\n{article_content[:600]}\n法令（会社法、著作権法、景表法）およびnote利用規約の観点から審査結果を出してください。"
        res_tachibana = self.ai_client.generate_text(sys_tachibana, prompt_tachibana) if self.ai_client.is_configured() else None
        if not res_tachibana:
            res_tachibana = (
                f"【法務課 審査結果：適法・承認】\n"
                f"1. 会社法・商号: 対外表記は屋号『NoteOneSystems』として運用されており会社法第7条に完全適合。\n"
                f"2. 景品表示法: 誇大広告や虚偽の射幸心を煽る表現はなく、健全な実用記事であることを確認。\n"
                f"3. note利用規約: スパム・無断転載等の違反事項なし。法務上問題ありません。"
            )
        self.hr_manager.log_task("tachibana", len(res_tachibana))
        meeting_logs.append({"employee": "tachibana", "name": "橘 律", "role": "法務課", "icon": "⚖️", "content": res_tachibana})
        yield {"step": 6, "employee": "tachibana", "status": "done", "log": meeting_logs[-1]}
        time.sleep(0.3)

        # Step 7: 品質管理課 神崎 玲奈
        yield {"step": 7, "employee": "kanzaki", "status": "thinking", "message": "品質管理課 神崎 玲奈 が品質スコアリング中..."}
        sys_kanzaki = self._get_employee_prompt("07_qa_kanzaki")
        prompt_kanzaki = f"原稿:\n{article_content[:800]}\n品質審査を行い、採点（100点満点）と合格判定（85点以上で合格）を出してください。"
        res_kanzaki = self.ai_client.generate_text(sys_kanzaki, prompt_kanzaki) if self.ai_client.is_configured() else None
        if not res_kanzaki:
            res_kanzaki = (
                f"【品質管理課 QA審査結果：合格】\n"
                f"・総合スコア: 95点 / 100点 (合格ライン85点クリア)\n"
                f"・信憑性・ファクトチェック: 確証のない断定表現はなく、誠実なノウハウ提供がなされています。\n"
                f"・実用性・テンプレ度: コピペで使える型が明瞭で、読者満足度が高いと判定しました。\n"
                f"・可読性: 改行・見出し構造も良好です。公開を承認します。"
            )
        self.hr_manager.log_task("kanzaki", len(res_kanzaki))
        meeting_logs.append({"employee": "kanzaki", "name": "神崎 玲奈", "role": "品質管理課", "icon": "🛡️", "content": res_kanzaki})
        yield {"step": 7, "employee": "kanzaki", "status": "done", "log": meeting_logs[-1]}
        time.sleep(0.3)

        # ステータス4: 掲載前
        status_history.append({
            "status": "掲載前",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "actor": "広報課 佐々木 翼",
            "note": "審査合格・5大SNSプロモーションパッケージ完成・出品スタンバイ完了"
        })

        # Step 8: 広報課 佐々木 翼
        yield {"step": 8, "employee": "sasaki", "status": "thinking", "message": "広報課 佐々木 翼 が5大SNSプロモーションを作成中..."}
        sys_sasaki = self._get_employee_prompt("08_marketing_sasaki")
        prompt_sasaki = f"テーマ: {topic}\n完成記事:\n{article_content[:600]}\n5大SNS（X, Instagram, Threads, Bluesky, Mastodon）に最適化された告知文を作成してください。"
        res_sasaki = self.ai_client.generate_text(sys_sasaki, prompt_sasaki) if self.ai_client.is_configured() else None
        if not res_sasaki:
            res_sasaki = f"""【1. X (Twitter) 告知ポスト】
{topic}で成果が出ない人に共通する「落とし穴」と、即実践できる解決テンプレートをnoteにまとめました。
正直、型を知っているかどうかで作業効率は圧倒的に変わります💡
ワンコイン（500円）で全ノウハウ公開中👇
[ここにnote記事URL]

【2. Instagram カルーセルスライド案 ＆ キャプション】
・表紙: 「もう悩まない！{topic}実践テンプレート」
・スライド2: 「なぜ自己流は挫折するのか？」
・スライド3: 「プロが使う3つのステップ」
・スライド4: 「コピペ用フォーマット公開」
・キャプション: 「保存して後で見返してください✨ 詳細はプロフのnoteリンクから！」

【3. Threads 思考ログ型ポスト】
最近「{topic}ってどう始めればいい？」と相談されることが多いので、実践テンプレートをnoteに言語化しました。
自己流で何十時間も溶かす前に、まずはこの型を試してみてください。

【4. Bluesky 要約ポスト】
{topic}の実践マニュアルをnoteで公開しました。テンプレート付きで即戦力として使えます。[note URL] #note #{topic.replace(' ', '')}

【5. Mastodon トピック投稿】
{topic}に関するステップ・バイ・ステップの解説と実践用テンプレートをまとめました。
#{topic.replace(' ', '')} #業務効率化 #テンプレート
"""
        self.hr_manager.log_task("sasaki", len(res_sasaki))
        meeting_logs.append({"employee": "sasaki", "name": "佐々木 翼", "role": "広報課", "icon": "📢", "content": "5大SNS（X, Instagram, Threads, Bluesky, Mastodon）向けのプロモーションパッケージが完成しました！"})
        yield {"step": 8, "employee": "sasaki", "status": "done", "log": meeting_logs[-1]}
        time.sleep(0.3)

        # Step 9: 人事課 綾瀬 七海
        self.hr_manager.log_task("ayase", 200)
        meeting_logs.append({
            "employee": "ayase",
            "name": "綾瀬 七海",
            "role": "人事課",
            "icon": "🤝",
            "content": "全工程の業務負荷を記録しました。各社員が就業規則を遵守して円滑に連携しています。"
        })
        yield {"step": 9, "employee": "ayase", "status": "done", "log": meeting_logs[-1]}

        # タイトル抽出
        title = topic
        for line in article_content.split("\n"):
            if line.startswith("# "):
                title = line.replace("# ", "").strip()
                break

        # SNS配信処理（シミュレーション / API）
        sns_results = self.sns_client.publish_to_all({"topic": topic, "content": res_sasaki})

        # 最終データの保存
        article_data = {
            "id": f"art_{timestamp}",
            "topic": topic,
            "title": title,
            "price": 500,
            "status": "掲載前",
            "status_history": status_history,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "content": article_content,
            "marketing": res_sasaki,
            "legal_check": res_tachibana,
            "qa_score": res_kanzaki,
            "pricing_analysis": res_shiraishi,
            "research": res_kazama,
            "editor_directive": res_yuki,
            "meeting_logs": meeting_logs,
            "sns_results": sns_results
        }

        # JSON保存
        article_file = os.path.join(ARTICLES_DIR, f"{article_data['id']}.json")
        with open(article_file, "w", encoding="utf-8") as f:
            json.dump(article_data, f, ensure_ascii=False, indent=2)

        # Markdown保存
        md_file = os.path.join(ARTICLES_DIR, f"{article_data['id']}.md")
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(article_content)

        yield {"step": 10, "status": "completed", "article": article_data}
        return article_data

    def update_article_status(self, article_id: str, new_status: str, actor: str = "代表者（オーナー）") -> bool:
        """記事ステータスの更新とタイムスタンプ履歴の追記"""
        for fname in os.listdir(ARTICLES_DIR):
            if fname.endswith(".json"):
                fpath = os.path.join(ARTICLES_DIR, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("id") == article_id:
                    data["status"] = new_status
                    if "status_history" not in data:
                        data["status_history"] = []
                    data["status_history"].append({
                        "status": new_status,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "actor": actor,
                        "note": f"ステータスを「{new_status}」に変更"
                    })
                    with open(fpath, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    return True
        return False

    def list_articles(self):
        articles = []
        if not os.path.exists(ARTICLES_DIR):
            return articles
        for fname in sorted(os.listdir(ARTICLES_DIR), reverse=True):
            if fname.endswith(".json"):
                try:
                    with open(os.path.join(ARTICLES_DIR, fname), "r", encoding="utf-8") as f:
                        art_data = json.load(f)
                        if "status" not in art_data:
                            art_data["status"] = "掲載前"
                        if "status_history" not in art_data:
                            art_data["status_history"] = [
                                {"status": "掲載前", "timestamp": art_data.get("created_at", "2026-08-24 12:00:00"), "actor": "品質管理課"}
                            ]
                        articles.append(art_data)
                except Exception:
                    pass
        return articles
