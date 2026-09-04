import json
import os

def get_office_game_html(lang: str = "en") -> str:
    """Generates the interactive 2D Virtual Office HTML with full dynamic employee support and i18n."""
    is_ja = (lang == "ja")

    # Load dynamic employees from company_info.json
    info_path = os.path.join(os.path.dirname(__file__), "company_info.json")
    all_employees = []
    if os.path.exists(info_path):
        try:
            with open(info_path, "r", encoding="utf-8") as f:
                c_data = json.load(f)
                all_employees = c_data.get("employees", [])
        except Exception:
            all_employees = []
            
    total_staff = len(all_employees) if all_employees else 9

    # Texts and labels
    hud_title = "🏢 Note One Systems バーチャルオフィスフロア" if is_ja else "🏢 Note One Systems Virtual Office Floor"
    hud_live = f"出社中: {total_staff}名（全員稼働中）" if is_ja else f"Live in Office: {total_staff}/{total_staff}"
    
    zone_ceo = "👑 役員執務室 (CEO)" if is_ja else "👑 Executive Suite"
    zone_admin = "🏛️ 管理部 (法務・人事・財務)" if is_ja else "🏛️ Administration"
    zone_center_title = "🗣️ ガラス張り戦略会議室" if is_ja else "🗣️ Strategy Glass Room"
    zone_center_table = "💡 全社戦略ミーティングテーブル" if is_ja else "💡 Central Strategy Table"
    zone_pr = "📢 広報課 (5大SNS運用)" if is_ja else "📢 Public Relations"
    zone_editorial = "📝 編集制作部 (調査・編集・執筆・増員ブース・QA)" if is_ja else "📝 Editorial Dept"

    # Employee names
    emp_names = {
        "ichijo": "一条 蓮 (CEO)" if is_ja else "Ichijo (CEO)",
        "tachibana": "橘 律 (法務)" if is_ja else "Tachibana (Legal)",
        "ayase": "綾瀬 七海 (人事)" if is_ja else "Ayase (HR)",
        "shiraishi": "白石 葵 (財務経理)" if is_ja else "Shiraishi (Finance)",
        "kazama": "風間 涼 (市場調査)" if is_ja else "Kazama (Research)",
        "yuki": "結城 紬 (編集長)" if is_ja else "Yuki (Editor)",
        "morikawa": "森川 拓真 (ライター)" if is_ja else "Morikawa (Writer)",
        "kanzaki": "神崎 玲奈 (品質管理)" if is_ja else "Kanzaki (QA)",
        "sasaki": "佐々木 翼 (広報)" if is_ja else "Sasaki (PR)",
        "kiryu": "桐生 蓮 (サブライター)" if is_ja else "Kiryu (Writer Assist)"
    }

    # Employee dialogue pools
    if is_ja:
        speeches = {
            "ichijo": [
                "全社の売上最大化と無料運用の規律を監督しています。",
                "読者満足度100%と高評価レビューを徹底します。",
                "完全無料（0円運用）で最大の利益を生み出します！"
            ],
            "tachibana": [
                "法務調査台帳確認済：note規約・著作権適合です。",
                "会社法第7条および商号表記スクリーニング完了！",
                "コンプライアンス審査クリア、法的リスクゼロです。"
            ],
            "ayase": [
                "全社員の業務負荷スコア監視中：健全稼働です ✨",
                "就業規則Ver1.0に基づき円滑にオフィスを運営中。",
                "必要に応じた無料増員計画のスタンバイも万全です。"
            ],
            "shiraishi": [
                "月額固定費0円（完全無料）確認完了 💰",
                "基本価格300円基準規程（粗利率85%）を厳格監査中 📈",
                "経理帳簿は正常、1円の無駄も発生していません。"
            ],
            "kazama": [
                "noteの最新トレンドキーワードを調査中... 🔍",
                "購入意欲の高い読者ペルソナの購買動線を分析！",
                "競合不在のブルーオーシャントピックを発見しました。"
            ],
            "yuki": [
                "購入率を高める有料ラインの境界線を設計中！",
                "読者の興味を惹きつけるタイトル構成をブラッシュアップ。",
                "森川さん、この黄金テンプレート構成で執筆を！"
            ],
            "morikawa": [
                "コピペで使える実践テンプレートを執筆中 ⚡",
                "自己流を排した再現性の高いノウハウを執筆完了！",
                "アスタリスクを使わず、美しい日本語で執筆しています。"
            ],
            "kanzaki": [
                "ファクトチェック完了：採点スコア95点！品質認証 🛡️",
                "誤字脱字ゼロ、論理構成とエビデンス確認済。",
                "信憑性スコアリング完了、オーナー決裁へ提出します。"
            ],
            "sasaki": [
                "X・Threads・Blueskyへ同時告知準備完了 📢",
                "Instagramカルーセルスライド案を制作中！",
                "Mastodonにも最新ノウハウ要約を投稿スタンバイ ✨"
            ],
            "kiryu": [
                "森川先輩の執筆を全力バックアップ中！テンプレート量産完了 🖋️",
                "4,000字以上の実践ノウハウ、速筆リライト体制万全です！",
                "先輩の負荷スコアを半減させるため、本日も全力執筆します！"
            ]
        }
    else:
        speeches = {
            "ichijo": [
                "Maximizing global revenue & enterprise value.",
                "Enforcing zero-cost operational discipline.",
                "Ensuring 100% subscriber satisfaction."
            ],
            "tachibana": [
                "Legal inquiry ledger verified: Fully compliant.",
                "Ensuring strict corporate & copyright compliance.",
                "Platform terms & privacy check passed!"
            ],
            "ayase": [
                "Monitoring workload metrics: Healthy distribution ✨",
                "Operating under Corporate Rulebook v1.0.",
                "Zero-cost staffing expansion ready if needed."
            ],
            "shiraishi": [
                "Monthly fixed costs verified at ¥0 (Zero Cost) 💰",
                "Rule-PRC-300 standard pricing audited with ~85% net margin!",
                "Accounting ledger balanced and operating smoothly 📈"
            ],
            "kazama": [
                "Analyzing top trending topics on note... 🔍",
                "Identifying high-intent buyer personas.",
                "Targeting uncontested profitable niches!"
            ],
            "yuki": [
                "Designing optimal paywall conversion ratio!",
                "Structuring high-impact compelling headlines.",
                "Morikawa-san, drafting with this proven framework!"
            ],
            "morikawa": [
                "Drafting actionable copy-and-paste templates ⚡",
                "Writing high-speed practical workflows!",
                "Structuring clear, immediate step-by-step guides."
            ],
            "kanzaki": [
                "Article status & audit trail updated 🛡️",
                "Fact-check score: 95/100! Quality Certified.",
                "Zero typos, high readability & logical flow!"
            ],
            "sasaki": [
                "Multi-syndicating across X, Threads & Bluesky 📢",
                "Instagram carousel assets prepared!",
                "Broadcasting actionable insights on Mastodon ✨"
            ],
            "kiryu": [
                "Supporting Morikawa-san with high-speed template drafting! 🖋️",
                "4,000+ words actionable content drafted & verified.",
                "Halving workload bottlenecks with autonomous writing sprints!"
            ]
        }

    from .dialogue_engine import EmployeeDialogueEngine
    dialogue_engine = EmployeeDialogueEngine()

    # Dynamic positioning & avatar setup
    BASE_POSITIONS = {
        "ichijo": {"top": "100px", "left": "100px", "walk": True},
        "tachibana": {"top": "290px", "left": "50px", "walk": False},
        "ayase": {"top": "405px", "left": "50px", "walk": True},
        "shiraishi": {"top": "350px", "left": "180px", "walk": False},
        "kazama": {"top": "290px", "left": "340px", "walk": False},
        "yuki": {"top": "290px", "left": "470px", "walk": True},
        "morikawa": {"top": "290px", "left": "600px", "walk": False},
        "kanzaki": {"top": "405px", "left": "470px", "walk": False},
        "sasaki": {"top": "100px", "left": "760px", "walk": True},
        "kiryu": {"top": "405px", "left": "600px", "walk": True},
    }

    EXPANSION_SLOTS = [
        {"top": "405px", "left": "600px", "walk": True},   # Under Morikawa (Kiryu / Writer assistant)
        {"top": "405px", "left": "340px", "walk": True},   # Under Kazama (Saotome / SEO)
        {"top": "100px", "left": "660px", "walk": True},   # Near Sasaki (PR Expansion)
        {"top": "195px", "left": "450px", "walk": True},   # Meeting Table Center (Misaki / Design)
        {"top": "195px", "left": "380px", "walk": True},   # Meeting Table Left
        {"top": "195px", "left": "520px", "walk": True},   # Meeting Table Right
        {"top": "240px", "left": "180px", "walk": True},   # Admin Wing
        {"top": "180px", "left": "780px", "walk": True},   # PR Wing lower
    ]

    dynamic_css_lines = []
    dynamic_avatars = []
    used_positions = set()
    for e_id, pos in BASE_POSITIONS.items():
        used_positions.add((pos["top"], pos["left"]))
        dynamic_css_lines.append(f"  #emp-{e_id} {{ top: {pos['top']}; left: {pos['left']}; }}")

    exp_slot_idx = 0

    # Ensure all employees in all_employees are registered
    for emp in all_employees:
        e_id = emp["id"]
        e_name = emp_names.get(e_id, f"{emp['name']} ({emp.get('role', 'AI')[:4]})")
        
        # Speeches
        if e_id not in speeches:
            motto = emp.get("motto", "読者に価値を届けるため、全力で業務を遂行します。")
            role = emp.get("role", "専門AI")
            speeches[e_id] = [
                f"「{motto}」✨",
                f"{role}として、チームの生産性と記事品質を全力支援中！",
                f"配属完了！代表者様、いつでもご指示をお待ちしています！"
            ]
            
        # Position
        if e_id in BASE_POSITIONS:
            walk_cls = "walk-around" if BASE_POSITIONS[e_id]["walk"] else ""
        else:
            # Pick from expansion slot
            while exp_slot_idx < len(EXPANSION_SLOTS) and (EXPANSION_SLOTS[exp_slot_idx]["top"], EXPANSION_SLOTS[exp_slot_idx]["left"]) in used_positions:
                exp_slot_idx += 1
            if exp_slot_idx < len(EXPANSION_SLOTS):
                slot = EXPANSION_SLOTS[exp_slot_idx]
                exp_slot_idx += 1
            else:
                slot = {"top": "195px", "left": f"{350 + (exp_slot_idx * 30) % 200}px", "walk": True}
                exp_slot_idx += 1
            used_positions.add((slot["top"], slot["left"]))
            walk_cls = "walk-around" if slot["walk"] else ""
            dynamic_css_lines.append(f"  #emp-{e_id} {{ top: {slot['top']}; left: {slot['left']}; }}")

        e_color = emp.get("color", "#38BDF8")
        e_icon = emp.get("icon", "👤")
        bubble_init = speeches[e_id][0]
        
        dynamic_avatars.append(f"""  <div class="chibi-avatar {walk_cls}" id="emp-{e_id}" onclick="triggerSpeak('{e_id}')">
    <div class="speech-bubble" id="bubble-{e_id}">{bubble_init}</div>
    <div class="chibi-head" style="background:{e_color}; border-color:#F8FAFC;">{e_icon}</div>
    <div class="chibi-body" style="background:{e_color};"></div>
    <div class="chibi-legs"><div class="chibi-leg"></div><div class="chibi-leg"></div></div>
    <div class="avatar-name">{e_name}</div>
  </div>""")

    dynamic_css = "\n".join(dynamic_css_lines)
    dynamic_avatars_html = "\n\n".join(dynamic_avatars)

    grumbles_json = json.dumps(dialogue_engine.grumble_templates, ensure_ascii=False)
    speeches_json = json.dumps(speeches, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="{'ja' if is_ja else 'en'}">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
  body {{ background: #0B132B; overflow: hidden; display: flex; justify-content: center; align-items: center; min-height: 540px; }}
  
  .office-game-container {{
    width: 100%;
    max-width: 920px;
    height: 530px;
    background: radial-gradient(circle at center, #1E293B 0%, #0F172A 100%);
    border: 2px solid #38BDF8;
    border-radius: 16px;
    position: relative;
    box-shadow: 0 12px 36px rgba(0,0,0,0.6), inset 0 0 25px rgba(56, 189, 248, 0.15);
  }}

  .top-hud-bar {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 42px;
    background: rgba(15, 23, 42, 0.85);
    border-bottom: 1px solid rgba(56, 189, 248, 0.3);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 18px;
    z-index: 100;
    backdrop-filter: blur(8px);
  }}

  .hud-title {{
    font-size: 12px;
    font-weight: 800;
    color: #38BDF8;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}

  .office-hud {{
    background: rgba(6, 78, 59, 0.85);
    border: 1px solid #22C55E;
    border-radius: 9999px;
    padding: 4px 12px;
    font-size: 11px;
    color: #4ADE80;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 7px;
    box-shadow: 0 2px 8px rgba(34, 197, 94, 0.25);
  }}
  .hud-live-dot {{
    width: 8px;
    height: 8px;
    background: #22C55E;
    border-radius: 50%;
    box-shadow: 0 0 8px #22C55E;
  }}

  .floor-grid {{
    position: absolute;
    top: 42px;
    left: 0;
    width: 100%;
    height: calc(100% - 42px);
    background-image: 
      linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 28px 28px;
  }}

  .room-zone {{
    position: absolute;
    border-radius: 12px;
    border: 1px dashed rgba(255,255,255,0.2);
    background: rgba(255,255,255,0.02);
  }}

  .zone-label {{
    position: absolute;
    top: 8px;
    left: 12px;
    font-size: 11px;
    font-weight: 800;
    color: #94A3B8;
    letter-spacing: 0.5px;
  }}

  .zone-ceo       {{ top: 54px; left: 20px; width: 220px; height: 175px; border-color: rgba(234, 179, 8, 0.4); }}
  .zone-admin     {{ top: 245px; left: 20px; width: 260px; height: 265px; border-color: rgba(99, 102, 241, 0.4); }}
  .zone-center    {{ top: 54px; left: 260px; width: 340px; height: 175px; border-color: rgba(56, 189, 248, 0.4); background: rgba(56, 189, 248, 0.03); }}
  .zone-editorial {{ top: 245px; left: 300px; width: 600px; height: 265px; border-color: rgba(249, 115, 22, 0.4); }}
  .zone-pr-mkt    {{ top: 54px; right: 20px; width: 260px; height: 175px; border-color: rgba(34, 197, 94, 0.4); }}

  .desk {{
    position: absolute;
    background: #1E293B;
    border-radius: 6px;
    border: 2px solid #475569;
  }}
  .pc-screen {{
    position: absolute;
    width: 22px;
    height: 14px;
    background: #38BDF8;
    border-radius: 3px;
    box-shadow: 0 0 10px #38BDF8;
    animation: pcGlow 2s infinite alternate;
  }}
  @keyframes pcGlow {{
    0% {{ opacity: 0.6; box-shadow: 0 0 4px #38BDF8; }}
    100% {{ opacity: 1; box-shadow: 0 0 14px #38BDF8; }}
  }}

  .meeting-table {{
    position: absolute;
    top: 42px;
    left: 35px;
    width: 270px;
    height: 88px;
    background: #0F172A;
    border: 3px solid #38BDF8;
    border-radius: 44px;
    box-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #38BDF8;
    font-size: 11px;
    font-weight: 700;
  }}

  .chibi-avatar {{
    position: absolute;
    width: 60px;
    height: 76px;
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
    z-index: 20;
  }}
  .chibi-avatar:hover {{
    transform: scale(1.2) translateY(-6px);
    z-index: 9999;
  }}
  .chibi-avatar.speaking {{
    z-index: 999999 !important;
  }}
  .chibi-avatar.speaking .speech-bubble {{
    z-index: 1000000 !important;
  }}

  .chibi-head {{
    width: 34px;
    height: 32px;
    border-radius: 12px;
    border: 2px solid #FFFFFF;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 17px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.5);
    position: relative;
    animation: headBob 2.5s infinite ease-in-out;
  }}
  @keyframes headBob {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-3px); }}
  }}

  .chibi-body {{
    width: 22px;
    height: 18px;
    border-radius: 4px;
    margin-top: 1px;
    position: relative;
    border: 1px solid rgba(255,255,255,0.4);
    display: flex;
    justify-content: center;
  }}
  .chibi-legs {{
    display: flex;
    gap: 4px;
    margin-top: -1px;
  }}
  .chibi-leg {{
    width: 6px;
    height: 8px;
    background: #0F172A;
    border-radius: 2px;
    border: 1px solid rgba(255,255,255,0.3);
    animation: legWalk 1.2s infinite alternate ease-in-out;
  }}
  @keyframes legWalk {{
    0% {{ transform: translateY(0); }}
    100% {{ transform: translateY(-2px); }}
  }}

  .avatar-name {{
    margin-top: 2px;
    font-size: 9.5px;
    font-weight: 800;
    color: #FFFFFF;
    background: rgba(15, 23, 42, 0.95);
    padding: 2px 6px;
    border-radius: 4px;
    white-space: nowrap;
    border: 1px solid rgba(56, 189, 248, 0.6);
    box-shadow: 0 2px 4px rgba(0,0,0,0.4);
  }}

  .speech-bubble {{
    position: absolute;
    bottom: 85px;
    left: 50%;
    transform: translateX(-50%) translateY(10px) scale(0.9);
    background: #FFFFFF;
    color: #0F172A;
    font-size: 13px;
    font-weight: 700;
    padding: 10px 16px;
    border-radius: 12px;
    box-shadow: 0 12px 36px rgba(0,0,0,0.75), 0 2px 8px rgba(0,0,0,0.3);
    pointer-events: none;
    opacity: 0;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    z-index: 9999 !important;
    border: 2px solid #38BDF8;
    min-width: 260px;
    max-width: 380px;
    width: max-content;
    white-space: normal;
    line-height: 1.6;
    letter-spacing: 0.3px;
  }}
  .speech-bubble.grumble {{
    background: #FFF1F2 !important;
    color: #881337 !important;
    border-color: #F43F5E !important;
    box-shadow: 0 12px 36px rgba(244,63,94,0.35), 0 4px 12px rgba(0,0,0,0.5) !important;
  }}
  .speech-bubble.grumble::after {{
    border-color: #FFF1F2 transparent !important;
  }}
  .speech-bubble::after {{
    content: '';
    position: absolute;
    bottom: -9px;
    left: 50%;
    transform: translateX(-50%);
    border-width: 9px 8px 0;
    border-style: solid;
    border-color: #FFFFFF transparent;
    display: block;
    width: 0;
  }}
  .speech-bubble.show {{
    opacity: 1;
    transform: translateX(-50%) translateY(0) scale(1);
  }}

  /* 画面端・上部の見切れ防止自動配置 */
  /* 1. 上段キャラクター (一条CEO・佐々木広報): 上ではなく下向きに吹き出しを展開して上部見切れを完全防止 */
  #emp-ichijo .speech-bubble {{
    bottom: auto;
    top: 85px;
    left: 20px;
    transform: translateX(0) translateY(-10px) scale(0.9);
  }}
  #emp-ichijo .speech-bubble.show {{
    transform: translateX(0) translateY(0) scale(1);
  }}
  #emp-ichijo .speech-bubble::after {{
    bottom: auto;
    top: -9px;
    left: 25px;
    transform: none;
    border-width: 0 8px 9px;
    border-color: #FFFFFF transparent;
  }}
  #emp-ichijo .speech-bubble.grumble::after {{
    border-color: #FFF1F2 transparent !important;
  }}

  #emp-sasaki .speech-bubble {{
    bottom: auto;
    top: 85px;
    left: auto;
    right: 20px;
    transform: translateX(0) translateY(-10px) scale(0.9);
  }}
  #emp-sasaki .speech-bubble.show {{
    transform: translateX(0) translateY(0) scale(1);
  }}
  #emp-sasaki .speech-bubble::after {{
    bottom: auto;
    top: -9px;
    left: auto;
    right: 25px;
    transform: none;
    border-width: 0 8px 9px;
    border-color: #FFFFFF transparent;
  }}
  #emp-sasaki .speech-bubble.grumble::after {{
    border-color: #FFF1F2 transparent !important;
  }}

  /* 2. 左端中下段キャラクター (橘法務・綾瀬人事): 横はみ出し防止 */
  #emp-tachibana .speech-bubble,
  #emp-ayase .speech-bubble {{
    left: 20px;
    transform: translateX(0) translateY(10px) scale(0.9);
  }}
  #emp-tachibana .speech-bubble.show,
  #emp-ayase .speech-bubble.show {{
    transform: translateX(0) translateY(0) scale(1);
  }}
  #emp-tachibana .speech-bubble::after,
  #emp-ayase .speech-bubble::after {{
    left: 25px;
    transform: none;
  }}

