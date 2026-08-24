import os
import json
from datetime import datetime
from typing import List, Dict, Any

CURRENT_DIR = os.path.dirname(os.path.dirname(__file__))
RINGI_DIR = os.path.join(CURRENT_DIR, "companies", "note_one_systems", "ringi")

class RingiManager:
    def __init__(self):
        os.makedirs(RINGI_DIR, exist_ok=True)
        self._init_sample_ringi()

    def _init_sample_ringi(self):
        sample_file = os.path.join(RINGI_DIR, "ringi_001_image_generation.json")
        if not os.path.exists(sample_file):
            sample_ringi = {
                "id": "ringi_001",
                "title": "有料画像生成API（アイキャッチ専用）導入に関する稟議",
                "proposer": "白石 葵（財務アナリスト）＆ 佐々木 翼（マーケター）",
                "department": "財務企画部 / マーケティング部",
                "created_at": "2026-08-24",
                "status": "pending",  # pending, approved, rejected
                "cost_monthly_yen": 2500,
                "estimated_increase_sales_yen": 18000,
                "roi_percentage": 620,
                "summary": "プロ品質のアイキャッチ画像を自動生成することで、note記事のクリック率（CTR）を約2.4倍に引き上げ、月間売上を大幅に向上させる提案です。",
                "cost_breakdown": "有料画像生成API月間利用料: 約2,500円（月間30枚生成想定）",
                "roi_analysis": "現状の無料アイキャッチ（クリック率1.5%）から、高品質プロ画像（想定3.6%）へ向上。月間追加販売数 +36部（@500円） ➔ 売上増 +18,000円。純増利益 +15,500円/月（投資回収率 620%）。",
                "free_alternative": "完全無料（0円）のCanva無料枠またはAIテキストによるタイトル文字画像生成を継続。費用は0円だがクリック率は標準にとどまる。",
                "ceo_opinion": "一条 蓮（CEO）: ROIが600%を超えており投資価値は極めて高いですが、就業規則第4条に基づき、代表者のご承認を仰ぎます。"
            }
            with open(sample_file, "w", encoding="utf-8") as f:
                json.dump(sample_ringi, f, ensure_ascii=False, indent=2)

    def list_ringi(self) -> List[Dict[str, Any]]:
        ringi_list = []
        if not os.path.exists(RINGI_DIR):
            return ringi_list
        for fname in sorted(os.listdir(RINGI_DIR)):
            if fname.endswith(".json"):
                try:
                    with open(os.path.join(RINGI_DIR, fname), "r", encoding="utf-8") as f:
                        ringi_list.append(json.load(f))
                except Exception:
                    pass
        return ringi_list

    def update_ringi_status(self, ringi_id: str, new_status: str) -> bool:
        for fname in os.listdir(RINGI_DIR):
            if fname.endswith(".json"):
                fpath = os.path.join(RINGI_DIR, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("id") == ringi_id:
                    data["status"] = new_status
                    data["resolved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    with open(fpath, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    return True
        return False
