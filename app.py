import streamlit.components.v1 as components
import streamlit as st
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
    page_title="NoteOneSystems | バーチャルAI企業ホールディングス",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS（リッチなオフィスUI）
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.3rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.2rem;
    }
    .office-section-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1E293B;
        border-left: 4px solid #3B82F6;
        padding-left: 10px;
        margin: 16px 0 10px 0;
    }
    .desk-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        border-radius: 12px;
        padding: 14px;
        border: 1px solid #CBD5E1;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .desk-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
    }
    .status-live {
        display: inline-flex;
        align-items: center;
        background-color: #DCFCE7;
        color: #166534;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 9999px;
        border: 1px solid #86EFAC;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #22C55E;
        border-radius: 50%;
        margin-right: 6px;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(34, 197, 94, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
    }
    .chat-bubble {
        background-color: #FFFFFF;
        border-left: 4px solid #2563EB;
        padding: 14px 18px;
        border-radius: 10px;
        margin-bottom: 14px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    .paid-area-box {
        background-color: #FFFBEB;
        border: 2px dashed #F59E0B;
        border-radius: 8px;
        padding: 16px;
        margin: 16px 0;
    }
    .ringi-card {
        background-color: #F0FDF4;
        border: 1px solid #86EFAC;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 16px;
    }
    .legal-box {
        background-color: #FEF2F2;
        border: 1px solid #FCA5A5;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
    }
    .dept-box {
        background-color: #F1F5F9;
        border-left: 4px solid #0EA5E9;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 14px;
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

ai_client = AIClient(api_key=st.session_state.api_key)
workflow = NoteOneWorkflow(ai_client)

# ==========================================
# サイドバー
# ==========================================
with st.sidebar:
    st.markdown("## 🏢 NoteOneSystems")
    st.caption("バーチャルAI企業ホールディングス")
    
    st.markdown("---")
    menu = st.radio(
        "メニューを選択",
        [
            "🏢 ホールディングス本部",
            "✍️ NoteOneSystems オフィス（執務室）",
            "📚 完成記事・5大SNS販売センター",
            "📝 有料リソース稟議センター",
            "⚖️ 法務相談室・コンプライアンス",
            "🤝 人事部・体制図 ＆ 職務分掌",
            "📜 AI社員就業規則",
            "👥 社員別フォルダ・プロファイル",
            "☁️ 24時間無料クラウド設定ガイド"
        ]
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ AI頭脳設定（Gemini）")
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

# ==========================================
# 画面1: ホールディングス本部
# ==========================================
if menu == "🏢 ホールディングス本部":
    st.markdown("<div class='main-header'>🏢 バーチャルAI企業ホールディングス本部</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>グループ全体の経営状況、傘下子会社の統括ダッシュボード</div>", unsafe_allow_html=True)
    
    holdings_info = st.session_state.holdings_manager.get_holdings_info()
    companies = holdings_info.get("companies", [])
    articles = workflow.list_articles()
    
    # 売上目標の読み込み
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

    st.markdown("--- ")
    with st.expander("🎯 オーナー売上目標を指示する ＆ 財務アナリストによる逆算プラン"):
        st.markdown("#### 👑 オーナー（あなた）からの月間売上目標の指示")
        st.caption("目標金額を設定すると、財務アナリストの白石とCEOの一条が達成に必要な記事数・価格戦略を自動逆算します。")
        
        c_tar1, c_tar2 = st.columns([2, 3])
        with c_tar1:
            new_target = st.number_input("月間売上目標金額（円）", min_value=10000, max_value=10000000, value=target_sales, step=10000)
            target_arts = st.slider("月間目標制作本数", min_value=5, max_value=60, value=target_data.get("target_articles_monthly", 15))
            if st.button("📢 売上目標を全社に通達・指示する", type="primary"):
                target_data["monthly_target_yen"] = int(new_target)
                target_data["target_articles_monthly"] = int(target_arts)
                target_data["updated_at"] = datetime.now().strftime("%Y-%m-%d")
                with open(target_file, "w", encoding="utf-8") as f:
                    json.dump(target_data, f, ensure_ascii=False, indent=2)
                st.success(f"🎉 月商目標『¥{int(new_target):,}』を全社に通達しました！財務と制作部が目標達成プランを策定しました。")
                st.rerun()
        
        with c_tar2:
            st.markdown("#### 📊 財務アナリスト 白石 葵 による達成ロードマップ")
            daily_sales_req = int(new_target / 500 / 30)
            st.info(f"""
            **【目標達成のための逆算プラン】**
            - 🎯 **日別必要販売部数:** 1日あたり約 **{max(1, daily_sales_req)}部**（単価500円想定）
            - 📝 **推奨記事リリース頻度:** 月 **{target_arts}本**（2日に1本ペース）
            - 💡 **財務アドバイス:** 
              入門用ワンコイン記事（500円）で読者を獲得し、ノウハウを凝縮した高単価マガジン（1,480円〜2,980円）を組み合わせることで、成約率を最大化できます。
            """)

    st.markdown("---")
    st.subheader("📋 傘下のグループ会社一覧")
    for comp in companies:
        with st.container():
            c_col1, c_col2, c_col3 = st.columns([1, 4, 2])
            with c_col1:
                st.markdown(f"### {comp.get('icon', '🏢')}")
            with c_col2:
                st.markdown(f"**{comp['name']}**")
                st.caption(comp.get('description', ''))
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
# 画面2: NoteOneSystems オフィス（執務室）
# ==========================================
elif menu == "✍️ NoteOneSystems オフィス（執務室）":
    st.markdown("<div class='main-header'>🏢 NoteOneSystems 本社バーチャル執務フロア</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>9名の専門AI社員がそれぞれのデスクで自律的に業務を行っています</div>", unsafe_allow_html=True)

    # 1. 2Dアニメーティブ・ゲーム風バーチャルオフィス（HTML5 Canvas & CSS Keyframes）
    st.markdown("### 🎮 リアルタイム 2Dアニメーティブ・オフィス（ゲーム画面ビュー）")
    st.caption("💡 社員たちが歩き回り、PCタイピングしながらリアルタイムにつぶやきます。社員をクリックしても会話できます！")
    
    html_path = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/assets/game_office.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            game_html = f.read()
        components.html(game_html, height=480)
    
    with st.expander("🖼️ 3Dアイソメトリック見取り図（詳細レイアウト）を表示"):
        img_path = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/assets/office_floor.jpg")
        if os.path.exists(img_path):
            st.image(img_path, caption="NoteOneSystems 3Dオフィスフロア見取り図", use_container_width=True)

    st.markdown("---")
    
    # 2. 部署別・執務席ライブステータス（座席表）
    st.markdown("### 🖥️ フロア別 執務デスク＆稼働状況")
    
    tab_floor1, tab_floor2, tab_floor3 = st.tabs(["🏛️ 経営統括 ＆ ガバナンス室", "✍️ コンテンツ制作スタジオ", "📢 マーケティング ＆ 財務ハブ"])
    
    with tab_floor1:
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            st.markdown("""
            <div class='desk-card'>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='font-size: 1.6rem;'>👩‍💼</span>
                    <span class='status-live'><span class='pulse-dot'></span>執務中</span>
                </div>
                <div style='font-weight: 700; font-size: 1.1rem; margin-top: 4px;'>一条 蓮</div>
                <div style='font-size: 0.8rem; color: #1E3A8A; font-weight: 600;'>代表取締役CEO</div>
                <div style='font-size: 0.75rem; color: #64748B; margin-top: 6px;'>📍 CEO Private Suite</div>
                <div style='font-size: 0.75rem; margin-top: 6px; background: #EEF2FF; padding: 6px; border-radius: 6px;'>💬 「全社売上最大化と、完全無料運用の規律を監督しています。」</div>
            </div>
            """, unsafe_allow_html=True)
        with col_f2:
            st.markdown("""
            <div class='desk-card'>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='font-size: 1.6rem;'>⚖️</span>
                    <span class='status-live'><span class='pulse-dot'></span>法務監視中</span>
                </div>
                <div style='font-weight: 700; font-size: 1.1rem; margin-top: 4px;'>橘 律</div>
                <div style='font-size: 0.8rem; color: #334155; font-weight: 600;'>法務・コンプライアンス顧問</div>
                <div style='font-size: 0.75rem; color: #64748B; margin-top: 6px;'>📍 Legal Department</div>
                <div style='font-size: 0.75rem; margin-top: 6px; background: #F1F5F9; padding: 6px; border-radius: 6px;'>💬 「会社法・著作権法・note規約の適合性を常時スクリーニングしています。」</div>
            </div>
            """, unsafe_allow_html=True)
        with col_f3:
            st.markdown("""
            <div class='desk-card'>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='font-size: 1.6rem;'>🤝</span>
                    <span class='status-live'><span class='pulse-dot'></span>負荷監視中</span>
                </div>
                <div style='font-weight: 700; font-size: 1.1rem; margin-top: 4px;'>綾瀬 七海</div>
                <div style='font-size: 0.8rem; color: #059669; font-weight: 600;'>人事・労務責任者</div>
                <div style='font-size: 0.75rem; color: #64748B; margin-top: 6px;'>📍 HR Department</div>
                <div style='font-size: 0.75rem; margin-top: 6px; background: #ECFDF5; padding: 6px; border-radius: 6px;'>💬 「各社員の業務負荷スコアを測定し、過負荷を未然に防止しています。」</div>
            </div>
            """, unsafe_allow_html=True)

    with tab_floor2:
        col_c1, col_c2, col_c3, col_c4 = st.columns(4)
        with col_c1:
            st.markdown("""
            <div class='desk-card'>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='font-size: 1.6rem;'>🔍</span>
                    <span class='status-live'><span class='pulse-dot'></span>リサーチ中</span>
                </div>
                <div style='font-weight: 700; font-size: 1.1rem; margin-top: 4px;'>風間 涼</div>
                <div style='font-size: 0.8rem; color: #0D9488; font-weight: 600;'>市場リサーチ担当</div>
                <div style='font-size: 0.75rem; color: #64748B; margin-top: 6px;'>📍 Research Desk</div>
                <div style='font-size: 0.75rem; margin-top: 6px; background: #F0FDFA; padding: 6px; border-radius: 6px;'>💬 「noteの売れ筋トレンドと読者ペルソナを分析中です。」</div>
            </div>
            """, unsafe_allow_html=True)
        with col_c2:
            st.markdown("""
            <div class='desk-card'>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='font-size: 1.6rem;'>📑</span>
                    <span class='status-live'><span class='pulse-dot'></span>構成設計中</span>
                </div>
                <div style='font-weight: 700; font-size: 1.1rem; margin-top: 4px;'>結城 紬</div>
                <div style='font-size: 0.8rem; color: #D97706; font-weight: 600;'>統括編集長</div>
                <div style='font-size: 0.75rem; color: #64748B; margin-top: 6px;'>📍 Editorial Studio</div>
                <div style='font-size: 0.75rem; margin-top: 6px; background: #FFFBEB; padding: 6px; border-radius: 6px;'>💬 「購入率を高める有料ラインの境界線を設計しています。」</div>
            </div>
            """, unsafe_allow_html=True)
        with col_c3:
            st.markdown("""
            <div class='desk-card'>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='font-size: 1.6rem;'>✍️</span>
                    <span class='status-live'><span class='pulse-dot'></span>執筆待機中</span>
                </div>
                <div style='font-weight: 700; font-size: 1.1rem; margin-top: 4px;'>森川 拓真</div>
                <div style='font-size: 0.8rem; color: #EA580C; font-weight: 600;'>チーフライター</div>
                <div style='font-size: 0.75rem; color: #64748B; margin-top: 6px;'>📍 Writer Studio</div>
                <div style='font-size: 0.75rem; margin-top: 6px; background: #FFF7ED; padding: 6px; border-radius: 6px;'>💬 「コピペで即使える実践テンプレートの執筆スタンバイ完了。」</div>
            </div>
            """, unsafe_allow_html=True)
        with col_c4:
            st.markdown("""
            <div class='desk-card'>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='font-size: 1.6rem;'>🛡️</span>
                    <span class='status-live'><span class='pulse-dot'></span>QA待機中</span>
                </div>
                <div style='font-weight: 700; font-size: 1.1rem; margin-top: 4px;'>神崎 玲奈</div>
                <div style='font-size: 0.8rem; color: #DC2626; font-weight: 600;'>品質管理責任者 (QA)</div>
                <div style='font-size: 0.75rem; color: #64748B; margin-top: 6px;'>📍 QA Inspection Booth</div>
                <div style='font-size: 0.75rem; margin-top: 6px; background: #FEF2F2; padding: 6px; border-radius: 6px;'>💬 「信憑性と100点満点スコアリングの準備万全です。」</div>
            </div>
            """, unsafe_allow_html=True)

    with tab_floor3:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("""
            <div class='desk-card'>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='font-size: 1.6rem;'>📢</span>
                    <span class='status-live'><span class='pulse-dot'></span>5大SNS待機中</span>
                </div>
                <div style='font-weight: 700; font-size: 1.1rem; margin-top: 4px;'>佐々木 翼</div>
                <div style='font-size: 0.8rem; color: #2563EB; font-weight: 600;'>マルチSNSマーケター</div>
                <div style='font-size: 0.75rem; color: #64748B; margin-top: 6px;'>📍 Marketing Hub</div>
                <div style='font-size: 0.75rem; margin-top: 6px; background: #EFF6FF; padding: 6px; border-radius: 6px;'>💬 「X・IG・Threads・Bluesky・Mastodonへの自動プロモーション待機中。」</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown("""
            <div class='desk-card'>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='font-size: 1.6rem;'>📊</span>
                    <span class='status-live'><span class='pulse-dot'></span>財務分析中</span>
                </div>
                <div style='font-weight: 700; font-size: 1.1rem; margin-top: 4px;'>白石 葵</div>
                <div style='font-size: 0.8rem; color: #7C3AED; font-weight: 600;'>財務アナリスト</div>
                <div style='font-size: 0.75rem; color: #64748B; margin-top: 6px;'>📍 Finance Booth</div>
                <div style='font-size: 0.75rem; margin-top: 6px; background: #F5F3FF; padding: 6px; border-radius: 6px;'>💬 「最適価格のデータ算出と稟議ROI試算を準備しています。」</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    
    # 3. 記事制作指示センター（中央会議室への召集）
    st.markdown("### 🗣️ 中央ガラス会議室（Central Strategy Room）：記事制作指示")
    
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
                            <div style='font-weight: bold;'>{log.get('icon')} {log.get('name')} <span style='font-size: 0.8rem; color: #64748B;'>（{log.get('role')}）</span></div>
                            <div style='white-space: pre-wrap; margin-top: 6px; font-size: 0.95rem;'>{log.get('content')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                elif event.get("status") == "completed":
                    completed_article = event.get("article")
                    progress_bar.progress(1.0)
                    status_text.markdown("✅ **全工程（執筆・法務・QA・5大SNSプロモーション）が完了しました！**")
            
            if completed_article:
                st.success(f"🎉 記事『{completed_article['title']}』が完成しました！「完成記事・5大SNS販売センター」で確認できます。")

# ==========================================
# 画面3: 完成記事・5大SNS販売センター
# ==========================================
elif menu == "📚 完成記事・5大SNS販売センター":
    st.markdown("<div class='main-header'>📚 完成記事 ＆ 5大SNS販売センター</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>記事のプレビュー、法務・QA審査結果、および5大SNS（X, IG, Threads, Bluesky, Mastodon）向け告知文</div>", unsafe_allow_html=True)
    
    articles = workflow.list_articles()
    
    if not articles:
        st.info("まだ作成された記事がありません。「NoteOneSystems オフィス」から記事を作成してみましょう！")
    else:
        article_titles = [f"{art.get('created_at', '')} | {art.get('title', '')}" for art in articles]
        selected_idx = st.selectbox("確認・出品する記事を選択", range(len(articles)), format_func=lambda x: article_titles[x])
        art = articles[selected_idx]
        
        tab_art, tab_sns, tab_sns_config, tab_qa_legal, tab_raw = st.tabs([
            "📄 記事プレビュー（無料/有料）",
            "📢 5大SNS告知文（即コピー可能）",
            "⚙️ SNSアカウント・自動投稿先設定",
            "⚖️ 法務・QA審査レポート",
            "📋 note貼り付け用テキスト"
        ])
        
        with tab_art:
            st.markdown(f"## {art.get('title', '')}")
            st.caption(f"作成日時: {art.get('created_at')} | 想定価格: {art.get('price', 500)}円")
            st.divider()
            content = art.get("content", "")
            if "🔒 ここから先は有料エリアです" in content:
                parts = content.split("🔒 ここから先は有料エリアです")
                st.markdown(parts[0])
                st.markdown("""
                <div class='paid-area-box'>
                    <h4>🔒 ここから先は有料エリア（noteの有料ライン設定位置）</h4>
                    <p style='color: #B45309; font-size: 0.9rem;'>noteの投稿画面で「ここから有料」ラインをこの位置に設定してください。</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(parts[1])
            else:
                st.markdown(content)

        with tab_sns:
            st.markdown("### 📢 5大SNSマルチプロモーションセット（佐々木 翼 作成）")
            st.text_area("5大SNS告知文（X, Instagram, Threads, Bluesky, Mastodon）", value=art.get("marketing", ""), height=400)
            if "sns_results" in art:
                st.markdown("#### 🚀 SNS配信ステータス")
                for key, res in art["sns_results"].items():
                    st.write(f"- **{res['platform']}**: :green[{res['status']}] ({res['cost']})")

        with tab_sns_config:
            st.markdown("### ⚙️ 5大SNSアカウント ＆ 自動配信先の設定")
            st.caption("あなたがお持ちのSNSアカウント情報やAPIキー（無料枠）をここで登録・指示できます。")
            
            cfg_path = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/sns_config.json")
            if os.path.exists(cfg_path):
                with open(cfg_path, "r", encoding="utf-8") as f:
                    sns_cfg = json.load(f)
            else:
                sns_cfg = {}
            
            c_x, c_ig = st.columns(2)
            with c_x:
                st.markdown("#### 🐦 X (旧Twitter)")
                x_acc = st.text_input("X アカウント名 / ID", value=sns_cfg.get("x", {}).get("account_name", "@NoteOneSystems"))
                x_key = st.text_input("X API Key (無料枠・任意)", value=sns_cfg.get("x", {}).get("api_key", ""), type="password", help="APIキー未設定時はワンクリックコピーで即投稿できます。")
            with c_ig:
                st.markdown("#### 📸 Instagram")
                ig_acc = st.text_input("Instagram アカウント名", value=sns_cfg.get("instagram", {}).get("account_name", "@noteonesystems_official"))
            
            c_th, c_bs = st.columns(2)
            with c_th:
                st.markdown("#### 🧵 Threads")
                th_acc = st.text_input("Threads アカウント名", value=sns_cfg.get("threads", {}).get("account_name", "@noteonesystems_official"))
            with c_bs:
                st.markdown("#### 🦋 Bluesky（完全無料・即自動投稿可）")
                bs_handle = st.text_input("Bluesky ハンドル名", value=sns_cfg.get("bluesky", {}).get("handle", "noteonesystems.bsky.social"))
                bs_pass = st.text_input("Bluesky App Password (任意)", value=sns_cfg.get("bluesky", {}).get("app_password", ""), type="password")
            
            st.markdown("#### 🐘 Mastodon（完全無料）")
            mast_inst = st.text_input("Mastodon インスタンスURL", value=sns_cfg.get("mastodon", {}).get("instance", "https://mstdn.jp"))
            
            if st.button("💾 SNSアカウント設定を保存する", type="primary"):
                sns_cfg["x"]["account_name"] = x_acc
                sns_cfg["x"]["api_key"] = x_key
                sns_cfg["instagram"]["account_name"] = ig_acc
                sns_cfg["threads"]["account_name"] = th_acc
                sns_cfg["bluesky"]["handle"] = bs_handle
                sns_cfg["bluesky"]["app_password"] = bs_pass
                sns_cfg["mastodon"]["instance"] = mast_inst
                with open(cfg_path, "w", encoding="utf-8") as f:
                    json.dump(sns_cfg, f, ensure_ascii=False, indent=2)
                st.success("🎉 5大SNSアカウント設定を保存しました！マーケター佐々木がこの設定先に配信します。")

        with tab_qa_legal:
            col_q1, col_q2 = st.columns(2)
            with col_q1:
                st.markdown("### 🛡️ 品質管理 (QA) 神崎 玲奈")
                st.info(art.get("qa_score", "審査完了: 95点/100点 (合格)"))
            with col_q2:
                st.markdown("### ⚖️ 法務顧問 橘 律")
                st.success(art.get("legal_check", "適法審査完了: 会社法・著作権法・note規約適合"))

        with tab_raw:
            st.markdown("### 📋 note貼り付け用 マークダウン")
            st.text_area("全文コード（全選択してnoteにペースト）", value=art.get("content", ""), height=450)

# ==========================================
# 画面4: 有料リソース稟議センター
# ==========================================
elif menu == "📝 有料リソース稟議センター":
    st.markdown("<div class='main-header'>📝 有料リソース稟議センター（Ringi Workflow）</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>売上向上につながる有料ツール・APIについて、ROI（投資回収率）を明記して代表者に決裁を仰ぐシステム</div>", unsafe_allow_html=True)
    
    st.info("💡 **完全無料原則**: あなたが「承認」ボタンを押さない限り、1円も課金されることはありません。")
    
    ringi_list = st.session_state.ringi_manager.list_ringi()
    for ringi in ringi_list:
        status_color = ":orange[未決裁（審議中）]" if ringi["status"] == "pending" else (":green[承認済]" if ringi["status"] == "approved" else ":red[却下]")
        
        with st.container():
            st.markdown(f"""
            <div class='ringi-card'>
                <h3>📋 {ringi['title']}</h3>
                <p><strong>起案者:</strong> {ringi['proposer']} | <strong>起案日:</strong> {ringi['created_at']}</p>
                <hr>
                <p><strong>概要:</strong> {ringi['summary']}</p>
                <div style='background-color: #FFFFFF; padding: 12px; border-radius: 8px; margin: 10px 0;'>
                    <p>💰 <strong>月額費用:</strong> ¥{ringi.get('cost_monthly_yen', 0):,}</p>
                    <p>📈 <strong>想定増収額:</strong> +¥{ringi.get('estimated_increase_sales_yen', 0):,} / 月</p>
                    <p>🎯 <strong>想定ROI（投資回収率）:</strong> {ringi.get('roi_percentage', 0)}%</p>
                </div>
                <p><strong>費用対効果詳細:</strong> {ringi['roi_analysis']}</p>
                <p><strong>無料の代替案:</strong> {ringi['free_alternative']}</p>
                <p><strong>CEO見解:</strong> {ringi['ceo_opinion']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"**現在の決裁状態:** {status_color}")
            if ringi["status"] == "pending":
                col_btn1, col_btn2, _ = st.columns([1, 1, 4])
                with col_btn1:
                    if st.button("✅ 承認する", key=f"app_{ringi['id']}", type="primary"):
                        st.session_state.ringi_manager.update_ringi_status(ringi['id'], "approved")
                        st.success("稟議を承認しました。")
                        st.rerun()
                with col_btn2:
                    if st.button("❌ 却下（無料を継続）", key=f"rej_{ringi['id']}"):
                        st.session_state.ringi_manager.update_ringi_status(ringi['id'], "rejected")
                        st.info("稟議を却下し、完全無料運用を継続します。")
                        st.rerun()
            st.divider()

# ==========================================
# 画面5: 法務相談室・コンプライアンス
# ==========================================
elif menu == "⚖️ 法務相談室・コンプライアンス":
    st.markdown("<div class='main-header'>⚖️ 法務相談室 ＆ コンプライアンス（橘 律 監修）</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>会社法、著作権法、景品表示法、note利用規約に対する公式見解と適法ガイドライン</div>", unsafe_allow_html=True)
    
    with open(os.path.join(os.path.dirname(__file__), "companies/note_one_systems/legal_opinions.json"), "r", encoding="utf-8") as f:
        legal_data = json.load(f)
    
    for op in legal_data["opinions"]:
        st.markdown(f"""
        <div class='legal-box'>
            <h3>📜 {op['topic']}</h3>
            <p><strong>法的根拠:</strong> {op['legal_basis']} | <strong>判定:</strong> {op['risk_level']}</p>
            <p>{op['summary']}</p>
        </div>
        """, unsafe_allow_html=True)
        if "guidelines" in op:
            st.markdown("#### 遵守ガイドライン")
            for g in op["guidelines"]:
                st.write(f"- {g}")
        st.divider()

# ==========================================
# 画面6: 人事部・体制図 ＆ 職務分掌
# ==========================================
elif menu == "🤝 人事部・体制図 ＆ 職務分掌":
    st.markdown("<div class='main-header'>🤝 人事部 ＆ 組織体制図・職務分掌（綾瀬 七海 監修）</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>9名の専門AI組織の体制図、詳細職務分掌規程、およびリアルタイム業務負荷管理</div>", unsafe_allow_html=True)
    
    tab_org, tab_roles, tab_load = st.tabs(["🏢 新組織体制図", "📋 詳細職務分掌規程", "📊 社員別 業務負荷監視"])
    
    with open(os.path.join(os.path.dirname(__file__), "companies/note_one_systems/org_chart_and_job_descriptions.json"), "r", encoding="utf-8") as f:
        org_data = json.load(f)

    with tab_org:
        st.subheader("🏢 NoteOneSystems 組織体制図")
        st.markdown("""
        ```mermaid
        flowchart TD
            CEO["👩‍💼 代表取締役CEO: 一条 蓮<br>【経営企画・全社統括・稟議決裁】"]
            
            subgraph 内部統制・ガバナンス
                LEGAL["⚖️ 法務顧問: 橘 律<br>【法令・note規約・商号審査】"]
                HR["🤝 人事責任者: 綾瀬 七海<br>【負荷監視・増員提案・就業規則】"]
            end
            
            subgraph コンテンツ制作事業部
                RESEARCH["🔍 市場リサーチ: 風間 涼<br>【ペルソナ・競合分析】"]
                EDITOR["📑 統括編集長: 結城 紬<br>【構成・目次・有料ライン設計】"]
                WRITER["✍️ チーフライター: 森川 拓真<br>【本文・実践テンプレ執筆】"]
                QA["🛡️ 品質管理責任者: 神崎 玲奈<br>【ファクトチェック・100点採点】"]
            end
            
            subgraph マーケティング・財務
                MKT["📢 マルチSNSマーケター: 佐々木 翼<br>【5大SNS自動プロモーション】"]
                FIN["📊 財務アナリスト: 白石 葵<br>【最適価格・稟議ROI試算】"]
            end
            
            CEO --> LEGAL
            CEO --> HR
            CEO --> RESEARCH
            RESEARCH --> FIN
            FIN --> CEO
            CEO --> EDITOR
            EDITOR --> WRITER
            WRITER --> LEGAL
            LEGAL --> QA
            QA --> MKT
            MKT --> HR
        ```
        """)
        st.info("💡 **組織の特徴**: 編集長とライターの役割分離、法務とQAの二重審査、人事による負荷監視が自律的に連携する高信頼設計です。")

    with tab_roles:
        st.subheader("📋 9名の詳細職務分掌規程")
        for dept in org_data["departments"]:
            with st.container():
                st.markdown(f"""
                <div class='dept-box'>
                    <h3>{dept['icon']} {dept['name']}</h3>
                    <p><strong>統括責任者:</strong> {dept['head']} | <strong>ミッション:</strong> {dept['mission']}</p>
                </div>
                """, unsafe_allow_html=True)
                for role in dept["roles"]:
                    with st.expander(f"{role['icon']} {role['role_name']}（{role['member']}）の職責とKPI"):
                        st.markdown("**【主な職務・権限】**")
                        for resp in role["responsibilities"]:
                            st.write(f"- {resp}")
                        st.markdown("**【主要成果責任 (KPI)】**")
                        st.write(f"🎯 {', '.join(role['kpis'])}")
                st.divider()

    with tab_load:
        st.subheader("📊 社員別 リアルタイム業務負荷ステータス")
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
        
        st.markdown("---")
        st.subheader("💡 人事部からの増員提案")
        proposals = st.session_state.hr_manager.get_staffing_proposals()
        if proposals:
            for prop in proposals:
                st.warning(f"""
                **【増員提案】対象部署: {prop['target_role']}（{prop['target_name']} / 負荷スコア: {prop['workload_score']}%）**
                - **提案内容:** {prop['proposed_role']} の新規雇用・配属
                - **理由:** {prop['reason']}
                - **費用:** {prop['cost']}
                """)
        else:
            st.success("現在、過度の業務偏重はありません。健全に稼働しています。")

# ==========================================
# 画面7: AI社員就業規則
# ==========================================
elif menu == "📜 AI社員就業規則":
    st.markdown("<div class='main-header'>📜 NoteOneSystems 株式会社 AI社員就業規則</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>就業規則 Ver 0.9（プレオープン版）</div>", unsafe_allow_html=True)
    
    with open(os.path.join(os.path.dirname(__file__), "companies/note_one_systems/employment_regulations.json"), "r", encoding="utf-8") as f:
        reg = json.load(f)
    
    st.markdown(f"**制定・改定者:** {reg.get('author', '人事部')} | **バージョン:** {reg.get('version', '0.9 (プレオープン版)')} | **施行日:** {reg.get('effective_date', '2026-08-24')}")
    st.markdown(f"**【前文】**\n\n{reg['preamble']}")
    st.divider()
    
    for ch in reg["chapters"]:
        st.subheader(ch["chapter"])
        for art in ch["articles"]:
            st.markdown(f"**{art['article']}**")
            st.write(art["content"])
            st.write("")
        st.divider()

# ==========================================
# 画面8: 社員別フォルダ・プロファイル
# ==========================================
elif menu == "👥 社員別フォルダ・プロファイル":
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
# 画面9: 24時間無料クラウド設定ガイド
# ==========================================
elif menu == "☁️ 24時間無料クラウド設定ガイド":
    st.markdown("<div class='main-header'>☁️ 24時間完全無料クラウド稼働マニュアル</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Macの電源を落としても、スマホや別PCからいつでもあなたのAI会社にアクセスできるようにする方法</div>", unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 完全無料（0円）でクラウド稼働させる3ステップ
    
    #### 1️⃣ ステップ1: GitHub（無料）にプログラムを保存
    1. [GitHub](https://github.com/) にアクセスし、新しいリポジトリ（Private）を作成します。
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