{dynamic_css}

  .walk-around {{
    animation: gentleWander 14s infinite alternate ease-in-out;
  }}
  @keyframes gentleWander {{
    0% {{ transform: translate(0, 0); }}
    25% {{ transform: translate(12px, -6px); }}
    50% {{ transform: translate(-8px, 8px); }}
    75% {{ transform: translate(6px, 6px); }}
    100% {{ transform: translate(0, 0); }}
  }}
</style>
</head>
<body>

<div class="office-game-container">
  <div class="top-hud-bar">
    <div class="hud-title">{hud_title}</div>
    <div class="office-hud">
      <div class="hud-live-dot"></div>
      <span>{hud_live}</span>
    </div>
  </div>

  <div class="floor-grid"></div>

  <!-- 1. CEO Zone -->
  <div class="room-zone zone-ceo">
    <span class="zone-label">{zone_ceo}</span>
    <div class="desk" style="top:55px; left:50px; width:80px; height:45px;"></div>
    <div class="pc-screen" style="top:67px; left:80px;"></div>
  </div>

  <!-- 2. Administration Zone -->
  <div class="room-zone zone-admin">
    <span class="zone-label">{zone_admin}</span>
    <div class="desk" style="top:45px; left:20px; width:70px; height:40px;"></div>
    <div class="pc-screen" style="top:55px; left:45px;"></div>

    <div class="desk" style="top:155px; left:20px; width:70px; height:40px;"></div>
    <div class="pc-screen" style="top:165px; left:45px;"></div>

    <div class="desk" style="top:95px; left:145px; width:75px; height:45px;"></div>
    <div class="pc-screen" style="top:107px; left:170px;"></div>
  </div>

  <!-- 3. Central Strategy Zone -->
  <div class="room-zone zone-center">
    <span class="zone-label">{zone_center_title}</span>
    <div class="meeting-table">
      <span style="font-size:12px; color:#FFFFFF;">{zone_center_table}</span>
    </div>
  </div>

  <!-- 4. Public Relations Zone -->
  <div class="room-zone zone-pr-mkt">
    <span class="zone-label">{zone_pr}</span>
    <div class="desk" style="top:55px; left:60px; width:80px; height:45px;"></div>
    <div class="pc-screen" style="top:67px; left:90px;"></div>
    <!-- Extra Expansion Desk for PR & Global Marketing -->
    <div class="desk" style="top:55px; left:160px; width:70px; height:45px; border-color:#6366F1;"></div>
    <div class="pc-screen" style="top:67px; left:185px; background:#6366F1; box-shadow:0 0 10px #6366F1;"></div>
  </div>

  <!-- 5. Editorial Zone -->
  <div class="room-zone zone-editorial">
    <span class="zone-label">{zone_editorial}</span>
    
    <div class="desk" style="top:45px; left:25px; width:80px; height:40px;"></div>
    <div class="pc-screen" style="top:55px; left:55px;"></div>

    <div class="desk" style="top:45px; left:155px; width:80px; height:40px;"></div>
    <div class="pc-screen" style="top:55px; left:185px;"></div>

    <div class="desk" style="top:45px; left:285px; width:80px; height:40px;"></div>
    <div class="pc-screen" style="top:55px; left:315px;"></div>

    <div class="desk" style="top:155px; left:155px; width:80px; height:40px; border-color:#DC2626;"></div>
    <div class="pc-screen" style="top:165px; left:185px; background:#EF4444; box-shadow:0 0 10px #EF4444;"></div>

    <!-- Expansion Desks in Editorial Zone (Writer & Research Assistance) -->
    <div class="desk" style="top:155px; left:285px; width:80px; height:40px; border-color:#F97316;"></div>
    <div class="pc-screen" style="top:165px; left:315px; background:#F97316; box-shadow:0 0 10px #F97316;"></div>
    <div class="desk" style="top:155px; left:25px; width:80px; height:40px; border-color:#10B981;"></div>
    <div class="pc-screen" style="top:165px; left:55px; background:#10B981; box-shadow:0 0 10px #10B981;"></div>
  </div>

  <!-- Dynamic Chibi Characters (Automatically spawns any recruited AI specialists) -->
{dynamic_avatars_html}

