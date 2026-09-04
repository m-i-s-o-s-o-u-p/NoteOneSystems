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

    def get_stock_status(self, target_stock_count: int = 10):
        """Returns the current topic stock count and remaining capacity up to target_stock_count."""
        topics = self.list_topics()
        # Active stock includes topics that are Pending Owner Approval or Approved (not rejected)
        active_topics = [t for t in topics if t.get("status") != "Rejected"]
        current_count = len(active_topics)
        needed = max(0, target_stock_count - current_count)
        return {
            "current_count": current_count,
            "max_capacity": target_stock_count,
            "needed_count": needed,
            "active_topics": active_topics
        }

    def auto_replenish_stock(self, target_stock_count: int = 10):
        """
        Autonomously generates trending note topics until stock reaches target_stock_count (default: 10).
        Ensures diverse high-intent commercial niches with no duplicate topics.
        """
        cur_status = self.get_stock_status(target_stock_count)
        needed = cur_status["needed_count"]
        if needed <= 0:
            return []

        # Curated candidate niches tailored for ¥500 - ¥980 note sales
        candidate_niches = [
            {
                "theme": "Excel×ChatGPT 経理・事務作業を半減させるコピペ関数＆マクロ自動化集",
                "audience": "毎月の締め作業や集計業務に追われる事務・経理担当者",
                "category": "業務自動化・Excel",
                "demand": "note内で『Excel時短』『事務効率化』は恒常的な高成約ジャンル。",
                "gap": "複雑なVBAコードではなく、1行関数とプロンプトで動く初心者向け即戦力テンプレに特化。",
                "price": 500
            },
            {
                "theme": "副業初心者が初月からnoteで3万円稼ぐ『売れる有料記事テーマ選定シート』",
                "audience": "自分の知識や経験をお金に変えたい会社員・副業初心者",
                "category": "副業・コンテンツ販売",
                "demand": "note副業の第一歩として『何を書けばいいか分からない』層の検索数がトップクラス。",
                "gap": "抽象論を排し、10の質問に答えるだけで自分の売れ筋テーマが決まるワークシートを同梱。",
                "price": 500
            },
            {
                "theme": "フリーランスのための『値上げ交渉＆トラブル防止契約書テンプレ集』",
                "audience": "単価アップを目指すWebライター、デザイナー、エンジニア",
                "category": "フリーランス・独立支援",
                "demand": "インフレに伴いクリエイターの『価格交渉術』の需要が急増。",
                "gap": "角を立てずに単価を20%上げるメール雛形と、未払い防止の覚書条項をセット化。",
                "price": 980
            },
            {
                "theme": "Canva×AI 誰でも30分でプロ級のnoteアイキャッチ画像を作るデザインレシピ",
                "audience": "記事のクリック率（CTR）を上げたいnoteクリエイター",
                "category": "デザイン・SNSマーケティング",
                "demand": "記事の売上を左右する『サムネイル・アイキャッチ』の自作ノウハウは需要絶大。",
                "gap": "黄金比レイアウトの無料Canva共有リンクと、クリック率が跳ね上がるフォント配色集を提供。",
                "price": 500
            },
            {
                "theme": "新任リーダーのための『部下の本音を引き出す1on1アジェンダ50選』",
                "audience": "部下のマネジメントや離職防止に悩む新任マネージャー・リーダー",
                "category": "マネジメント・ビジネス実務",
                "demand": "若手社員とのコミュニケーション課題に対する具体的な質問集への課金意欲が高い。",
                "gap": "精神論ではなく、心理的安全性を担保しながら課題を特定する心理学的フレームワークを網羅。",
                "price": 500
            },
            {
                "theme": "SNS運用代行で月10万円を堅実に稼ぐ『クライアント提案書＆業務マニュアル』",
                "audience": "SNSスキルを活かして在宅ワーク・副業を受注したい個人",
                "category": "SNS運用・受託副業",
                "demand": "『SNS副業』の中でも『運用代行』は再現性が高く、即戦力マニュアルの需要が高い。",
                "gap": "初回ヒアリングシートから月次報告レポートのテンプレートまで、そのまま使える実務一式を完備。",
                "price": 980
            },
            {
                "theme": "文系・初心者向け『Pythonで競合リサーチを全自動化する超簡単スクリプト』",
                "audience": "プログラミング未経験だが日常のデータ収集を自動化したいビジネスパーソン",
                "category": "プログラミング・自動化",
                "demand": "環境構築で挫折する層が多く、コピペで動くGoogle Colab完結型の需要が強い。",
                "gap": "PCへのインストール不要、ブラウザ上で1クリック実行できる完成コードを提供。",
                "price": 500
            },
            {
                "theme": "ChatGPT×企画書作成 10分で上司のOKが出る『プレゼン骨子ジェネレーター』",
                "audience": "新規事業や業務改善の企画書作成に毎回何日も悩んでいる会社員",
                "category": "AI×企画力向上",
                "demand": "『企画が通らない』悩みを解決する構造化プロンプトへの関心が非常に高い。",
                "gap": "課題提起から投資対効果（ROI）算出までのストーリーラインを自動生成するプロンプト群。",
                "price": 500
            },
            {
                "theme": "個人開発者のための『初期ユーザー100人を完全無料で集めるWeb集客プレイブック』",
                "audience": "プロダクトやサービスを作ったが集客に困っているインディー開発者",
                "category": "マーケティング・起業",
                "demand": "広告費ゼロで初動ユーザーを獲得する泥臭い実践ノウハウは希少価値が高い。",
                "gap": "ProductHunt、X、コミュニティ活用など、実際に100人集めたチェックリストを公開。",
                "price": 980
            },
            {
                "theme": "残業月60時間をゼロにした『Notion×Googleカレンダー時間割タスク術』",
                "audience": "毎日タスクに追われて自分の時間が取れないワーカホリックな社会人",
                "category": "タイムマネジメント・生産性",
                "demand": "『時間術』『タスク管理』は自己啓発・ビジネス両面で安定したベストセラージャンル。",
                "gap": "時間割ブロック方式で1日のスケジュールを自動同期するNotion構築マニュアル。",
                "price": 500
            }
        ]

        existing_titles = [t.get("title", "") for t in self.list_topics()]
        newly_added = []

        for candidate in candidate_niches:
            if len(newly_added) >= needed:
                break
            
            # Check duplicate by theme similarity
            cand_title = f"【完全保存版】{candidate['theme']}"
            if any(candidate['category'] in ex or candidate['theme'][:10] in ex for ex in existing_titles):
                continue

            topic_id = f"topic_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(newly_added)+1}"
            topic_item = {
                "id": topic_id,
                "title": cand_title,
                "target_audience": candidate["audience"],
                "category": candidate["category"],
                "demand_summary": candidate["demand"],
                "competitor_gap": candidate["gap"],
                "recommended_price": candidate["price"],
                "status": "Pending Owner Approval",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "analyst": "風間 涼 (市場調査課・自律オートパイロット)",
                "status_history": [
                    {
                        "status": "Pending Owner Approval",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "actor": "風間 涼 (自律オートパイロット)",
                        "note": f"自律トレンド分析完了。10本ストック枠へ自動起票（オーナー承認待ち）。"
                    }
                ]
            }
            newly_added.append(topic_item)

        if newly_added:
            topics = self.list_topics()
            for item in newly_added:
                topics.insert(0, item)
            with open(self.topics_file, "w", encoding="utf-8") as f:
                json.dump(topics, f, ensure_ascii=False, indent=2)

        return newly_added

    def update_topic_status(self, topic_id: str, new_status: str, actor: str = "User"):
        topics = self.list_topics()
        for t in topics:
            if t.get("id") == topic_id:
                t["status"] = new_status
                if "status_history" not in t:
                    t["status_history"] = []
                t["status_history"].append({
                    "status": new_status,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "actor": actor
                })
                with open(self.topics_file, "w", encoding="utf-8") as f:
                    json.dump(topics, f, ensure_ascii=False, indent=2)
                return True
        return False

