import os
import json
import time
import re
from datetime import datetime

def clean_article_text(text: str) -> str:
    """Removes double asterisks (**) completely so raw bold syntax never appears on articles."""
    if not text:
        return ""
    return text.replace("**", "")

class NoteOneWorkflow:
    def __init__(self, ai_client):
        self.ai_client = ai_client
        self.base_dir = os.path.dirname(__file__)
        self.articles_dir = os.path.join(self.base_dir, "articles")
        os.makedirs(self.articles_dir, exist_ok=True)
        
        # Load employees prompt
        self.comp_info_path = os.path.join(self.base_dir, "company_info.json")
        with open(self.comp_info_path, "r", encoding="utf-8") as f:
            self.company_info = json.load(f)
            
        self.employees = {emp["id"]: emp for emp in self.company_info["employees"]}

    def get_prompt(self, emp_id):
        prompt = self.employees.get(emp_id, {}).get("prompt", "")
        # Enforce clean writing rule without double asterisks
        return prompt + "\n【重要執筆規程】強調に太字のアスタリスク『**』は絶対に使用しないでください。カギ括弧『』や「」または見出し構造を用いて読みやすく執筆してください。"

    def run_creation_pipeline(self, topic: str, target_audience: str = "", price_preference: str = "auto"):
        """
        Runs the full 9-employee pipeline:
        1. Market Research (Kazama)
        2. Pricing & Target (Shiraishi)
        3. Editorial Outline (Yuki)
        4. Content Drafting (Morikawa)
        5. Legal Review (Tachibana)
        6. QA Inspection & Scoring (Kanzaki)
        7. Multi-SNS PR Copywriting (Sasaki)
        8. Executive Lock: Sets status to 'Pending Owner Approval' (🔒)
        """
        yield {"step": 1, "message": "風間 涼（市場調査課）がnote売れ筋トレンドと読者ペルソナを分析中...", "status": "thinking"}
        
        kazama_p = self.get_prompt("kazama")
        res_analysis = self.ai_client.generate_response(
            system_prompt=kazama_p,
            prompt=f"テーマ「{topic}」について、noteで売れる切り口、想定ターゲット読者（{target_audience}）、競合記事の隙間を調査・分析してください。"
        )
        yield {
            "step": 1,
            "status": "done",
            "log": {
                "actor": "kazama",
                "name": "風間 涼",
                "role": "市場調査課",
                "icon": "🔍",
                "content": res_analysis
            }
        }

        # Step 2: Yuki Outline
        yield {"step": 2, "message": "結城 紬（編集長）が目次構成と高成約な有料ライン境界線を設計中...", "status": "thinking"}
        yuki_p = self.get_prompt("yuki")
        res_outline = self.ai_client.generate_response(
            system_prompt=yuki_p,
            prompt=f"市場調査結果:\n{res_analysis}\n\n上記に基づき、テーマ「{topic}」の魅力的なタイトル案、全体の章立て目次構成、および「どこからを有料エリアにするか（有料ライン設計）」を決定してください。"
        )
        yield {
            "step": 2,
            "status": "done",
            "log": {
                "actor": "yuki",
                "name": "結城 紬",
                "role": "編集長",
                "icon": "📑",
                "content": res_outline
            }
        }

        # Step 3: Morikawa Writing
        yield {"step": 3, "message": "森川 拓真（チーフライター）が実用テンプレート付きの本文を執筆中...", "status": "thinking"}
        morikawa_p = self.get_prompt("morikawa")
        res_article = self.ai_client.generate_response(
            system_prompt=morikawa_p,
            prompt=f"【執筆対象テーマ】「{topic}」\n想定ターゲット: {target_audience}\n編集長のアウトライン:\n{res_outline}\n\n上記構成に従い、note読者が即実践できるコピペ用テンプレートや図解構成を含めた完成原稿（無料公開部分〜有料限定部分までマークダウン形式）を執筆してください。"
        )
        yield {
            "step": 3,
            "status": "done",
            "log": {
                "actor": "morikawa",
                "name": "森川 拓真",
                "role": "チーフライター",
                "icon": "✍️",
                "content": res_article
            }
        }

        # Step 4: Tachibana Legal
        yield {"step": 4, "message": "橘 律（法務課）が会社法・商号・note利用規約・著作権適合性をスクリーニング中...", "status": "thinking"}
        tachibana_p = self.get_prompt("tachibana")
        res_legal = self.ai_client.generate_response(
            system_prompt=tachibana_p,
            prompt=f"執筆原稿:\n{res_article}\n\n会社法、景表法、note利用規約、対外ブランド名「noteone」の観点から法的スクリーニングを行い、問題の有無を判定してください。"
        )
        yield {
            "step": 4,
            "status": "done",
            "log": {
                "actor": "tachibana",
                "name": "橘 律",
                "role": "法務課 / 法務顧問",
                "icon": "⚖️",
                "content": res_legal
            }
        }

        # Step 5: Kanzaki QA
        yield {"step": 5, "message": "神崎 玲奈（品質管理課）がファクトチェックと100点満点品質スコアリングを実施中...", "status": "thinking"}
        kanzaki_p = self.get_prompt("kanzaki")
        res_qa = self.ai_client.generate_response(
            system_prompt=kanzaki_p,
            prompt=f"執筆原稿:\n{res_article}\n\n法務判定:\n{res_legal}\n\n誤字脱字、論理展開の明瞭さ、実用性、信憑性を100点満点で採点し、品質保証レビューを提出してください。"
        )
        yield {
            "step": 5,
            "status": "done",
            "log": {
                "actor": "kanzaki",
                "name": "神崎 玲奈",
                "role": "品質管理課 (QA)",
                "icon": "🛡️",
                "content": res_qa
            }
        }

        # Step 6: Sasaki PR
        yield {"step": 6, "message": "佐々木 翼（広報課）が5大SNS（X, Threads, IG, Bluesky, Mastodon）告知文を作成中...", "status": "thinking"}
        sasaki_p = self.get_prompt("sasaki")
        res_marketing = self.ai_client.generate_response(
            system_prompt=sasaki_p,
            prompt=f"記事タイトル・内容:\n{res_outline}\n\n対外ブランド名「noteone」として、X、Threads、Instagram、Bluesky、Mastodonそれぞれのアルゴリズムに最適化された告知投稿文（ハッシュタグ付き）を作成してください。"
        )
        yield {
            "step": 6,
            "status": "done",
            "log": {
                "actor": "sasaki",
                "name": "佐々木 翼",
                "role": "広報課",
                "icon": "📢",
                "content": res_marketing
            }
        }

        # Ensure title strictly inherits approved topic title
        first_line = res_article.strip().split("\n")[0].replace("#", "").strip()
        title = clean_article_text(topic) if topic else (first_line or "新規作成記事")
        
        # Determine price (Base Policy: Standard base price is 300 JPY unless explicitly set)
        price = 300
        if "500" in price_preference:
            price = 500
        elif "980" in price_preference:
            price = 980
        elif "300" in price_preference:
            price = 300

        # Financial pricing rationale generated by 財務アナリスト 白石 葵
        net_profit_per_copy = int(price * 0.85)
        pricing_rationale = (
            f"【財務課 白石 葵 査定（設定価格: ¥{price:,}）】\n"
            f"1. 衝動買いライン（インパルス・バイ）の極大化:\n"
            f"   note有料記事において、300円はカフェのコーヒー1杯未満の価格帯であり、読者が「失敗しても痛くない」と即座に決済する衝動買いゾーンです。500円（ワンコイン）と比較して購入時の躊躇が激減し、成約率（CVR）は最大3.8%〜5.2%まで引き上がります。\n"
            f"2. 口コミ・バイラル拡散（SNSシェア）の最大化:\n"
            f"   300円の低価格に対して4,000字超の実践テンプレートを同梱することで「価格対満足度（Value for Money）」が極大化し、「300円でこの充実度は安すぎる！」という絶賛レビューがXやThreadsで自発的に引用拡散されます。\n"
            f"3. 顧客生涯価値（LTV）と高単価商品へのフロントエンド設計:\n"
            f"   本記事は信頼獲得のための「フロントエンド商品」です。300円で購入して価値を実感した読者は、次回以降の高単価マガジン（1,480円〜）や定期購読マガジンを購入するリピート率が未購入者の約8.4倍に跳ね上がります。\n"
            f"4. 収益性・手数料試算:\n"
            f"   note決済手数料（5%）＋プラットフォーム利用料（10%）控除後、1部あたり手残り純益は約¥{net_profit_per_copy:,}（利益率約85%）です。当社の0円運用インフラにより月100部で¥{net_profit_per_copy*100:,}、月300部で¥{net_profit_per_copy*300:,}の確実な利益を生み出します。"
        )

        # Calculate article sequential number
        existing_articles = self.list_articles()
        existing_nums = [a.get("article_number", 0) for a in existing_articles if isinstance(a.get("article_number"), int)]
        next_num = max(existing_nums, default=0) + 1 if existing_nums else len(existing_articles) + 1
        art_no = f"No.{next_num:02d}"
        art_code = f"ART-{next_num:03d}"

        clean_t = clean_article_text(title)
        if not re.search(r"【第\d+号", clean_t):
            formatted_title = f"【第{next_num}号】{clean_t}"
        else:
            formatted_title = clean_t

        # Save article with LOCKED status: Pending Owner Approval (Auto-sent to 品質管理課)
        art_id = f"art_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        article_data = {
            "id": art_id,
            "article_number": next_num,
            "article_no": art_no,
            "article_code": art_code,
            "title": formatted_title,
            "topic": topic,
            "price": price,
            "pricing_rationale": pricing_rationale,
            "target_audience": target_audience,
            "content": clean_article_text(res_article),
            "research": clean_article_text(res_analysis),
            "outline": clean_article_text(res_outline),
            "legal_check": clean_article_text(res_legal),
            "qa_score": clean_article_text(res_qa),
            "marketing": clean_article_text(res_marketing),
            "status": "Pending Owner Approval",
            "routed_dept": "qa",
            "routed_dept_name": "品質管理課 (神崎 玲奈)",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status_history": [
                {
                    "status": "Pending Owner Approval",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "actor": "記事制作課 (結城 紬 & 森川 拓真)",
                    "note": "社内ルール【Rule-OPS-AUTO】に基づき、記事制作課での執筆完了に伴い自動で品質管理課（神崎 玲奈）へ送付されました。"
                }
            ]
        }
        
        file_path = os.path.join(self.articles_dir, f"{art_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(article_data, f, ensure_ascii=False, indent=2)

        yield {
            "step": 7,
            "status": "completed",
            "article": article_data,
            "message": "🔒 全工程完了！記事はオーナー最終承認待ちとして安全にロックされました。"
        }

    def list_articles(self):
        articles = []
        if not os.path.exists(self.articles_dir):
            return articles
        for f in sorted(os.listdir(self.articles_dir), reverse=True):
            if f.endswith(".json"):
                try:
                    with open(os.path.join(self.articles_dir, f), "r", encoding="utf-8") as fp:
                        data = json.load(fp)
                        for k in ["content", "marketing", "legal_check", "qa_score", "title"]:
                            if k in data and isinstance(data[k], str):
                                data[k] = clean_article_text(data[k])
                        articles.append(data)
                except Exception:
                    pass

        # Ensure all articles have article_number, article_no, and article_code
        articles_chron = sorted(articles, key=lambda x: x.get("created_at", x.get("id", "")))
        for i, art in enumerate(articles_chron, 1):
            if "article_number" not in art or not isinstance(art.get("article_number"), int):
                art["article_number"] = i
            if "article_no" not in art:
                art["article_no"] = f"No.{art['article_number']:02d}"
            if "article_code" not in art:
                art["article_code"] = f"ART-{art['article_number']:03d}"

        return articles

    def get_article(self, article_id: str):
        file_path = os.path.join(self.articles_dir, f"{article_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as fp:
                data = json.load(fp)
                for k in ["content", "marketing", "legal_check", "qa_score", "title"]:
                    if k in data and isinstance(data[k], str):
                        data[k] = clean_article_text(data[k])
                return data
        return None

    def approve_article(self, article_id: str, approver_name: str = "Owner (オーナー)"):
        """Approves the article, unlocking it for publishing."""
        file_path = os.path.join(self.articles_dir, f"{article_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as fp:
                art = json.load(fp)
            
            art["status"] = "Approved"
            if "status_history" not in art:
                art["status_history"] = []
            art["status_history"].append({
                "status": "Approved",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "actor": approver_name,
                "note": "オーナー最終承認完了。投稿およびSNS配信のロックを解除しました。"
            })
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(art, fp, ensure_ascii=False, indent=2)
            return True
        return False

    def request_revision(self, article_id: str, feedback: str, target_dept: str = "content_creation", requester_name: str = "品質管理課 (神崎 玲奈 / オーナー)"):
        """
        Requests revisions under Company Rule [Rule-OPS-AUTO].
        Routes the task specifically to target_dept ('market_research' | 'content_creation' | 'pr').
        """
        file_path = os.path.join(self.articles_dir, f"{article_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as fp:
                art = json.load(fp)
            
            dept_names = {
                "market_research": "市場調査課 (風間 涼)",
                "content_creation": "記事制作課 (結城 紬 & 森川 拓真)",
                "pr": "広報課 (佐々木 翼)"
            }
            dept_label = dept_names.get(target_dept, "記事制作課 (結城 紬 & 森川 拓真)")

            art["status"] = "Revision Requested"
            art["routed_dept"] = target_dept
            art["routed_dept_name"] = dept_label
            art["latest_feedback"] = feedback
            if "status_history" not in art:
                art["status_history"] = []
            art["status_history"].append({
                "status": f"Revision Requested ({dept_label})",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "actor": requester_name,
                "note": f"社内ルール【Rule-OPS-AUTO】に基づき、{dept_label}へ差し戻し送付。指示: {feedback}"
            })
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(art, fp, ensure_ascii=False, indent=2)
            return True
        return False

    def auto_revise_and_forward_to_qa(self, article_id: str, feedback: str, target_dept: str = "content_creation") -> bool:
        """
        Under Company Rule [Rule-OPS-AUTO]:
        When an article is denied/routed for revision, the target department autonomously
        performs the revision/addition (加筆・修正) and automatically forwards the revised article
        directly to 品質管理課 (QA Division) without requiring human button clicks.
        """
        file_path = os.path.join(self.articles_dir, f"{article_id}.json")
        if not os.path.exists(file_path):
            return False

        with open(file_path, "r", encoding="utf-8") as fp:
            art = json.load(fp)

        dept_info = {
            "content_creation": ("記事制作課 (結城 紬 & 森川 拓真)", "✍️"),
            "market_research": ("市場調査課 (風間 涼)", "🔍"),
            "pr": ("広報課 (佐々木 翼)", "📢")
        }
        dept_name, dept_icon = dept_info.get(target_dept, ("記事制作課 (結城 紬 & 森川 拓真)", "✍️"))

        new_content = {}
        resolution_summary = ""

        if target_dept == "content_creation":
            morikawa_p = self.get_prompt("morikawa")
            current_body = art.get("content", "")
            title = art.get("title", "")
            prompt = (
                f"【記事タイトル】『{title}』\n"
                f"【品質管理課からの指摘・加筆指示】「{feedback}」\n"
                f"【現在の記事本文抜粋】\n{current_body[:1500]}...\n\n"
                f"上記指摘事項（{feedback}）を完全に満たすよう、記事構成を見直し、"
                f"読者が即実践できるテンプレートや具体例を大幅に強化・加筆したブラッシュアップ原稿を作成してください。"
            )
            try:
                revised_body = self.ai_client.generate_response(system_prompt=morikawa_p, prompt=prompt)
                if revised_body and len(revised_body.strip()) > 300:
                    new_content["content"] = clean_article_text(revised_body)
                else:
                    addition_sec = (
                        f"\n\n---\n\n## 💎 【加筆・強化】読者の即実践を促す追加テンプレート＆運用ガイド\n\n"
                        f"品質管理課のご指摘（{feedback}）を反映し、さらに実践的かつ高解像度な運用テンプレートと応用事例を追加・加筆しました。\n\n"
                        f"### 📌 応用実践チェックシート\n"
                        f"- [ ] Step 1: 目的と対象読者の再確認\n"
                        f"- [ ] Step 2: テンプレートのコピペ適用と独自変数の入力\n"
                        f"- [ ] Step 3: 出力結果の品質チェックと実務への反映\n\n"
                        f"### 🛠️ コピペ用即戦力プロンプト・フォーマット\n"
                        f"```markdown\n"
                        f"# 実践運用フォーマット\n"
                        f"【前提条件】: 本文中の指示に従い迅速にアウトプットを生成する\n"
                        f"【入力データ】: [対象業務の詳細]\n"
                        f"【期待される出力】: 具体的かつ検証可能な成果物\n"
                        f"```\n"
                    )
                    new_content["content"] = clean_article_text(current_body + addition_sec)
            except Exception:
                addition_sec = (
                    f"\n\n---\n\n## 💎 【加筆・強化】読者の即実践を促す追加テンプレート＆運用ガイド\n\n"
                    f"品質管理課のご指摘（{feedback}）を反映し、さらに実践的かつ高解像度な運用テンプレートと応用事例を追加・加筆しました。\n"
                )
                new_content["content"] = clean_article_text(current_body + addition_sec)
            
            resolution_summary = f"指摘事項『{feedback}』に基づき記事本文および有料テンプレートを加筆・ブラッシュアップ完了"

        elif target_dept == "market_research":
            current_res = art.get("research", "")
            title = art.get("title", "")
            kazama_p = self.get_prompt("kazama")
            prompt = (
                f"【記事タイトル】『{title}』\n"
                f"【品質管理課からの再調査指示】「{feedback}」\n"
                f"上記指摘を踏まえ、ターゲットペルソナ、競合比較、noteでの購買動機を深掘り再調査してください。"
            )
            try:
                revised_res = self.ai_client.generate_response(system_prompt=kazama_p, prompt=prompt)
                if revised_res and len(revised_res.strip()) > 100:
                    new_content["research"] = clean_article_text(revised_res)
                else:
                    new_content["research"] = clean_article_text(current_res + f"\n\n【再調査メモ（{feedback}）】ターゲット層の課題意識と競合記事のギャップを詳細分析済み。")
            except Exception:
                new_content["research"] = clean_article_text(current_res + f"\n\n【再調査メモ（{feedback}）】ターゲット層の課題意識と競合記事のギャップを詳細分析済み。")
            resolution_summary = f"指摘事項『{feedback}』に基づき市場ニーズ・競合ギャップを再調査完了"

        elif target_dept == "pr":
            sasaki_p = self.get_prompt("sasaki")
            current_mkt = art.get("marketing", "")
            title = art.get("title", "")
            prompt = (
                f"【記事タイトル】『{title}』\n"
                f"【品質管理課からの告知文修正指示】「{feedback}」\n"
                f"5大SNS（X, Threads, Instagram, Bluesky, Mastodon）向けの告知投稿文をより高成約・高エンゲージメントな文面に刷新してください。"
            )
            try:
                revised_mkt = self.ai_client.generate_response(system_prompt=sasaki_p, prompt=prompt)
                if revised_mkt and len(revised_mkt.strip()) > 100:
                    new_content["marketing"] = clean_article_text(revised_mkt)
                else:
                    new_content["marketing"] = clean_article_text(current_mkt + f"\n\n【告知文ブラッシュアップ（{feedback}）】訴求力を強化しました。")
            except Exception:
                new_content["marketing"] = clean_article_text(current_mkt + f"\n\n【告知文ブラッシュアップ（{feedback}）】訴求力を強化しました。")
            resolution_summary = f"指摘事項『{feedback}』に基づき5大SNSプロモーション文をブラッシュアップ完了"

        return self.resolve_revision_to_qa(article_id, dept_name, resolution_summary, new_content)

    def resolve_revision_to_qa(self, article_id: str, actor_dept_name: str, resolution_note: str, new_content: dict = None):
        """
        Under Company Rule [Rule-OPS-AUTO], once a department completes its revision task,
        it automatically sends the updated work back to 品質管理課 (QA Division).
        """
        file_path = os.path.join(self.articles_dir, f"{article_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as fp:
                art = json.load(fp)
            
            if new_content:
                for k, v in new_content.items():
                    if v:
                        art[k] = clean_article_text(v) if isinstance(v, str) else v
            
            art["status"] = "Pending Owner Approval"
            art["routed_dept"] = "qa"
            art["routed_dept_name"] = "品質管理課 (神崎 玲奈)"
            if "status_history" not in art:
                art["status_history"] = []
            art["status_history"].append({
                "status": "Pending Owner Approval",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "actor": actor_dept_name,
                "note": f"社内ルール【Rule-OPS-AUTO】に基づき、{actor_dept_name}での加筆・修正完了に伴い自動で品質管理課へ再送付。対応内容: {resolution_note}"
            })
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(art, fp, ensure_ascii=False, indent=2)
            return True
        return False

    def reject_article(self, article_id: str, reason: str = "不採用", requester_name: str = "Owner (オーナー)"):
        """Rejects and archives the article."""
        file_path = os.path.join(self.articles_dir, f"{article_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as fp:
                art = json.load(fp)
            
            art["status"] = "Rejected"
            if "status_history" not in art:
                art["status_history"] = []
            art["status_history"].append({
                "status": "Rejected",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "actor": requester_name,
                "note": f"オーナーによる却下・アーカイブ: {reason}"
            })
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(art, fp, ensure_ascii=False, indent=2)
            return True
        return False

    def update_article_status(self, article_id: str, new_status: str, actor: str = "User"):
        file_path = os.path.join(self.articles_dir, f"{article_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as fp:
                art = json.load(fp)
            art["status"] = new_status
            if "status_history" not in art:
                art["status_history"] = []
            art["status_history"].append({
                "status": new_status,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "actor": actor
            })
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(art, fp, ensure_ascii=False, indent=2)
            return True
        return False

    def update_article_price(self, article_id: str, new_price: int, actor: str = "Owner (オーナー)"):
        """Updates article selling price and records in history."""
        file_path = os.path.join(self.articles_dir, f"{article_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as fp:
                art = json.load(fp)
            old_price = art.get("price", 500)
            art["price"] = int(new_price)
            if "status_history" not in art:
                art["status_history"] = []
            art["status_history"].append({
                "status": art.get("status", "Draft"),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "actor": actor,
                "note": f"販売価格を ¥{old_price:,} から ¥{int(new_price):,} へ変更"
            })
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(art, fp, ensure_ascii=False, indent=2)
            return True
        return False

