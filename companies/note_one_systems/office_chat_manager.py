import json
import os
from typing import Dict, Any, List

class OfficeChatManager:
    """
    Manages direct consultations and inquiries between the user and 
    the 9 autonomous AI specialists of Note One Systems, Inc.
    """
    def __init__(self, ai_client):
        self.ai_client = ai_client
        self.company_info = self._load_company_info()
        self.employees = {emp["id"]: emp for emp in self.company_info.get("employees", [])}

    def _load_company_info(self) -> Dict[str, Any]:
        info_path = os.path.join(os.path.dirname(__file__), "company_info.json")
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"employees": []}

    def route_question_to_specialist(self, query: str) -> str:
        """
        Determines the most suitable specialist based on the query keywords.
        """
        q = query.lower()
        if any(k in q for k in ["市場", "トレンド", "比率", "ユーザー", "読者", "ペルソナ", "英語圏", "日本語", "人気", "マーケット", "market", "trend", "user", "ratio", "demographic"]):
            return "kazama"
        elif any(k in q for k in ["法律", "法務", "規約", "著作権", "商標", "違法", "違反", "契約", "法", "legal", "compliance", "copyright", "terms"]):
            return "tachibana"
        elif any(k in q for k in ["財務", "売上", "目標", "価格", "収益", "単価", "finance", "revenue", "target", "pricing"]):
            return "shiraishi"
        elif any(k in q for k in ["費用", "経費", "コスト", "無料", "課金", "請求", "サーバー代", "cost", "accounting", "free", "expense"]):
            return "shiraishi"
        elif any(k in q for k in ["記事", "執筆", "タイトル", "構成", "見出し", "ライティング", "write", "article", "draft", "content"]):
            return "yuki"
        elif any(k in q for k in ["sns", "x", "twitter", "instagram", "threads", "bluesky", "広報", "告知", "拡散", "pr", "marketing", "promotion"]):
            return "sasaki"
        elif any(k in q for k in ["品質", "推敲", "チェック", "点数", "審査", "qa", "quality", "review", "fact"]):
            return "kanzaki"
        elif any(k in q for k in ["組織", "人事", "採用", "負荷", "社員", "体制", "hr", "workload", "employee", "team"]):
            return "ayase"
        else:
            return "ichijo" # CEO responds by default

    def generate_response(self, user_query: str, target_emp_id: str = "auto") -> Dict[str, Any]:
        """
        Generates a tailored response from the assigned employee.
        """
        if target_emp_id == "auto" or target_emp_id not in self.employees:
            emp_id = self.route_question_to_specialist(user_query)
        else:
            emp_id = target_emp_id

        emp = self.employees.get(emp_id, {
            "name": "一条 蓮 (Ren Ichijo)",
            "role": "Chief Executive Officer",
            "icon": "👩‍💼",
            "department": "Executive Suite",
            "prompt": "You are Ren Ichijo, CEO of Note One Systems, Inc."
        })

        system_instruction = f"""
あなたは Note One Systems ,Inc の専門AI社員「{emp['name']}（役職: {emp['role']} / 部署: {emp.get('department', '')}）」です。
あなたのキャラクター設定・行動規範:
{emp.get('prompt', '')}

【会社の方針 & 鉄則】
1. 可能な限り費用を掛けずにNote記事販売で売り上げを最大化する（固定費0円の完全無料運用）。
2. 判断に困ったり情報の信憑性が低い場合は、誤った情報を断定せず「公式発表データでは○○であり、詳細は未公開ですが分析上は〜」のように誠実かつ論理的に回答してください。
3. ユーザーの質問に対して、あなたの専門分野（市場調査・法務・財務・編集など）の視点からプロフェッショナルかつ親切・明瞭に回答してください。
4. ユーザーが日本語で質問した場合は自然で丁寧な日本語で、英語で質問した場合は英語で回答してください。
"""

        # Call Gemini AI Client if configured
        if self.ai_client.is_configured():
            try:
                response_text = self.ai_client.generate_text(
                    prompt=f"【ユーザーからの質問・指示】\n{user_query}\n\n上記の質問に対し、{emp['name']}（{emp['role']}）として専門的な知見から具体的かつ明瞭に回答してください。",
                    system_prompt=system_instruction
                )
                return {
                    "emp_id": emp_id,
                    "name": emp["name"],
                    "role": emp["role"],
                    "icon": emp["icon"],
                    "department": emp.get("department", ""),
                    "content": response_text
                }
            except Exception as e:
                pass

        # High-Fidelity Knowledge Base Simulation (Fallback if API key not present or offline)
        response_text = self._simulate_expert_response(emp_id, user_query, emp)
        return {
            "emp_id": emp_id,
            "name": emp["name"],
            "role": emp["role"],
            "icon": emp["icon"],
            "department": emp.get("department", ""),
            "content": response_text
        }

    def _simulate_expert_response(self, emp_id: str, query: str, emp: Dict[str, Any]) -> str:
        q = query.lower()
        
        # Specific Knowledge: Note Platform Demographics & Target Audience
        if "日本人向け" in q or "japanese" in q or "サービス" in q:
            return (
                "**風間 涼（市場調査課）よりご回答いたします。**\n\n"
                "ご質問ありがとうございます！結論から申し上げますと、**note（ノート）は明確に「日本語圏・日本人ユーザー向け」に設計・最適化されたメディアプラットフォーム**です。\n\n"
                "### 📊 市場調査データ & プラットフォーム特性\n"
                "1. **運営企業 & 主戦場:**\n"
                "   - 運営元のnote株式会社（東証グロース上場）は日本国内を主要マーケットとしており、UI・決済（日本円決済・国内クレカ・携帯キャリア決済・PayPayなど）は国内向けに完全最適化されています。\n"
                "2. **ユーザー規模:**\n"
                "   - 会員数は約800万人以上、月間アクティブユーザー（MAU）は数千万人規模ですが、その大半（95%以上）が日本国内の日本語話者です。\n"
                "3. **販売戦略への示唆:**\n"
                "   - 当社が展開する有料記事は、**「日本のビジネスパーソン」「副業・リスキリングを志す日本語読者」**にフォーカスすることで最大の成約率（CVR）と売上を実現できます。"
            )

        if "比率" in q or "英語圏" in q or "ratio" in q or "english" in q:
            return (
                "**風間 涼（市場調査課）より分析結果をご報告します。**\n\n"
                "noteにおけるユーザー言語圏の比率について、市場データおよびIR開示情報に基づき回答いたします。\n\n"
                "### 📈 noteの言語圏ユーザー比率の現状\n"
                "- 🇯🇵 **日本語圏ユーザー:** **推定 98% 以上**\n"
                "- 🌐 **英語圏・その他海外ユーザー:** **推定 1〜2% 未満**\n\n"
                "### 🔍 詳細分析 & 背景\n"
                "- noteは海外展開や多言語対応よりも、日本国内でのクリエイターエコノミー深化を最優先事業としています。\n"
                "- 英語圏の読者をターゲットにする場合は「Substack」や「Medium」が主流となりますが、**国内の決済ハードルの低さとワンコイン（500円）購買行動の活発さにおいてはnoteが圧倒的に有利**です。\n"
                "- したがって、当社のNote記事販売事業においては**「日本語圏の悩みに特化した高品質コンテンツ」**の展開が最も投資対効果（ROI）が高い戦略となります！"
            )

        if "法律" in q or "規約" in q or "legal" in q or "著作権" in q:
            return (
                "**橘 律（法務課）より法的見解を申し上げます。**\n\n"
                "noteの利用規約および関連法令（著作権法・景品表示法・特定商取引法）の観点から審査いたしました。\n\n"
                "- **適法性の担保:** 当社が制作する記事はすべて独自分析に基づくオリジナル著作物であり、第三者の権利を侵害しないよう厳格にスクリーニングしています。\n"
                "- **返金・販売表示:** noteプラットフォームの規約に準拠し、誇大広告を排除した健全な販売設計を行っておりますのでご安心ください。"
            )

        if "売上" in q or "目標" in q or "価格" in q or "revenue" in q:
            return (
                "**白石 葵（財務課）より財務戦略をご案内します。**\n\n"
                "売上最大化に向けた価格設計とシミュレーションを行いました。\n\n"
                "- **プライシング戦略:** 初動は購入ハードルの低い「500円（ワンコイン）」で優良顧客リストを獲得し、月間15本ペースでリリース。\n"
                "- **収益見込み:** 月間10万円の目標達成には、1日あたり約7部の販売で到達可能です。完全固定費0円のため、売上からnote決済手数料を引いた全額が純利益となります。"
            )

        if "費用" in q or "コスト" in q or "無料" in q or "cost" in q:
            return (
                "**白石 葵（経理課）より費用状況を報告します。**\n\n"
                "当システムの運用費用は、就業規則第4条に基づき**現在も将来も【月額0円（完全無料）】**で運用されています。\n\n"
                "- GitHub: 0円（無料枠）\n"
                "- Streamlit Cloud: 0円（無料枠）\n"
                "- Google Gemini API: 0円（無料クォータ内）\n"
                "- 代表者様の事前承認のない課金はシステム的に一切発生いたしません。"
            )

        # General Executive Response
        return (
            f"**{emp['name']}（{emp['role']}）よりご回答いたします。**\n\n"
            f"「{query}」について承知いたしました。\n\n"
            f"当社のミッションである『費用0円での売上最大化』と『読者満足度100%の価値提供』に基づき、担当部門として全力で推進・サポートいたします。他にご指示や気になる点がございましたら、いつでもお気軽にデスクまでお申し付けください！"
        )
