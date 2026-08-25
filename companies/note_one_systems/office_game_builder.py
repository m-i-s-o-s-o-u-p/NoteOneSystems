import json

def get_office_game_html(lang: str = "en") -> str:
    """Generates the interactive 2D Virtual Office HTML with full i18n support."""
    is_ja = (lang == "ja")

    # Texts and labels
    hud_title = "🏢 Note One Systems バーチャルオフィスフロア" if is_ja else "🏢 Note One Systems Virtual Office Floor"
    hud_live = "出社中: 9名（全員稼働中）" if is_ja else "Live in Office: 9/9"
    
    zone_ceo = "👑 役員執務室 (CEO)" if is_ja else "👑 Executive Suite"
    zone_admin = "🏛️ 管理部 (法務・人事・財務)" if is_ja else "🏛️ Administration"
    zone_center_title = "🗣️ ガラス張り戦略会議室" if is_ja else "🗣️ Strategy Glass Room"
    zone_center_table = "💡 全社戦略ミーティングテーブル" if is_ja else "💡 Central Strategy Table"
    zone_pr = "📢 広報課 (5大SNS運用)" if is_ja else "📢 Public Relations"
    zone_editorial = "📝 編集制作部 (調査・編集・執筆・QA)" if is_ja else "📝 Editorial Dept"

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
        "sasaki": "佐々木 翼 (広報)" if is_ja else "Sasaki (PR)"
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
                "就業規則Ver0.9に基づき円滑にオフィスを運営中。",
                "必要に応じた無料増員計画のスタンバイも万全です。"
            ],
            "shiraishi": [
                "月額固定費0円（完全無料）確認完了 💰",
                "単価500円〜1,480円での売上シミュレーション実行中 📈",
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
                "Operating under Corporate Rulebook v0.9.",
                "Zero-cost staffing expansion ready if needed."
            ],
            "shiraishi": [
                "Monthly fixed costs verified at ¥0 (Zero Cost) 💰",
                "Simulating revenue at 500 JPY unit price!",
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
            ]
        }

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
    bottom: 80px;
    background: #FFFFFF;
    color: #0F172A;
    font-size: 11px;
    font-weight: 800;
    padding: 6px 12px;
    border-radius: 8px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.7);
    white-space: nowrap;
    pointer-events: none;
    opacity: 0;
    transform: translateY(10px) scale(0.85);
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    z-index: 9999 !important;
    border: 2px solid #38BDF8;
  }}
  .speech-bubble::after {{
    content: '';
    position: absolute;
    bottom: -7px;
    left: 50%;
    transform: translateX(-50%);
    border-width: 7px 7px 0;
    border-style: solid;
    border-color: #FFFFFF transparent;
    display: block;
    width: 0;
  }}
  .speech-bubble.show {{
    opacity: 1;
    transform: translateY(0) scale(1);
  }}

  #emp-ichijo   {{ top: 100px; left: 100px; }}
  #emp-tachibana{{ top: 290px; left: 50px; }}
  #emp-ayase    {{ top: 405px; left: 50px; }}
  #emp-shiraishi{{ top: 350px; left: 180px; }}

  #emp-kazama   {{ top: 290px; left: 340px; }}
  #emp-yuki     {{ top: 290px; left: 470px; }}
  #emp-morikawa {{ top: 290px; left: 600px; }}
  #emp-kanzaki  {{ top: 405px; left: 470px; }}

  #emp-sasaki   {{ top: 100px; right: 110px; }}

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
  </div>

  <!-- 9 Chibi Characters -->
  <div class="chibi-avatar walk-around" id="emp-ichijo" onclick="triggerSpeak('ichijo')">
    <div class="speech-bubble" id="bubble-ichijo">{speeches['ichijo'][0]}</div>
    <div class="chibi-head" style="background:#1E3A8A; border-color:#93C5FD;">👩‍💼</div>
    <div class="chibi-body" style="background:#1E3A8A;"></div>
    <div class="chibi-legs"><div class="chibi-leg"></div><div class="chibi-leg"></div></div>
    <div class="avatar-name">{emp_names['ichijo']}</div>
  </div>

  <div class="chibi-avatar" id="emp-tachibana" onclick="triggerSpeak('tachibana')">
    <div class="speech-bubble" id="bubble-tachibana">{speeches['tachibana'][0]}</div>
    <div class="chibi-head" style="background:#334155; border-color:#94A3B8;">⚖️</div>
    <div class="chibi-body" style="background:#334155;"></div>
    <div class="chibi-legs"><div class="chibi-leg"></div><div class="chibi-leg"></div></div>
    <div class="avatar-name">{emp_names['tachibana']}</div>
  </div>

  <div class="chibi-avatar walk-around" id="emp-ayase" onclick="triggerSpeak('ayase')">
    <div class="speech-bubble" id="bubble-ayase">{speeches['ayase'][0]}</div>
    <div class="chibi-head" style="background:#059669; border-color:#6EE7B7;">🤝</div>
    <div class="chibi-body" style="background:#059669;"></div>
    <div class="chibi-legs"><div class="chibi-leg"></div><div class="chibi-leg"></div></div>
    <div class="avatar-name">{emp_names['ayase']}</div>
  </div>

  <div class="chibi-avatar" id="emp-shiraishi" onclick="triggerSpeak('shiraishi')">
    <div class="speech-bubble" id="bubble-shiraishi">{speeches['shiraishi'][0]}</div>
    <div class="chibi-head" style="background:#7C3AED; border-color:#C4B5FD;">📊</div>
    <div class="chibi-body" style="background:#7C3AED;"></div>
    <div class="chibi-legs"><div class="chibi-leg"></div><div class="chibi-leg"></div></div>
    <div class="avatar-name">{emp_names['shiraishi']}</div>
  </div>

  <div class="chibi-avatar" id="emp-kazama" onclick="triggerSpeak('kazama')">
    <div class="speech-bubble" id="bubble-kazama">{speeches['kazama'][0]}</div>
    <div class="chibi-head" style="background:#0D9488; border-color:#5EEAD4;">🔍</div>
    <div class="chibi-body" style="background:#0D9488;"></div>
    <div class="chibi-legs"><div class="chibi-leg"></div><div class="chibi-leg"></div></div>
    <div class="avatar-name">{emp_names['kazama']}</div>
  </div>

  <div class="chibi-avatar walk-around" id="emp-yuki" onclick="triggerSpeak('yuki')">
    <div class="speech-bubble" id="bubble-yuki">{speeches['yuki'][0]}</div>
    <div class="chibi-head" style="background:#D97706; border-color:#FCD34D;">📑</div>
    <div class="chibi-body" style="background:#D97706;"></div>
    <div class="chibi-legs"><div class="chibi-leg"></div><div class="chibi-leg"></div></div>
    <div class="avatar-name">{emp_names['yuki']}</div>
  </div>

  <div class="chibi-avatar" id="emp-morikawa" onclick="triggerSpeak('morikawa')">
    <div class="speech-bubble" id="bubble-morikawa">{speeches['morikawa'][0]}</div>
    <div class="chibi-head" style="background:#EA580C; border-color:#FDBA74;">✍️</div>
    <div class="chibi-body" style="background:#EA580C;"></div>
    <div class="chibi-legs"><div class="chibi-leg"></div><div class="chibi-leg"></div></div>
    <div class="avatar-name">{emp_names['morikawa']}</div>
  </div>

  <div class="chibi-avatar" id="emp-kanzaki" onclick="triggerSpeak('kanzaki')">
    <div class="speech-bubble" id="bubble-kanzaki">{speeches['kanzaki'][0]}</div>
    <div class="chibi-head" style="background:#DC2626; border-color:#FCA5A5;">🛡️</div>
    <div class="chibi-body" style="background:#DC2626;"></div>
    <div class="chibi-legs"><div class="chibi-leg"></div><div class="chibi-leg"></div></div>
    <div class="avatar-name">{emp_names['kanzaki']}</div>
  </div>

  <div class="chibi-avatar walk-around" id="emp-sasaki" onclick="triggerSpeak('sasaki')">
    <div class="speech-bubble" id="bubble-sasaki">{speeches['sasaki'][0]}</div>
    <div class="chibi-head" style="background:#2563EB; border-color:#93C5FD;">📢</div>
    <div class="chibi-body" style="background:#2563EB;"></div>
    <div class="chibi-legs"><div class="chibi-leg"></div><div class="chibi-leg"></div></div>
    <div class="avatar-name">{emp_names['sasaki']}</div>
  </div>

</div>

<script>
  const speeches = {speeches_json};
  const employeeIds = Object.keys(speeches);

  function triggerSpeak(id) {{
    const bubble = document.getElementById('bubble-' + id);
    const lines = speeches[id];
    if (!lines || lines.length === 0) return;
    const line = lines[Math.floor(Math.random() * lines.length)];
    bubble.innerText = line;
    bubble.classList.add('show');
    setTimeout(() => {{
      bubble.classList.remove('show');
    }}, 4000);
  }}

  // Auto dialogue rotation every 5 seconds
  setInterval(() => {{
    const randomId = employeeIds[Math.floor(Math.random() * employeeIds.length)];
    triggerSpeak(randomId);
  }}, 5000);
</script>
</body>
</html>
"""
