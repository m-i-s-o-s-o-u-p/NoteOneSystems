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

# ページ設定
st.set_page_config(
    page_title="Note One Systems ,Inc | AI Enterprise Platform",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 徹底的な白文字＆セルリアンブルー選択色・高コントラストCSS
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
    
    /* サイドバーのテキストリンクボタン風デザイン */
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

    /* 選択中のメニューボタン：セルリアンブルー（#007BA7） */
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

# セッション初期化
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

ai_client = AIClient(api_key=st.session_state.api_key)
workflow = NoteOneWorkflow(ai_client)

# ==========================================
# サイドバー（Company Dashboard最上部、「├」「└」撤廃）
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#FFFFFF !important;'>🏢 Note One Systems ,Inc</h2>", unsafe_allow_html=True)
    st.caption("AI Enterprise Holdings Platform")
    st.markdown("---")

    # 1. 🏢 Company Dashboard（最上部）
    if st.button("🏢 Company Dashboard", use_container_width=True, type="primary" if st.session_state.nav_page == "🏢 Company Dashboard" else "secondary"):
        st.session_state.nav_page = "🏢 Company Dashboard"
        st.rerun()

    # 2. 🏢 Headquarter Office Room
    if st.button("🏢 Headquarter Office Room", use_container_width=True, type="primary" if st.session_state.nav_page == "🏢 Headquarter Office Room" else "secondary"):
        st.session_state.nav_page = "🏢 Headquarter Office Room"
        st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 3. 📝 編集部
    st.markdown("<div style='font-size:0.95rem; font-weight:800; color:#38BDF8; padding: 4px 6px;'>📝 編集部</div>", unsafe_allow_html=True)
    if st.button("　 🔍 市場調査課", use_container_width=True, type="primary" if st.session_state.nav_page == "🔍 市場調査課" else "secondary"):
        st.session_state.nav_page = "🔍 市場調査課"
        st.rerun()
    if st.button("　 ✍️ 記事制作課", use_container_width=True, type="primary" if st.session_state.nav_page == "✍️ 記事制作課" else "secondary"):
        st.session_state.nav_page = "✍️ 記事制作課"
        st.rerun()
    if st.button("　 📢 広報課", use_container_width=True, type="primary" if st.session_state.nav_page == "📢 広報課" else "secondary"):
        st.session_state.nav_page = "📢 広報課"
        st.rerun()
    if st.button("　 ✨ 品質管理課", use_container_width=True, type="primary" if st.session_state.nav_page == "✨ 品質管理課" else "secondary"):
        st.session_state.nav_page = "✨ 品質管理課"
        st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 4. 🏛️ 管理部
    st.markdown("<div style='font-size:0.95rem; font-weight:800; color:#A78BFA; padding: 4px 6px;'>🏛️ 管理部</div>", unsafe_allow_html=True)
    if st.button("　 🤝 人事課", use_container_width=True, type="primary" if st.session_state.nav_page == "🤝 人事課" else "secondary"):
        st.session_state.nav_page = "🤝 人事課"
        st.rerun()
    if st.button("　 📚 法務課", use_container_width=True, type="primary" if st.session_state.nav_page == "📚 法務課" else "secondary"):
        st.session_state.nav_page = "📚 法務課"
        st.rerun()
    if st.button("　 📊 財務課", use_container_width=True, type="primary" if st.session_state.nav_page == "📊 財務課" else "secondary"):
        st.session_state.nav_page = "📊 財務課"
        st.rerun()
    if st.button("　 💳 経理課", use_container_width=True, type="primary" if st.session_state.nav_page == "💳 経理課" else "secondary"):
        st.session_state.nav_page = "💳 経理課"
        st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 5. その他単独項目
    if st.button("💻 社内ヘルプデスク", use_container_width=True, type="primary" if st.session_state.nav_page == "💻 社内ヘルプデスク" else "secondary"):
        st.session_state.nav_page = "💻 社内ヘルプデスク"
        st.rerun()
    if st.button("👥 社員プロファイル", use_container_width=True, type="primary" if st.session_state.nav_page == "👥 社員プロファイル" else "secondary"):
        st.session_state.nav_page = "👥 社員プロファイル"
        st.rerun()
    if st.button("☁️ 24時間無料クラウド設定ガイド", use_container_width=True, type="primary" if st.session_state.nav_page == "☁️ 24時間無料クラウド設定ガイド" else "secondary"):
        st.session_state.nav_page = "☁️ 24時間無料クラウド設定ガイド"
        st.rerun()

    st.markdown("---")
    st.markdown("<h4 style='color:#FFFFFF !important;'>⚙️ AI頭脳設定（Gemini）</h4>", unsafe_allow_html=True)
    api_key_input = st.text_input(
        "Gemini API Key (無料枠)",
        value=st.session_state.api_key,
        type="password",
        help="Google AI Studioで取得した無料のAPIキー。未入力時はデモシミュレーションで動きます。"
    )
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
        st.rerun()

    if ai_client.is_configured():
        st.success("🟢 AI頭脳: Gemini API 接続中")
    else:
        st.info("🟡 AI頭脳: デモモード（無料シミュレーション中）")

    st.markdown("---")
    st.caption("💡 **維持費: 0円（完全無料）**")
    st.caption("9名の専門AI社員が24時間稼働中")

# 現在のページ
page = st.session_state.nav_page

# ==========================================
# 1. 🏢 Company Dashboard
# ==========================================
if page == "🏢 Company Dashboard":
    st.markdown("<div class='main-header'>🏢 Company Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Note One Systems ,Inc グループ全体の経営概況・全社統括ダッシュボード</div>", unsafe_allow_html=True)
    
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
        st.metric(label="傘下の子会社数", value=f"{len(companies)} 社")
    with col2:
        st.metric(label="総生産記事数", value=f"{len(articles)} 本")
    with col3:
        st.metric(label="月間想定売上 / 目標", value=f"¥{total_sales:,}", delta=f"目標: ¥{target_sales:,} (達成率 {int(progress_ratio*100)}%)")
    with col4:
        st.metric(label="システム固定維持費", value="¥0 (完全無料)")
    
    st.progress(progress_ratio, text=f"🎯 月間売上目標達成度: {int(progress_ratio*100)}% (¥{total_sales:,} / ¥{target_sales:,})")

    st.markdown("---")
    st.markdown("<div class='section-title'>📋 傘下のグループ会社一覧</div>", unsafe_allow_html=True)
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
                st.markdown(f"ステータス: :green[{comp.get('status', '稼働中')}]")
                st.caption(f"所属社員: 9名 | 制作記事数: {len(articles)} 本")
            st.divider()

    with st.expander("➕ 新しい子会社を設立する（ホールディングス化）"):
        st.markdown("#### 新会社設立申請フォーム")
        new_c_name = st.text_input("会社名（例: KindleOne AI 株式会社、PromptOne AI 株式会社）")
        new_c_type = st.selectbox("事業モデル", ["note記事販売", "電子書籍(Kindle)出版", "AIプロンプト販売", "SNS運用代行", "その他"])
        new_c_icon = st.selectbox("会社アイコン", ["✍️", "📚", "🤖", "📈", "💡", "🎨"])
        new_c_desc = st.text_area("事業内容・ビジョン")
        
        if st.button("🚀 新会社を設立・ホールディングスに統合", type="primary"):
            if new_c_name.strip():
                c_id = f"company_{int(datetime.now().timestamp())}"
                success = st.session_state.holdings_manager.add_company(
                    company_id=c_id,
                    name=new_c_name,
                    company_type=new_c_type,
                    icon=new_c_icon,
                    description=new_c_desc,
                    employees=[{"id": "ceo", "name": "AI統括リーダー", "role": "CEO", "icon": "👩‍💼"}]
                )
                if success:
                    st.success(f"🎉 新会社「{new_c_name}」が設立されました！")
                    st.rerun()
            else:
                st.warning("会社名を入力してください。")

# ==========================================
# 2. 🏢 Headquarter Office Room
# ==========================================
elif page == "🏢 Headquarter Office Room":
    st.markdown("<div class='main-header'>Headquarter</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>9名の専門AI社員がそれぞれのデスクで自律的に業務を行っています</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Office Room</div>", unsafe_allow_html=True)
    
    html_path = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/assets/game_office.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            game_html = f.read()
        components.html(game_html, height=530)

    st.markdown("---")
    st.markdown("<div class='section-title'>🖥️ フロア別 執務デスク＆リアルタイム稼働状況</div>", unsafe_allow_html=True)
    
    st.markdown("#### 🏛️ 経営統括 ＆ 管理部（人事課・法務課）")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>👩‍💼</span>
                <span class='status-live'><span class='pulse-dot'></span>執務中</span>
            </div>
            <div style='font-weight: 800; font-size: 1.15rem; color: #FFFFFF; margin-top: 4px;'>一条 蓮</div>
            <div style='font-size: 0.85rem; color: #93C5FD; font-weight: 700;'>代表取締役CEO</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 CEO Private Suite</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 10px; border-radius: 6px; border: 1px solid #334155;'>💬 「全社売上最大化と、完全無料運用の規律を監督しています。」</div>
        </div>
        """, unsafe_allow_html=True)
    with col_f2:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>⚖️</span>
                <span class='status-live'><span class='pulse-dot'></span>法務監視中</span>
            </div>
            <div style='font-weight: 800; font-size: 1.15rem; color: #FFFFFF; margin-top: 4px;'>橘 律</div>
            <div style='font-size: 0.85rem; color: #CBD5E1; font-weight: 700;'>法務課 / 法務顧問</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 Legal Department</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 10px; border-radius: 6px; border: 1px solid #334155;'>💬 「会社法・著作権法・note規約の適合性を常時スクリーニングしています。」</div>
        </div>
        """, unsafe_allow_html=True)
    with col_f3:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>🤝</span>
                <span class='status-live'><span class='pulse-dot'></span>負荷監視中</span>
            </div>
            <div style='font-weight: 800; font-size: 1.15rem; color: #FFFFFF; margin-top: 4px;'>綾瀬 七海</div>
            <div style='font-size: 0.85rem; color: #6EE7B7; font-weight: 700;'>人事課 / 人事責任者</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 HR Department</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 10px; border-radius: 6px; border: 1px solid #334155;'>💬 「各社員の業務負荷スコアを測定し、過負荷を未然に防止しています。」</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 📝 編集部（市場調査・制作・広報・品質管理）")
    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    with col_c1:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>🔍</span>
                <span class='status-live'><span class='pulse-dot'></span>調査中</span>
            </div>
            <div style='font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-top: 4px;'>風間 涼</div>
            <div style='font-size: 0.85rem; color: #5EEAD4; font-weight: 700;'>市場調査課</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 Research Desk</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 8px; border-radius: 6px; border: 1px solid #334155;'>💬 「note売れ筋トレンドと読者ペルソナを分析中です。」</div>
        </div>
        """, unsafe_allow_html=True)
    with col_c2:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>📑</span>
                <span class='status-live'><span class='pulse-dot'></span>構成中</span>
            </div>
            <div style='font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-top: 4px;'>結城 紬</div>
            <div style='font-size: 0.85rem; color: #FCD34D; font-weight: 700;'>記事制作課 (編集長)</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 Editorial Studio</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 8px; border-radius: 6px; border: 1px solid #334155;'>💬 「購入率を高める有料ラインの境界線を設計しています。」</div>
        </div>
        """, unsafe_allow_html=True)
    with col_c3:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>✍️</span>
                <span class='status-live'><span class='pulse-dot'></span>執筆待機</span>
            </div>
            <div style='font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-top: 4px;'>森川 拓真</div>
            <div style='font-size: 0.85rem; color: #FDBA74; font-weight: 700;'>記事制作課 (ライター)</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 Writer Studio</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 8px; border-radius: 6px; border: 1px solid #334155;'>💬 「コピペで使える実践テンプレート執筆スタンバイ完了。」</div>
        </div>
        """, unsafe_allow_html=True)
    with col_c4:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>🛡️</span>
                <span class='status-live'><span class='pulse-dot'></span>QA待機</span>
            </div>
            <div style='font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-top: 4px;'>神崎 玲奈</div>
            <div style='font-size: 0.85rem; color: #FCA5A5; font-weight: 700;'>品質管理課 (QA)</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 QA Inspection Booth</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 8px; border-radius: 6px; border: 1px solid #334155;'>💬 「信憑性と100点採点スコアリングの準備万全です。」</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 📢 広報課 ＆ 📊 財務課・💳 経理課")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>📢</span>
                <span class='status-live'><span class='pulse-dot'></span>5大SNS待機</span>
            </div>
            <div style='font-weight: 800; font-size: 1.15rem; color: #FFFFFF; margin-top: 4px;'>佐々木 翼</div>
            <div style='font-size: 0.85rem; color: #93C5FD; font-weight: 700;'>広報課</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 PR Hub</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 10px; border-radius: 6px; border: 1px solid #334155;'>💬 「X・IG・Threads・Bluesky・Mastodonへの自動プロモーション待機中。」</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown("""
        <div class='desk-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 1.6rem;'>📊</span>
                <span class='status-live'><span class='pulse-dot'></span>財務・経理分析中</span>
            </div>
            <div style='font-weight: 800; font-size: 1.15rem; color: #FFFFFF; margin-top: 4px;'>白石 葵</div>
            <div style='font-size: 0.85rem; color: #C4B5FD; font-weight: 700;'>財務課 ＆ 経理課</div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 Finance & Accounting</div>
            <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 10px; border-radius: 6px; border: 1px solid #334155;'>💬 「システム維持費0円（完全無料）確認済。価格シミュレーション準備完了。」</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 3. 🔍 市場調査課（単一画面）
