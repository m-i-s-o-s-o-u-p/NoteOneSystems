# -*- coding: utf-8 -*-
"""
Internationalization (i18n) dictionary for Note One Systems, Inc.
Supports seamless switching between Japanese (ja) and English (en).
"""

MESSAGES = {
    "ja": {
        # App Title & Headers
        "app_title": "Note One Systems ,Inc | AI Enterprise Platform",
        "sidebar_subtitle": "AIバーチャル企業ホールディングス",
        "dept_editorial": "📝 編集部",
        "dept_admin": "🏛️ 管理部",
        "nav_dashboard": "🏢 カンパニーダッシュボード",
        "nav_office": "🏢 オフィスルーム",
        "nav_market_research": "🔍 市場調査課",
        "nav_content_creation": "✍️ 記事制作課",
        "nav_pr": "📢 広報課",
        "nav_qa": "✨ 品質管理課",
        "nav_hr": "🤝 人事課",
        "nav_legal": "📚 法務課",
        "nav_finance": "📊 財務課",
        "nav_accounting": "💳 経理課",
        "nav_helpdesk": "💻 社内ヘルプデスク",
        "nav_profiles": "👥 社員プロファイル",
        "nav_cloud_guide": "☁️ 24時間無料クラウド設定ガイド",
        
        # Sidebar Footer
        "ai_engine_title": "⚙️ AI頭脳設定（Gemini）",
        "ai_key_label": "Gemini API Key (無料枠)",
        "ai_key_help": "Google AI Studioで取得した無料のAPIキー。未入力時はデモシミュレーションで動きます。",
        "ai_connected": "🟢 AI頭脳: Gemini API 接続中",
        "ai_demo": "🟡 AI頭脳: デモモード（無料シミュレーション中）",
        "cost_free_caption": "💡 維持費: 0円（完全無料）",
        "active_specialists_caption": "9名の専門AI社員が24時間稼働中",
        "lang_section_title": "🌐 言語設定 / Language",
        
        # 1. Dashboard
        "dash_title": "🏢 カンパニーダッシュボード",
        "dash_sub": "Note One Systems ,Inc グループ全体の経営概況・全社統括ダッシュボード",
        "dash_subsidiaries": "傘下の子会社数",
        "dash_articles": "総生産記事数",
        "dash_revenue": "月間想定売上 / 目標",
        "dash_fixed_costs": "システム固定維持費",
        "dash_cost_val": "¥0 (完全無料0円)",
        "dash_progress_text": "🎯 月間売上目標達成度",
        "dash_group_list": "📋 傘下のグループ会社一覧",
        "dash_new_sub_btn": "➕ 新しい子会社を設立する（ホールディングス化）",
        "dash_form_title": "新会社設立申請フォーム",
        "dash_form_name": "会社名（例: KindleOne AI 株式会社、PromptOne AI 株式会社）",
        "dash_form_model": "事業モデル",
        "dash_form_icon": "会社アイコン",
        "dash_form_desc": "事業内容・ビジョン",
        "dash_form_submit": "🚀 新会社を設立・ホールディングスに統合",

        # 2. Office Room
        "office_main_header": "🏢 Office Room",
        "office_sub_header": "9名の専門AI社員がそれぞれのデスクで自律的に業務を行っています",
        "office_sec_title": "Headquarter",
        "consult_title": "💬 社員との直接対話・質問・指示デスク",
        "consult_sub": "質問や指示を入力すると、最適な担当部署の専門AI社員が自律的に判定・回答します。",
        "quick_inquiries_title": "💡 Quick Inquiries (クリックして質問を入力):",
        "consult_input_label": "質問・指示を入力してください",
        "consult_placeholder": "例: 「Noteの英語圏ユーザと日本語圏ユーザの比率は？」「note記事販売の法的な注意点は？」「売上を伸ばすための価格戦略は？」",
        "consult_assign_label": "担当者指定",
        "consult_assign_auto": "Auto-Routing (自動判別)",
        "consult_submit_btn": "📨 送信して回答を得る",
        "consult_log_title": "📜 対話・業務指示ログ",
        "consult_user_prefix": "👤 あなたからの質問・指示:",
        "consult_status_done": "回答完了",
        "consult_clear_btn": "🗑️ 対話ログをクリア",
        "floor_status_title": "🖥️ フロア別 執務デスク＆リアルタイム稼働状況",
        "floor_exec_title": "🏛️ 経営統括 ＆ 管理部（人事課・法務課）",
        "floor_edit_title": "📝 編集部（市場調査・制作・広報・品質管理）",
        "floor_pr_fin_title": "📢 広報課 ＆ 📊 財務課・💳 経理課",

        # 3. Market Research
        "mr_title": "🔍 市場調査課",
        "mr_sub": "担当: 風間 涼（Market Research Analyst）",
        "mr_mission": "💡 **市場調査課のミッション**: noteの最新売れ筋トレンド、競合記事のギャップ、読者ペルソナの深層心理を分析し、売れるテーマを特定します。",
        "mr_report_title": "📊 最新トレンド分析レポート",

        # 4. Content Creation
        "cc_title": "✍️ 記事制作課",
        "cc_sub": "統括: 結城 紬（編集長） / 執筆: 森川 拓真（チーフライター）",
        "cc_form_title": "🗣️ 中央ガラス会議室：記事制作指示フォーム",
        "cc_topic_label": "記事のテーマ・キーワード",
        "cc_topic_ph": "例: 「Notionで劇的に業務効率化する実践テンプレート集」「未経験から月5万円稼ぐAI副業の完全マップ」",
        "cc_target_label": "ターゲット読者（任意）",
        "cc_target_ph": "例: 「忙しい会社員」「副業を始めたい初心者」",
        "cc_price_label": "価格方針",
        "cc_price_opt_auto": "自動提案（アナリスト最適化）",
        "cc_price_opt_500": "ワンコイン（500円）",
        "cc_price_opt_300": "入門価格（300円）",
        "cc_price_opt_prem": "高付加価値（980円〜）",
        "cc_start_btn": "🚀 9名を中央会議室に招集して執筆開始",
        "cc_stream_title": "🎙️ 中央会議室 リアルタイム戦略会議 ＆ 執筆ライブログ",

        # 5. PR
        "pr_title": "📢 広報課",
        "pr_sub": "担当: 佐々木 翼（Multi-SNS PR Specialist）",
        "pr_hub_title": "⚙️ 5大SNSアカウント ＆ 自動配信先の設定",
        "pr_save_btn": "💾 広報課 SNS設定を保存する",

        # 6. QA
        "qa_title": "✨ 品質管理課",
        "qa_sub": "担当: 神崎 玲奈（Quality Assurance Director）",
        "qa_registry_title": "📋 作成記事一覧・ステータス管理 ＆ タイムスタンプ履歴",
        "qa_no_articles": "まだ記事がありません。「✍️ 記事制作課」から記事を執筆してください。",
        "qa_select_label": "管理する記事を選択",
        "qa_cur_status": "現在のステータス:",
        "qa_change_label": "ステータスを変更する",
        "qa_update_btn": "🔄 ステータスを更新（タイムスタンプ追記）",
        "qa_history_title": "⏱️ ステータス遷移タイムスタンプ履歴",
        "qa_preview_title": "📄 記事プレビュー（無料エリア / 有料エリア）",
        "qa_paywall_badge": "🔒 ここから先は有料エリア（noteの有料ライン設定位置）",
        "qa_sns_copy_title": "📢 5大SNS告知文（佐々木 翼 作成）",
        "qa_markdown_title": "📋 note貼り付け用 マークダウン全文",

        # 7. HR
        "hr_title": "🤝 人事課",
        "hr_sub": "担当: 綾瀬 七海（HR & Culture Director）",
        "hr_org_title": "🏢 組織体制図 ＆ 職務分掌規程",
        "hr_view_ledger": "📋 9名の詳細職務分掌一覧を開く",
        "hr_workload_title": "📊 社員別 リアルタイム業務負荷監視",

        # 8. Legal
        "legal_title": "📚 法務課",
        "legal_sub": "担当: 橘 律（Legal & Compliance Counsel）",
        "legal_ledger_title": "📜 他部門からの法的調査・相談管理台帳",

        # 9. Finance
        "fin_title": "📊 財務課",
        "fin_sub": "担当: 白石 葵（Financial Strategist）",
        "fin_target_title": "🎯 オーナー売上目標指示 ＆ 逆算ロードマップ",
        "fin_target_amt_label": "月間売上目標金額（円）",
        "fin_target_art_label": "月間目標制作本数",
        "fin_submit_btn": "📢 売上目標を指示する",

        # 10. Accounting
        "acc_title": "💳 経理課",
        "acc_sub": "担当: 白石 葵（Chief Accountant 兼任）",
        "acc_ledger_title": "💰 システム運用費用・0円運用管理台帳",
        "acc_total_cost_prefix": "現在の月間システム運用費用合計:",
        "acc_total_cost_val": "¥0 （完全無料0円）",

        # 11. IT Helpdesk
        "it_title": "💻 社内ヘルプデスク",
        "it_sub": "システム内で発生した全エラー・インシデントの管理台帳および解決状況",
        "it_total_label": "総インシデント件数",
        "it_resolved_label": "解決済み",
        "it_health_label": "システム健全性",
        "it_ledger_title": "📋 エラー・トラブルシューティング管理台帳",

        # 12. Profiles
        "prof_title": "👥 社員別フォルダ ＆ プロファイル管理",
        "prof_sub": "9名の社員がそれぞれ独立したフォルダでプロンプト・設定を管理されています",

        # 13. Cloud Guide
        "cloud_title": "☁️ 24時間完全無料クラウド稼働マニュアル",
        "cloud_sub": "Macの電源を落としても、スマホや別PCからいつでもあなたのAI会社にアクセスできるようにする方法"
    },
    
    "en": {
        # App Title & Headers
        "app_title": "Note One Systems, Inc. | AI Enterprise Platform",
        "sidebar_subtitle": "AI Enterprise Holdings Platform",
        "dept_editorial": "📝 Editorial Department",
        "dept_admin": "🏛️ Administration Department",
        "nav_dashboard": "🏢 Company Dashboard",
        "nav_office": "🏢 Office Room",
        "nav_market_research": "🔍 Market Research Division",
        "nav_content_creation": "✍️ Content Creation Division",
        "nav_pr": "📢 Public Relations Division",
        "nav_qa": "✨ Quality Assurance Division",
        "nav_hr": "🤝 Human Resources Division",
        "nav_legal": "📚 Legal & Compliance Division",
        "nav_finance": "📊 Financial Strategy Division",
        "nav_accounting": "💳 Accounting & Operations Division",
        "nav_helpdesk": "💻 IT Helpdesk & Error Logs",
        "nav_profiles": "👥 Employee Profiles",
        "nav_cloud_guide": "☁️ 24/7 Free Cloud Setup Guide",

        # Sidebar Footer
        "ai_engine_title": "⚙️ AI Intelligence Engine (Gemini)",
        "ai_key_label": "Gemini API Key (Free Tier)",
        "ai_key_help": "Free API key from Google AI Studio. If blank, high-fidelity demo simulation will run.",
        "ai_connected": "🟢 AI Engine: Gemini API Connected",
        "ai_demo": "🟡 AI Engine: Demo Mode (Free Simulation Active)",
        "cost_free_caption": "💡 Fixed Operating Cost: ¥0 (100% Free Tier)",
        "active_specialists_caption": "9 Autonomous AI Specialists Active 24/7",
        "lang_section_title": "🌐 Language Settings / 言語設定",

        # 1. Dashboard
        "dash_title": "🏢 Company Dashboard",
        "dash_sub": "Executive overview and holdings performance metrics for Note One Systems, Inc.",
        "dash_subsidiaries": "Active Subsidiaries",
        "dash_articles": "Published Articles",
        "dash_revenue": "Est. Monthly Revenue / Goal",
        "dash_fixed_costs": "Fixed Operating Costs",
        "dash_cost_val": "¥0 (100% Free Tier)",
        "dash_progress_text": "🎯 Monthly Revenue Target Progress",
        "dash_group_list": "📋 Group Subsidiaries & Operating Units",
        "dash_new_sub_btn": "➕ Establish a New Subsidiary (Holdings Expansion)",
        "dash_form_title": "New Entity Incorporation Form",
        "dash_form_name": "Company Name (e.g., KindleOne AI Inc., PromptOne AI Corp.)",
        "dash_form_model": "Business Model",
        "dash_form_icon": "Company Icon",
        "dash_form_desc": "Business Mission & Vision",
        "dash_form_submit": "🚀 Incorporate & Integrate into Holdings",

        # 2. Office Room
        "office_main_header": "🏢 Office Room",
        "office_sub_header": "9 specialized autonomous AI employees working in their designated virtual workspaces",
        "office_sec_title": "Headquarter",
        "consult_title": "💬 Direct Inquiries & Employee Consultation Desk",
        "consult_sub": "Ask a question or issue a directive; the most relevant AI specialist will autonomously respond.",
        "quick_inquiries_title": "💡 Quick Inquiries (Click to run):",
        "consult_input_label": "Ask a question or issue a directive to the team",
        "consult_placeholder": "e.g., 'What is the ratio of English vs Japanese users on note?', 'What are the legal guidelines for selling content?', 'What is our pricing strategy?'",
        "consult_assign_label": "Assignee",
        "consult_assign_auto": "Auto-Routing (Autonomous)",
        "consult_submit_btn": "📨 Send Inquiry & Get Answer",
        "consult_log_title": "📜 Consultation & Directives Log",
        "consult_user_prefix": "👤 Your Inquiry / Directive:",
        "consult_status_done": "Answered",
        "consult_clear_btn": "🗑️ Clear Consultation Log",
        "floor_status_title": "🖥️ Workspace Desks & Live Employee Activity",
        "floor_exec_title": "🏛️ Executive & Corporate Administration (HR & Legal)",
        "floor_edit_title": "📝 Editorial Department (Research, Content, PR, QA)",
        "floor_pr_fin_title": "📢 Public Relations & 📊 Financial Strategy / 💳 Accounting",

        # 3. Market Research
        "mr_title": "🔍 Market Research Division",
        "mr_sub": "Lead Analyst: Ryo Kazama (Market Research Analyst)",
        "mr_mission": "💡 **Mission**: Uncover high-converting trends on note, analyze competitor content gaps, and identify deep reader pain points to formulate winning themes.",
        "mr_report_title": "📊 High-Conversion Trend Report",

        # 4. Content Creation
        "cc_title": "✍️ Content Creation Division",
        "cc_sub": "Supervision: Tsumugi Yuki (Editor-in-Chief) / Writing: Takuma Morikawa (Chief Content Writer)",
        "cc_form_title": "🗣️ Central Strategy Room: Content Production Brief",
        "cc_topic_label": "Article Topic / Target Keyword",
        "cc_topic_ph": "e.g., 'Complete Guide to Work Automation with Notion & AI', 'Zero to $500/mo AI Side Hustle Blueprint'",
        "cc_target_label": "Target Audience Persona (Optional)",
        "cc_target_ph": "e.g., 'Busy corporate professionals', 'Beginners seeking online monetization'",
        "cc_price_label": "Pricing Strategy",
        "cc_price_opt_auto": "Auto-Optimized (AI Recommended)",
        "cc_price_opt_500": "Standard (500 JPY)",
        "cc_price_opt_300": "Entry Level (300 JPY)",
        "cc_price_opt_prem": "Premium Tier (980+ JPY)",
        "cc_start_btn": "🚀 Convene 9 AI Specialists & Begin Writing",
        "cc_stream_title": "🎙️ Central Strategy Room: Live Editorial Stream",

        # 5. PR
        "pr_title": "📢 Public Relations Division",
        "pr_sub": "Lead: Tsubasa Sasaki (Multi-SNS PR Specialist)",
        "pr_hub_title": "⚙️ 5 Major Social Media Accounts & Auto-Syndication Hub",
        "pr_save_btn": "💾 Save Social Media Configuration",

        # 6. QA
        "qa_title": "✨ Quality Assurance Division",
        "qa_sub": "Lead: Reina Kanzaki (Quality Assurance Director)",
        "qa_registry_title": "📋 Published Articles Registry & Status Audit Trail",
        "qa_no_articles": "No articles found in registry. Launch a writing session in '✍️ Content Creation Division'.",
        "qa_select_label": "Select Article to Manage",
        "qa_cur_status": "Current Status:",
        "qa_change_label": "Change Lifecycle Status",
        "qa_update_btn": "🔄 Update Status & Record Timestamp",
        "qa_history_title": "⏱️ Status Transition Timestamp Log",
        "qa_preview_title": "📄 Article Preview (Free Introduction / Paid Paywall Area)",
        "qa_paywall_badge": "🔒 Paid Subscriber Paywall Threshold (Set on note platform)",
        "qa_sns_copy_title": "📢 5-SNS Syndication Copy (Crafted by Tsubasa Sasaki)",
        "qa_markdown_title": "📋 Full Markdown Source Code (Ready for note editor)",

        # 7. HR
        "hr_title": "🤝 Human Resources Division",
        "hr_sub": "Lead: Nanami Ayase (HR & Culture Director)",
        "hr_org_title": "🏢 Organizational Hierarchy & Job Responsibilities",
        "hr_view_ledger": "📋 View Complete 9-Member Job Description Ledger",
        "hr_workload_title": "📊 Real-Time Employee Workload & Operational Metrics",

        # 8. Legal
        "legal_title": "📚 Legal & Compliance Division",
        "legal_sub": "Counsel: Ritsu Tachibana (Legal & Compliance Counsel)",
        "legal_ledger_title": "📜 Inter-Department Legal Inquiry & Compliance Audit Ledger",

        # 9. Finance
        "fin_title": "📊 Financial Strategy Division",
        "fin_sub": "Strategist: Aoi Shiraishi (Financial Strategist)",
        "fin_target_title": "🎯 Executive Monthly Revenue Target & Monetization Roadmap",
        "fin_target_amt_label": "Monthly Revenue Target (JPY)",
        "fin_target_art_label": "Monthly Article Production Target",
        "fin_submit_btn": "📢 Issue Executive Financial Directive",

        # 10. Accounting
        "acc_title": "💳 Accounting & Operations Division",
        "acc_sub": "Lead: Aoi Shiraishi (Chief Accountant)",
        "acc_ledger_title": "💰 Zero-Cost Operational Ledger & Expense Verification",
        "acc_total_cost_prefix": "Total Verified Monthly Operating Costs:",
        "acc_total_cost_val": "¥0 (100% Zero Cost)",

        # 11. IT Helpdesk
        "it_title": "💻 IT Helpdesk & Error Logs",
        "it_sub": "Central Incident Management, Diagnostics & Self-Healing Registry",
        "it_total_label": "Total Logged Incidents",
        "it_resolved_label": "Resolved Incidents",
        "it_health_label": "System Health",
        "it_ledger_title": "📋 Incident Resolution Registry",

        # 12. Profiles
        "prof_title": "👥 Employee Profiles & System Prompts",
        "prof_sub": "9 autonomous specialized AI professionals with isolated prompt configurations",

        # 13. Cloud Guide
        "cloud_title": "☁️ 24/7 Zero-Cost Cloud Deployment Guide",
        "cloud_sub": "How to host and access your AI enterprise from any device 24/7 with zero server fees"
    }
}

def t(key: str, lang: str = "ja") -> str:
    """Helper to get translated string safely."""
    lang_dict = MESSAGES.get(lang, MESSAGES["ja"])
    return lang_dict.get(key, MESSAGES["ja"].get(key, key))
