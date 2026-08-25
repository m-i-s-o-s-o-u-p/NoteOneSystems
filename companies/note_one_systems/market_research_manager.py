import os
import json
from datetime import datetime

class MarketResearchManager:
    def __init__(self, ai_client):
        self.ai_client = ai_client
        self.base_dir = os.path.dirname(__file__)
        self.topics_file = os.path.join(self.base_dir, "market_topics.json")
        self._init_default_topics()

    def _init_default_topics(self):
        if not os.path.exists(self.topics_file):
            default_topics = [
                {
                    "id": "topic_20260825_001",
                    "title": "ChatGPTで残業をゼロにする実務プロンプト50選＆自動化テンプレ",
                    "target_audience": "残業を削減したいデスクワーカー・ビジネスパーソン",
                    "category": "AI×実務効率化",
                    "demand_summary": "note内で『残業削減』『ChatGPT実務』の検索ボリュームが急増中。コピペで動くプロンプトの需要が極めて高い。",
                    "competitor_gap": "一般的なプロンプト集は抽象的。当社は『メール返信』『議事録要約』『Excel関数生成』の即戦力3分野に特化して差別化。",
                    "recommended_price": 500,
                    "status": "Pending Owner Approval",
                    "created_at": "2026-08-25 10:00:00",
                    "analyst": "風間 涼 (Ryo Kazama)",
                    "status_history": [
                        {
                            "status": "Pending Owner Approval",
                            "timestamp": "2026-08-25 10:00:00",
                            "actor": "風間 涼 (市場調査課)",
                            "note": "note市場トレンド分析完了。オーナーのトピック承認待ち（ロック中）。"
                        }
                    ]
                },
                {
                    "id": "topic_20260825_002",
                    "title": "知識ゼロからのnote有料記事販売ロードマップ【初月5万円達成モデル】",
                    "target_audience": "副業でnote記事販売を始めたい初心者・クリエイター",
                    "category": "副業・マネタイズ",
                    "demand_summary": "『note副業』『有料記事の書き方』の購買意欲が常に上位。特にワンコイン（500円）での入門記事が最もCVRが高い。",
                    "competitor_gap": "精神論ではなく、売れるテーマの選定方法、有料ラインの引き方、5大SNS告知の具体手順を網羅。",
                    "recommended_price": 500,
                    "status": "Approved",
                    "created_at": "2026-08-25 09:30:00",
                    "analyst": "風間 涼 (Ryo Kazama)",
                    "status_history": [
                        {
                            "status": "Pending Owner Approval",
                            "timestamp": "2026-08-25 09:30:00",
                            "actor": "風間 涼 (市場調査課)",
                            "note": "市場調査完了。"
                        },
                        {
                            "status": "Approved",
                            "timestamp": "2026-08-25 11:15:00",
                            "actor": "Owner (オーナー)",
                            "note": "オーナー承認完了。記事制作課での執筆を許可。"
                        }
                    ]
                },
                {
                    "id": "topic_20260825_003",
                    "title": "Notion×AI 自動化オペレーション構築ガイド【チーム標準化テンプレ付】",
                    "target_audience": "Notionを業務で活用したいチームリーダー・フリーランス",
                    "category": "業務自動化ツール",
                    "demand_summary": "NotionデータベースとAI連携によるタスク自動管理のニーズが国内企業で拡大中。",
                    "competitor_gap": "設定手順のスクリーンショット図解と、ワンクリック複製可能な公開Notionテンプレートを同梱して高付加価値化。",
                    "recommended_price": 980,
                    "status": "Pending Owner Approval",
                    "created_at": "2026-08-25 11:00:00",
                    "analyst": "風間 涼 (Ryo Kazama)",
                    "status_history": [
                        {
                            "status": "Pending Owner Approval",
                            "timestamp": "2026-08-25 11:00:00",
                            "actor": "風間 涼 (市場調査課)",
                            "note": "市場調査完了。オーナー承認待ち。"
                        }
                    ]
                }
            ]
            with open(self.topics_file, "w", encoding="utf-8") as f:
                json.dump(default_topics, f, ensure_ascii=False, indent=2)

    def list_topics(self):
        if not os.path.exists(self.topics_file):
            return []
        with open(self.topics_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_topic(self, topic_id: str):
        topics = self.list_topics()
        for t in topics:
            if t.get("id") == topic_id:
                return t
        return None

    def conduct_research(self, keyword_or_theme: str, target_audience: str = ""):
        """Runs AI research through Ryo Kazama prompt and stores new topic pending approval."""
        prompt = f"""
あなたはNote One Systems, Inc.の市場調査アナリスト「風間 涼」です。
キーワードまたはテーマ: 「{keyword_or_theme}」
想定ターゲット層: 「{target_audience}」

noteプラットフォームにおける最新の購買トレンド、競合記事のギャップ、高成約率な切り口を調査・分析し、以下のJSONフォーマットのみを出力してください。

```json
{{
  "title": "読者を惹きつける魅力的なnote記事タイトル案",
  "category": "カテゴリ（例: AI×実務効率化、副業・マネタイズ等）",
  "target_audience": "明確なターゲット読者像",
  "demand_summary": "市場ニーズ・検索トレンドの分析結果",
  "competitor_gap": "競合記事との差別化ポイント・独自の付加価値",
  "recommended_price": 500
}}
```
"""
        response_text = self.ai_client.generate_response(
            system_prompt="あなたはnote市場調査のエキスパートアナリスト風間涼です。必ず有効なJSONを出力してください。",
            prompt=prompt
        )
        
        # Parse JSON
        parsed_data = {}
        try:
            cleaned = response_text.replace("```json", "").replace("```", "").strip()
            parsed_data = json.loads(cleaned)
        except Exception:
            parsed_data = {
                "title": f"【徹底解説】{keyword_or_theme} 実践マスターガイド",
                "category": "実務ノウハウ",
                "target_audience": target_audience if target_audience else "関心を持つすべての読者",
                "demand_summary": f"「{keyword_or_theme}」に関する実践的ノウハウの需要がnote上で堅調に推移しています。",
                "competitor_gap": "コピペで即使えるテンプレートと実務フローを網羅することで差別化を図ります。",
                "recommended_price": 500
            }

        topic_id = f"topic_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        new_topic = {
            "id": topic_id,
            "title": parsed_data.get("title", f"{keyword_or_theme} 実践ガイド"),
            "target_audience": parsed_data.get("target_audience", target_audience),
            "category": parsed_data.get("category", "実務ノウハウ"),
            "demand_summary": parsed_data.get("demand_summary", ""),
            "competitor_gap": parsed_data.get("competitor_gap", ""),
            "recommended_price": parsed_data.get("recommended_price", 500),
            "status": "Pending Owner Approval",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "analyst": "風間 涼 (Ryo Kazama)",
            "status_history": [
                {
                    "status": "Pending Owner Approval",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "actor": "風間 涼 (市場調査課)",
                    "note": f"テーマ「{keyword_or_theme}」の市場調査完了。オーナー承認待ち（ロック中）。"
                }
            ]
        }

        topics = self.list_topics()
        topics.insert(0, new_topic)
        with open(self.topics_file, "w", encoding="utf-8") as f:
            json.dump(topics, f, ensure_ascii=False, indent=2)

        return new_topic

    def approve_topic(self, topic_id: str, approver_name: str = "Owner (オーナー)"):
        """Approves the topic for article creation."""
        topics = self.list_topics()
        for t in topics:
            if t.get("id") == topic_id:
                t["status"] = "Approved"
                if "status_history" not in t:
                    t["status_history"] = []
                t["status_history"].append({
                    "status": "Approved",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "actor": approver_name,
                    "note": "オーナー承認完了。記事制作課での本格執筆・構成設計を許可。"
                })
                with open(self.topics_file, "w", encoding="utf-8") as f:
                    json.dump(topics, f, ensure_ascii=False, indent=2)
                return True
        return False

    def request_revision(self, topic_id: str, feedback: str, requester_name: str = "Owner (オーナー)"):
        """Requests topic angle revisions."""
        topics = self.list_topics()
        for t in topics:
            if t.get("id") == topic_id:
                t["status"] = "Revision Requested"
                t["latest_feedback"] = feedback
                if "status_history" not in t:
                    t["status_history"] = []
                t["status_history"].append({
                    "status": "Revision Requested",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "actor": requester_name,
                    "note": f"オーナーからの再調査・切り口指示: {feedback}"
                })
                with open(self.topics_file, "w", encoding="utf-8") as f:
                    json.dump(topics, f, ensure_ascii=False, indent=2)
                return True
        return False

    def reject_topic(self, topic_id: str, reason: str = "不採用", requester_name: str = "Owner (オーナー)"):
        """Rejects the topic."""
        topics = self.list_topics()
        for t in topics:
            if t.get("id") == topic_id:
                t["status"] = "Rejected"
                if "status_history" not in t:
                    t["status_history"] = []
                t["status_history"].append({
                    "status": "Rejected",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "actor": requester_name,
                    "note": f"オーナーによる却下: {reason}"
                })
                with open(self.topics_file, "w", encoding="utf-8") as f:
                    json.dump(topics, f, ensure_ascii=False, indent=2)
                return True
        return False
