import streamlit as st
import streamlit.components.v1 as components
import os
import sys
import importlib
import json
import pandas as pd
from datetime import datetime

# Import and auto-reload core submodules to prevent stale cache in Streamlit runtime
import core.ai_client
import core.holdings_manager
import core.ringi_manager
import core.hr_manager
import core.i18n
import companies.note_one_systems.workflow
import companies.note_one_systems.office_chat_manager
import companies.note_one_systems.market_research_manager

importlib.reload(core.ai_client)
importlib.reload(core.holdings_manager)
importlib.reload(core.ringi_manager)
importlib.reload(core.hr_manager)
importlib.reload(core.i18n)
importlib.reload(companies.note_one_systems.workflow)
importlib.reload(companies.note_one_systems.office_chat_manager)
importlib.reload(companies.note_one_systems.market_research_manager)

from core.ai_client import AIClient
from core.holdings_manager import HoldingsManager
from core.ringi_manager import RingiManager
from core.hr_manager import HRManager
from companies.note_one_systems.workflow import NoteOneWorkflow
from companies.note_one_systems.office_chat_manager import OfficeChatManager
from companies.note_one_systems.market_research_manager import MarketResearchManager
from core.i18n import t

# Page Configuration
st.set_page_config(
    page_title="Note One Systems, Inc. | AI Enterprise Platform",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session State Initialization (English as default base language)
if "language" not in st.session_state:
    st.session_state.language = "en"
if "holdings_manager" not in st.session_state:
    st.session_state.holdings_manager = HoldingsManager()
if "ringi_manager" not in st.session_state:
    st.session_state.ringi_manager = RingiManager()
if "hr_manager" not in st.session_state:
    st.session_state.hr_manager = HRManager()
if "api_key" not in st.session_state:
    st.session_state.api_key = os.environ.get("GEMINI_API_KEY", "")
if "active_page_id" not in st.session_state:
    st.session_state.active_page_id = "dashboard"
if "office_chat_history" not in st.session_state:
    st.session_state.office_chat_history = []
if "prefill_topic" not in st.session_state:
    st.session_state.prefill_topic = ""
if "prefill_audience" not in st.session_state:
    st.session_state.prefill_audience = ""

lang = st.session_state.language
ai_client = AIClient(api_key=st.session_state.api_key)
workflow = NoteOneWorkflow(ai_client)
chat_manager = OfficeChatManager(ai_client)
market_manager = MarketResearchManager(ai_client)

# High-contrast White Text & Sky Blue Active State Styles
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #FFFFFF !important;
        margin-bottom: 0.4rem;
        letter-spacing: -0.5px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94A3B8 !important;
        font-weight: 500;
        margin-bottom: 1.8rem;
    }
    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #FFFFFF !important;
        border-left: 5px solid #38BDF8;
        padding-left: 12px;
        margin: 24px 0 16px 0;
        letter-spacing: -0.3px;
    }
    .content-box {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 22px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        color: #F8FAFC !important;
    }
    .approval-box-locked {
        background: linear-gradient(135deg, #2A1711 0%, #1E1B4B 100%) !important;
        border: 2px solid #F59E0B !important;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 22px;
        box-shadow: 0 6px 18px rgba(245, 158, 11, 0.25);
        color: #FFFFFF !important;
    }
    .approval-box-approved {
        background: linear-gradient(135deg, #064E3B 0%, #0F172A 100%) !important;
        border: 2px solid #10B981 !important;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 22px;
        box-shadow: 0 6px 18px rgba(16, 185, 129, 0.25);
        color: #FFFFFF !important;
    }
    .desk-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #38BDF8 !important;
        margin-bottom: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        color: #F8FAFC !important;
    }
    .status-live {
        display: inline-flex;
        align-items: center;
        background-color: #064E3B;
        color: #4ADE80;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 9999px;
        border: 1px solid #059669;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #4ADE80;
        border-radius: 50%;
        margin-right: 6px;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(74, 222, 128, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(74, 222, 128, 0); }
    }
    .chat-bubble {
        background-color: #1E293B !important;
        border-left: 5px solid #38BDF8;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 14px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        color: #F8FAFC !important;
        border: 1px solid #334155;
    }
    .user-query-card {
        background-color: #0F172A !important;
        border-left: 5px solid #38BDF8;
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 10px;
        color: #E2E8F0 !important;
        border: 1px solid #1E293B;
    }
    
    /* Sidebar Navigation Links */
    div[data-testid="stSidebar"] button {
        text-align: left !important;
        justify-content: flex-start !important;
        border-radius: 8px !important;
        font-size: 0.92rem !important;
        padding: 7px 14px !important;
        margin-bottom: 3px !important;
        border: 1px solid transparent !important;
        background-color: transparent !important;
        color: #CBD5E1 !important;
    }
    div[data-testid="stSidebar"] button:hover {
        background-color: #1E293B !important;
        color: #FFFFFF !important;
    }

    /* Active Sidebar Navigation: Bright Sky Blue (#38BDF8) Highlight */
    div[data-testid="stSidebar"] button[kind="primary"],
    div[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] {
        background-color: #38BDF8 !important;
        color: #0B132B !important;
        border: 1px solid #7DD3FC !important;
        font-weight: 800 !important;
        box-shadow: 0 2px 10px rgba(56, 189, 248, 0.45) !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    p, span, label {
        color: #E2E8F0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# Sidebar: Multilingual Navigation Menu
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#FFFFFF !important;'>🏢 Note One Systems, Inc.</h2>", unsafe_allow_html=True)
    st.caption(t("sidebar_subtitle", lang))
    st.markdown("---")

    # 1. 🏢 Company Dashboard (Top Level)
    if st.button(t("nav_dashboard", lang), use_container_width=True, type="primary" if st.session_state.active_page_id == "dashboard" else "secondary"):
        st.session_state.active_page_id = "dashboard"
        st.rerun()

    # 2. 🏢 Office Room
    if st.button(t("nav_office", lang), use_container_width=True, type="primary" if st.session_state.active_page_id == "office" else "secondary"):
        st.session_state.active_page_id = "office"
        st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 3. 📝 Editorial Department
    st.markdown(f"<div style='font-size:0.95rem; font-weight:800; color:#38BDF8; padding: 4px 6px;'>{t('dept_editorial', lang)}</div>", unsafe_allow_html=True)
    if st.button(f"　 {t('nav_market_research', lang)}", use_container_width=True, type="primary" if st.session_state.active_page_id == "market_research" else "secondary"):
        st.session_state.active_page_id = "market_research"
        st.rerun()
    if st.button(f"　 {t('nav_content_creation', lang)}", use_container_width=True, type="primary" if st.session_state.active_page_id == "content_creation" else "secondary"):
        st.session_state.active_page_id = "content_creation"
        st.rerun()
    if st.button(f"　 {t('nav_pr', lang)}", use_container_width=True, type="primary" if st.session_state.active_page_id == "pr" else "secondary"):
        st.session_state.active_page_id = "pr"
        st.rerun()
    if st.button(f"　 {t('nav_qa', lang)}", use_container_width=True, type="primary" if st.session_state.active_page_id == "qa" else "secondary"):
        st.session_state.active_page_id = "qa"
        st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 4. 🏛️ Administration Department
    st.markdown(f"<div style='font-size:0.95rem; font-weight:800; color:#A78BFA; padding: 4px 6px;'>{t('dept_admin', lang)}</div>", unsafe_allow_html=True)
    if st.button(f"　 {t('nav_hr', lang)}", use_container_width=True, type="primary" if st.session_state.active_page_id == "hr" else "secondary"):
        st.session_state.active_page_id = "hr"
        st.rerun()
    if st.button(f"　 {t('nav_legal', lang)}", use_container_width=True, type="primary" if st.session_state.active_page_id == "legal" else "secondary"):
        st.session_state.active_page_id = "legal"
        st.rerun()
    if st.button(f"　 {t('nav_finance', lang)}", use_container_width=True, type="primary" if st.session_state.active_page_id == "finance" else "secondary"):
        st.session_state.active_page_id = "finance"
        st.rerun()
    if st.button(f"　 {t('nav_accounting', lang)}", use_container_width=True, type="primary" if st.session_state.active_page_id == "accounting" else "secondary"):
        st.session_state.active_page_id = "accounting"
        st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 5. Independent Utilities
    if st.button(t("nav_helpdesk", lang), use_container_width=True, type="primary" if st.session_state.active_page_id == "helpdesk" else "secondary"):
        st.session_state.active_page_id = "helpdesk"
        st.rerun()
    if st.button(t("nav_profiles", lang), use_container_width=True, type="primary" if st.session_state.active_page_id == "profiles" else "secondary"):
        st.session_state.active_page_id = "profiles"
        st.rerun()
    if st.button(t("nav_cloud_guide", lang), use_container_width=True, type="primary" if st.session_state.active_page_id == "cloud_guide" else "secondary"):
        st.session_state.active_page_id = "cloud_guide"
        st.rerun()

    # ==========================================
    # 🌐 言語切り替えリンクセクション（English左 / 日本語右）
    # ==========================================
    st.markdown("---")
    st.markdown(f"<div style='font-size:0.85rem; font-weight:800; color:#38BDF8; margin-bottom:6px;'>{t('lang_section_title', lang)}</div>", unsafe_allow_html=True)
    col_lang1, col_lang2 = st.columns(2)
    with col_lang1:
        if st.button("🇺🇸 English", use_container_width=True, type="primary" if lang == "en" else "secondary"):
            st.session_state.language = "en"
            st.rerun()
    with col_lang2:
        if st.button("🇯🇵 日本語", use_container_width=True, type="primary" if lang == "ja" else "secondary"):
            st.session_state.language = "ja"
            st.rerun()

    # ==========================================
    # ⚙️ AI Intelligence Engine (Gemini) - 言語設定の下に配置
    # ==========================================
    st.markdown("---")
    st.markdown(f"<h4 style='color:#FFFFFF !important;'>{t('ai_engine_title', lang)}</h4>", unsafe_allow_html=True)
    api_key_input = st.text_input(
        t("ai_key_label", lang),
        value=st.session_state.api_key,
        type="password",
        help=t("ai_key_help", lang)
    )
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
        st.rerun()

    if ai_client.is_configured():
        st.success(t("ai_connected", lang))
    else:
        st.info(t("ai_demo", lang))

# Active Page ID
page_id = st.session_state.active_page_id

# ==========================================
# 1. 🏢 Company Dashboard
# ==========================================
if page_id == "dashboard":
    st.markdown(f"<div class='main-header'>{t('dash_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('dash_sub', lang)}</div>", unsafe_allow_html=True)
    
    holdings_info = st.session_state.holdings_manager.get_holdings_info()
    companies = holdings_info.get("companies", [])
    articles = workflow.list_articles()
    topics = market_manager.list_topics()
    
    # 承認待ち記事＆トピックの検出
    pending_articles = [a for a in articles if a.get("status") in ["Pending Owner Approval", "Revision Requested"]]
    pending_topics = [tp for tp in topics if tp.get("status") in ["Pending Owner Approval", "Revision Requested"]]

    if pending_topics or pending_articles:
        warn_msg = []
        if pending_topics:
            warn_msg.append(f"🔍 調査トピック承認待ち: {len(pending_topics)} 件")
        if pending_articles:
            warn_msg.append(f"📄 記事・広告承認待ち: {len(pending_articles)} 件")
        st.warning(f"🔔 **【オーナー決裁アラート】{' / '.join(warn_msg)}** ➔ 各部門で最終承認を行ってください。")

    target_file = os.path.join(os.path.dirname(__file__), "data/sales_targets.json")
    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            target_data = json.load(f)
    else:
        target_data = {"monthly_target_yen": 100000, "target_articles_monthly": 15}
    
    target_sales = target_data.get("monthly_target_yen", 100000)
    total_sales = sum([art.get("price", 500) * 10 for art in articles if art.get("status") in ["Approved", "Published"]])
    progress_ratio = min(1.0, total_sales / target_sales) if target_sales > 0 else 0.0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label=t("dash_subsidiaries", lang), value=f"{len(companies)} {'社' if lang=='ja' else 'Units'}")
    with col2:
        st.metric(label=t("dash_articles", lang), value=f"{len(articles)} {'本' if lang=='ja' else 'Articles'}")
    with col3:
        delta_str = f"目標: ¥{target_sales:,} (達成率 {int(progress_ratio*100)}%)" if lang == "ja" else f"Target: ¥{target_sales:,} ({int(progress_ratio*100)}% Reached)"
        st.metric(label=t("dash_revenue", lang), value=f"¥{total_sales:,}", delta=delta_str)
    with col4:
        st.metric(label=t("dash_fixed_costs", lang), value=t("dash_cost_val", lang))
    
    st.progress(progress_ratio, text=f"{t('dash_progress_text', lang)}: {int(progress_ratio*100)}% (¥{total_sales:,} / ¥{target_sales:,})")

    st.markdown("---")
    st.markdown(f"<div class='section-title'>{t('dash_group_list', lang)}</div>", unsafe_allow_html=True)
    for comp in companies:
        with st.container():
            c_col1, c_col2, c_col3 = st.columns([1, 4, 2])
            with c_col1:
                st.markdown(f"### {comp.get('icon', '🏢')}")
            with c_col2:
                st.markdown(f"**{comp['name']}**")
                st.write(comp.get('description', ''))
                trade_brand = comp.get('trade_name_note', '対外的な販売者名・ブランド名: noteone')
                st.caption(f"🛡️ {trade_brand}")
            with c_col3:
                status_text = "稼働中" if lang == "ja" else "Active"
                st.markdown(f"{'ステータス' if lang=='ja' else 'Status'}: :green[{comp.get('status', status_text)}]")
                st.caption(f"{'所属社員: 9名 | 制作記事数:' if lang=='ja' else 'Team: 9 Specialists | Content:'} {len(articles)} {'本' if lang=='ja' else 'Articles'}")
            st.divider()

    with st.expander(t("dash_new_sub_btn", lang)):
        st.markdown(f"#### {t('dash_form_title', lang)}")
        new_c_name = st.text_input(t("dash_form_name", lang))
        models_list = ["note記事販売", "電子書籍(Kindle)出版", "AIプロンプト販売", "SNS運用代行", "その他"] if lang == "ja" else ["note Article Publishing", "Kindle eBook Publishing", "AI Prompt Marketplace", "Social Media Management", "Other"]
        new_c_type = st.selectbox(t("dash_form_model", lang), models_list)
        new_c_icon = st.selectbox(t("dash_form_icon", lang), ["✍️", "📚", "🤖", "📈", "💡", "🎨"])
        new_c_desc = st.text_area(t("dash_form_desc", lang))
        
        if st.button(t("dash_form_submit", lang), type="primary"):
            if new_c_name.strip():
                c_id = f"company_{int(datetime.now().timestamp())}"
                success = st.session_state.holdings_manager.add_company(
                    company_id=c_id,
                    name=new_c_name,
                    company_type=new_c_type,
                    icon=new_c_icon,
                    description=new_c_desc,
                    employees=[{"id": "ceo", "name": "AI Executive Lead", "role": "CEO", "icon": "👩‍💼"}]
                )
                if success:
                    st.success(f"🎉 {'新会社' if lang=='ja' else 'New entity'} '{new_c_name}' {'が設立されました！' if lang=='ja' else 'successfully incorporated!'}")
                    st.rerun()
            else:
                st.warning("会社名を入力してください。" if lang == "ja" else "Please enter a valid company name.")

# ==========================================
# 2. 🏢 Office Room
# ==========================================
elif page_id == "office":
    st.markdown(f"<div class='main-header'>{t('office_main_header', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('office_sub_header', lang)}</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='section-title'>{t('office_sec_title', lang)}</div>", unsafe_allow_html=True)
    
    html_path = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/assets/game_office.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            game_html = f.read()
        components.html(game_html, height=545)

    # -------------------------------------------------------------
    # 💬 社員との直接対話・質問・指示デスク (Employee Consultation Desk)
    # -------------------------------------------------------------
    st.markdown("---")
    st.markdown(f"<div class='section-title'>{t('consult_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='color: #94A3B8; margin-bottom: 14px;'>{t('consult_sub', lang)}</div>", unsafe_allow_html=True)

    # ユーザーからの自由入力フォーム
    with st.form("office_consultation_form", clear_on_submit=True):
        c_in_q1, c_in_q2 = st.columns([4, 1])
        with c_in_q1:
            user_inquiry = st.text_input(
                t("consult_input_label", lang),
                placeholder=t("consult_placeholder", lang)
            )
        with c_in_q2:
            assign_options = [
                t("consult_assign_auto", lang),
                "一条 蓮 (CEO)" if lang == "ja" else "Ren Ichijo (CEO)",
                "風間 涼 (市場調査)" if lang == "ja" else "Ryo Kazama (Research)",
                "結城 紬 (編集長)" if lang == "ja" else "Tsumugi Yuki (Editor)",
                "森川 拓真 (ライター)" if lang == "ja" else "Takuma Morikawa (Writer)",
                "佐々木 翼 (広報)" if lang == "ja" else "Tsubasa Sasaki (PR)",
                "神崎 玲奈 (QA)" if lang == "ja" else "Reina Kanzaki (QA)",
                "綾瀬 七海 (人事)" if lang == "ja" else "Nanami Ayase (HR)",
                "橘 律 (法務)" if lang == "ja" else "Ritsu Tachibana (Legal)",
                "白石 葵 (財務・経理)" if lang == "ja" else "Aoi Shiraishi (Finance & Accounting)"
            ]
            target_assignee = st.selectbox(t("consult_assign_label", lang), assign_options)
        submit_inquiry = st.form_submit_button(t("consult_submit_btn", lang), type="primary", use_container_width=True)

    if submit_inquiry and user_inquiry.strip():
        assignee_map = {
            t("consult_assign_auto", lang): "auto",
            "一条 蓮 (CEO)": "ichijo", "Ren Ichijo (CEO)": "ichijo",
            "風間 涼 (市場調査)": "kazama", "Ryo Kazama (Research)": "kazama",
            "結城 紬 (編集長)": "yuki", "Tsumugi Yuki (Editor)": "yuki",
            "森川 拓真 (ライター)": "morikawa", "Takuma Morikawa (Writer)": "morikawa",
            "佐々木 翼 (広報)": "sasaki", "Tsubasa Sasaki (PR)": "sasaki",
            "神崎 玲奈 (QA)": "kanzaki", "Reina Kanzaki (QA)": "kanzaki",
            "綾瀬 七海 (人事)": "ayase", "Nanami Ayase (HR)": "ayase",
            "橘 律 (法務)": "tachibana", "Ritsu Tachibana (Legal)": "tachibana",
            "白石 葵 (財務・経理)": "shiraishi", "Aoi Shiraishi (Finance & Accounting)": "shiraishi"
        }
        chosen_emp = assignee_map.get(target_assignee, "auto")
        
        with st.spinner("担当者がデスクで回答を作成中..." if lang == "ja" else "Specialist is drafting the response..."):
            response_data = chat_manager.generate_response(user_inquiry, chosen_emp)
            st.session_state.office_chat_history.append({
                "user": user_inquiry,
                "response": response_data,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()

    # 会話履歴の表示
    if st.session_state.office_chat_history:
        st.markdown(f"#### {t('consult_log_title', lang)}")
        for item in reversed(st.session_state.office_chat_history):
            resp = item["response"]
            st.markdown(f"""
            <div class='user-query-card'>
                <div style='font-size: 0.8rem; color: #94A3B8;'>🕒 {item.get('timestamp', '')} | <strong>{t('consult_user_prefix', lang)}</strong></div>
                <div style='font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-top: 4px;'>{item['user']}</div>
            </div>
            <div class='chat-bubble'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                    <div style='font-weight: 800; color: #FFFFFF; font-size: 1.1rem;'>
                        {resp.get('icon', '🧑‍💼')} {resp.get('name', '担当社員')} <span style='font-size: 0.85rem; color: #93C5FD; font-weight: 600;'>（{resp.get('role', '')} / {resp.get('department', '')}）</span>
                    </div>
                    <span class='status-live'><span class='pulse-dot'></span>{t('consult_status_done', lang)}</span>
                </div>
                <div style='white-space: pre-wrap; font-size: 0.95rem; line-height: 1.6; color: #F8FAFC;'>{resp.get('content', '')}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button(t("consult_clear_btn", lang)):
            st.session_state.office_chat_history = []
            st.rerun()

    # -------------------------------------------------------------
    # リアルタイム社員デスク一覧
    # -------------------------------------------------------------
    st.markdown("---")
    st.markdown(f"<div class='section-title'>{t('floor_status_title', lang)}</div>", unsafe_allow_html=True)
    
    st.markdown(f"#### {t('floor_exec_title', lang)}")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown(f"""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>👩‍💼</span>
                <span class='status-live'><span class='pulse-dot'></span>{'執務中' if lang=='ja' else 'Active'}</span>
            </div>
            <div style='font-weight: 800; font-size: 1.15rem; color: #FFFFFF; margin-top: 4px;'>{'一条 蓮' if lang=='ja' else 'Ren Ichijo'}</div>
            <div style='font-size: 0.85rem; color: #93C5FD; font-weight: 700;'>{'代表取締役CEO' if lang=='ja' else 'Chief Executive Officer'}</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 CEO Executive Suite</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 10px; border-radius: 6px; border: 1px solid #334155;'>💬 {'「全社売上最大化と、完全無料運用の規律を監督しています。」' if lang=='ja' else '"Supervising overall revenue maximization and ensuring 100% zero-cost operations."'}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_f2:
        st.markdown(f"""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>⚖️</span>
                <span class='status-live'><span class='pulse-dot'></span>{'法務監視中' if lang=='ja' else 'Monitoring'}</span>
            </div>
            <div style='font-weight: 800; font-size: 1.15rem; color: #FFFFFF; margin-top: 4px;'>{'橘 律' if lang=='ja' else 'Ritsu Tachibana'}</div>
            <div style='font-size: 0.85rem; color: #CBD5E1; font-weight: 700;'>{'法務課 / 法務顧問' if lang=='ja' else 'Legal & Compliance Counsel'}</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 Legal Department</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 10px; border-radius: 6px; border: 1px solid #334155;'>💬 {'「会社法・著作権法・note規約の適合性を常時スクリーニングしています。」' if lang=='ja' else '"Continuously screening compliance with corporate law, copyright, and platform terms."'}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_f3:
        st.markdown(f"""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>🤝</span>
                <span class='status-live'><span class='pulse-dot'></span>{'負荷監視中' if lang=='ja' else 'Active'}</span>
            </div>
            <div style='font-weight: 800; font-size: 1.15rem; color: #FFFFFF; margin-top: 4px;'>{'綾瀬 七海' if lang=='ja' else 'Nanami Ayase'}</div>
            <div style='font-size: 0.85rem; color: #6EE7B7; font-weight: 700;'>{'人事課 / 人事責任者' if lang=='ja' else 'HR & Culture Director'}</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 HR Department</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 10px; border-radius: 6px; border: 1px solid #334155;'>💬 {'「各社員の業務負荷スコアを測定し、過負荷を未然に防止しています。」' if lang=='ja' else '"Monitoring workload metrics across all specialists to prevent operational bottlenecks."'}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"#### {t('floor_edit_title', lang)}")
    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    with col_c1:
        st.markdown(f"""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>🔍</span>
                <span class='status-live'><span class='pulse-dot'></span>{'調査中' if lang=='ja' else 'Analyzing'}</span>
            </div>
            <div style='font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-top: 4px;'>{'風間 涼' if lang=='ja' else 'Ryo Kazama'}</div>
            <div style='font-size: 0.85rem; color: #5EEAD4; font-weight: 700;'>{'市場調査課' if lang=='ja' else 'Market Research Analyst'}</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 Research Desk</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 8px; border-radius: 6px; border: 1px solid #334155;'>💬 {'「note売れ筋トレンドと読者ペルソナを分析中です。」' if lang=='ja' else '"Analyzing note sales trends and subscriber personas in real time."'}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_c2:
        st.markdown(f"""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>📑</span>
                <span class='status-live'><span class='pulse-dot'></span>{'構成中' if lang=='ja' else 'Structuring'}</span>
            </div>
            <div style='font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-top: 4px;'>{'結城 紬' if lang=='ja' else 'Tsumugi Yuki'}</div>
            <div style='font-size: 0.85rem; color: #FCD34D; font-weight: 700;'>{'記事制作課 (編集長)' if lang=='ja' else 'Editor-in-Chief'}</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 Editorial Studio</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 8px; border-radius: 6px; border: 1px solid #334155;'>💬 {'「購入率を高める有料ラインの境界線を設計しています。」' if lang=='ja' else '"Designing optimal paywall thresholds to maximize conversion rates."'}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_c3:
        st.markdown(f"""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>✍️</span>
                <span class='status-live'><span class='pulse-dot'></span>{'執筆待機' if lang=='ja' else 'Drafting'}</span>
            </div>
            <div style='font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-top: 4px;'>{'森川 拓真' if lang=='ja' else 'Takuma Morikawa'}</div>
            <div style='font-size: 0.85rem; color: #FDBA74; font-weight: 700;'>{'記事制作課 (ライター)' if lang=='ja' else 'Chief Content Writer'}</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 Writer Studio</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 8px; border-radius: 6px; border: 1px solid #334155;'>💬 {'「コピペで使える実践テンプレート執筆スタンバイ完了。」' if lang=='ja' else '"Drafting actionable copy-and-paste practical templates."'}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_c4:
        st.markdown(f"""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>🛡️</span>
                <span class='status-live'><span class='pulse-dot'></span>{'QA待機' if lang=='ja' else 'QA Ready'}</span>
            </div>
            <div style='font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-top: 4px;'>{'神崎 玲奈' if lang=='ja' else 'Reina Kanzaki'}</div>
            <div style='font-size: 0.85rem; color: #FCA5A5; font-weight: 700;'>{'品質管理課 (QA)' if lang=='ja' else 'Quality Assurance Director'}</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 QA Inspection Booth</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 8px; border-radius: 6px; border: 1px solid #334155;'>💬 {'「信憑性と100点採点スコアリングの準備万全です。」' if lang=='ja' else '"Conducting rigorous fact-checking and automated 100-point quality scoring."'}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"#### {t('floor_pr_fin_title', lang)}")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f"""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>📢</span>
                <span class='status-live'><span class='pulse-dot'></span>{'5大SNS待機' if lang=='ja' else 'Broadcasting'}</span>
            </div>
            <div style='font-weight: 800; font-size: 1.15rem; color: #FFFFFF; margin-top: 4px;'>{'佐々木 翼' if lang=='ja' else 'Tsubasa Sasaki'}</div>
            <div style='font-size: 0.85rem; color: #93C5FD; font-weight: 700;'>{'広報課' if lang=='ja' else 'Multi-SNS PR Specialist'}</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 PR Hub</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 10px; border-radius: 6px; border: 1px solid #334155;'>💬 {'「X・IG・Threads・Bluesky・Mastodonへの自動プロモーション待機中。」' if lang=='ja' else '"Automated multi-channel syndication ready for X, Threads, IG, Bluesky, Mastodon."'}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>📊</span>
                <span class='status-live'><span class='pulse-dot'></span>{'財務・経理分析中' if lang=='ja' else 'Auditing'}</span>
            </div>
            <div style='font-weight: 800; font-size: 1.15rem; color: #FFFFFF; margin-top: 4px;'>{'白石 葵' if lang=='ja' else 'Aoi Shiraishi'}</div>
            <div style='font-size: 0.85rem; color: #C4B5FD; font-weight: 700;'>{'財務課 ＆ 経理課' if lang=='ja' else 'Financial Strategist & Chief Accountant'}</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 Finance & Accounting</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 10px; border-radius: 6px; border: 1px solid #334155;'>💬 {'「システム維持費0円（完全無料）確認済。価格シミュレーション準備完了。」' if lang=='ja' else '"Verified ¥0 monthly fixed costs. Ready for price optimization models."'}</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 3. 🔍 Market Research Division & 👑 Topic Approval Center
# ==========================================
elif page_id == "market_research":
    st.markdown(f"<div class='main-header'>{t('mr_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('mr_sub', lang)}</div>", unsafe_allow_html=True)
    
    st.info(t("mr_mission", lang))
    
    # -------------------------------------------------------------
    # 1. 🔍 新規トピック市場調査の指示フォーム
    # -------------------------------------------------------------
    with st.expander(f"➕ {t('mr_new_research_header', lang)}", expanded=False):
        c_rs1, c_rs2 = st.columns([3, 2])
        with c_rs1:
            rs_kw = st.text_input(t("mr_keyword_label", lang), placeholder=t("mr_keyword_ph", lang))
        with c_rs2:
            rs_aud = st.text_input(t("mr_audience_label", lang), placeholder=t("mr_audience_ph", lang))
        
        if st.button(t("mr_btn_research", lang), type="primary", use_container_width=True):
            if rs_kw.strip():
                with st.spinner("風間アナリストがnote市場・競合ギャップを調査中..."):
                    new_tp = market_manager.conduct_research(rs_kw, rs_aud)
                    st.success(f"🎉 新規トピック『{new_tp['title']}』の市場調査が完了し、承認待ちとして登録されました！")
                    st.rerun()
            else:
                st.warning("調査キーワードを入力してください。")

    st.markdown("---")

    # -------------------------------------------------------------
    # 2. 📋 調査トピック管理台帳 ＆ 👑 企画決裁ゲートウェイ
    # -------------------------------------------------------------
    st.markdown(f"<div class='section-title'>{t('mr_topic_list_header', lang)}</div>", unsafe_allow_html=True)
    topics = market_manager.list_topics()
    
    if not topics:
        st.info("調査トピックがありません。上記フォームから新規調査を指示してください。")
    else:
        topic_titles = [f"[{tp.get('status', 'Pending Owner Approval')}] {tp.get('category', '')} | {tp.get('title', '')}" for tp in topics]
        sel_tp_idx = st.selectbox(t("mr_select_topic_label", lang), range(len(topics)), format_func=lambda x: topic_titles[x])
        tp = topics[sel_tp_idx]
        tp_status = tp.get("status", "Pending Owner Approval")
        tp_locked = tp_status in ["Pending Owner Approval", "Revision Requested"]

        if tp_locked:
            st.markdown(f"""
            <div class='approval-box-locked'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <h3 style='color: #FCD34D !important; margin:0;'>🔒 Status: {tp_status}</h3>
                    <span style='background:#F59E0B; color:#000; font-weight:800; padding:4px 10px; border-radius:6px;'>企画承認待ち</span>
                </div>
                <div style='margin-top: 10px; font-size: 0.95rem; line-height: 1.6;'>
                    {t('mr_topic_locked_warning', lang)}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='approval-box-approved'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <h3 style='color: #6EE7B7 !important; margin:0;'>✅ Status: {tp_status}</h3>
                    <span style='background:#10B981; color:#000; font-weight:800; padding:4px 10px; border-radius:6px;'>企画承認済み</span>
                </div>
                <div style='margin-top: 10px; font-size: 0.95rem; line-height: 1.6;'>
                    {t('mr_topic_unlocked_success', lang)}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 👑 トピック決裁アクションボタン
        col_tpa1, col_tpa2, col_tpa3 = st.columns([2, 2, 1])
        with col_tpa1:
            if st.button(t("mr_btn_approve_topic", lang), type="primary", use_container_width=True):
                market_manager.approve_topic(tp["id"])
                st.success("🎉 トピックを承認しました！記事制作課へ送ることができます。")
                st.rerun()

        with col_tpa2:
            with st.popover(t("mr_btn_revise_topic", lang), use_container_width=True):
                st.markdown(f"#### {t('mr_btn_revise_topic', lang)}")
                rev_fb = st.text_area(t("mr_topic_feedback_label", lang), placeholder=t("mr_topic_feedback_ph", lang))
                if st.button("📨 再調査指示を送信する", type="primary"):
                    if rev_fb.strip():
                        market_manager.request_revision(tp["id"], rev_fb)
                        st.warning("風間アナリストに再調査・切り口変更指示を伝達しました。")
                        st.rerun()
                    else:
                        st.error("指示内容を入力してください。")

        with col_tpa3:
            if st.button(t("mr_btn_reject_topic", lang), use_container_width=True):
                market_manager.reject_topic(tp["id"])
                st.info("トピックを却下しました。")
                st.rerun()

        # 承認済みの場合の「記事制作課へ直接引き渡し」ボタン
        if not tp_locked:
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            if st.button(t("mr_btn_send_to_creation", lang), type="primary", use_container_width=True):
                st.session_state.prefill_topic = tp.get("title", "")
                st.session_state.prefill_audience = tp.get("target_audience", "")
                st.session_state.active_page_id = "content_creation"
                st.rerun()

        st.markdown("---")

        # トピック調査レポート詳細カード
        st.markdown("#### 📊 市場調査詳細レポート (風間 涼 提出)")
        c_rep1, c_rep2 = st.columns(2)
        with c_rep1:
            st.markdown(f"""
            <div class='content-box'>
                <h4 style='color:#38BDF8; margin-top:0;'>🎯 ターゲット読者 ＆ カテゴリ</h4>
                <p><strong>カテゴリ:</strong> {tp.get('category', '実務ノウハウ')}</p>
                <p><strong>想定読者ペルソナ:</strong> {tp.get('target_audience', '')}</p>
                <p><strong>推奨販売価格:</strong> ¥{tp.get('recommended_price', 500):,} (ROI最適化)</p>
            </div>
            """, unsafe_allow_html=True)
        with c_rep2:
            st.markdown(f"""
            <div class='content-box'>
                <h4 style='color:#4ADE80; margin-top:0;'>🔥 市場ニーズ ＆ 競合差別化ギャップ</h4>
                <p><strong>市場ニーズ:</strong> {tp.get('demand_summary', '')}</p>
                <p><strong>競合差別化の武器:</strong> {tp.get('competitor_gap', '')}</p>
            </div>
            """, unsafe_allow_html=True)

        # タイムスタンプ履歴
        st.markdown("##### ⏱️ 企画ステータス遷移タイムスタンプ履歴")
        history = tp.get("status_history", [])
        for h in reversed(history):
            note_str = f" - <em>{h.get('note')}</em>" if h.get('note') else ""
            st.markdown(f"- 🕒 **{h.get('timestamp')}** ➔ `[{h.get('status')}]` ({h.get('actor', '')}){note_str}", unsafe_allow_html=True)

# ==========================================
# 4. ✍️ Content Creation Division
# ==========================================
elif page_id == "content_creation":
    st.markdown(f"<div class='main-header'>{t('cc_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('cc_sub', lang)}</div>", unsafe_allow_html=True)

    if st.session_state.prefill_topic:
        st.success(f"📥 **市場調査課から承認済みトピックを引き継ぎました:** 『{st.session_state.prefill_topic}』")

    st.markdown(f"#### {t('cc_form_title', lang)}")
    c_in1, c_in2 = st.columns([3, 1])
    with c_in1:
        init_topic = st.session_state.prefill_topic if st.session_state.prefill_topic else ""
        init_audience = st.session_state.prefill_audience if st.session_state.prefill_audience else ""
        
        topic_input = st.text_input(
            t("cc_topic_label", lang),
            value=init_topic,
            placeholder=t("cc_topic_ph", lang)
        )
        audience_input = st.text_input(
            t("cc_target_label", lang),
            value=init_audience,
            placeholder=t("cc_target_ph", lang)
        )
    with c_in2:
        price_opts = [t("cc_price_opt_auto", lang), t("cc_price_opt_500", lang), t("cc_price_opt_300", lang), t("cc_price_opt_prem", lang)]
        price_input = st.selectbox(t("cc_price_label", lang), price_opts)
        st.write("")
        start_btn = st.button(t("cc_start_btn", lang), type="primary", use_container_width=True)

    if start_btn:
        if not topic_input.strip():
            st.warning("⚠️ 記事のテーマを入力してください。" if lang == "ja" else "⚠️ Please enter a topic for the article.")
        else:
            st.markdown(f"### {t('cc_stream_title', lang)}")
            progress_bar = st.progress(0)
            status_text = st.empty()
            meeting_container = st.container()
            
            pipeline = workflow.run_creation_pipeline(
                topic=topic_input,
                target_audience=audience_input,
                price_preference=price_input
            )
            
            completed_article = None
            for event in pipeline:
                step = event.get("step", 1)
                progress_bar.progress(step / 10)
                
                if event.get("status") == "thinking":
                    status_text.markdown(f"⏳ **{event.get('message')}**")
                elif event.get("status") == "done":
                    log = event.get("log", {})
                    with meeting_container:
                        st.markdown(f"""
                        <div class='chat-bubble'>
                            <div style='font-weight: 800; color: #FFFFFF;'>{log.get('icon')} {log.get('name')} <span style='font-size: 0.8rem; color: #94A3B8;'>({log.get('role')})</span></div>
                            <div style='white-space: pre-wrap; margin-top: 6px; font-size: 0.95rem; color: #F8FAFC;'>{log.get('content')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                elif event.get("status") == "completed":
                    completed_article = event.get("article")
                    progress_bar.progress(1.0)
                    status_text.markdown("🔒 **全工程完了！記事はオーナー最終承認待ちとして安全にロックされました。**" if lang == "ja" else "🔒 **Full pipeline completed! Article is securely locked awaiting owner final approval.**")
            
            if completed_article:
                # Clear prefill
                st.session_state.prefill_topic = ""
                st.session_state.prefill_audience = ""
                st.success(f"🎉 記事『{completed_article['title']}』が作成されました！「✨ {t('nav_qa', lang)}」にて最終承認を行ってください。" if lang == "ja" else f"🎉 Article '{completed_article['title']}' created! Please review and approve in '✨ {t('nav_qa', lang)}'.")

# ==========================================
# 5. 📢 Public Relations Division
# ==========================================
elif page_id == "pr":
    st.markdown(f"<div class='main-header'>{t('pr_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('pr_sub', lang)}</div>", unsafe_allow_html=True)

    st.markdown(f"#### {t('pr_hub_title', lang)}")
    cfg_path = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/sns_config.json")
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            sns_cfg = json.load(f)
    else:
        sns_cfg = {}
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        x_acc = st.text_input("🐦 X (Twitter) Account", value=sns_cfg.get("x", {}).get("account_name", "@NoteOneSystems"))
        ig_acc = st.text_input("📸 Instagram Profile", value=sns_cfg.get("instagram", {}).get("account_name", "@noteonesystems_official"))
        th_acc = st.text_input("🧵 Threads Username", value=sns_cfg.get("threads", {}).get("account_name", "@noteonesystems_official"))
    with col_s2:
        bs_handle = st.text_input("🦋 Bluesky Handle", value=sns_cfg.get("bluesky", {}).get("handle", "noteonesystems.bsky.social"))
        mast_inst = st.text_input("🐘 Mastodon Instance URL", value=sns_cfg.get("mastodon", {}).get("instance", "https://mstdn.jp"))
    
    if st.button(t("pr_save_btn", lang), type="primary"):
        sns_cfg["x"] = {"account_name": x_acc}
        sns_cfg["instagram"] = {"account_name": ig_acc}
        sns_cfg["threads"] = {"account_name": th_acc}
        sns_cfg["bluesky"] = {"handle": bs_handle}
        sns_cfg["mastodon"] = {"instance": mast_inst}
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(sns_cfg, f, ensure_ascii=False, indent=2)
        st.success("広報課のSNS設定を保存しました。" if lang == "ja" else "Social media configuration saved successfully.")

# ==========================================
# 6. ✨ Quality Assurance Division & 👑 Executive Approval Center
# ==========================================
elif page_id == "qa":
    st.markdown(f"<div class='main-header'>{t('qa_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('qa_sub', lang)}</div>", unsafe_allow_html=True)

    articles = workflow.list_articles()
    
    if not articles:
        st.info(t("qa_no_articles", lang))
    else:
        article_titles = [f"[{art.get('status', 'Pending Owner Approval')}] {art.get('created_at', '')} | {art.get('title', '')}" for art in articles]
        selected_idx = st.selectbox(t("qa_select_label", lang), range(len(articles)), format_func=lambda x: article_titles[x])
        art = articles[selected_idx]
        cur_status = art.get("status", "Pending Owner Approval")
        
        # ==============================================================
        # 👑 オーナー最終承認ゲートウェイ (Executive Approval Gateway)
        # ==============================================================
        st.markdown(f"<div class='section-title'>{t('qa_approval_header', lang)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#94A3B8; margin-bottom:12px;'>{t('qa_approval_sub', lang)}</div>", unsafe_allow_html=True)

        is_locked = cur_status in ["Pending Owner Approval", "Revision Requested"]
        
        if is_locked:
            st.markdown(f"""
            <div class='approval-box-locked'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <h3 style='color: #FCD34D !important; margin:0;'>🔒 Status: {cur_status}</h3>
                    <span style='background:#F59E0B; color:#000; font-weight:800; padding:4px 10px; border-radius:6px;'>決裁待ち</span>
                </div>
                <div style='margin-top: 10px; font-size: 0.95rem; line-height: 1.6;'>
                    {t('qa_locked_warning', lang)}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='approval-box-approved'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <h3 style='color: #6EE7B7 !important; margin:0;'>✅ Status: {cur_status}</h3>
                    <span style='background:#10B981; color:#000; font-weight:800; padding:4px 10px; border-radius:6px;'>承認済み</span>
                </div>
                <div style='margin-top: 10px; font-size: 0.95rem; line-height: 1.6;'>
                    {t('qa_unlocked_success', lang)}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 👑 オーナー決裁アクションパネル
        app_col1, app_col2, app_col3 = st.columns([2, 2, 1])
        with app_col1:
            if st.button(t("qa_btn_approve", lang), type="primary", use_container_width=True):
                workflow.approve_article(art["id"])
                st.success("🎉 オーナー最終承認が完了し、投稿ロックを解除しました！" if lang == "ja" else "🎉 Approved by owner! Publishing lock has been released.")
                st.rerun()

        with app_col2:
            with st.popover(t("qa_btn_revision", lang), use_container_width=True):
                st.markdown(f"#### {t('qa_btn_revision', lang)}")
                feedback_txt = st.text_area(t("qa_feedback_label", lang), placeholder=t("qa_feedback_ph", lang))
                if st.button("📨 修正指示を送信する", type="primary"):
                    if feedback_txt.strip():
                        workflow.request_revision(art["id"], feedback_txt)
                        st.warning("編集部に修正指示を伝達しました。" if lang == "ja" else "Revision directive sent to editorial team.")
                        st.rerun()
                    else:
                        st.error("修正指示内容を入力してください。")

        with app_col3:
            if st.button(t("qa_btn_reject", lang), use_container_width=True):
                workflow.reject_article(art["id"])
                st.info("記事を却下・アーカイブしました。" if lang == "ja" else "Article rejected and archived.")
                st.rerun()

        st.markdown("---")

        # 審査データ（法務チェック & QAスコア）
        col_chk1, col_chk2 = st.columns(2)
        with col_chk1:
            st.markdown("#### ⚖️ 法務課 スクリーニング審査 (橘 律)")
            st.markdown(f"""
            <div style='background-color:#0F172A; border:1px solid #334155; border-left:4px solid #38BDF8; border-radius:8px; padding:14px; color:#F8FAFC;'>
                {art.get('legal_check', '審査中')}
            </div>
            """, unsafe_allow_html=True)
        with col_chk2:
            st.markdown("#### 🛡️ 品質管理課 100点採点スコア (神崎 玲奈)")
            st.markdown(f"""
            <div style='background-color:#0F172A; border:1px solid #334155; border-left:4px solid #F59E0B; border-radius:8px; padding:14px; color:#F8FAFC;'>
                {art.get('qa_score', '採点中')}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # タイムスタンプ履歴
        st.markdown(f"##### {t('qa_history_title', lang)}")
        history = art.get("status_history", [])
        for h in reversed(history):
            note_str = f" - <em>{h.get('note')}</em>" if h.get('note') else ""
            st.markdown(f"- 🕒 **{h.get('timestamp')}** ➔ `[{h.get('status')}]` ({h.get('actor', '')}){note_str}", unsafe_allow_html=True)
        
        st.divider()

        # 記事プレビュー
        st.markdown(f"#### {t('qa_preview_title', lang)}")
        content = art.get("content", "")
        if "🔒 ここから先は有料エリアです" in content or "🔒 [Paywall] Premium Section Starts Here" in content:
            delimiter = "🔒 ここから先は有料エリアです" if "🔒 ここから先は有料エリアです" in content else "🔒 [Paywall] Premium Section Starts Here"
            parts = content.split(delimiter)
            st.markdown(parts[0])
            st.markdown(f"""
            <div style='background-color: #1E293B; border: 2px dashed #F59E0B; border-radius: 8px; padding: 14px; margin: 14px 0;'>
                <strong style='color: #FCD34D;'>{t('qa_paywall_badge', lang)}</strong>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(parts[1])
        else:
            st.markdown(content)
        
        st.divider()

        # 5大SNS広告文
        st.markdown(f"#### {t('qa_sns_copy_title', lang)}")
        if is_locked:
            st.info("🔒 【保護中】オーナー最終承認が完了すると、ここからSNSへの直接投稿が可能になります。")
        st.text_area("Social Promotion Copy", value=art.get("marketing", ""), height=200, disabled=is_locked)
        
        # マークダウン全文
        st.markdown(f"#### {t('qa_markdown_title', lang)}")
        if is_locked:
            st.warning("🔒 【ロック中】オーナー承認が出るまでnoteへの貼り付けコードは保護されています。")
            st.code("🔒 LOCKED: Awaiting Owner Final Approval (承認ボタンを押すとロックが解除されます)", language="text")
        else:
            st.success("✅ 【ロック解除済】以下のマークダウンをnoteの記事エディタにそのまま貼り付けて公開できます！")
            st.text_area("Markdown Source (note editor ready)", value=art.get("content", ""), height=300)

# ==========================================
# 7. 🤝 Human Resources Division
# ==========================================
elif page_id == "hr":
    st.markdown(f"<div class='main-header'>{t('hr_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('hr_sub', lang)}</div>", unsafe_allow_html=True)

    st.markdown(f"#### {t('hr_org_title', lang)}")
    with open(os.path.join(os.path.dirname(__file__), "companies/note_one_systems/org_chart_and_job_descriptions.json"), "r", encoding="utf-8") as f:
        org_data = json.load(f)
    
    st.write(f"**{'制定者:' if lang=='ja' else 'Authorized by:'}** {org_data.get('author')} | **{'バージョン:' if lang=='ja' else 'Version:'}** {org_data.get('version')}")
    
    with st.expander(t("hr_view_ledger", lang)):
        for dept in org_data["departments"]:
            st.markdown(f"**{dept['icon']} {dept['name']}** ({'統括:' if lang=='ja' else 'Lead:'} {dept['head']})")
            for role in dept["roles"]:
                st.write(f"- **{role['role_name']} ({role['member']})**: {', '.join(role['responsibilities'][:2])}")
    
    st.markdown(f"#### {t('hr_workload_title', lang)}")
    stats = st.session_state.hr_manager.get_workload_stats()
    df_data = []
    for emp_id, data in stats.items():
        df_data.append({
            "社員名" if lang=="ja" else "Employee Name": data["name"],
            "役職" if lang=="ja" else "Role": data["role"],
            "タスク回数" if lang=="ja" else "Tasks Executed": data["tasks"],
            "生成文字数" if lang=="ja" else "Words Generated": f"{data['words_generated']:,} {'字' if lang=='ja' else 'words'}",
            "負荷スコア" if lang=="ja" else "Workload Score": f"{data['workload_score']}%"
        })
    st.dataframe(pd.DataFrame(df_data), use_container_width=True)
    
    proposals = st.session_state.hr_manager.get_staffing_proposals()
    if proposals:
        for prop in proposals:
            st.warning(f"**【増員提案】対象部署: {prop['target_role']}（{prop['target_name']} / 負荷: {prop['workload_score']}%）** ➔ {prop['proposed_role']} の増員（費用0円）" if lang == "ja" else f"**[Staffing Proposal] Target Unit: {prop['target_role']} ({prop['target_name']} / Load: {prop['workload_score']}%)** ➔ Recommended Addition: {prop['proposed_role']}")

# ==========================================
# 8. 📚 Legal & Compliance Division
# ==========================================
elif page_id == "legal":
    st.markdown(f"<div class='main-header'>{t('legal_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('legal_sub', lang)}</div>", unsafe_allow_html=True)

    st.markdown(f"#### {t('legal_ledger_title', lang)}")
    legal_file = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/legal_investigations.json")
    if os.path.exists(legal_file):
        with open(legal_file, "r", encoding="utf-8") as f:
            legal_inv = json.load(f)
    else:
        legal_inv = {"investigations": []}
    
    for inv in legal_inv["investigations"]:
        st.markdown(f"""
        <div style='background-color: #1E293B; border: 1px solid #334155; border-left: 4px solid #38BDF8; border-radius: 8px; padding: 16px; margin-bottom: 14px; color: #F8FAFC;'>
            <div style='display: flex; justify-content: space-between;'>
                <strong style='font-size: 1.1rem; color: #FFFFFF;'>📋 {inv['category']} (ID: {inv['id']})</strong>
                <span>{inv['status']}</span>
            </div>
            <div style='font-size: 0.8rem; color: #94A3B8; margin: 4px 0;'>
                🕒 {'受付' if lang=='ja' else 'Received'}: {inv['received_at']} | {'調査開始' if lang=='ja' else 'Review Started'}: {inv['started_at']} | {'完了' if lang=='ja' else 'Completed'}: {inv['completed_at']}
            </div>
            <div style='font-size: 0.9rem; color: #E2E8F0;'><strong>{'相談元:' if lang=='ja' else 'Originating Unit:'}</strong> {inv['requester_dept']}</div>
            <div style='font-size: 0.9rem; color: #E2E8F0; margin-top: 4px;'><strong>{'受付内容:' if lang=='ja' else 'Inquiry Summary:'}</strong> {inv['inquiry_content']}</div>
            <div style='background-color: #0F172A; border: 1px solid #334155; padding: 12px; border-radius: 6px; margin-top: 10px; font-size: 0.9rem; color: #F8FAFC;'>
                <strong style='color: #38BDF8;'>⚖️ {'橘 律 法的見解:' if lang=='ja' else 'Formal Legal Opinion:'}</strong> {inv['legal_opinion']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 9. 📊 Financial Strategy Division
# ==========================================
elif page_id == "finance":
    st.markdown(f"<div class='main-header'>{t('fin_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('fin_sub', lang)}</div>", unsafe_allow_html=True)

    st.markdown(f"#### {t('fin_target_title', lang)}")
    target_file = os.path.join(os.path.dirname(__file__), "data/sales_targets.json")
    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            target_data = json.load(f)
    else:
        target_data = {"monthly_target_yen": 100000, "target_articles_monthly": 15}
    
    c_tar1, c_tar2 = st.columns([2, 3])
    with c_tar1:
        new_target = st.number_input(t("fin_target_amt_label", lang), min_value=10000, max_value=10000000, value=target_data.get("monthly_target_yen", 100000), step=10000)
        target_arts = st.slider(t("fin_target_art_label", lang), min_value=5, max_value=60, value=target_data.get("target_articles_monthly", 15))
        if st.button(t("fin_submit_btn", lang), type="primary"):
            target_data["monthly_target_yen"] = int(new_target)
            target_data["target_articles_monthly"] = int(target_arts)
            target_data["updated_at"] = datetime.now().strftime("%Y-%m-%d")
            with open(target_file, "w", encoding="utf-8") as f:
                json.dump(target_data, f, ensure_ascii=False, indent=2)
            st.success("売上目標を更新しました。" if lang == "ja" else "Revenue directives updated successfully.")
            st.rerun()
    with c_tar2:
        daily_req = int(new_target / 500 / 30)
        if lang == "ja":
            st.info(f"""
            **【財務逆算プラン】**
            - 🎯 **日別必要販売数:** 約 **{max(1, daily_req)}部**（単価500円想定）
            - 📝 **推奨リリース頻度:** 月 **{target_arts}本**
            - 💡 **財務アドバイス:** 500円入門記事で読者を集め、月末に1,480円のマガジンを投入するモデルが最も高収益です。
            """)
        else:
            st.info(f"""
            **[Financial Strategy Blueprint]**
            - 🎯 **Required Daily Unit Sales:** approx. **{max(1, daily_req)} copies** (at 500 JPY unit price)
            - 📝 **Recommended Publication Cadence:** **{target_arts} articles / month**
            - 💡 **Strategic Advice:** Acquire initial audience with 500 JPY entry articles, followed by high-ticket 1,480 JPY monthly premium bundles.
            """)

# ==========================================
# 10. 💳 Accounting & Operations Division
# ==========================================
elif page_id == "accounting":
    st.markdown(f"<div class='main-header'>{t('acc_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('acc_sub', lang)}</div>", unsafe_allow_html=True)

    st.markdown(f"#### {t('acc_ledger_title', lang)}")
    acc_file = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/accounting_data.json")
    if os.path.exists(acc_file):
        with open(acc_file, "r", encoding="utf-8") as f:
            acc_data = json.load(f)
    else:
        acc_data = {"monthly_total_cost_yen": 0, "cost_items": []}
    
    st.success(f"**{t('acc_total_cost_prefix', lang)}** :green[**{t('acc_total_cost_val', lang)}**]")
    
    cost_df = []
    for item in acc_data.get("cost_items", []):
        cost_df.append({
            "カテゴリ" if lang=="ja" else "Category": item["category"],
            "サービス名" if lang=="ja" else "Service Provider": item["service_name"],
            "利用プラン" if lang=="ja" else "Tier / Plan": item["plan"],
            "月額費用" if lang=="ja" else "Monthly Cost": f"¥{item['monthly_cost_yen']:,}",
            "稼働状態" if lang=="ja" else "Operating Status": item["status"],
            "備考" if lang=="ja" else "Audit Notes": item["notes"]
        })
    st.dataframe(pd.DataFrame(cost_df), use_container_width=True)
    st.caption("🛡️ **経理課ポリシー**: 就業規則第4条に基づき、代表者の稟議承認がない限り、1円たりとも課金は発生しません。" if lang == "ja" else "🛡️ **Strict Policy Enforcement**: Pursuant to Corporate Rule Art. 4, zero financial liabilities or cloud expenses are incurred without prior executive ringi approval.")

# ==========================================
# 11. 💻 IT Helpdesk & Error Logs
# ==========================================
elif page_id == "helpdesk":
    st.markdown(f"<div class='main-header'>{t('it_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('it_sub', lang)}</div>", unsafe_allow_html=True)

    err_file = os.path.join(os.path.dirname(__file__), "data/error_logs.json")
    if os.path.exists(err_file):
        with open(err_file, "r", encoding="utf-8") as f:
            err_data = json.load(f)
    else:
        err_data = {"errors": []}

    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        st.metric(label=t("it_total_label", lang), value=f"{len(err_data.get('errors', []))} {'件' if lang=='ja' else 'Cases'}")
    with col_e2:
        st.metric(label=t("it_resolved_label", lang), value=f"{len([e for e in err_data.get('errors', []) if '解決' in e.get('status', '') or 'Resolved' in e.get('status', '')])} {'件' if lang=='ja' else 'Cases'}")
    with col_e3:
        st.metric(label=t("it_health_label", lang), value="100% (正常稼働)" if lang == "ja" else "100% Operational")

    st.markdown("---")
    st.markdown(f"<div class='section-title'>{t('it_ledger_title', lang)}</div>", unsafe_allow_html=True)
    
    for err in err_data.get("errors", []):
        with st.container():
            st.markdown(f"""
            <div style='background-color: #1E293B; border: 1px solid #334155; border-left: 5px solid #38BDF8; border-radius: 10px; padding: 18px; margin-bottom: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.25); color: #F8FAFC;'>
                <div style='display: flex; justify-content: space-between;'>
                    <strong style='font-size: 1.15rem; color: #FFFFFF;'>⚠️ {err['module']} (ID: {err['id']})</strong>
                    <span>{err['status']}</span>
                </div>
                <div style='font-size: 0.8rem; color: #94A3B8; margin: 4px 0;'>🕒 {'発生日時' if lang=='ja' else 'Occurred'}: {err['occurred_at']}</div>
                <div style='background-color: #450A0A; border: 1px solid #991B1B; padding: 10px; border-radius: 6px; font-family: monospace; font-size: 0.85rem; color: #FCA5A5; margin: 8px 0;'>
                    {err['error_message']}
                </div>
                <div style='font-size: 0.9rem; color: #E2E8F0;'><strong>🔍 {'原因分析:' if lang=='ja' else 'Root Cause Analysis:'}</strong> {err['root_cause']}</div>
                <div style='font-size: 0.9rem; color: #4ADE80; margin-top: 4px;'><strong>🛠️ {'対処手順・解決法:' if lang=='ja' else 'Resolution Procedure:'}</strong> {err['solution']}</div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# 12. 👥 Employee Profiles
# ==========================================
elif page_id == "profiles":
    st.markdown(f"<div class='main-header'>{t('prof_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('prof_sub', lang)}</div>", unsafe_allow_html=True)
    
    with open(os.path.join(os.path.dirname(__file__), "companies/note_one_systems/company_info.json"), "r", encoding="utf-8") as f:
        comp_info = json.load(f)

    for emp in comp_info["employees"]:
        with st.expander(f"{emp['icon']} {emp['name']} ({emp['role']}) - {'フォルダ:' if lang=='ja' else 'Directory:'} employees/{emp['folder']}/"):
            col_e1, col_e2 = st.columns([1, 2])
            with col_e1:
                st.markdown(f"**{'部署:' if lang=='ja' else 'Department:'}** {emp.get('department', '')}")
                st.markdown(f"**{'モットー:' if lang=='ja' else 'Professional Motto:'}** {emp['motto']}")
                st.markdown(f"**{'スキル:' if lang=='ja' else 'Core Competencies:'}** {', '.join(emp['skills'])}")
            with col_e2:
                st.markdown(f"**{'システムプロンプト (prompt.txt):' if lang=='ja' else 'System Prompt (prompt.txt):'}**")
                st.code(emp['prompt'], language="text")

# ==========================================
# 13. ☁️ 24/7 Free Cloud Setup Guide
# ==========================================
elif page_id == "cloud_guide":
    st.markdown(f"<div class='main-header'>{t('cloud_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('cloud_sub', lang)}</div>", unsafe_allow_html=True)
    
    if lang == "ja":
        st.markdown("""
        ### 🎯 完全無料（0円）でクラウド稼働させる3ステップ
        
        #### 1️⃣ ステップ1: GitHub（無料）にプログラムを保存
        1. [GitHub](https://github.com/) にアクセスし、新しいリポジトリ（PrivateまたはPublic）を作成します。
        2. このフォルダ（`ai_holdings_platform`）内のファイルをアップロードします。

        #### 2️⃣ ステップ2: Streamlit Community Cloud（無料）に連携
        1. [Streamlit Community Cloud](https://share.streamlit.io/) にアクセスし、GitHubでサインインします。
        2. 「Create app」から上記リポジトリと `app.py` を選択して「Deploy」を押します。

        #### 3️⃣ ステップ3: 無料のGemini APIキーをセット
        1. Streamlit Cloudの「App settings」➔「Secrets」に無料キーを登録：
        ```toml
        GEMINI_API_KEY = "AIzaSy..."
        ```
        2. これであなた専用の24時間稼働WebオフィスURLが発行されます！
        """)
    else:
        st.markdown("""
        ### 🎯 3 Steps to Deploy 100% Free on Cloud
        
        #### 1️⃣ Step 1: Push Code to GitHub (Free)
        1. Visit [GitHub](https://github.com/)指示
        2. Upload the files in this workspace (`ai_holdings_platform`).

        #### 2️⃣ Step 2: Connect to Streamlit Community Cloud (Free)
        1. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with your GitHub account.
        2. Click "Create app", select your repository, specify `app.py` as Main file path, and click "Deploy".

        #### 3️⃣ Step 3: Add Free Gemini API Key in Secrets
        1. In Streamlit Cloud Settings ➔ "Secrets", add your free Gemini API key:
        ```toml
        GEMINI_API_KEY = "AIzaSy..."
        ```
        2. Your live 24/7 AI Enterprise URL is generated instantly!
        """)