# ==========================================
elif page == "🔍 市場調査課":
    st.markdown("<div class='main-header'>🔍 市場調査課</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>担当: 風間 涼（Market Research Analyst）</div>", unsafe_allow_html=True)
    
    st.info("💡 **市場調査課のミッション**: noteの最新売れ筋トレンド、競合記事のギャップ、読者ペルソナの深層心理を分析し、売れるテーマを特定します。")
    
    st.markdown("<div class='section-title'>📊 最新トレンド分析レポート</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='content-box'>
        <h4 style='color:#38BDF8;'>🔥 今週のnote高成約キーワード</h4>
        <ul>
            <li><strong>AI×実務効率化:</strong> 「ChatGPTで残業をゼロにする実践プロンプト集」「Notion×AI 自動化テンプレート」</li>
            <li><strong>初心者向け副業マップ:</strong> 「知識ゼロからのnote有料記事販売ロードマップ」</li>
            <li><strong>即戦力テンプレ:</strong> 「コピペで使える企画書・業務マニュアルの型」</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 4. ✍️ 記事制作課（単一画面）
# ==========================================
elif page == "✍️ 記事制作課":
    st.markdown("<div class='main-header'>✍️ 記事制作課</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>統括: 結城 紬（編集長） / 執筆: 森川 拓真（チーフライター）</div>", unsafe_allow_html=True)

    st.markdown("#### 🗣️ 中央ガラス会議室：記事制作指示フォーム")
    c_in1, c_in2 = st.columns([3, 1])
    with c_in1:
        topic_input = st.text_input(
            "記事のテーマ・キーワード",
            placeholder="例: 「Notionで劇的に業務効率化する実践テンプレート集」「未経験から月5万円稼ぐAI副業の完全マップ」"
        )
        audience_input = st.text_input(
            "ターゲット読者（任意）",
            placeholder="例: 「忙しい会社員」「副業を始めたい初心者」"
        )
    with c_in2:
        price_input = st.selectbox(
            "価格方針",
            ["自動提案（アナリスト最適化）", "ワンコイン（500円）", "入門価格（300円）", "高付加価値（980円〜）"]
        )
        st.write("")
        start_btn = st.button("🚀 9名を中央会議室に招集して執筆開始", type="primary", use_container_width=True)

    if start_btn:
        if not topic_input.strip():
            st.warning("⚠️ 記事のテーマを入力してください。")
        else:
            st.markdown("### 🎙️ 中央会議室 リアルタイム戦略会議 ＆ 執筆ライブログ")
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
                            <div style='font-weight: 800; color: #FFFFFF;'>{log.get('icon')} {log.get('name')} <span style='font-size: 0.8rem; color: #94A3B8;'>（{log.get('role')}）</span></div>
                            <div style='white-space: pre-wrap; margin-top: 6px; font-size: 0.95rem; color: #F8FAFC;'>{log.get('content')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                elif event.get("status") == "completed":
                    completed_article = event.get("article")
                    progress_bar.progress(1.0)
                    status_text.markdown("✅ **全工程（執筆・法務・QA・5大SNSプロモーション）が完了しました！**")
            
            if completed_article:
                st.success(f"🎉 記事『{completed_article['title']}』が完成し、品質管理課の台帳に「掲載前」として登録されました！")

# ==========================================
# 5. 📢 広報課（単一画面）
# ==========================================
elif page == "📢 広報課":
    st.markdown("<div class='main-header'>📢 広報課</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>担当: 佐々木 翼（Multi-SNS PR Specialist）</div>", unsafe_allow_html=True)

    st.markdown("#### ⚙️ 5大SNSアカウント ＆ 自動配信先の設定")
    cfg_path = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/sns_config.json")
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            sns_cfg = json.load(f)
    else:
        sns_cfg = {}
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        x_acc = st.text_input("🐦 X アカウント名", value=sns_cfg.get("x", {}).get("account_name", "@NoteOneSystems"))
        ig_acc = st.text_input("📸 Instagram アカウント名", value=sns_cfg.get("instagram", {}).get("account_name", "@noteonesystems_official"))
        th_acc = st.text_input("🧵 Threads アカウント名", value=sns_cfg.get("threads", {}).get("account_name", "@noteonesystems_official"))
    with col_s2:
        bs_handle = st.text_input("🦋 Bluesky ハンドル名", value=sns_cfg.get("bluesky", {}).get("handle", "noteonesystems.bsky.social"))
        mast_inst = st.text_input("🐘 Mastodon インスタンスURL", value=sns_cfg.get("mastodon", {}).get("instance", "https://mstdn.jp"))
    
    if st.button("💾 広報課 SNS設定を保存する", type="primary"):
        sns_cfg["x"] = {"account_name": x_acc}
        sns_cfg["instagram"] = {"account_name": ig_acc}
        sns_cfg["threads"] = {"account_name": th_acc}
        sns_cfg["bluesky"] = {"handle": bs_handle}
        sns_cfg["mastodon"] = {"instance": mast_inst}
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(sns_cfg, f, ensure_ascii=False, indent=2)
        st.success("広報課のSNS設定を保存しました。")

# ==========================================
# 6. ✨ 品質管理課（単一画面）
# ==========================================
elif page == "✨ 品質管理課":
    st.markdown("<div class='main-header'>✨ 品質管理課</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>担当: 神崎 玲奈（Quality Assurance Director）</div>", unsafe_allow_html=True)

    st.markdown("#### 📋 作成記事一覧・ステータス管理 ＆ タイムスタンプ履歴")
    articles = workflow.list_articles()
    
    if not articles:
        st.info("まだ記事がありません。「✍️ 記事制作課」から記事を執筆してください。")
    else:
        article_titles = [f"【{art.get('status', '掲載前')}】 {art.get('created_at', '')} | {art.get('title', '')}" for art in articles]
        selected_idx = st.selectbox("管理する記事を選択", range(len(articles)), format_func=lambda x: article_titles[x])
        art = articles[selected_idx]
        
        col_stat1, col_stat2 = st.columns([2, 3])
        with col_stat1:
            cur_status = art.get("status", "掲載前")
            st.markdown(f"**現在のステータス:** :green[**{cur_status}**]")
            new_stat = st.selectbox("ステータスを変更する", ["考案中", "執筆中", "査読中", "掲載前", "掲載済み"], index=["考案中", "執筆中", "査読中", "掲載前", "掲載済み"].index(cur_status) if cur_status in ["考案中", "執筆中", "査読中", "掲載前", "掲載済み"] else 3)
            if st.button("🔄 ステータスを更新（タイムスタンプ追記）", type="primary"):
                workflow.update_article_status(art["id"], new_stat)
                st.success(f"ステータスを「{new_stat}」に更新し、タイムスタンプを記録しました！")
                st.rerun()
        
        with col_stat2:
            st.markdown("##### ⏱️ ステータス遷移タイムスタンプ履歴")
            history = art.get("status_history", [])
            for h in reversed(history):
                st.write(f"- **{h.get('timestamp')}** ➔ `【{h.get('status')}】` ({h.get('actor', '')})")
        
        st.divider()
        st.markdown("#### 📄 記事プレビュー（無料エリア / 有料エリア）")
        content = art.get("content", "")
        if "🔒 ここから先は有料エリアです" in content:
            parts = content.split("🔒 ここから先は有料エリアです")
            st.markdown(parts[0])
            st.markdown("""
            <div style='background-color: #1E293B; border: 2px dashed #F59E0B; border-radius: 8px; padding: 14px; margin: 14px 0;'>
                <strong style='color: #FCD34D;'>🔒 ここから先は有料エリア（noteの有料ライン設定位置）</strong>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(parts[1])
        else:
            st.markdown(content)
        
        st.markdown("#### 📢 5大SNS告知文（佐々木 翼 作成）")
        st.text_area("SNS告知テキスト", value=art.get("marketing", ""), height=250)
        
        st.markdown("#### 📋 note貼り付け用 マークダウン全文")
        st.text_area("記事コード", value=art.get("content", ""), height=300)

# ==========================================
# 7. 🤝 人事課（単一画面）
# ==========================================
elif page == "🤝 人事課":
    st.markdown("<div class='main-header'>🤝 人事課</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>担当: 綾瀬 七海（HR & Culture Director）</div>", unsafe_allow_html=True)

    st.markdown("#### 🏢 組織体制図 ＆ 職務分掌規程")
    with open(os.path.join(os.path.dirname(__file__), "companies/note_one_systems/org_chart_and_job_descriptions.json"), "r", encoding="utf-8") as f:
        org_data = json.load(f)
    
    st.write(f"**制定者:** {org_data.get('author')} | **バージョン:** {org_data.get('version')}")
    
    with st.expander("📋 9名の詳細職務分掌一覧を開く"):
        for dept in org_data["departments"]:
            st.markdown(f"**{dept['icon']} {dept['name']}** (統括: {dept['head']})")
            for role in dept["roles"]:
                st.write(f"- **{role['role_name']}（{role['member']}）**: {', '.join(role['responsibilities'][:2])}")
    
    st.markdown("#### 📊 社員別 リアルタイム業務負荷監視")
    stats = st.session_state.hr_manager.get_workload_stats()
    df_data = []
    for emp_id, data in stats.items():
        df_data.append({
            "社員名": data["name"],
            "役職": data["role"],
            "タスク回数": data["tasks"],
            "生成文字数": f"{data['words_generated']:,} 字",
            "負荷スコア": f"{data['workload_score']}%"
        })
    st.dataframe(pd.DataFrame(df_data), use_container_width=True)
    
    proposals = st.session_state.hr_manager.get_staffing_proposals()
    if proposals:
        for prop in proposals:
            st.warning(f"**【増員提案】対象部署: {prop['target_role']}（{prop['target_name']} / 負荷: {prop['workload_score']}%）** ➔ {prop['proposed_role']} の増員（費用0円）")

# ==========================================
# 8. 📚 法務課（単一画面）
# ==========================================
elif page == "📚 法務課":
    st.markdown("<div class='main-header'>📚 法務課</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>担当: 橘 律（Legal & Compliance Counsel）</div>", unsafe_allow_html=True)

    st.markdown("#### 📜 他部門からの法的調査・相談管理台帳")
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
                <strong style='font-size: 1.1rem; color: #FFFFFF;'>📋 {inv['category']}（ID: {inv['id']}）</strong>
                <span>{inv['status']}</span>
            </div>
            <div style='font-size: 0.8rem; color: #94A3B8; margin: 4px 0;'>
                🕒 受付: {inv['received_at']} | 調査開始: {inv['started_at']} | 完了: {inv['completed_at']}
            </div>
            <div style='font-size: 0.9rem; color: #E2E8F0;'><strong>相談元:</strong> {inv['requester_dept']}</div>
            <div style='font-size: 0.9rem; color: #E2E8F0; margin-top: 4px;'><strong>受付内容:</strong> {inv['inquiry_content']}</div>
            <div style='background-color: #0F172A; border: 1px solid #334155; padding: 12px; border-radius: 6px; margin-top: 10px; font-size: 0.9rem; color: #F8FAFC;'>
                <strong style='color: #38BDF8;'>⚖️ 橘 律 法的見解:</strong> {inv['legal_opinion']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 9. 📊 財務課（単一画面）
# ==========================================
elif page == "📊 財務課":
    st.markdown("<div class='main-header'>📊 財務課</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>担当: 白石 葵（Financial Strategist）</div>", unsafe_allow_html=True)

    st.markdown("#### 🎯 オーナー売上目標指示 ＆ 逆算ロードマップ")
    target_file = os.path.join(os.path.dirname(__file__), "data/sales_targets.json")
    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            target_data = json.load(f)
    else:
        target_data = {"monthly_target_yen": 100000, "target_articles_monthly": 15}
    
    c_tar1, c_tar2 = st.columns([2, 3])
    with c_tar1:
        new_target = st.number_input("月間売上目標金額（円）", min_value=10000, max_value=10000000, value=target_data.get("monthly_target_yen", 100000), step=10000)
        target_arts = st.slider("月間目標制作本数", min_value=5, max_value=60, value=target_data.get("target_articles_monthly", 15))
        if st.button("📢 売上目標を指示する", type="primary"):
            target_data["monthly_target_yen"] = int(new_target)
            target_data["target_articles_monthly"] = int(target_arts)
            target_data["updated_at"] = datetime.now().strftime("%Y-%m-%d")
            with open(target_file, "w", encoding="utf-8") as f:
                json.dump(target_data, f, ensure_ascii=False, indent=2)
            st.success("売上目標を更新しました。")
            st.rerun()
    with c_tar2:
        daily_req = int(new_target / 500 / 30)
        st.info(f"""
        **【財務逆算プラン】**
        - 🎯 **日別必要販売数:** 約 **{max(1, daily_req)}部**（単価500円想定）
        - 📝 **推奨リリース頻度:** 月 **{target_arts}本**
        - 💡 **財務アドバイス:** 500円入門記事で読者を集め、月末に1,480円のマガジンを投入するモデルが最も高収益です。
        """)

# ==========================================
# 10. 💳 経理課（単一画面）
# ==========================================
elif page == "💳 経理課":
    st.markdown("<div class='main-header'>💳 経理課</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>担当: 白石 葵（Chief Accountant 兼任）</div>", unsafe_allow_html=True)

    st.markdown("#### 💰 システム運用費用・0円運用管理台帳")
    acc_file = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/accounting_data.json")
    if os.path.exists(acc_file):
        with open(acc_file, "r", encoding="utf-8") as f:
            acc_data = json.load(f)
    else:
        acc_data = {"monthly_total_cost_yen": 0, "cost_items": []}
    
    st.success(f"**現在の月間システム運用費用合計:** :green[**¥{acc_data.get('monthly_total_cost_yen', 0):,} （完全無料0円）**]")
    
    cost_df = []
    for item in acc_data.get("cost_items", []):
        cost_df.append({
            "カテゴリ": item["category"],
            "サービス名": item["service_name"],
            "利用プラン": item["plan"],
            "月額費用": f"¥{item['monthly_cost_yen']:,}",
            "稼働状態": item["status"],
            "備考": item["notes"]
        })
    st.dataframe(pd.DataFrame(cost_df), use_container_width=True)
    st.caption("🛡️ **経理課ポリシー**: 就業規則第4条に基づき、代表者の稟議承認がない限り、1円たりとも課金は発生しません。")

# ==========================================
# 11. 💻 社内ヘルプデスク
# ==========================================
elif page == "💻 社内ヘルプデスク":
    st.markdown("<div class='main-header'>💻 社内ヘルプデスク</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>システム内で発生した全エラー・インシデントの管理台帳および解決状況</div>", unsafe_allow_html=True)

    err_file = os.path.join(os.path.dirname(__file__), "data/error_logs.json")
    if os.path.exists(err_file):
        with open(err_file, "r", encoding="utf-8") as f:
            err_data = json.load(f)
    else:
        err_data = {"errors": []}

    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        st.metric(label="総インシデント件数", value=f"{len(err_data.get('errors', []))} 件")
    with col_e2:
        st.metric(label="解決済み", value=f"{len([e for e in err_data.get('errors', []) if '解決' in e.get('status', '')])} 件")
    with col_e3:
        st.metric(label="システム健全性", value="100% (正常稼働)")

    st.markdown("---")
    st.markdown("<div class='section-title'>📋 エラー・トラブルシューティング管理台帳</div>", unsafe_allow_html=True)
    
    for err in err_data.get("errors", []):
        with st.container():
            st.markdown(f"""
            <div style='background-color: #1E293B; border: 1px solid #334155; border-left: 5px solid #007BA7; border-radius: 10px; padding: 18px; margin-bottom: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.25); color: #F8FAFC;'>
                <div style='display: flex; justify-content: space-between;'>
                    <strong style='font-size: 1.15rem; color: #FFFFFF;'>⚠️ {err['module']}（ID: {err['id']}）</strong>
                    <span>{err['status']}</span>
                </div>
                <div style='font-size: 0.8rem; color: #94A3B8; margin: 4px 0;'>🕒 発生日時: {err['occurred_at']}</div>
                <div style='background-color: #450A0A; border: 1px solid #991B1B; padding: 10px; border-radius: 6px; font-family: monospace; font-size: 0.85rem; color: #FCA5A5; margin: 8px 0;'>
                    {err['error_message']}
                </div>
                <div style='font-size: 0.9rem; color: #E2E8F0;'><strong>🔍 原因分析:</strong> {err['root_cause']}</div>
                <div style='font-size: 0.9rem; color: #4ADE80; margin-top: 4px;'><strong>🛠️ 対処手順・解決法:</strong> {err['solution']}</div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# 12. 👥 社員プロファイル
# ==========================================
elif page == "👥 社員プロファイル":
    st.markdown("<div class='main-header'>👥 社員別フォルダ ＆ プロファイル管理</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>9名の社員がそれぞれ独立したフォルダでプロンプト・設定を管理されています</div>", unsafe_allow_html=True)
    
    with open(os.path.join(os.path.dirname(__file__), "companies/note_one_systems/company_info.json"), "r", encoding="utf-8") as f:
        comp_info = json.load(f)

    for emp in comp_info["employees"]:
        with st.expander(f"{emp['icon']} {emp['name']}（{emp['role']}） - フォルダ: employees/{emp['folder']}/"):
            col_e1, col_e2 = st.columns([1, 2])
            with col_e1:
                st.markdown(f"**部署:** {emp.get('department', '')}")
                st.markdown(f"**モットー:** {emp['motto']}")
                st.markdown(f"**スキル:** {', '.join(emp['skills'])}")
            with col_e2:
                st.markdown("**システムプロンプト (prompt.txt):**")
                st.code(emp['prompt'], language="text")

# ==========================================
# 13. ☁️ 24時間無料クラウド設定ガイド
# ==========================================
elif page == "☁️ 24時間無料クラウド設定ガイド":
    st.markdown("<div class='main-header'>☁️ 24時間完全無料クラウド稼働マニュアル</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Macの電源を落としても、スマホや別PCからいつでもあなたのAI会社にアクセスできるようにする方法</div>", unsafe_allow_html=True)
    
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
