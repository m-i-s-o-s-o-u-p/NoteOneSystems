import json
import os
from typing import List, Dict, Any

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
COMPANIES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "companies")

class HoldingsManager:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.holdings_info_file = os.path.join(DATA_DIR, "holdings_info.json")
        self._init_data()

    def _init_data(self):
        if not os.path.exists(self.holdings_info_file):
            default_holdings = {
                "name": "AI Virtual Holdings Inc.（バーチャルAI企業ホールディングス）",
                "vision": "完全自動・費用0円で複数のデジタル事業を展開する次世代AI持株会社",
                "founded_date": "2026-08-24",
                "companies": [
                    {
                        "id": "note_publishing",
                        "name": "NotePub AI 株式会社",
                        "type": "note_publishing",
                        "icon": "✍️",
                        "description": "note有料記事の市場調査・企画・執筆・マーケティングを行うAI出版会社",
                        "status": "稼働中",
                        "created_at": "2026-08-24"
                    }
                ]
            }
            with open(self.holdings_info_file, "w", encoding="utf-8") as f:
                json.dump(default_holdings, f, ensure_ascii=False, indent=2)

    def get_holdings_info(self) -> Dict[str, Any]:
        with open(self.holdings_info_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_companies(self) -> List[Dict[str, Any]]:
        info = self.get_holdings_info()
        return info.get("companies", [])

    def add_company(self, company_id: str, name: str, company_type: str, icon: str, description: str, employees: List[Dict[str, str]]) -> bool:
        info = self.get_holdings_info()
        for comp in info.get("companies", []):
            if comp["id"] == company_id:
                return False  # 重複
        
        new_comp = {
            "id": company_id,
            "name": name,
            "type": company_type,
            "icon": icon,
            "description": description,
            "status": "稼働中",
            "created_at": "2026-08-24"
        }
        info["companies"].append(new_comp)
        
        with open(self.holdings_info_file, "w", encoding="utf-8") as f:
            json.dump(info, f, ensure_ascii=False, indent=2)

        # 会社ディレクトリと設定ファイルを作成
        comp_dir = os.path.join(COMPANIES_DIR, company_id)
        os.makedirs(comp_dir, exist_ok=True)
        os.makedirs(os.path.join(comp_dir, "articles"), exist_ok=True)
        os.makedirs(os.path.join(comp_dir, "meetings"), exist_ok=True)
        
        comp_info = {
            "id": company_id,
            "name": name,
            "type": company_type,
            "icon": icon,
            "description": description,
            "employees": employees
        }
        with open(os.path.join(comp_dir, "company_info.json"), "w", encoding="utf-8") as f:
            json.dump(comp_info, f, ensure_ascii=False, indent=2)
            
        return True
