import os
import json
import time
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
        
        # Determine price
        price = 500
        if "300" in price_preference:
            price = 300
        elif "980" in price_preference:
            price = 980

        # Save article with LOCKED status: Pending Owner Approval
        art_id = f"art_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        article_data = {
            "id": art_id,
            "title": clean_article_text(title),
            "topic": topic,
            "price": price,
            "target_audience": target_audience,
            "content": clean_article_text(res_article),
            "research": clean_article_text(res_analysis),
            "outline": clean_article_text(res_outline),
            "legal_check": clean_article_text(res_legal),
            "qa_score": clean_article_text(res_qa),
            "marketing": clean_article_text(res_marketing),
            "status": "Pending Owner Approval",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status_history": [
                {
                    "status": "Pending Owner Approval",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "actor": "System Pipeline (AI Team Complete)",
                    "note": "9名のAI社員による作成・法務審査・QA完了。オーナーの最終承認待ち（ロック中）。"
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

    def request_revision(self, article_id: str, feedback: str, requester_name: str = "Owner (オーナー)"):
        """Requests revisions with specific feedback from owner."""
        file_path = os.path.join(self.articles_dir, f"{article_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as fp:
                art = json.load(fp)
            
            art["status"] = "Revision Requested"
            art["latest_feedback"] = feedback
            if "status_history" not in art:
                art["status_history"] = []
            art["status_history"].append({
                "status": "Revision Requested",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "actor": requester_name,
                "note": f"オーナーからの修正指示: {feedback}"
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

