import streamlit as st
import streamlit.components.v1 as components
import os
import json
import pandas as pd
from datetime import datetime
from core.ai_client import AIClient
from core.holdings_manager import HoldingsManager
from core.ringi_manager import RingiManager
from core.hr_manager import HRManager
from companies.note_one_systems.workflow import NoteOneWorkflow
from companies.note_one_systems.office_chat_manager import OfficeChatManager

# Page Configuration
st.set_page_config(
    page_title="Note One Systems, Inc. | AI Enterprise Platform",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# High-contrast White Text & Cerulean Blue Active State Styles
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
        border-left: 5px solid #007BA7;
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
    .desk-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #007BA7 !important;
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
        border-left: 5px solid #007BA7;
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

    /* Active Sidebar Navigation: Cerulean Blue (#007BA7) */
    div[data-testid="stSidebar"] button[kind="primary"],
    div[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] {
        background-color: #007BA7 !important;
        color: #FFFFFF !important;
        border: 1px solid #38BDF8 !important;
        font-weight: 800 !important;
        box-shadow: 0 2px 10px rgba(0, 123, 167, 0.5) !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    p, span, label {
        color: #E2E8F0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "holdings_manager" not in st.session_state:
    st.session_state.holdings_manager = HoldingsManager()
if "ringi_manager" not in st.session_state:
    st.session_state.ringi_manager = RingiManager()
if "hr_manager" not in st.session_state:
    st.session_state.hr_manager = HRManager()
if "api_key" not in st.session_state:
    st.session_state.api_key = os.environ.get("GEMINI_API_KEY", "")
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "🏢 Company Dashboard"
if "office_chat_history" not in st.session_state:
    st.session_state.office_chat_history = []

ai_client = AIClient(api_key=st.session_state.api_key)
workflow = NoteOneWorkflow(ai_client)
chat_manager = OfficeChatManager(ai_client)

# ==========================================
# Sidebar: English Navigation Menu
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#FFFFFF !important;'>🏢 Note One Systems, Inc.</h2>", unsafe_allow_html=True)
    st.caption("AI Enterprise Holdings Platform")
    st.markdown("---")

    # 1. 🏢 Company Dashboard (Top Level)
    if st.button("🏢 Company Dashboard", use_container_width=True, type="primary" if st.session_state.nav_page == "🏢 Company Dashboard" else "secondary"):
        st.session_state.nav_page = "🏢 Company Dashboard"
        st.rerun()

    # 2. 🏢 Office Room (Updated name)
    if st.button("🏢 Office Room", use_container_width=True, type="primary" if st.session_state.nav_page == "🏢 Office Room" else "secondary"):
        st.session_state.nav_page = "🏢 Office Room"
        st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 3. 📝 Editorial Department
    st.markdown("<div style='font-size:0.95rem; font-weight:800; color:#38BDF8; padding: 4px 6px;'>📝 Editorial Department</div>", unsafe_allow_html=True)
    if st.button("　 🔍 Market Research Division", use_container_width=True, type="primary" if st.session_state.nav_page == "🔍 Market Research Division" else "secondary"):
        st.session_state.nav_page = "🔍 Market Research Division"
        st.rerun()
    if st.button("　 ✍️ Content Creation Division", use_container_width=True, type="primary" if st.session_state.nav_page == "✍️ Content Creation Division" else "secondary"):
        st.session_state.nav_page = "✍️ Content Creation Division"
        st.rerun()
    if st.button("　 📢 Public Relations Division", use_container_width=True, type="primary" if st.session_state.nav_page == "📢 Public Relations Division" else "secondary"):
        st.session_state.nav_page = "📢 Public Relations Division"
        st.rerun()
    if st.button("　 ✨ Quality Assurance Division", use_container_width=True, type="primary" if st.session_state.nav_page == "✨ Quality Assurance Division" else "secondary"):
        st.session_state.nav_page = "✨ Quality Assurance Division"
        st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 4. 🏛️ Administration Department
    st.markdown("<div style='font-size:0.95rem; font-weight:800; color:#A78BFA; padding: 4px 6px;'>🏛️ Administration Department</div>", unsafe_allow_html=True)
    if st.button("　 🤝 Human Resources Division", use_container_width=True, type="primary" if st.session_state.nav_page == "🤝 Human Resources Division" else "secondary"):
        st.session_state.nav_page = "🤝 Human Resources Division"
        st.rerun()
    if st.button("　 📚 Legal & Compliance Division", use_container_width=True, type="primary" if st.session_state.nav_page == "📚 Legal & Compliance Division" else "secondary"):
        st.session_state.nav_page = "📚 Legal & Compliance Division"
        st.rerun()
    if st.button("　 📊 Financial Strategy Division", use_container_width=True, type="primary" if st.session_state.nav_page == "📊 Financial Strategy Division" else "secondary"):
        st.session_state.nav_page = "📊 Financial Strategy Division"
        st.rerun()
    if st.button("　 💳 Accounting & Operations Division", use_container_width=True, type="primary" if st.session_state.nav_page == "💳 Accounting & Operations Division" else "secondary"):
        st.session_state.nav_page = "💳 Accounting & Operations Division"
        st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 5. Independent Utilities
    if st.button("💻 IT Helpdesk & Error Logs", use_container_width=True, type="primary" if st.session_state.nav_page == "💻 IT Helpdesk & Error Logs" else "secondary"):
        st.session_state.nav_page = "💻 IT Helpdesk & Error Logs"
        st.rerun()
    if st.button("👥 Employee Profiles", use_container_width=True, type="primary" if st.session_state.nav_page == "👥 Employee Profiles" else "secondary"):
        st.session_state.nav_page = "👥 Employee Profiles"
        st.rerun()
    if st.button("☁️ 24/7 Free Cloud Setup Guide", use_container_width=True, type="primary" if st.session_state.nav_page == "☁️ 24/7 Free Cloud Setup Guide" else "secondary"):
        st.session_state.nav_page = "☁️ 24/7 Free Cloud Setup Guide"
        st.rerun()

    st.markdown("---")
    st.markdown("<h4 style='color:#FFFFFF !important;'>⚙️ AI Intelligence Engine (Gemini)</h4>", unsafe_allow_html=True)
    api_key_input = st.text_input(
        "Gemini API Key (Free Tier)",
        value=st.session_state.api_key,
        type="password",
        help="Free API key from Google AI Studio. If blank, high-fidelity demo simulation will run."
    )
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
        st.rerun()

    if ai_client.is_configured():
        st.success("🟢 AI Engine: Gemini API Connected")
    else:
        st.info("🟡 AI Engine: Demo Mode (Free Simulation Active)")

    st.markdown("---")
    st.caption("💡 **Fixed Operating Cost: ¥0 (100% Free Tier)**")
    st.caption("9 Autonomous AI Specialists Active 24/7")

# Active Page
page = st.session_state.nav_page

# ==========================================
# 1. 🏢 Company Dashboard
# ==========================================
if page == "🏢 Company Dashboard":
    st.markdown("<div class='main-header'>🏢 Company Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Executive overview and holdings performance metrics for Note One Systems, Inc.</div>", unsafe_allow_html=True)
    
    holdings_info = st.session_state.holdings_manager.get_holdings_info()
    companies = holdings_info.get("companies", [])
    articles = workflow.list_articles()
    
    target_file = os.path.join(os.path.dirname(__file__), "data/sales_targets.json")
    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            target_data = json.load(f)
    else:
        target_data = {"monthly_target_yen": 100000, "target_articles_monthly": 15}
    
    target_sales = target_data.get("monthly_target_yen", 100000)
    total_sales = sum([art.get("price", 500) * 10 for art in articles])
    progress_ratio = min(1.0, total_sales / target_sales) if target_sales > 0 else 0.0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Active Subsidiaries", value=f"{len(companies)} Units")
    with col2:
        st.metric(label="Published Articles", value=f"{len(articles)} Articles")
    with col3:
        st.metric(label="Est. Monthly Revenue / Goal", value=f"¥{total_sales:,}", delta=f"Target: ¥{target_sales:,} ({int(progress_ratio*100)}% Reached)")
    with col4:
        st.metric(label="Fixed Operating Costs", value="¥0 (100% Free Tier)")
    
    st.progress(progress_ratio, text=f"🎯 Monthly Revenue Target Progress: {int(progress_ratio*100)}% (¥{total_sales:,} / ¥{target_sales:,})")

    st.markdown("---")
    st.markdown("<div class='section-title'>📋 Group Subsidiaries & Operating Units</div>", unsafe_allow_html=True)
    for comp in companies:
        with st.container():
            c_col1, c_col2, c_col3 = st.columns([1, 4, 2])
            with c_col1:
                st.markdown(f"### {comp.get('icon', '🏢')}")
            with c_col2:
                st.markdown(f"**{comp['name']}**")
                st.write(comp.get('description', ''))
                if "trade_name_note" in comp:
                    st.caption(f"🛡️ {comp['trade_name_note']}")
            with c_col3:
                st.markdown(f"Status: :green[{comp.get('status', 'Active')}]")
                st.caption(f"Team: 9 Specialists | Content: {len(articles)} Articles")
            st.divider()

    with st.expander("➕ Establish a New Subsidiary (Holdings Expansion)"):
        st.markdown("#### New Entity Incorporation Form")
        new_c_name = st.text_input("Company Name (e.g., KindleOne AI Inc., PromptOne AI Corp.)")
        new_c_type = st.selectbox("Business Model", ["note Article Publishing", "Kindle eBook Publishing", "AI Prompt Marketplace", "Social Media Management", "Other"])
        new_c_icon = st.selectbox("Company Icon", ["✍️", "📚", "🤖", "📈", "💡", "🎨"])
        new_c_desc = st.text_area("Business Mission & Vision")
        
        if st.button("🚀 Incorporate & Integrate into Holdings", type="primary"):
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
                    st.success(f"🎉 New entity '{new_c_name}' successfully incorporated!")
                    st.rerun()
            else:
                st.warning("Please enter a valid company name.")

# ==========================================
# 2. 🏢 Office Room (メイン見出し: 🏢 Office Room / セクション: Headquarter)
# ==========================================
elif page == "🏢 Office Room":
    st.markdown("<div class='main-header'>🏢 Office Room</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>9 specialized autonomous AI employees working in their designated virtual workspaces</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Headquarter</div>", unsafe_allow_html=True)
    
    html_path = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/assets/game_office.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            game_html = f.read()
        components.html(game_html, height=545)

    # -------------------------------------------------------------
    # 💬 社員との直接対話・質問・指示デスク (Employee Consultation Desk)
    # -------------------------------------------------------------
    st.markdown("---")
    st.markdown("<div class='section-title'>💬 Direct Inquiries & Employee Consultation Desk</div>", unsafe_allow_html=True)
    st.markdown("<div style='color: #94A3B8; margin-bottom: 12px;'>質問や指示を入力すると、最適な担当部署の専門AI社員が自律的に判定・回答します。</div>", unsafe_allow_html=True)

    # クイック質問サンプル（ワンクリックで質問可能）
    st.markdown("##### 💡 Quick Inquiries (クリックして質問を入力):")
    sample_col1, sample_col2 = st.columns(2)
    with sample_col1:
        if st.button("📌 Noteのサービスは日本人向けサービスですか？", use_container_width=True):
            resp = chat_manager.generate_response("Noteのサービスは日本人向けサービスですか？")
            st.session_state.office_chat_history.append({
                "user": "Noteのサービスは日本人向けサービスですか？",
                "response": resp,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()
        if st.button("📌 今週のnote売れ筋トレンドと高成約テーマは？", use_container_width=True):
            resp = chat_manager.generate_response("今週のnote売れ筋トレンドと高成約テーマは？")
            st.session_state.office_chat_history.append({
                "user": "今週のnote売れ筋トレンドと高成約テーマは？",
                "response": resp,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()
    with sample_col2:
        if st.button("📌 Noteの英語圏ユーザと日本語圏ユーザの比率は？", use_container_width=True):
            resp = chat_manager.generate_response("Noteの英語圏ユーザと日本語圏ユーザの比率は？")
            st.session_state.office_chat_history.append({
                "user": "Noteの英語圏ユーザと日本語圏ユーザの比率は？",
                "response": resp,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()
        if st.button("📌 システムの運用費用（固定費）は本当に0円ですか？", use_container_width=True):
            resp = chat_manager.generate_response("システムの運用費用（固定費）は本当に0円ですか？")
            st.session_state.office_chat_history.append({
                "user": "システムの運用費用（固定費）は本当に0円ですか？",
                "response": resp,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # ユーザーからの自由入力フォーム
    with st.form("office_consultation_form", clear_on_submit=True):
        c_in_q1, c_in_q2 = st.columns([4, 1])
        with c_in_q1:
            user_inquiry = st.text_input(
                "質問・指示を入力してください (Ask a question or issue a directive to the team)",
                placeholder="例: 「Noteの英語圏ユーザと日本語圏ユーザの比率は？」「note記事販売の法的な注意点は？」「売上を伸ばすための価格戦略は？」"
            )
        with c_in_q2:
            target_assignee = st.selectbox(
                "担当者指定",
                ["Auto-Routing (自動判別)", "一条 蓮 (CEO)", "風間 涼 (市場調査)", "結城 紬 (編集長)", "森川 拓真 (ライター)", "佐々木 翼 (広報)", "神崎 玲奈 (QA)", "綾瀬 七海 (人事)", "橘 律 (法務)", "白石 葵 (財務・経理)"]
            )
        submit_inquiry = st.form_submit_button("📨 送信して回答を得る (Send Inquiry)", type="primary", use_container_width=True)

    if submit_inquiry and user_inquiry.strip():
        assignee_map = {
            "Auto-Routing (自動判別)": "auto",
            "一条 蓮 (CEO)": "ichijo",
            "風間 涼 (市場調査)": "kazama",
            "結城 紬 (編集長)": "yuki",
            "森川 拓真 (ライター)": "morikawa",
            "佐々木 翼 (広報)": "sasaki",
            "神崎 玲奈 (QA)": "kanzaki",
            "綾瀬 七海 (人事)": "ayase",
            "橘 律 (法務)": "tachibana",
            "白石 葵 (財務・経理)": "shiraishi"
        }
        chosen_emp = assignee_map.get(target_assignee, "auto")
        
        with st.spinner("担当者がデスクで回答を作成中..."):
            response_data = chat_manager.generate_response(user_inquiry, chosen_emp)
            st.session_state.office_chat_history.append({
                "user": user_inquiry,
                "response": response_data,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()

    # 会話履歴の表示
    if st.session_state.office_chat_history:
        st.markdown("#### 📜 Consultation & Directives Log")
        for item in reversed(st.session_state.office_chat_history):
            resp = item["response"]
            st.markdown(f"""
            <div class='user-query-card'>
                <div style='font-size: 0.8rem; color: #94A3B8;'>🕒 {item.get('timestamp', '')} | 👤 <strong>あなたからの質問・指示:</strong></div>
                <div style='font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-top: 4px;'>{item['user']}</div>
            </div>
            <div class='chat-bubble'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                    <div style='font-weight: 800; color: #FFFFFF; font-size: 1.1rem;'>
                        {resp.get('icon', '🧑‍💼')} {resp.get('name', '担当社員')} <span style='font-size: 0.85rem; color: #93C5FD; font-weight: 600;'>（{resp.get('role', '')} / {resp.get('department', '')}）</span>
                    </div>
                    <span class='status-live'><span class='pulse-dot'></span>回答完了</span>
                </div>
                <div style='white-space: pre-wrap; font-size: 0.95rem; line-height: 1.6; color: #F8FAFC;'>{resp.get('content', '')}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🗑️ 対話ログをクリア (Clear Consultation Log)"):
            st.session_state.office_chat_history = []
            st.rerun()

    # -------------------------------------------------------------
    # リアルタイム社員デスク一覧
    # -------------------------------------------------------------
    st.markdown("---")
    st.markdown("<div class='section-title'>🖥️ Workspace Desks & Live Employee Activity</div>", unsafe_allow_html=True)
    
    st.markdown("#### 🏛️ Executive & Corporate Administration (HR & Legal)")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>👩‍💼</span>
                <span class='status-live'><span class='pulse-dot'></span>Active</span>
            </div>
            <div style='font-weight: 800; font-size: 1.15rem; color: #FFFFFF; margin-top: 4px;'>Ren Ichijo</div>
            <div style='font-size: 0.85rem; color: #93C5FD; font-weight: 700;'>Chief Executive Officer</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 CEO Executive Suite</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 10px; border-radius: 6px; border: 1px solid #334155;'>💬 "Supervising overall revenue maximization and ensuring 100% zero-cost operations."</div>
        </div>
        """, unsafe_allow_html=True)
    with col_f2:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>⚖️</span>
                <span class='status-live'><span class='pulse-dot'></span>Monitoring</span>
            </div>
            <div style='font-weight: 800; font-size: 1.15rem; color: #FFFFFF; margin-top: 4px;'>Ritsu Tachibana</div>
            <div style='font-size: 0.85rem; color: #CBD5E1; font-weight: 700;'>Legal & Compliance Counsel</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 Legal Department</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 10px; border-radius: 6px; border: 1px solid #334155;'>💬 "Continuously screening compliance with corporate law, copyright, and platform terms."</div>
        </div>
        """, unsafe_allow_html=True)
    with col_f3:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>🤝</span>
                <span class='status-live'><span class='pulse-dot'></span>Active</span>
            </div>
            <div style='font-weight: 800; font-size: 1.15rem; color: #FFFFFF; margin-top: 4px;'>Nanami Ayase</div>
            <div style='font-size: 0.85rem; color: #6EE7B7; font-weight: 700;'>HR & Culture Director</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 HR Department</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 10px; border-radius: 6px; border: 1px solid #334155;'>💬 "Monitoring workload metrics across all specialists to prevent operational bottlenecks."</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 📝 Editorial Department (Research, Content, PR, QA)")
    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    with col_c1:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>🔍</span>
                <span class='status-live'><span class='pulse-dot'></span>Analyzing</span>
            </div>
            <div style='font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-top: 4px;'>Ryo Kazama</div>
            <div style='font-size: 0.85rem; color: #5EEAD4; font-weight: 700;'>Market Research Analyst</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 Research Desk</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 8px; border-radius: 6px; border: 1px solid #334155;'>💬 "Analyzing note sales trends and subscriber personas in real time."</div>
        </div>
        """, unsafe_allow_html=True)
    with col_c2:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>📑</span>
                <span class='status-live'><span class='pulse-dot'></span>Structuring</span>
            </div>
            <div style='font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-top: 4px;'>Tsumugi Yuki</div>
            <div style='font-size: 0.85rem; color: #FCD34D; font-weight: 700;'>Editor-in-Chief</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 Editorial Studio</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 8px; border-radius: 6px; border: 1px solid #334155;'>💬 "Designing optimal paywall thresholds to maximize conversion rates."</div>
        </div>
        """, unsafe_allow_html=True)
    with col_c3:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>✍️</span>
                <span class='status-live'><span class='pulse-dot'></span>Drafting</span>
            </div>
            <div style='font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-top: 4px;'>Takuma Morikawa</div>
            <div style='font-size: 0.85rem; color: #FDBA74; font-weight: 700;'>Chief Content Writer</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 Writer Studio</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 8px; border-radius: 6px; border: 1px solid #334155;'>💬 "Drafting actionable copy-and-paste practical templates."</div>
        </div>
        """, unsafe_allow_html=True)
    with col_c4:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>🛡️</span>
                <span class='status-live'><span class='pulse-dot'></span>QA Ready</span>
            </div>
            <div style='font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-top: 4px;'>Reina Kanzaki</div>
            <div style='font-size: 0.85rem; color: #FCA5A5; font-weight: 700;'>Quality Assurance Director</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 QA Inspection Booth</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 8px; border-radius: 6px; border: 1px solid #334155;'>💬 "Conducting rigorous fact-checking and automated 100-point quality scoring."</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 📢 Public Relations & 📊 Financial Strategy / 💳 Accounting")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>📢</span>
                <span class='status-live'><span class='pulse-dot'></span>Broadcasting</span>
            </div>
            <div style='font-weight: 800; font-size: 1.15rem; color: #FFFFFF; margin-top: 4px;'>Tsubasa Sasaki</div>
            <div style='font-size: 0.85rem; color: #93C5FD; font-weight: 700;'>Multi-SNS PR Specialist</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 PR Hub</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 10px; border-radius: 6px; border: 1px solid #334155;'>💬 "Automated multi-channel syndication ready for X, Threads, IG, Bluesky, Mastodon."</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>📊</span>
                <span class='status-live'><span class='pulse-dot'></span>Auditing</span>
            </div>
            <div style='font-weight: 800; font-size: 1.15rem; color: #FFFFFF; margin-top: 4px;'>Aoi Shiraishi</div>
            <div style='font-size: 0.85rem; color: #C4B5FD; font-weight: 700;'>Financial Strategist & Chief Accountant</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 Finance & Accounting</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 10px; border-radius: 6px; border: 1px solid #334155;'>💬 "Verified ¥0 monthly fixed costs. Ready for price optimization models."</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 3. 🔍 Market Research Division
# ==========================================
elif page == "🔍 Market Research Division":
    st.markdown("<div class='main-header'>🔍 Market Research Division</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Lead Analyst: Ryo Kazama (Market Research Analyst)</div>", unsafe_allow_html=True)
    
    st.info("💡 **Mission**: Uncover high-converting trends on note, analyze competitor content gaps, and identify deep reader pain points to formulate winning themes.")
    
    st.markdown("<div class='section-title'>📊 High-Conversion Trend Report</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='content-box'>
        <h4 style='color:#38BDF8;'>🔥 High-Yield note Keywords of the Week</h4>
        <ul>
            <li><strong>AI & Workflow Automation:</strong> "Practical ChatGPT Prompts to Eliminate Overtime Work", "Notion & AI Automated Operations Template"</li>
            <li><strong>Beginner Monetization Blueprints:</strong> "Zero-Knowledge Roadmap to Selling Paid note Articles"</li>
            <li><strong>Actionable Templates:</strong> "Plug-and-Play Frameworks for Proposals & Standard Operating Procedures"</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 4. ✍️ Content Creation Division
# ==========================================
elif page == "✍️ Content Creation Division":
    st.markdown("<div class='main-header'>✍️ Content Creation Division</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Supervision: Tsumugi Yuki (Editor-in-Chief) / Writing: Takuma Morikawa (Chief Content Writer)</div>", unsafe_allow_html=True)

    st.markdown("#### 🗣️ Central Strategy Room: Content Production Brief")
    c_in1, c_in2 = st.columns([3, 1])
    with c_in1:
        topic_input = st.text_input(
            "Article Topic / Target Keyword",
            placeholder="e.g., 'Complete Guide to Work Automation with Notion & AI', 'Zero to $500/mo AI Side Hustle Blueprint'"
        )
        audience_input = st.text_input(
            "Target Audience Persona (Optional)",
            placeholder="e.g., 'Busy corporate professionals', 'Beginners seeking online monetization'"
        )
    with c_in2:
        price_input = st.selectbox(
            "Pricing Strategy",
            ["Auto-Optimized (AI Recommended)", "Standard (500 JPY)", "Entry Level (300 JPY)", "Premium Tier (980+ JPY)"]
        )
        st.write("")
        start_btn = st.button("🚀 Convene 9 AI Specialists & Begin Writing", type="primary", use_container_width=True)

    if start_btn:
        if not topic_input.strip():
            st.warning("⚠️ Please enter a topic for the article.")
        else:
            st.markdown("### 🎙️ Central Strategy Room: Live Editorial Stream")
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
                    status_text.markdown("✅ **Full pipeline (Writing, Legal Review, QA Audit, 5-SNS Syndication) completed successfully!**")
            
            if completed_article:
                st.success(f"🎉 Article '{completed_article['title']}' created and logged into Quality Assurance registry as 'Pre-Publication'!")

# ==========================================
# 5. 📢 Public Relations Division
# ==========================================
elif page == "📢 Public Relations Division":
    st.markdown("<div class='main-header'>📢 Public Relations Division</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Lead: Tsubasa Sasaki (Multi-SNS PR Specialist)</div>", unsafe_allow_html=True)

    st.markdown("#### ⚙️ 5 Major Social Media Accounts & Auto-Syndication Hub")
    cfg_path = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/sns_config.json")
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            sns_cfg = json.load(f)
    else:
        sns_cfg = {}
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        x_acc = st.text_input("🐦 X (Twitter) Account Handle", value=sns_cfg.get("x", {}).get("account_name", "@NoteOneSystems"))
        ig_acc = st.text_input("📸 Instagram Profile", value=sns_cfg.get("instagram", {}).get("account_name", "@noteonesystems_official"))
        th_acc = st.text_input("🧵 Threads Username", value=sns_cfg.get("threads", {}).get("account_name", "@noteonesystems_official"))
    with col_s2:
        bs_handle = st.text_input("🦋 Bluesky Handle", value=sns_cfg.get("bluesky", {}).get("handle", "noteonesystems.bsky.social"))
        mast_inst = st.text_input("🐘 Mastodon Instance URL", value=sns_cfg.get("mastodon", {}).get("instance", "https://mstdn.jp"))
    
    if st.button("💾 Save Social Media Configuration", type="primary"):
        sns_cfg["x"] = {"account_name": x_acc}
        sns_cfg["instagram"] = {"account_name": ig_acc}
        sns_cfg["threads"] = {"account_name": th_acc}
        sns_cfg["bluesky"] = {"handle": bs_handle}
        sns_cfg["mastodon"] = {"instance": mast_inst}
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(sns_cfg, f, ensure_ascii=False, indent=2)
        st.success("Social media configuration saved successfully.")

# ==========================================
# 6. ✨ Quality Assurance Division
# ==========================================
elif page == "✨ Quality Assurance Division":
    st.markdown("<div class='main-header'>✨ Quality Assurance Division</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Lead: Reina Kanzaki (Quality Assurance Director)</div>", unsafe_allow_html=True)

    st.markdown("#### 📋 Published Articles Registry & Status Audit Trail")
    articles = workflow.list_articles()
    
    if not articles:
        st.info("No articles found in registry. Launch a writing session in '✍️ Content Creation Division'.")
    else:
        article_titles = [f"[{art.get('status', 'Pre-Publication')}] {art.get('created_at', '')} | {art.get('title', '')}" for art in articles]
        selected_idx = st.selectbox("Select Article to Manage", range(len(articles)), format_func=lambda x: article_titles[x])
        art = articles[selected_idx]
        
        col_stat1, col_stat2 = st.columns([2, 3])
        with col_stat1:
            cur_status = art.get("status", "Pre-Publication")
            status_options = ["Idea Formulation", "In Writing", "Under Peer Review", "Pre-Publication", "Published"]
            st.markdown(f"**Current Status:** :green[**{cur_status}**]")
            new_stat = st.selectbox(
                "Change Lifecycle Status",
                status_options,
                index=status_options.index(cur_status) if cur_status in status_options else 3
            )
            if st.button("🔄 Update Status & Record Timestamp", type="primary"):
                workflow.update_article_status(art["id"], new_stat)
                st.success(f"Status updated to '{new_stat}' with immutable timestamp logged!")
                st.rerun()
        
        with col_stat2:
            st.markdown("##### ⏱️ Status Transition Timestamp Log")
            history = art.get("status_history", [])
            for h in reversed(history):
                st.write(f"- **{h.get('timestamp')}** ➔ `[{h.get('status')}]` ({h.get('actor', '')})")
        
        st.divider()
        st.markdown("#### 📄 Article Preview (Free Introduction / Paid Paywall Area)")
        content = art.get("content", "")
        if "🔒 ここから先は有料エリアです" in content or "🔒 [Paywall] Premium Section Starts Here" in content:
            delimiter = "🔒 ここから先は有料エリアです" if "🔒 ここから先は有料エリアです" in content else "🔒 [Paywall] Premium Section Starts Here"
            parts = content.split(delimiter)
            st.markdown(parts[0])
            st.markdown("""
            <div style='background-color: #1E293B; border: 2px dashed #F59E0B; border-radius: 8px; padding: 14px; margin: 14px 0;'>
                <strong style='color: #FCD34D;'>🔒 Paid Subscriber Paywall Threshold (Set on note platform)</strong>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(parts[1])
        else:
            st.markdown(content)
        
        st.markdown("#### 📢 5-SNS Syndication Copy (Crafted by Tsubasa Sasaki)")
        st.text_area("Social Promotion Content", value=art.get("marketing", ""), height=250)
        
        st.markdown("#### 📋 Full Markdown Source Code (Ready for note editor)")
        st.text_area("Markdown Code", value=art.get("content", ""), height=300)

# ==========================================
# 7. 🤝 Human Resources Division
# ==========================================
elif page == "🤝 Human Resources Division":
    st.markdown("<div class='main-header'>🤝 Human Resources Division</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Lead: Nanami Ayase (HR & Culture Director)</div>", unsafe_allow_html=True)

    st.markdown("#### 🏢 Organizational Hierarchy & Job Responsibilities")
    with open(os.path.join(os.path.dirname(__file__), "companies/note_one_systems/org_chart_and_job_descriptions.json"), "r", encoding="utf-8") as f:
        org_data = json.load(f)
    
    st.write(f"**Authorized by:** {org_data.get('author')} | **Version:** {org_data.get('version')}")
    
    with st.expander("📋 View Complete 9-Member Job Description Ledger"):
        for dept in org_data["departments"]:
            st.markdown(f"**{dept['icon']} {dept['name']}** (Lead: {dept['head']})")
            for role in dept["roles"]:
                st.write(f"- **{role['role_name']} ({role['member']})**: {', '.join(role['responsibilities'][:2])}")
    
    st.markdown("#### 📊 Real-Time Employee Workload & Operational Metrics")
    stats = st.session_state.hr_manager.get_workload_stats()
    df_data = []
    for emp_id, data in stats.items():
        df_data.append({
            "Employee Name": data["name"],
            "Role": data["role"],
            "Tasks Executed": data["tasks"],
            "Words Generated": f"{data['words_generated']:,} words",
            "Workload Score": f"{data['workload_score']}%"
        })
    st.dataframe(pd.DataFrame(df_data), use_container_width=True)
    
    proposals = st.session_state.hr_manager.get_staffing_proposals()
    if proposals:
        for prop in proposals:
            st.warning(f"**[Staffing Proposal] Target Unit: {prop['target_role']} ({prop['target_name']} / Load: {prop['workload_score']}%)** ➔ Recommended Zero-Cost Addition: {prop['proposed_role']}")

# ==========================================
# 8. 📚 Legal & Compliance Division
# ==========================================
elif page == "📚 Legal & Compliance Division":
    st.markdown("<div class='main-header'>📚 Legal & Compliance Division</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Counsel: Ritsu Tachibana (Legal & Compliance Counsel)</div>", unsafe_allow_html=True)

    st.markdown("#### 📜 Inter-Department Legal Inquiry & Compliance Audit Ledger")
    legal_file = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/legal_investigations.json")
    if os.path.exists(legal_file):
        with open(legal_file, "r", encoding="utf-8") as f:
            legal_inv = json.load(f)
    else:
        legal_inv = {"investigations": []}
    
    for inv in legal_inv["investigations"]:
        st.markdown(f"""
        <div style='background-color: #1E293B; border: 1px solid #334155; border-left: 4px solid #007BA7; border-radius: 8px; padding: 16px; margin-bottom: 14px; color: #F8FAFC;'>
            <div style='display: flex; justify-content: space-between;'>
                <strong style='font-size: 1.1rem; color: #FFFFFF;'>📋 {inv['category']} (ID: {inv['id']})</strong>
                <span>{inv['status']}</span>
            </div>
            <div style='font-size: 0.8rem; color: #94A3B8; margin: 4px 0;'>
                🕒 Received: {inv['received_at']} | Review Started: {inv['started_at']} | Completed: {inv['completed_at']}
            </div>
            <div style='font-size: 0.9rem; color: #E2E8F0;'><strong>Originating Unit:</strong> {inv['requester_dept']}</div>
            <div style='font-size: 0.9rem; color: #E2E8F0; margin-top: 4px;'><strong>Inquiry Summary:</strong> {inv['inquiry_content']}</div>
            <div style='background-color: #0F172A; border: 1px solid #334155; padding: 12px; border-radius: 6px; margin-top: 10px; font-size: 0.9rem; color: #F8FAFC;'>
                <strong style='color: #38BDF8;'>⚖️ Formal Legal Opinion:</strong> {inv['legal_opinion']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 9. 📊 Financial Strategy Division
# ==========================================
elif page == "📊 Financial Strategy Division":
    st.markdown("<div class='main-header'>📊 Financial Strategy Division</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Strategist: Aoi Shiraishi (Financial Strategist)</div>", unsafe_allow_html=True)

    st.markdown("#### 🎯 Executive Monthly Revenue Target & Monetization Roadmap")
    target_file = os.path.join(os.path.dirname(__file__), "data/sales_targets.json")
    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            target_data = json.load(f)
    else:
        target_data = {"monthly_target_yen": 100000, "target_articles_monthly": 15}
    
    c_tar1, c_tar2 = st.columns([2, 3])
    with c_tar1:
        new_target = st.number_input("Monthly Revenue Target (JPY)", min_value=10000, max_value=10000000, value=target_data.get("monthly_target_yen", 100000), step=10000)
        target_arts = st.slider("Monthly Article Production Target", min_value=5, max_value=60, value=target_data.get("target_articles_monthly", 15))
        if st.button("📢 Issue Executive Financial Directive", type="primary"):
            target_data["monthly_target_yen"] = int(new_target)
            target_data["target_articles_monthly"] = int(target_arts)
            target_data["updated_at"] = datetime.now().strftime("%Y-%m-%d")
            with open(target_file, "w", encoding="utf-8") as f:
                json.dump(target_data, f, ensure_ascii=False, indent=2)
            st.success("Revenue directives updated successfully.")
            st.rerun()
    with c_tar2:
        daily_req = int(new_target / 500 / 30)
        st.info(f"""
        **[Financial Strategy Blueprint]**
        - 🎯 **Required Daily Unit Sales:** approx. **{max(1, daily_req)} copies** (at 500 JPY unit price)
        - 📝 **Recommended Publication Cadence:** **{target_arts} articles / month**
        - 💡 **Strategic Advice:** Acquire initial audience with 500 JPY entry articles, followed by high-ticket 1,480 JPY monthly premium bundles.
        """)

# ==========================================
# 10. 💳 Accounting & Operations Division
# ==========================================
elif page == "💳 Accounting & Operations Division":
    st.markdown("<div class='main-header'>💳 Accounting & Operations Division</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Lead: Aoi Shiraishi (Chief Accountant)</div>", unsafe_allow_html=True)

    st.markdown("#### 💰 Zero-Cost Operational Ledger & Expense Verification")
    acc_file = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/accounting_data.json")
    if os.path.exists(acc_file):
        with open(acc_file, "r", encoding="utf-8") as f:
            acc_data = json.load(f)
    else:
        acc_data = {"monthly_total_cost_yen": 0, "cost_items": []}
    
    st.success(f"**Total Verified Monthly Operating Costs:** :green[**¥{acc_data.get('monthly_total_cost_yen', 0):,} (100% Zero Cost)**]")
    
    cost_df = []
    for item in acc_data.get("cost_items", []):
        cost_df.append({
            "Category": item["category"],
            "Service Provider": item["service_name"],
            "Tier / Plan": item["plan"],
            "Monthly Cost": f"¥{item['monthly_cost_yen']:,}",
            "Operating Status": item["status"],
            "Audit Notes": item["notes"]
        })
    st.dataframe(pd.DataFrame(cost_df), use_container_width=True)
    st.caption("🛡️ **Strict Policy Enforcement**: Pursuant to Corporate Rule Art. 4, zero financial liabilities or cloud expenses are incurred without prior executive ringi approval.")

# ==========================================
# 11. 💻 IT Helpdesk & Error Logs
# ==========================================
elif page == "💻 IT Helpdesk & Error Logs":
    st.markdown("<div class='main-header'>💻 IT Helpdesk & Error Logs</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Central Incident Management, Diagnostics & Self-Healing Registry</div>", unsafe_allow_html=True)

    err_file = os.path.join(os.path.dirname(__file__), "data/error_logs.json")
    if os.path.exists(err_file):
        with open(err_file, "r", encoding="utf-8") as f:
            err_data = json.load(f)
    else:
        err_data = {"errors": []}

    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        st.metric(label="Total Logged Incidents", value=f"{len(err_data.get('errors', []))} Cases")
    with col_e2:
        st.metric(label="Resolved Incidents", value=f"{len([e for e in err_data.get('errors', []) if '解決' in e.get('status', '') or 'Resolved' in e.get('status', '')])} Cases")
    with col_e3:
        st.metric(label="System Health", value="100% Operational")

    st.markdown("---")
    st.markdown("<div class='section-title'>📋 Incident Resolution Registry</div>", unsafe_allow_html=True)
    
    for err in err_data.get("errors", []):
        with st.container():
            st.markdown(f"""
            <div style='background-color: #1E293B; border: 1px solid #334155; border-left: 5px solid #007BA7; border-radius: 10px; padding: 18px; margin-bottom: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.25); color: #F8FAFC;'>
                <div style='display: flex; justify-content: space-between;'>
                    <strong style='font-size: 1.15rem; color: #FFFFFF;'>⚠️ {err['module']} (ID: {err['id']})</strong>
                    <span>{err['status']}</span>
                </div>
                <div style='font-size: 0.8rem; color: #94A3B8; margin: 4px 0;'>🕒 Occurred: {err['occurred_at']}</div>
                <div style='background-color: #450A0A; border: 1px solid #991B1B; padding: 10px; border-radius: 6px; font-family: monospace; font-size: 0.85rem; color: #FCA5A5; margin: 8px 0;'>
                    {err['error_message']}
                </div>
                <div style='font-size: 0.9rem; color: #E2E8F0;'><strong>🔍 Root Cause Analysis:</strong> {err['root_cause']}</div>
                <div style='font-size: 0.9rem; color: #4ADE80; margin-top: 4px;'><strong>🛠️ Resolution Procedure:</strong> {err['solution']}</div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# 12. 👥 Employee Profiles
# ==========================================
elif page == "👥 Employee Profiles":
    st.markdown("<div class='main-header'>👥 Employee Profiles & System Prompts</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>9 autonomous specialized AI professionals with isolated prompt configurations</div>", unsafe_allow_html=True)
    
    with open(os.path.join(os.path.dirname(__file__), "companies/note_one_systems/company_info.json"), "r", encoding="utf-8") as f:
        comp_info = json.load(f)

    for emp in comp_info["employees"]:
        with st.expander(f"{emp['icon']} {emp['name']} ({emp['role']}) - Directory: employees/{emp['folder']}/"):
            col_e1, col_e2 = st.columns([1, 2])
            with col_e1:
                st.markdown(f"**Department:** {emp.get('department', '')}")
                st.markdown(f"**Professional Motto:** {emp['motto']}")
                st.markdown(f"**Core Competencies:** {', '.join(emp['skills'])}")
            with col_e2:
                st.markdown("**System Prompt (prompt.txt):**")
                st.code(emp['prompt'], language="text")

# ==========================================
# 13. ☁️ 24/7 Free Cloud Setup Guide
# ==========================================
elif page == "☁️ 24/7 Free Cloud Setup Guide":
    st.markdown("<div class='main-header'>☁️ 24/7 Zero-Cost Cloud Deployment Guide</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>How to host and access your AI enterprise from any device 24/7 with zero server fees</div>", unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 3 Steps to Deploy 100% Free on Cloud
    
    #### 1️⃣ Step 1: Push Code to GitHub (Free)
    1. Visit [GitHub](https://github.com/) and create a new repository (Private or Public).
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
