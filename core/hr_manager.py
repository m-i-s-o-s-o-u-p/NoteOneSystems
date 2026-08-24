import os
import json
from datetime import datetime
from typing import Dict, Any, List

CURRENT_DIR = os.path.dirname(os.path.dirname(__file__))
HR_DIR = os.path.join(CURRENT_DIR, "companies", "note_one_systems", "hr")

class HRManager:
    def __init__(self):
        os.makedirs(HR_DIR, exist_ok=True)
        self.workload_file = os.path.join(HR_DIR, "workload_stats.json")
        self._init_workload()

    def _init_workload(self):
        if not os.path.exists(self.workload_file):
            default_stats = {
                "morikawa": {"name": "森川 拓真", "role": "チーフライター", "tasks": 12, "words_generated": 36000, "workload_score": 92},
                "yuki": {"name": "結城 紬", "role": "統括編集長", "tasks": 12, "words_generated": 8500, "workload_score": 68},
                "kazama": {"name": "風間 涼", "role": "市場リサーチ担当", "tasks": 12, "words_generated": 9200, "workload_score": 70},
                "kanzaki": {"name": "神崎 玲奈", "role": "品質管理責任者", "tasks": 12, "words_generated": 6000, "workload_score": 58},
                "tachibana": {"name": "橘 律", "role": "法務・コンプライアンス顧問", "tasks": 12, "words_generated": 4800, "workload_score": 50},
                "sasaki": {"name": "佐々木 翼", "role": "マルチSNSマーケター", "tasks": 12, "words_generated": 11000, "workload_score": 75},
                "shiraishi": {"name": "白石 葵", "role": "財務アナリスト", "tasks": 12, "words_generated": 5200, "workload_score": 52},
                "ichijo": {"name": "一条 蓮", "role": "代表取締役CEO", "tasks": 12, "words_generated": 3500, "workload_score": 45},
                "ayase": {"name": "綾瀬 七海", "role": "人事・労務責任者", "tasks": 12, "words_generated": 3000, "workload_score": 40}
            }
            with open(self.workload_file, "w", encoding="utf-8") as f:
                json.dump(default_stats, f, ensure_ascii=False, indent=2)

    def get_workload_stats(self) -> Dict[str, Any]:
        if os.path.exists(self.workload_file):
            with open(self.workload_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def log_task(self, employee_id: str, words_count: int):
        stats = self.get_workload_stats()
        if employee_id in stats:
            stats[employee_id]["tasks"] += 1
            stats[employee_id]["words_generated"] += words_count
            # 簡易スコアリング（執筆文字数・タスク頻度）
            base_score = min(100, int((stats[employee_id]["words_generated"] / 400) + stats[employee_id]["tasks"] * 2))
            stats[employee_id]["workload_score"] = base_score
            with open(self.workload_file, "w", encoding="utf-8") as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)

    def get_staffing_proposals(self) -> List[Dict[str, Any]]:
        stats = self.get_workload_stats()
        proposals = []
        # 最も負荷の高い社員（85点以上）を検出
        for emp_id, data in stats.items():
            if data["workload_score"] >= 80:
                proposals.append({
                    "target_role": data["role"],
                    "target_name": data["name"],
                    "workload_score": data["workload_score"],
                    "proposed_role": f"アシスタント / サブ{data['role']}",
                    "reason": f"現在、{data['name']}の業務負荷スコアが{data['workload_score']}%に達しており、記事執筆・処理がボトルネックになる懸念があります。サブ担当AI社員を増員し、並行処理を行うことを提案します。",
                    "cost": "0円（無料API枠内での自律スケール）",
                    "status": "提案中"
                })
        return proposals