</div>

<script>
  const speeches = {speeches_json};
  const grumbleTemplates = {grumbles_json};
  const employeeIds = Object.keys(speeches);

  function generateGrumble(id) {{
    const tmpl = grumbleTemplates[id];
    if (!tmpl) return null;
    const t = tmpl.targets[Math.floor(Math.random() * tmpl.targets.length)];
    const a = tmpl.actions[Math.floor(Math.random() * tmpl.actions.length)];
    const i = tmpl.impacts[Math.floor(Math.random() * tmpl.impacts.length)];
    const e = tmpl.endings[Math.floor(Math.random() * tmpl.endings.length)];
    return "💢 " + t + a + i + e;
  }}

  function triggerSpeak(id) {{
    const avatar = document.getElementById('emp-' + id);
    const bubble = document.getElementById('bubble-' + id);
    if (!bubble || !avatar) return;
    
    // 他の吹き出しと最前面クラスを一旦リセット
    document.querySelectorAll('.chibi-avatar').forEach(el => el.classList.remove('speaking'));
    document.querySelectorAll('.speech-bubble').forEach(el => el.classList.remove('show'));

    // 50% chance of official duty report, 50% chance of 10,000 combinations authentic grumble
    const isGrumble = Math.random() < 0.5;
    let line = "";
    
    if (isGrumble) {{
      line = generateGrumble(id);
      bubble.classList.add('grumble');
    }} else {{
      const lines = speeches[id];
      if (lines && lines.length > 0) {{
        line = lines[Math.floor(Math.random() * lines.length)];
      }}
      bubble.classList.remove('grumble');
    }}

    if (!line) return;
    bubble.innerText = line;
    avatar.classList.add('speaking');
    bubble.classList.add('show');
    
    setTimeout(() => {{
      bubble.classList.remove('show');
      avatar.classList.remove('speaking');
    }}, 6500);
  }}

  // Auto dialogue rotation every 6 seconds
  setInterval(() => {{
    const randomId = employeeIds[Math.floor(Math.random() * employeeIds.length)];
    triggerSpeak(randomId);
  }}, 6000);
</script>
</body>
</html>
"""
