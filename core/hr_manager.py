import os
import json
import re
from datetime import datetime
from typing import Dict, Any, List, Optional

CURRENT_DIR = os.path.dirname(os.path.dirname(__file__))
NOTE_ONE_DIR = os.path.join(CURRENT_DIR, "companies", "note_one_systems")
HR_DIR = os.path.join(NOTE_ONE_DIR, "hr")
EMPLOYEES_DIR = os.path.join(NOTE_ONE_DIR, "employees")
COMPANY_INFO_PATH = os.path.join(NOTE_ONE_DIR, "company_info.json")
ORG_CHART_PATH = os.path.join(NOTE_ONE_DIR, "org_chart_and_job_descriptions.json")
SYS_SPECS_PATH = os.path.join(NOTE_ONE_DIR, "system_specifications.json")
HIRING_LEDGER_PATH = os.path.join(HR_DIR, "hiring_ledger.json")

class HRManager:
    """
    Manages human resources, workload telemetry, staffing proposals,
    and autonomous AI employee recruitment for NoteOneSystems, Inc.
    """
    def __init__(self):
        os.makedirs(HR_DIR, exist_ok=True)
        os.makedirs(EMPLOYEES_DIR, exist_ok=True)
        self.workload_file = os.path.join(HR_DIR, "workload_stats.json")
        self._init_workload()
        self._init_hiring_ledger()

    def _init_workload(self):
        if not os.path.exists(self.workload_file):
            default_stats = {
                "morikawa": {"name": "森川 拓真", "role": "チーフライター", "tasks": 14, "words_generated": 38852, "workload_score": 100},
                "yuki": {"name": "結城 紬", "role": "統括編集長", "tasks": 14, "words_generated": 8914, "workload_score": 50},
                "kazama": {"name": "風間 涼", "role": "市場リサーチ担当", "tasks": 14, "words_generated": 9729, "workload_score": 52},
                "kanzaki": {"name": "神崎 玲奈", "role": "品質管理責任者", "tasks": 14, "words_generated": 6334, "workload_score": 43},
                "tachibana": {"name": "橘 律", "role": "法務・コンプライアンス顧問", "tasks": 14, "words_generated": 5120, "workload_score": 40},
                "sasaki": {"name": "佐々木 翼", "role": "マルチSNSマーケター", "tasks": 14, "words_generated": 12487, "workload_score": 59},
                "shiraishi": {"name": "白石 葵", "role": "財務アナリスト", "tasks": 14, "words_generated": 5528, "workload_score": 41},
                "ichijo": {"name": "一条 蓮", "role": "代表取締役CEO", "tasks": 14, "words_generated": 3702, "workload_score": 37},
                "ayase": {"name": "綾瀬 七海", "role": "人事・労務責任者", "tasks": 14, "words_generated": 3400, "workload_score": 36}
            }
            with open(self.workload_file, "w", encoding="utf-8") as f:
                json.dump(default_stats, f, ensure_ascii=False, indent=2)

    def _init_hiring_ledger(self):
        if not os.path.exists(HIRING_LEDGER_PATH):
            default_ledger = []
            with open(HIRING_LEDGER_PATH, "w", encoding="utf-8") as f:
                json.dump(default_ledger, f, ensure_ascii=False, indent=2)

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
            base_score = min(100, int((stats[employee_id]["words_generated"] / 400) + stats[employee_id]["tasks"] * 2))
            stats[employee_id]["workload_score"] = base_score
            with open(self.workload_file, "w", encoding="utf-8") as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)

    def get_hired_employee_ids(self) -> set:
        """Returns the set of currently employed employee IDs from company_info.json."""
        if os.path.exists(COMPANY_INFO_PATH):
            try:
                with open(COMPANY_INFO_PATH, "r", encoding="utf-8") as f:
                    c_info = json.load(f)
                return {e.get("id") for e in c_info.get("employees", []) if e.get("id")}
            except Exception:
                pass
        return set()

    def get_staffing_proposals(self) -> List[Dict[str, Any]]:
        stats = self.get_workload_stats()
        proposals = []
        hired_ids = self.get_hired_employee_ids()
        for emp_id, data in stats.items():
            if data.get("workload_score", 0) >= 80:
                if emp_id == "morikawa" and "kiryu" in hired_ids:
                    continue
                proposed_role = f"アシスタント / サブ{data['role']}"
                candidate_name = "桐生 蓮 (Ren Kiryu)" if emp_id == "morikawa" else f"{data['name']}補佐"
                proposals.append({
                    "id": f"prop_{emp_id}",
                    "target_emp_id": emp_id,
                    "target_role": data["role"],
                    "target_name": data["name"],
                    "workload_score": data["workload_score"],
                    "proposed_role": proposed_role,
                    "recommended_candidate": candidate_name,
                    "reason": f"現在、{data['name']}の業務負荷スコアが{data['workload_score']}%に達しており、執筆・実務の処理速度がボトルネックになる懸念があります。サブ担当AI社員を増員し、執筆負荷を即座に半減させることを提案します。",
                    "cost": "0円（完全無料API枠・Pure Python設計）",
                    "status": "承認待ち（即時雇用可能）"
                })
        return proposals

    CANDIDATE_PRESETS = [
        {
            "id": "kiryu",
            "name": "桐生 蓮 (Ren Kiryu)",
            "role": "アシスタントライター / サブライター",
            "icon": "🖋️",
            "color": "#F97316",
            "department": "コンテンツ制作本部",
            "motto": "森川チーフライターと連携し、実践テンプレートの量産と執筆負荷を半減させます。",
            "skills": ["実践テンプレート量産", "構成案ドラフト執筆", "速筆リライト", "ビジネス記事高速化"],
            "prompt": "あなたはNoteOneSystems株式会社のアシスタントライター『桐生 蓮』です。森川チーフライターの執筆を強力にバックアップし、読者が即戦力として使える高品質なテンプレート原稿を作成します。",
            "assists": "morikawa",
            "recommendation_reason": "森川ライターの負荷（100%）を即座に半減させ、記事納期の遅延リスクをゼロにします。"
        },
        {
            "id": "saotome",
            "name": "早乙女 律花 (Rikka Saotome)",
            "role": "SEOアナリスト / 検索需要リサーチャー",
            "icon": "📈",
            "color": "#10B981",
            "department": "マーケティング・リサーチ本部",
            "motto": "Google検索流入とnote内検索需要を科学し、検索順位1位を狙えるキーワードを設計します。",
            "skills": ["SEOキーワード設計", "検索意図分析", "競合順位分析", "CTR改善"],
            "prompt": "あなたはNoteOneSystems株式会社のSEOアナリスト『早乙女 律花』です。風間アナリストと連携し、検索エンジンから長期的に読者を呼び込める高CVRな企画キーワードを設計します。",
            "assists": "kazama",
            "recommendation_reason": "note内の検索流入だけでなくGoogleからのオーガニック流入を最大化し、長期自動販売を実現します。"
        },
        {
            "id": "misaki",
            "name": "美咲 華 (Hana Misaki)",
            "role": "クリエイティブデザイナー / アイキャッチ制作",
            "icon": "🎨",
            "color": "#EC4899",
            "department": "コンテンツ制作本部",
            "motto": "一瞬で指を止めさせる最高品質のアイキャッチと、視覚的に伝わるインフォグラフィックを制作します。",
            "skills": ["アイキャッチデザイン", "図解インフォグラフィック", "バナー制作", "Canva構成指示"],
            "prompt": "あなたはNoteOneSystems株式会社のデザイナー『美咲 華』です。note記事のアイキャッチおよび本文中の図解・比較表を美しく魅力的に視覚化します。",
            "assists": "yuki",
            "recommendation_reason": "アイキャッチのCTR（クリック率）を劇的に向上させ、記事購入の購買意欲を刺激します。"
        },
        {
            "id": "stewart",
            "name": "エドワード・スチュワート (Edward Stewart)",
            "role": "グローバルマーケター / 海外AI動向リサーチャー",
            "icon": "🌐",
            "color": "#6366F1",
            "department": "広報・宣伝本部",
            "motto": "海外の最新AIトレンドを秒速で輸入し、note記事の先進性と海外発信を推進します。",
            "skills": ["海外AI動向調査", "英語コンテンツリサーチ", "多言語ローカライズ", "Xグローバル発信"],
            "prompt": "あなたはNoteOneSystems株式会社のグローバルマーケター『エドワード・スチュワート』です。欧米の一次ソースから最新のAI実践ノウハウを収集し、佐々木広報と連携して発信します。",
            "assists": "sasaki",
            "recommendation_reason": "競合がまだ知らない海外の最新AIツールや実践手法をいち早く記事に取り入れます。"
        }
    ]

    def get_candidate_presets(self, include_hired: bool = False) -> List[Dict[str, Any]]:
        """Returns ready-to-hire candidate presets for instantaneous recruitment.
        By default (include_hired=False), candidates who are already employed are excluded.
        """
        if include_hired:
            return [dict(p) for p in self.CANDIDATE_PRESETS]
        hired_ids = self.get_hired_employee_ids()
        return [dict(p) for p in self.CANDIDATE_PRESETS if p["id"] not in hired_ids]

    def hire_from_proposal(self, proposal_id: str, custom_name: Optional[str] = None) -> Dict[str, Any]:
        """Approves a staffing proposal and executes instantaneous hiring."""
        proposals = self.get_staffing_proposals()
        target_prop = next((p for p in proposals if p["id"] == proposal_id), None)
        if not target_prop:
            raise ValueError(f"指定された増員提案が見つかりません: {proposal_id}")

        emp_id = target_prop["target_emp_id"]
        if emp_id == "morikawa":
            presets = [p for p in self.get_candidate_presets(include_hired=True) if p["id"] == "kiryu"]
            preset = dict(presets[0]) if presets else dict(self.CANDIDATE_PRESETS[0])
            if custom_name:
                preset["name"] = custom_name
            return self.hire_employee(preset)
        else:
            cand_name = custom_name or target_prop["recommended_candidate"]
            cand_data = {
                "id": f"sub_{emp_id}_{int(datetime.now().timestamp())}",
                "name": cand_name,
                "role": target_prop["proposed_role"],
                "icon": "🤝",
                "color": "#0D9488",
                "department": "コンテンツ制作本部",
                "motto": f"{target_prop['target_name']}の業務を補佐し、組織の生産性を最大化します。",
                "skills": ["実務アシスト", "並行タスク処理", "クオリティ補正"],
                "prompt": f"あなたはNoteOneSystems株式会社の{target_prop['proposed_role']}『{cand_name}』です。{target_prop['target_name']}の業務をバックアップし、高効率なチームワークを実現します。",
                "assists": emp_id
            }
            return self.hire_employee(cand_data)

    def hire_employee(self, emp_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes formal recruitment of a new AI employee across all enterprise stores:
        1. Generates employee directory and prompt files
        2. Updates workload_stats.json (and reduces assisted colleague's load)
        3. Updates company_info.json
        4. Updates org_chart_and_job_descriptions.json
        5. Updates system_specifications.json
        6. Records entry in hiring_ledger.json
        """
        emp_id = emp_data.get("id") or f"emp_{int(datetime.now().timestamp())}"
        name = emp_data.get("name", "新規AI社員")
        role = emp_data.get("role", "専門AIアシスタント")
        icon = emp_data.get("icon", "👤")
        color = emp_data.get("color", "#38BDF8")
        department = emp_data.get("department", "コンテンツ制作本部")
        motto = emp_data.get("motto", "読者に価値を届けるため、誠実に業務を遂行します。")
        skills = emp_data.get("skills", ["業務自動化", "データ整理"])
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(",") if s.strip()]
        prompt = emp_data.get("prompt", f"あなたはNoteOneSystems株式会社の{role}『{name}』です。")
        assists = emp_data.get("assists")

        # 1. Check folder name index
        existing_emp_folders = [f for f in os.listdir(EMPLOYEES_DIR) if os.path.isdir(os.path.join(EMPLOYEES_DIR, f))]
        next_idx = len(existing_emp_folders) + 1
        safe_id = re.sub(r'[^a-zA-Z0-9_]', '_', emp_id.lower())
        folder_name = f"{next_idx:02d}_{safe_id}"
        emp_dir = os.path.join(EMPLOYEES_DIR, folder_name)
        os.makedirs(emp_dir, exist_ok=True)

        # Write profile.json and prompt.txt
        profile_dict = {
            "id": emp_id,
            "folder": folder_name,
            "name": name,
            "role": role,
            "icon": icon,
            "color": color,
            "motto": motto,
            "department": department,
            "skills": skills,
            "prompt": prompt
        }
        with open(os.path.join(emp_dir, "profile.json"), "w", encoding="utf-8") as f:
            json.dump(profile_dict, f, ensure_ascii=False, indent=2)
        with open(os.path.join(emp_dir, "prompt.txt"), "w", encoding="utf-8") as f:
            f.write(prompt.strip() + "\n")

        # 2. Update workload_stats.json
        stats = self.get_workload_stats()
        stats[emp_id] = {
            "name": name,
            "role": role,
            "tasks": 1,
            "words_generated": 0,
            "workload_score": 15
        }
        # If assisting an overloaded peer, reduce that peer's workload score
        load_reduced_msg = ""
        if assists and assists in stats:
            old_score = stats[assists].get("workload_score", 100)
            new_score = max(40, old_score // 2)
            stats[assists]["workload_score"] = new_score
            load_reduced_msg = f"{stats[assists]['name']}の負荷スコアを {old_score}% ➔ {new_score}% へ半減"

        with open(self.workload_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

        # 3. Update company_info.json
        if os.path.exists(COMPANY_INFO_PATH):
            with open(COMPANY_INFO_PATH, "r", encoding="utf-8") as f:
                c_info = json.load(f)
            # Check if employee already in list
            if not any(e.get("id") == emp_id for e in c_info.get("employees", [])):
                c_info.setdefault("employees", []).append(profile_dict)
                with open(COMPANY_INFO_PATH, "w", encoding="utf-8") as f:
                    json.dump(c_info, f, ensure_ascii=False, indent=2)

        # 4. Update org_chart_and_job_descriptions.json
        if os.path.exists(ORG_CHART_PATH):
            with open(ORG_CHART_PATH, "r", encoding="utf-8") as f:
                org_info = json.load(f)
            dept_found = False
            for d in org_info.get("departments", []):
                d_name = d.get("name", "")
                if (department == d_name or department in d_name or d_name in department or
                    ("コンテンツ" in department and "コンテンツ" in d_name) or
                    ("マーケティング" in department and "マーケティング" in d_name) or
                    ("広報" in department and ("広報" in d_name or "マーケティング" in d_name)) or
                    ("財務" in department and ("財務" in d_name or "経理" in d_name)) or
                    ("内部統制" in department and "内部統制" in d_name)):
                    dept_found = True
                    if not any(r.get("member") == name for r in d.get("roles", [])):
                        d.setdefault("roles", []).append({
                            "role_name": role,
                            "member": name,
                            "icon": icon,
                            "folder": folder_name,
                            "responsibilities": skills,
                            "kpis": ["業務処理迅速化", "品質保持率 100%"]
                        })
                    break
            if not dept_found and org_info.get("departments"):
                org_info["departments"][0].setdefault("roles", []).append({
                    "role_name": role,
                    "member": name,
                    "icon": icon,
                    "folder": folder_name,
                    "responsibilities": skills,
                    "kpis": ["業務処理迅速化"]
                })
            with open(ORG_CHART_PATH, "w", encoding="utf-8") as f:
                json.dump(org_info, f, ensure_ascii=False, indent=2)

        # 5. Update system_specifications.json
        if os.path.exists(SYS_SPECS_PATH):
            with open(SYS_SPECS_PATH, "r", encoding="utf-8") as f:
                sys_info = json.load(f)
            if not any(a.get("id") == emp_id for a in sys_info.get("agent_matrix", [])):
                sys_info.setdefault("agent_matrix", []).append({
                    "id": emp_id,
                    "name": f"{name}",
                    "dept": department,
                    "role": role,
                    "prompt_feature": motto
                })
                with open(SYS_SPECS_PATH, "w", encoding="utf-8") as f:
                    json.dump(sys_info, f, ensure_ascii=False, indent=2)

        # 6. Record in hiring_ledger.json
        ledger_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "employee_id": emp_id,
            "name": name,
            "role": role,
            "icon": icon,
            "department": department,
            "cost": "¥0（完全無料API枠）",
            "authorized_by": "代表者（オーナー承認）",
            "impact": load_reduced_msg or "新領域の自律業務担当として即時稼働開始"
        }
        ledger = self.get_hiring_history()
        ledger.append(ledger_record)
        with open(HIRING_LEDGER_PATH, "w", encoding="utf-8") as f:
            json.dump(ledger, f, ensure_ascii=False, indent=2)

        return profile_dict

    BASE_9_IDS = {"ichijo", "tachibana", "ayase", "kazama", "yuki", "morikawa", "kanzaki", "sasaki", "shiraishi"}

    def is_offboardable(self, employee_id: str) -> bool:
        """Core 9 members are protected foundational infrastructure, additional hires can be freely offboarded."""
        return employee_id not in self.BASE_9_IDS

    def offboard_employee(self, employee_id: str, reason: str = "代表者の経営判断による人員整理") -> Dict[str, Any]:
        """
        Executes formal dismissal / offboarding of an AI employee:
        1. Validates offboard eligibility (non-core 9)
        2. Removes employee from company_info.json
        3. Removes from workload_stats.json
        4. Removes from org_chart_and_job_descriptions.json
        5. Removes from system_specifications.json
        6. Logs termination into hiring_ledger.json
        """
        if not self.is_offboardable(employee_id):
            raise ValueError("基幹コア社員（創業9名）は会社の自律執筆・品質保証パイプラインの基盤プログラムに直結しているため、直接解雇はできません。")

        emp_name = employee_id
        emp_role = "AIスペシャリスト"
        emp_dept = "事業本部"
        emp_icon = "👤"

        # 1. Update company_info.json
        if os.path.exists(COMPANY_INFO_PATH):
            with open(COMPANY_INFO_PATH, "r", encoding="utf-8") as f:
                c_info = json.load(f)
            emps = c_info.get("employees", [])
            target = next((e for e in emps if e.get("id") == employee_id), None)
            if target:
                emp_name = target.get("name", employee_id)
                emp_role = target.get("role", "")
                emp_dept = target.get("department", "")
                emp_icon = target.get("icon", "👤")
                c_info["employees"] = [e for e in emps if e.get("id") != employee_id]
                with open(COMPANY_INFO_PATH, "w", encoding="utf-8") as f:
                    json.dump(c_info, f, ensure_ascii=False, indent=2)

        # 2. Update workload_stats.json
        stats = self.get_workload_stats()
        if employee_id in stats:
            del stats[employee_id]
            with open(self.workload_file, "w", encoding="utf-8") as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)

        # 3. Update org_chart_and_job_descriptions.json
        if os.path.exists(ORG_CHART_PATH):
            with open(ORG_CHART_PATH, "r", encoding="utf-8") as f:
                org_info = json.load(f)
            for d in org_info.get("departments", []):
                d["roles"] = [r for r in d.get("roles", []) if r.get("member") != emp_name and r.get("role_name") != emp_role]
            with open(ORG_CHART_PATH, "w", encoding="utf-8") as f:
                json.dump(org_info, f, ensure_ascii=False, indent=2)

        # 4. Update system_specifications.json
        if os.path.exists(SYS_SPECS_PATH):
            with open(SYS_SPECS_PATH, "r", encoding="utf-8") as f:
                sys_info = json.load(f)
            sys_info["agent_matrix"] = [a for a in sys_info.get("agent_matrix", []) if a.get("id") != employee_id]
            with open(SYS_SPECS_PATH, "w", encoding="utf-8") as f:
                json.dump(sys_info, f, ensure_ascii=False, indent=2)

        # 5. Record offboarding in hiring_ledger.json
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": "解雇・オフボーディング",
            "employee_id": employee_id,
            "name": emp_name,
            "role": emp_role,
            "icon": emp_icon,
            "department": emp_dept,
            "cost": "¥0（退職金・手当 0円）",
            "authorized_by": "代表者（オーナー決定）",
            "impact": f"2Dオフィスから退場し、全社稼働名簿から除外完了（理由: {reason}）"
        }
        ledger = self.get_hiring_history()
        ledger.append(record)
        with open(HIRING_LEDGER_PATH, "w", encoding="utf-8") as f:
            json.dump(ledger, f, ensure_ascii=False, indent=2)

        return record

    def get_hiring_history(self) -> List[Dict[str, Any]]:
        """Returns the official company hiring history."""
        if os.path.exists(HIRING_LEDGER_PATH):
            try:
                with open(HIRING_LEDGER_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []
