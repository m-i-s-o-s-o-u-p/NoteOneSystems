import streamlit as st
import streamlit.components.v1 as components
import os
import sys
import importlib
import json
import re
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
import companies.note_one_systems.office_game_builder

importlib.reload(core.ai_client)
importlib.reload(core.holdings_manager)
importlib.reload(core.ringi_manager)
importlib.reload(core.hr_manager)
importlib.reload(core.i18n)
importlib.reload(companies.note_one_systems.workflow)
importlib.reload(companies.note_one_systems.office_chat_manager)
importlib.reload(companies.note_one_systems.market_research_manager)
importlib.reload(companies.note_one_systems.office_game_builder)

from core.ai_client import AIClient
from core.holdings_manager import HoldingsManager
from core.ringi_manager import RingiManager
from core.hr_manager import HRManager
from companies.note_one_systems.workflow import NoteOneWorkflow
from companies.note_one_systems.office_chat_manager import OfficeChatManager
from companies.note_one_systems.market_research_manager import MarketResearchManager
from companies.note_one_systems.office_game_builder import get_office_game_html
from core.i18n import t

# Helper to completely strip double asterisks and stray HTML tags from text
def clean_txt(val: str) -> str:
    if not val or not isinstance(val, str):
        return ""
    cleaned = val.replace("**", "")
    cleaned = re.sub(r'<[^>]+>', '', cleaned)
    return cleaned.strip()

# Helper to build 100% Clean Article Dossier HTML rendered via st.html (Zero Markdown parser interference)
def get_article_dossier_html(art: dict, lang: str = "ja") -> str:
    clean_content = clean_txt(art.get("content", ""))
    char_count = len(clean_content)
    read_time_min = max(1, round(char_count / 450))
    origin_topic_str = f"企画テーマ: 『{clean_txt(art.get('topic', ''))}』 (市場調査課 風間 涼 分析・承認済)" if art.get('topic') else "実務効率化・Notionテンプレート実践"
    delimiter = "🔒 ここから先は有料エリアです" if "🔒 ここから先は有料エリアです" in clean_content else ("🔒 [Paywall] Premium Section Starts Here" if "🔒 [Paywall] Premium Section Starts Here" in clean_content else None)

    if delimiter:
        parts = clean_content.split(delimiter)
        free_part = parts[0].strip()
        paid_part = parts[1].strip() if len(parts) > 1 else ""
        body_html = f"""
        <div style="color: #0F172A; font-size: 1rem; line-height: 1.85; white-space: pre-wrap; margin-bottom: 20px;">{free_part}</div>
        <div style="background-color: #FFFFFF; border: 2px dashed #0284C7; border-radius: 8px; padding: 14px; margin: 24px 0; color: #0369A1; font-weight: 800; text-align: center; font-size: 1rem;">
            🔒 {t('qa_paywall_badge', lang)}
        </div>
        <div style="color: #0F172A; font-size: 1rem; line-height: 1.85; white-space: pre-wrap; margin-top: 20px;">{paid_part}</div>
        """
    else:
        body_html = f"""
        <div style="color: #0F172A; font-size: 1rem; line-height: 1.85; white-space: pre-wrap;">{clean_content}</div>
        """

    sns_raw = clean_txt(art.get("marketing", ""))
    sns_blocks = []
    
    # Platform badge color styling map
    badge_styles = {
        "X": ("#0F1419", "#FFFFFF", "🐦"),
        "Instagram": ("#E1306C", "#FFFFFF", "📸"),
        "Threads": ("#000000", "#FFFFFF", "🧵"),
        "Bluesky": ("#0284C7", "#FFFFFF", "🦋"),
        "Mastodon": ("#6364FF", "#FFFFFF", "🐘")
    }

    for sec in sns_raw.split("【"):
        if not sec.strip():
            continue
        sec_str = "【" + sec.strip()
        lines = sec_str.split("\n", 1)
        s_title = lines[0].strip()
        s_body = lines[1].strip() if len(lines) > 1 else ""
        
        # Determine badge color
        bg_col, txt_col, icon = ("#1E293B", "#FFFFFF", "📢")
        for k, v in badge_styles.items():
            if k.lower() in s_title.lower():
                bg_col, txt_col, icon = v
                break

        sns_blocks.append(f"""
        <div style="background: #FFFFFF; border: 1.5px solid #CBD5E1; border-radius: 8px; padding: 18px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);">
            <div style="display: flex; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #E2E8F0; padding-bottom: 8px;">
                <span class="sns-platform-badge" style="background: {bg_col}; color: #FFFFFF !important; font-weight: 800; font-size: 0.85rem; padding: 4px 12px; border-radius: 6px; letter-spacing: 0.2px;">{icon} {s_title}</span>
            </div>
            <div style="color: #0F172A !important; font-size: 0.96rem; line-height: 1.8; white-space: pre-wrap; font-weight: 500;">{s_body}</div>
        </div>
        """)
    sns_html = "".join(sns_blocks)

    legal_txt = clean_txt(art.get('legal_check', '審査中'))
    qa_txt = clean_txt(art.get('qa_score', '採点中'))

    return f"""
    <div class="review-paper-white" style="border-left: 6px solid #0284C7; background-color:#FFFFFF; padding:28px; border-radius:12px; border:2px solid #CBD5E1; box-shadow:0 6px 24px rgba(0,0,0,0.15); margin: 18px 0;">
        <div style="background: #F1F5F9; border-radius: 10px; padding: 18px 20px; border: 1px solid #CBD5E1; margin-bottom: 24px;">
            <div style="background: #E0F2FE; border: 1.5px solid #38BDF8; border-radius: 8px; padding: 10px 16px; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="background: #0284C7; color: #FFFFFF !important; font-weight: 800; font-size: 0.95rem; padding: 3px 12px; border-radius: 6px; letter-spacing: 0.05em;">{art.get('article_no', 'No.01')}</span>
                    <strong style="color: #0369A1 !important; font-size: 1.02rem;">🔖 記事管理番号: {art.get('article_code', 'ART-001')} （通算第{art.get('article_number', 1)}号）</strong>
                </div>
                <span style="background: #BAE6FD; color: #0369A1; font-size: 0.78rem; font-weight: 800; padding: 2px 8px; border-radius: 4px;">公式ナンバリング付与済</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; border-bottom: 1px solid #CBD5E1; padding-bottom: 8px;">
                <span style="font-weight: 800; font-size: 1.05rem; color: #0F172A !important;">📋 査読前提・品質監査情報 (Executive Review Header)</span>
                <span style="background: #0284C7; color: #FFFFFF !important; font-size: 0.78rem; font-weight: 800; padding: 3px 10px; border-radius: 4px;">Ready for Sign-off</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; font-size: 0.92rem;">
                <div style="background:#FFFFFF; padding:10px 14px; border-radius:6px; border:1px solid #CBD5E1;">
                    <strong style="color: #0369A1 !important;">🏢 担当部門・課:</strong>
                    <div style="color: #1E293B !important; margin-top:2px;">編集部 記事制作課（執筆: 森川 拓真 / 編集: 結城 紬）<br>マーケティング部 広報課（佐々木 翼）</div>
                </div>
                <div style="background:#FFFFFF; padding:10px 14px; border-radius:6px; border:1px solid #CBD5E1;">
                    <strong style="color: #047857 !important;">📝 文字数・読了目安:</strong>
                    <div style="color: #1E293B !important; margin-top:2px;"><strong style="color:#0F172A !important;">{char_count:,} 文字</strong>（読了目安: 約 {read_time_min} 分 / 推奨価格: ¥{art.get('price', 300):,}）</div>
                </div>
                <div style="background:#FFFFFF; padding:10px 14px; border-radius:6px; border:1px solid #CBD5E1;">
                    <strong style="color: #D97706 !important;">💡 発生元企画提案:</strong>
                    <div style="color: #1E293B !important; margin-top:2px;">{origin_topic_str}</div>
                </div>
                <div style="background:#FFFFFF; padding:10px 14px; border-radius:6px; border:1px solid #CBD5E1;">
                    <strong style="color: #7C3AED !important;">🔍 品質管理・検証ソース:</strong>
                    <div style="color: #1E293B !important; margin-top:2px;">note利用規約(2026最新版), 景品表示法(不当表示防止基準), 会社法第7条(商号), 社内QA規程Ver.2.1</div>
                </div>
            </div>
        </div>

        <h3 style="color: #0F172A !important; margin: 24px 0 12px 0; border-bottom: 2px solid #E2E8F0; padding-bottom: 8px; font-size:1.25rem; font-weight:800;">📋 note完成原稿プレビュー</h3>
        {body_html}

        <div style="height: 1px; background: #CBD5E1; margin: 28px 0;"></div>

        <h3 style="color: #0F172A !important; margin: 24px 0 12px 0; border-bottom: 2px solid #E2E8F0; padding-bottom: 8px; font-size:1.25rem; font-weight:800;">📢 5大SNS告知文（佐々木 翼 作成）</h3>
        <div style="background: #F8FAFC; padding: 20px; border-radius: 10px; border: 1px solid #CBD5E1; margin: 16px 0;">
            {sns_html}
        </div>

        <div style="height: 1px; background: #CBD5E1; margin: 26px 0;"></div>

        <h3 style="color: #0369A1; margin: 24px 0 12px 0; border-bottom: 2px solid #E2E8F0; padding-bottom: 8px; font-size:1.25rem; font-weight:800;">⚖️ 法的適合性 ＆ 🛡️ 品質管理スコア（橘 律 ＆ 神崎 玲奈）</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 14px;">
            <div style="background: #F8FAFC; padding: 16px; border-radius: 8px; border: 1px solid #CBD5E1;">
                <strong style="color: #0369A1; font-size: 0.95rem;">⚖️ 法務課 スクリーニング審査 (橘 律)</strong>
                <div style="white-space: pre-wrap; font-size: 0.92rem; color: #1E293B; margin-top: 8px; line-height: 1.65;">{legal_txt}</div>
            </div>
            <div style="background: #F8FAFC; padding: 16px; border-radius: 8px; border: 1px solid #CBD5E1;">
                <strong style="color: #B45309; font-size: 0.95rem;">🛡️ 品質管理課 100点採点スコア (神崎 玲奈)</strong>
                <div style="white-space: pre-wrap; font-size: 0.92rem; color: #1E293B; margin-top: 8px; line-height: 1.65;">{qa_txt}</div>
            </div>
        </div>

        <div style="height: 1px; background: #CBD5E1; margin: 26px 0;"></div>

        <h3 style="color: #7C3AED; margin: 24px 0 12px 0; border-bottom: 2px solid #E2E8F0; padding-bottom: 8px; font-size:1.25rem; font-weight:800;">📊 財務・価格決定根拠 ＆ 収益性試算（財務課: 白石 葵 査定）</h3>
        <div style="background: #FAF5FF; padding: 20px; border-radius: 10px; border: 1.5px solid #DDD6FE; margin: 16px 0;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; border-bottom: 1px solid #E9D5FF; padding-bottom: 10px;">
                <span style="font-weight: 800; font-size: 1.05rem; color: #5B21B6;">💰 設定販売価格: ¥{art.get('price', 300):,}（基本インパルス・バイ価格）</span>
                <span style="background: #7C3AED; color: #FFFFFF !important; font-size: 0.78rem; font-weight: 800; padding: 3px 10px; border-radius: 4px;">財務アナリスト査定済</span>
            </div>
            <div style="color: #1E293B !important; font-size: 0.94rem; line-height: 1.8; white-space: pre-wrap;">{clean_txt(art.get('pricing_rationale', '【基本300円の戦略的根拠】カフェのコーヒー1杯未満の衝動買い（インパルス・バイ）ゾーンに設定することで購入時の躊躇を極小化し、成約率（CVR 3.8%〜5.2%）とSNS口コミ拡散を最大化します。'))}</div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 16px;">
                <div style="background: #FFFFFF; padding: 12px; border-radius: 6px; border: 1px solid #DDD6FE; text-align: center;">
                    <div style="font-size: 0.8rem; color: #6D28D9; font-weight: 700;">想定成約率 (CVR)</div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin-top: 4px;">3.8% 〜 5.2%</div>
                </div>
                <div style="background: #FFFFFF; padding: 12px; border-radius: 6px; border: 1px solid #DDD6FE; text-align: center;">
                    <div style="font-size: 0.8rem; color: #6D28D9; font-weight: 700;">1部あたり手残り純益 (約85%)</div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #059669; margin-top: 4px;">¥{int(art.get('price', 300) * 0.85):,}</div>
                </div>
                <div style="background: #FFFFFF; padding: 12px; border-radius: 6px; border: 1px solid #DDD6FE; text-align: center;">
                    <div style="font-size: 0.8rem; color: #6D28D9; font-weight: 700;">月商目標貢献額 (月150部)</div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #0284C7; margin-top: 4px;">¥{int(art.get('price', 300) * 0.85 * 150):,}</div>
                </div>
            </div>
        </div>
    </div>
    """

# Helper to build 100% Clean Topic Dossier HTML rendered via st.html
def get_topic_dossier_html(tp: dict, lang: str = "ja") -> str:
    title = clean_txt(tp.get('title', ''))
    category = clean_txt(tp.get('category', '実務ノウハウ'))
    audience = clean_txt(tp.get('target_audience', '業務効率化を目指すビジネスパーソン'))
    price = tp.get('recommended_price', 300)
    demand = clean_txt(tp.get('demand_summary', 'note市場において当該領域の検索需要・購買ニーズが急増中。'))
    diff_gap = clean_txt(tp.get('competitor_gap', '現場ですぐ使える完成版テンプレートと具体的手順を提示して差別化。'))

    # Professional analytical breakdown
    persona_pain = f"ターゲット読者である『{audience}』は、日々の実務や作業に追われ「情報収集に時間をかけられない」「調べても抽象論や精神論ばかりで現場ですぐ動くコードや雛形がない」という強いペイン（痛点）を抱えています。"
    purchase_trigger = f"無料のWeb記事では得られない「そのままコピペして10分で成果が出る実務テンプレート」や「角を立てずにトラブルを防ぐ実践マニュアル」が同梱されていることで、価格（¥{price:,}）以上の即時ROI（費用対効果）を感じて購入に至ります。"
    competitor_analysis = f"noteプラットフォーム内の既存競合記事（約250〜320件）を精査したところ、7割以上が「概要の説明」にとどまり、読者が自力で落とし込むステップで挫折しています。当社は『{diff_gap}』に焦点を絞り、完全なブルーオーシャンとして高成約率を狙います。"
    
    # 5-Chapter Outline Proposal for Content Creation Division
    outline_ch1 = f"第1章: 【現状の罠】なぜ『{audience}』の多くが同じ失敗を繰り返すのか？"
    outline_ch2 = f"第2章: 【最短攻略の思考法】{category}で成果を最大化する3大コア原則"
    outline_ch3 = f"第3章: 【実践テンプレート】コピペで即日使える完成版実務シート＆導入手順"
    outline_ch4 = f"第4章: 【トラブル予防】現場でありがちなミスと即時リカバリーQ&A"
    outline_ch5 = f"第5章: 【購入者限定特典】自己診断チェックリスト ＆ アクションプラン"

    sample_articles = 280
    search_queries = 45000
    target_words = "4,000〜6,500 文字（実務テンプレ同梱）"
    est_cvr = "3.8% 〜 5.2%（基本300円・衝動買い最適化）"
    target_sales_1st_month = f"{int(30000 / price)} 〜 {int(90000 / price)} 部（月商予測: 約 3.0万〜9.0万円）"

    return f"""
    <div class="review-paper-white" style="border-left: 6px solid #0284C7; background-color:#FFFFFF; padding:26px; border-radius:12px; border:2px solid #CBD5E1; box-shadow:0 6px 22px rgba(0,0,0,0.18); margin: 18px 0;">
        <!-- 1. Metadata Header Dossier -->
        <div style="background: #F1F5F9; border-radius: 10px; padding: 18px 20px; border: 1px solid #CBD5E1; margin-bottom: 22px;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; border-bottom: 1px solid #CBD5E1; padding-bottom: 8px;">
                <span style="font-weight: 800; font-size: 1.05rem; color: #0F172A;">📋 企画査読前提・市場調査データ諸元 (Research Metadata Dossier)</span>
                <span style="background: #0284C7; color: #FFFFFF; font-size: 0.78rem; font-weight: 800; padding: 3px 10px; border-radius: 4px;">調査分析完了・承認待ち</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; font-size: 0.92rem;">
                <div style="background:#FFFFFF; padding:10px 14px; border-radius:6px; border:1px solid #CBD5E1;">
                    <strong style="color: #0369A1;">🏢 担当アナリスト:</strong>
                    <div style="color: #1E293B; margin-top:2px;">市場調査課 風間 涼（Ryo Kazama）</div>
                </div>
                <div style="background:#FFFFFF; padding:10px 14px; border-radius:6px; border:1px solid #CBD5E1;">
                    <strong style="color: #047857;">📊 調査分析母数 (データサンプル):</strong>
                    <div style="color: #1E293B; margin-top:2px;">note競合 {sample_articles}記事 ／ 関連検索母数 {search_queries:,}クエリ</div>
                </div>
                <div style="background:#FFFFFF; padding:10px 14px; border-radius:6px; border:1px solid #CBD5E1;">
                    <strong style="color: #D97706;">🎯 カテゴリ ／ 想定読者:</strong>
                    <div style="color: #1E293B; margin-top:2px;">{category} ／ {audience}</div>
                </div>
                <div style="background:#FFFFFF; padding:10px 14px; border-radius:6px; border:1px solid #CBD5E1;">
                    <strong style="color: #7C3AED;">✍️ 記事制作課への目標仕上がり:</strong>
                    <div style="color: #1E293B; margin-top:2px;">{target_words}（推奨価格: ¥{price:,}）</div>
                </div>
            </div>
        </div>

        <!-- 2. Detailed Market Research Report -->
        <h3 style="color: #0369A1; margin: 24px 0 14px 0; border-bottom: 2px solid #E2E8F0; padding-bottom: 8px; font-size:1.25rem; font-weight:800;">
            📊 {'市場調査・企画提案書（風間 涼 提出レポート）' if lang=='ja' else 'Comprehensive Market Research Proposal (Ryo Kazama)'}
        </h3>

        <!-- Section 1 & 2: Grid -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 14px;">
            <div style="background:#F8FAFC; padding:18px; border-radius:8px; border:1px solid #CBD5E1;">
                <strong style="color:#0369A1; font-size:1.0rem; display:block; margin-bottom:8px; border-bottom:1px solid #E2E8F0; padding-bottom:4px;">
                    🎯 読者ペルソナの深層心理 ＆ 購買トリガー
                </strong>
                <p style="margin:8px 0; color:#1E293B; font-size:0.92rem; line-height:1.6;">
                    <strong>【ペイン（痛点）】:</strong> {persona_pain}
                </p>
                <p style="margin:8px 0; color:#1E293B; font-size:0.92rem; line-height:1.6;">
                    <strong>【購買動機】:</strong> {purchase_trigger}
                </p>
                <div style="margin-top:10px; background:#EFF6FF; padding:8px 12px; border-radius:6px; border-left:3px solid #3B82F6; font-size:0.86rem; color:#1E40AF;">
                    💡 読者の「今すぐ時間を節約したい」欲求を満たす実用テンプレで高CVR（成約率）を担保。
                </div>
            </div>

            <div style="background:#F8FAFC; padding:18px; border-radius:8px; border:1px solid #CBD5E1;">
                <strong style="color:#047857; font-size:1.0rem; display:block; margin-bottom:8px; border-bottom:1px solid #E2E8F0; padding-bottom:4px;">
                    🔥 市場ニーズ ＆ 競合ブルーオーシャン戦略
                </strong>
                <p style="margin:8px 0; color:#1E293B; font-size:0.92rem; line-height:1.6;">
                    <strong>【市場需要】:</strong> {demand}
                </p>
                <p style="margin:8px 0; color:#1E293B; font-size:0.92rem; line-height:1.6;">
                    <strong>【競合差別化】:</strong> {competitor_analysis}
                </p>
                <div style="margin-top:10px; background:#ECFDF5; padding:8px 12px; border-radius:6px; border-left:3px solid #10B981; font-size:0.86rem; color:#065F46;">
                    ⚡ 抽象論を徹底排除し、即日業務に導入できる完成度で他社記事を圧倒。
                </div>
            </div>
        </div>

        <!-- Section 3: Proposed Table of Contents (Outline) -->
        <div style="background:#F8FAFC; padding:18px; border-radius:8px; border:1px solid #CBD5E1; margin-top:16px;">
            <strong style="color:#6366F1; font-size:1.0rem; display:block; margin-bottom:8px; border-bottom:1px solid #E2E8F0; padding-bottom:4px;">
                📑 記事制作課（結城・森川）への推奨目次構成案（4,000〜6,500字規模）
            </strong>
            <div style="display:grid; grid-template-columns: 1fr; gap:6px; font-size:0.9rem; color:#1E293B; margin-top:8px;">
                <div style="background:#FFFFFF; padding:8px 12px; border-radius:6px; border:1px solid #E2E8F0;">📌 <strong>{outline_ch1}</strong></div>
                <div style="background:#FFFFFF; padding:8px 12px; border-radius:6px; border:1px solid #E2E8F0;">📌 <strong>{outline_ch2}</strong></div>
                <div style="background:#FFFFFF; padding:8px 12px; border-radius:6px; border:1px solid #E2E8F0; border-left:4px solid #10B981;">⭐ <strong>{outline_ch3}</strong>（※ここから有料エリア設定）</div>
                <div style="background:#FFFFFF; padding:8px 12px; border-radius:6px; border:1px solid #E2E8F0;">📌 <strong>{outline_ch4}</strong></div>
                <div style="background:#FFFFFF; padding:8px 12px; border-radius:6px; border:1px solid #E2E8F0;">📌 <strong>{outline_ch5}</strong></div>
            </div>
        </div>

        <!-- Section 4: Commercial Projection -->
        <div style="background:#F0FDF4; padding:16px 20px; border-radius:8px; border:1px solid #86EFAC; margin-top:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:8px;">
                <div>
                    <strong style="color:#166534; font-size:0.98rem;">💰 販売収益予測シミュレーション:</strong>
                    <div style="color:#15803D; font-size:0.88rem; margin-top:3px;">
                        推奨基本価格: <strong>¥{price:,}</strong>（衝動買い推奨） ／ 想定成約率: <strong>{est_cvr}</strong> ／ 初月予測販売数: <strong>{target_sales_1st_month}</strong>
                    </div>
                </div>
                <span style="background:#15803D; color:#FFFFFF; font-weight:800; font-size:0.82rem; padding:4px 12px; border-radius:20px;">
                    基本300円・高成約モデル
                </span>
            </div>
            <div style="background:#DCFCE7; padding:8px 12px; border-radius:6px; font-size:0.84rem; color:#14532D; line-height:1.5;">
                💡 <strong>【基本300円の価格設定根拠】</strong>: カフェのコーヒー1杯未満の「インパルス・バイ（衝動買い）価格」に設定することで購入障壁を最小化し、初期読者レビューの獲得とSNS拡散を最速で起こす戦略的価格です。
            </div>
        </div>
    </div>
    """

# Page Configuration
st.set_page_config(
    page_title="Note One Systems, Inc. | AI Enterprise Platform",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session State Initialization
if "language" not in st.session_state:
    st.session_state.language = "ja"
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
if "scroll_trigger" not in st.session_state:
    st.session_state.scroll_trigger = 0
if "office_chat_history" not in st.session_state:
    st.session_state.office_chat_history = []
if "prefill_topic" not in st.session_state:
    st.session_state.prefill_topic = ""
if "prefill_audience" not in st.session_state:
    st.session_state.prefill_audience = ""
if "auto_start_creation" not in st.session_state:
    st.session_state.auto_start_creation = False

if "show_univ_rev_form" not in st.session_state:
    st.session_state.show_univ_rev_form = False
if "show_mr_tp_rev" not in st.session_state:
    st.session_state.show_mr_tp_rev = False
if "show_qa_art_rev" not in st.session_state:
    st.session_state.show_qa_art_rev = False
if "auto_transferred_to_qa" not in st.session_state:
    st.session_state.auto_transferred_to_qa = False
if "qa_selected_art_id" not in st.session_state:
    st.session_state.qa_selected_art_id = None
if "just_sent_to_qa_title" not in st.session_state:
    st.session_state.just_sent_to_qa_title = ""

def navigate_to(target_id: str):
    st.session_state.active_page_id = target_id
    st.session_state.scroll_trigger += 1
    st.rerun()

lang = st.session_state.language
ai_client = AIClient(api_key=st.session_state.api_key)
workflow = NoteOneWorkflow(ai_client)
chat_manager = OfficeChatManager(ai_client)
market_manager = MarketResearchManager(ai_client)

# High-contrast UI Styling: Scoped Dark Theme & Pure White Review Dossier
st.markdown("""
<style>
    /* ============================================================== */
    /* 🏢 1. GLOBAL BASE STYLES & TYPOGRAPHY                         */
    /* ============================================================== */
    .stApp {
        background-color: #0B132B !important;
        color: #F8FAFC !important;
    }
    
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
    
    /* ============================================================== */
    /* 📄 2. PAPER-WHITE REVIEW DOSSIER (100% High-Contrast Black)   */
    /* ============================================================== */
    .review-paper-white,
    .review-paper-white * {
        color: #0F172A !important;
    }
    .review-paper-white {
        background-color: #FFFFFF !important;
        border: 2px solid #CBD5E1 !important;
        border-left: 6px solid #0284C7 !important;
        border-radius: 12px;
        padding: 28px;
        margin: 18px 0;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15);
        line-height: 1.85;
    }
    .review-paper-white h1, 
    .review-paper-white h2, 
    .review-paper-white h3, 
    .review-paper-white h4, 
    .review-paper-white h5, 
    .review-paper-white h6 {
        color: #0F172A !important;
        font-weight: 800 !important;
    }
    .review-paper-white p, 
    .review-paper-white li, 
    .review-paper-white label,
    .review-paper-white div {
        color: #1E293B !important;
    }
    .review-paper-white strong {
        color: #0F172A !important;
        font-weight: 800 !important;
    }
    
    /* Dedicated override for branded SNS badges to keep white text */
    .sns-platform-badge,
    .review-paper-white .sns-platform-badge {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    /* ============================================================== */
    /* 👑 3. APPROVAL BOXES & STATUS CARDS                           */
    /* ============================================================== */
    .approval-box-locked {
        background: linear-gradient(135deg, #2A1711 0%, #1E1B4B 100%) !important;
        border: 2px solid #F59E0B !important;
        border-radius: 12px;
        padding: 22px;
        margin: 20px 0;
        box-shadow: 0 6px 18px rgba(245, 158, 11, 0.25);
    }
    .approval-box-locked h3 {
        color: #FCD34D !important;
    }
    .approval-box-locked div {
        color: #FFFFFF !important;
    }
    
    .approval-box-approved {
        background: linear-gradient(135deg, #064E3B 0%, #0F172A 100%) !important;
        border: 2px solid #10B981 !important;
        border-radius: 12px;
        padding: 22px;
        margin: 20px 0;
        box-shadow: 0 6px 18px rgba(16, 185, 129, 0.25);
    }
    .approval-box-approved h3 {
        color: #6EE7B7 !important;
    }
    .approval-box-approved div {
        color: #FFFFFF !important;
    }
    
    .desk-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #38BDF8 !important;
        margin-bottom: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .desk-card div, .desk-card span {
        color: #F8FAFC !important;
    }
    
    .status-live {
        display: inline-flex;
        align-items: center;
        background-color: #064E3B;
        color: #4ADE80 !important;
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
    
    /* ============================================================== */
    /* 📋 3.5. INTEGRATED RADIO RECORD TABLE                          */
    /* ============================================================== */
    div.st-key-univ_record_radio_table div[role="radiogroup"] {
        gap: 6px !important;
    }
    div.st-key-univ_record_radio_table div[role="radiogroup"] > label {
        background: rgba(15, 23, 42, 0.75) !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 9px 14px !important;
        margin-bottom: 2px !important;
        transition: all 0.2s ease !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
    }
    div.st-key-univ_record_radio_table div[role="radiogroup"] > label:hover {
        background: rgba(30, 41, 59, 0.95) !important;
        border-color: #38BDF8 !important;
        cursor: pointer !important;
    }
    div.st-key-univ_record_radio_table div[role="radiogroup"] > label:has(input:checked) {
        background: rgba(14, 165, 233, 0.12) !important;
        border: 1.5px solid #38BDF8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.25) !important;
    }
    div.st-key-univ_record_radio_table div[role="radiogroup"] > label p {
        font-size: 0.92rem !important;
        color: #F8FAFC !important;
        font-weight: 600 !important;
        margin-bottom: 0 !important;
    }
    div.st-key-univ_record_radio_table div[role="radiogroup"] > label div[data-testid="stCaptionContainer"] p {
        font-size: 0.8rem !important;
        color: #94A3B8 !important;
        margin-top: 2px !important;
    }
    
    /* ============================================================== */
    /* 🧭 4. SIDEBAR NAVIGATION LINKS                                 */
    /* ============================================================== */
    div[data-testid="stSidebar"] button {
        text-align: left !important;
        justify-content: flex-start !important;
        border-radius: 8px !important;
        font-size: 0.92rem !important;
        padding: 7px 14px !important;
        margin-bottom: 3px !important;
        border: 1px solid transparent !important;
        background-color: transparent !important;
        color: #E2E8F0 !important;
    }
    div[data-testid="stSidebar"] button:hover {
        background-color: #1E293B !important;
        color: #FFFFFF !important;
    }

    div[data-testid="stSidebar"] button[kind="primary"],
    div[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] {
        background-color: #38BDF8 !important;
        color: #0B132B !important;
        border: 1px solid #7DD3FC !important;
        font-weight: 800 !important;
        box-shadow: 0 2px 10px rgba(56, 189, 248, 0.45) !important;
    }
    
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 3rem !important;
    }
</style>
""", unsafe_allow_html=True)

# 100% Guaranteed Scroll-to-Top Handler targeting the exact [data-testid="stMain"] container
components.html(f"""
<div id="scroll-anchor-{st.session_state.scroll_trigger}"></div>
<script>
(function() {{
    function scrollToTopNow() {{
        try {{
            const pDoc = window.parent.document;
            const mainContainer = pDoc.querySelector('[data-testid="stMain"]') ||
                                  pDoc.querySelector('.stMain') ||
                                  pDoc.querySelector('[data-testid="stAppViewContainer"]') ||
                                  pDoc.querySelector('section.main');
            if (mainContainer) {{
                mainContainer.scrollTop = 0;
                try {{ mainContainer.scrollTo({{ top: 0, left: 0, behavior: 'instant' }}); }} catch(e) {{ mainContainer.scrollTop = 0; }}
            }}
            pDoc.documentElement.scrollTop = 0;
            pDoc.body.scrollTop = 0;
            window.parent.scrollTo(0, 0);
        }} catch(e) {{}}
    }}

    // 1. Install permanent click listener on parent document for all sidebar buttons
    try {{
        const pWin = window.parent;
        const pDoc = pWin.document;
        if (!pWin._st_sidebar_scroll_installed) {{
            pWin._st_sidebar_scroll_installed = true;
            pDoc.addEventListener('click', function(e) {{
                const sidebar = pDoc.querySelector('[data-testid="stSidebar"]') ||
                                pDoc.querySelector('section[data-testid="stSidebar"]');
                if (sidebar && sidebar.contains(e.target)) {{
                    scrollToTopNow();
                    setTimeout(scrollToTopNow, 20);
                    setTimeout(scrollToTopNow, 60);
                    setTimeout(scrollToTopNow, 120);
                    setTimeout(scrollToTopNow, 250);
                    setTimeout(scrollToTopNow, 500);
                }}
            }}, true);
        }}
    }} catch(e) {{}}

    // 2. Trigger on this frame mount
    scrollToTopNow();
    setTimeout(scrollToTopNow, 30);
    setTimeout(scrollToTopNow, 100);
    setTimeout(scrollToTopNow, 250);
}})();
</script>
""", height=0)

# ==========================================
# Sidebar: Multilingual Navigation Menu
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#FFFFFF !important;'>🏢 Note One Systems, Inc.</h2>", unsafe_allow_html=True)
    st.caption(t("sidebar_subtitle", lang))
    st.markdown("---")

    # 1. 🏢 Company Dashboard (Top Level)
    if st.button(t("nav_dashboard", lang), use_container_width=True, key="nav_btn_dashboard", type="primary" if st.session_state.active_page_id == "dashboard" else "secondary"):
        navigate_to("dashboard")

    # 2. 🏢 Office Room
    if st.button(t("nav_office", lang), use_container_width=True, key="nav_btn_office", type="primary" if st.session_state.active_page_id == "office" else "secondary"):
        navigate_to("office")

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 3. 📝 Editorial Department
    st.markdown(f"<div style='font-size:0.95rem; font-weight:800; color:#38BDF8; padding: 4px 6px;'>{t('dept_editorial', lang)}</div>", unsafe_allow_html=True)
    if st.button(f"　 {t('nav_market_research', lang)}", use_container_width=True, key="nav_btn_mr", type="primary" if st.session_state.active_page_id == "market_research" else "secondary"):
        navigate_to("market_research")
    if st.button(f"　 {t('nav_content_creation', lang)}", use_container_width=True, key="nav_btn_cc", type="primary" if st.session_state.active_page_id == "content_creation" else "secondary"):
        navigate_to("content_creation")
    if st.button(f"　 {t('nav_pr', lang)}", use_container_width=True, key="nav_btn_pr", type="primary" if st.session_state.active_page_id == "pr" else "secondary"):
        navigate_to("pr")
    if st.button(f"　 {t('nav_qa', lang)}", use_container_width=True, key="nav_btn_qa", type="primary" if st.session_state.active_page_id == "qa" else "secondary"):
        navigate_to("qa")

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 4. 🏛️ Administration Department
    st.markdown(f"<div style='font-size:0.95rem; font-weight:800; color:#A78BFA; padding: 4px 6px;'>{t('dept_admin', lang)}</div>", unsafe_allow_html=True)
    if st.button(f"　 {t('nav_hr', lang)}", use_container_width=True, key="nav_btn_hr", type="primary" if st.session_state.active_page_id == "hr" else "secondary"):
        navigate_to("hr")
    if st.button(f"　 {t('nav_legal', lang)}", use_container_width=True, key="nav_btn_legal", type="primary" if st.session_state.active_page_id == "legal" else "secondary"):
        navigate_to("legal")
    if st.button(f"　 {t('nav_finance', lang)}", use_container_width=True, key="nav_btn_finance", type="primary" if st.session_state.active_page_id == "finance" else "secondary"):
        navigate_to("finance")
    if st.button(f"　 {t('nav_accounting', lang)}", use_container_width=True, key="nav_btn_accounting", type="primary" if st.session_state.active_page_id == "accounting" else "secondary"):
        navigate_to("accounting")

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 5. Independent Utilities
    if st.button(t("nav_helpdesk", lang), use_container_width=True, key="nav_btn_helpdesk", type="primary" if st.session_state.active_page_id == "helpdesk" else "secondary"):
        navigate_to("helpdesk")
    if st.button(t("nav_profiles", lang), use_container_width=True, key="nav_btn_profiles", type="primary" if st.session_state.active_page_id == "profiles" else "secondary"):
        navigate_to("profiles")
    if st.button(t("nav_cloud_guide", lang), use_container_width=True, key="nav_btn_cloud", type="primary" if st.session_state.active_page_id == "cloud_guide" else "secondary"):
        navigate_to("cloud_guide")

    # ==========================================
    # 🌐 言語切り替えリンクセクション
    # ==========================================
    st.markdown("---")
    st.markdown(f"<div style='font-size:0.85rem; font-weight:800; color:#38BDF8; margin-bottom:6px;'>{t('lang_section_title', lang)}</div>", unsafe_allow_html=True)
    col_lang1, col_lang2 = st.columns(2)
    with col_lang1:
        if st.button("🇺🇸 English", use_container_width=True, type="primary" if lang == "en" else "secondary"):
            st.session_state.language = "en"
            st.session_state.scroll_trigger += 1
            st.rerun()
    with col_lang2:
        if st.button("🇯🇵 日本語", use_container_width=True, type="primary" if lang == "ja" else "secondary"):
            st.session_state.language = "ja"
            st.session_state.scroll_trigger += 1
            st.rerun()

    # ==========================================
    # ⚙️ AI Intelligence Engine (Gemini)
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
    
    pending_articles = [a for a in articles if a.get("status") in ["Pending Owner Approval", "Revision Requested"]]
    pending_topics = [tp for tp in topics if tp.get("status") in ["Pending Owner Approval", "Revision Requested"]]

    if pending_topics or pending_articles:
        warn_msg = []
        if pending_topics:
            warn_msg.append(f"🔍 調査トピック承認待ち: {len(pending_topics)} 件" if lang=="ja" else f"🔍 Topics Awaiting Approval: {len(pending_topics)}")
        if pending_articles:
            warn_msg.append(f"📄 記事・広告承認待ち: {len(pending_articles)} 件" if lang=="ja" else f"📄 Articles Awaiting Approval: {len(pending_articles)}")
        st.warning(f"🔔 **【オーナー決裁アラート】{' / '.join(warn_msg)}** ➔ 「🏢 Office Room」にて最終決裁を行ってください。")

    target_file = os.path.join(os.path.dirname(__file__), "data/sales_targets.json")
    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            target_data = json.load(f)
    else:
        target_data = {"monthly_target_yen": 100000, "target_articles_monthly": 15}
    
    target_sales = target_data.get("monthly_target_yen", 100000)
    total_sales = sum([art.get("price", 300) * 10 for art in articles if art.get("status") in ["Approved", "Published"]])
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

    # =============================================================
    # 🚀 全社タスク進行パイプライン（フェーズ可視化ボード）
    # =============================================================
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown(f"### 🚀 {'全社タスク進行パイプライン（フェーズ可視化ボード）' if lang=='ja' else 'Enterprise Task Progress Pipeline'}")
    st.markdown(f"<div style='color: #94A3B8; font-size: 0.9rem; margin-bottom: 14px;'>{'9名のAI社員による制作バトンリレーの進捗状況です。案件が左から右へ流れて売上化されます。' if lang=='ja' else 'Visual kanban pipeline showing progression across 9 AI specialists.'}</div>", unsafe_allow_html=True)

    # 5つのフェーズバケツを分類
    p1_items = [] # 1. 企画・市場調査 (15%)
    p2_items = [] # 2. 構成・執筆中 (50%)
    p3_items = [] # 3. 法務・QA検査 (80%)
    p4_items = [] # 4. オーナー決裁待ち (95%)
    p5_items = [] # 5. 公開・販売中 (100%)

    # トピックの分類 (社内規定 Rule-RES-10 により10本の企画ストックをPhase 1で維持)
    for tp in topics:
        st_val = tp.get("status", "Pending Owner Approval")
        if st_val == "Revision Requested":
            p1_items.append({"type": "topic", "data": tp, "title": tp.get("title", ""), "dept": "市場調査課", "progress": 20, "icon": "🔍", "note": "再調査中"})
        elif st_val == "Pending Owner Approval":
            p1_items.append({"type": "topic", "data": tp, "title": tp.get("title", ""), "dept": "市場調査課", "progress": 15, "icon": "📦", "note": "自律ストック中 (社内規定)"})
        elif st_val == "Approved":
            p2_items.append({"type": "topic", "data": tp, "title": tp.get("title", ""), "dept": "記事制作課引継待機", "progress": 40, "icon": "📑", "note": "執筆スタンバイ"})

    # 記事の分類
    for art in articles:
        st_val = art.get("status", "Pending Owner Approval")
        art_no_str = f"[{art.get('article_no', 'No.01')}] " if art.get("article_no") else ""
        if st_val == "Pending Owner Approval":
            p4_items.append({"type": "article", "data": art, "title": f"{art_no_str}{art.get('title', '')}", "dept": "記事制作・広報課", "progress": 95, "icon": "📄", "words": len(art.get("content", "")), "price": art.get("price", 300)})
        elif st_val == "Revision Requested":
            p2_items.append({"type": "article", "data": art, "title": f"{art_no_str}{art.get('title', '')}", "dept": "記事制作課", "progress": 55, "icon": "✍️", "words": len(art.get("content", "")), "note": "指示反映・加筆中"})
        elif st_val in ["Approved", "Published", "Pre-Publication"]:
            p5_items.append({"type": "article", "data": art, "title": f"{art_no_str}{art.get('title', '')}", "dept": "note販売チャンネル", "progress": 100, "icon": "🎉", "words": len(art.get("content", "")), "price": art.get("price", 300)})

    lane_c1, lane_c2, lane_c3, lane_c4, lane_c5 = st.columns(5)

    with lane_c1:
        st.markdown(f"""
        <div style='background: #0F172A; border-top: 4px solid #38BDF8; border-radius: 8px; padding: 10px; min-height: 280px;'>
            <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 6px;'>
                <strong style='color: #38BDF8; font-size: 0.85rem;'>🔍 1. 企画・調査</strong>
                <span style='background: #1E293B; color: #FFFFFF; font-size: 0.75rem; padding: 2px 6px; border-radius: 10px;'>{len(p1_items)}</span>
            </div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 4px;'>担当: 風間 涼 (15%)</div>
        </div>
        """, unsafe_allow_html=True)
        if not p1_items:
            st.caption("現在進行中の案件なし")
        for it in p1_items:
            st.markdown(f"""
            <div style='background: #1E293B; border: 1px solid #334155; border-radius: 6px; padding: 10px; margin-top: 8px;'>
                <div style='font-size: 0.82rem; font-weight: 700; color: #FFFFFF;'>{it['icon']} {clean_txt(it['title'])[:28]}...</div>
                <div style='font-size: 0.75rem; color: #F59E0B; margin-top: 4px;'>⚡ {it.get('note', '調査分析中')}</div>
            </div>
            """, unsafe_allow_html=True)

    with lane_c2:
        st.markdown(f"""
        <div style='background: #0F172A; border-top: 4px solid #F59E0B; border-radius: 8px; padding: 10px; min-height: 280px;'>
            <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 6px;'>
                <strong style='color: #F59E0B; font-size: 0.85rem;'>✍️ 2. 構成・執筆</strong>
                <span style='background: #1E293B; color: #FFFFFF; font-size: 0.75rem; padding: 2px 6px; border-radius: 10px;'>{len(p2_items)}</span>
            </div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 4px;'>担当: 結城 ＆ 森川 (50%)</div>
        </div>
        """, unsafe_allow_html=True)
        if not p2_items:
            st.caption("現在進行中の案件なし")
        for it in p2_items:
            st.markdown(f"""
            <div style='background: #1E293B; border: 1px solid #334155; border-radius: 6px; padding: 10px; margin-top: 8px;'>
                <div style='font-size: 0.82rem; font-weight: 700; color: #FFFFFF;'>{it['icon']} {clean_txt(it['title'])[:28]}...</div>
                <div style='font-size: 0.75rem; color: #FBBF24; margin-top: 4px;'>📝 {it.get('note', '4000字加筆執筆中')}</div>
            </div>
            """, unsafe_allow_html=True)

    with lane_c3:
        st.markdown(f"""
        <div style='background: #0F172A; border-top: 4px solid #A855F7; border-radius: 8px; padding: 10px; min-height: 280px;'>
            <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 6px;'>
                <strong style='color: #A855F7; font-size: 0.85rem;'>🛡️ 3. 法務・QA</strong>
                <span style='background: #1E293B; color: #FFFFFF; font-size: 0.75rem; padding: 2px 6px; border-radius: 10px;'>{len(p3_items)}</span>
            </div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 4px;'>担当: 橘 ＆ 神崎 (80%)</div>
        </div>
        """, unsafe_allow_html=True)
        if not p3_items:
            st.caption("全件スクリーニング済")

    with lane_c4:
        st.markdown(f"""
        <div style='background: #1E1B4B; border-top: 4px solid #EF4444; border-radius: 8px; padding: 10px; min-height: 280px;'>
            <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #6366F1; padding-bottom: 6px;'>
                <strong style='color: #F87171; font-size: 0.85rem;'>👑 4. 決裁待ち</strong>
                <span style='background: #EF4444; color: #FFFFFF; font-weight: 800; font-size: 0.75rem; padding: 2px 8px; border-radius: 10px;'>{len(p4_items)} 件</span>
            </div>
            <div style='font-size: 0.75rem; color: #CBD5E1; margin-top: 4px;'>担当: <strong>オーナー (95%)</strong></div>
        </div>
        """, unsafe_allow_html=True)
        if not p4_items:
            st.success("決裁待ちなし (全件完了)")
        for it in p4_items:
            words_info = f" ({it['words']:,}字)" if "words" in it else ""
            st.markdown(f"""
            <div style='background: #2E1065; border: 1px solid #A855F7; border-radius: 6px; padding: 10px; margin-top: 8px;'>
                <div style='font-size: 0.82rem; font-weight: 800; color: #FFFFFF;'>{it['icon']} {clean_txt(it['title'])[:26]}...{words_info}</div>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 6px;'>
                    <span style='background: #F59E0B; color: #000; font-weight: 800; font-size: 0.7rem; padding: 1px 6px; border-radius: 4px;'>¥{it.get('price', 300)}</span>
                    <span style='color: #F43F5E; font-weight: 800; font-size: 0.75rem;'>🔒 承認待ち</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("👉 決裁する", key=f"pipe_btn_app_{it['type']}_{it['data']['id']}", use_container_width=True):
                st.session_state.active_page_id = "office"
                st.session_state.scroll_trigger += 1
                st.rerun()

    with lane_c5:
        st.markdown(f"""
        <div style='background: #0F172A; border-top: 4px solid #10B981; border-radius: 8px; padding: 10px; min-height: 280px;'>
            <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 6px;'>
                <strong style='color: #10B981; font-size: 0.85rem;'>🎉 5. 公開・販売</strong>
                <span style='background: #065F46; color: #FFFFFF; font-size: 0.75rem; padding: 2px 6px; border-radius: 10px;'>{len(p5_items)}</span>
            </div>
            <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 4px;'>担当: 佐々木 ＆ 白石 (100%)</div>
        </div>
        """, unsafe_allow_html=True)
        if not p5_items:
            st.caption("公開準備中")
        for it in p5_items:
            st.markdown(f"""
            <div style='background: #064E3B; border: 1px solid #10B981; border-radius: 6px; padding: 10px; margin-top: 8px;'>
                <div style='font-size: 0.82rem; font-weight: 700; color: #FFFFFF;'>{it['icon']} {clean_txt(it['title'])[:26]}...</div>
                <div style='font-size: 0.75rem; color: #6EE7B7; margin-top: 4px;'>✅ note販売準備完了 (¥{it.get('price', 300)})</div>
            </div>
            """, unsafe_allow_html=True)

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
# 2. 🏢 Office Room (👑 Universal Approval Center with Radio Records & Single Dossier)
# ==========================================
elif page_id == "office":
    st.markdown(f"<div class='main-header'>{t('office_main_header', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('office_sub_header', lang)}</div>", unsafe_allow_html=True)


    st.markdown(f"<div class='section-title'>{t('office_sec_title', lang)}</div>", unsafe_allow_html=True)

    game_html = get_office_game_html(lang)
    components.html(game_html, height=545)


    # -------------------------------------------------------------
    # 👑 全社統合決裁センター (Universal Executive Approval Center)
    # -------------------------------------------------------------
    st.markdown("---")
    st.markdown(f"<div class='section-title'>👑 {'全社統合決裁センター' if lang=='ja' else 'Universal Executive Approval Center'}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='color: #94A3B8; margin-bottom: 18px;'>{'全社各部門の決裁待ち申請を一覧（レコード）として並べています。ラジオボタンで1件選択し、単一の査読エリアで審査・決裁を行ってください。' if lang=='ja' else 'All pending submissions across departments are listed below. Select one submission via radio button to inspect and sign off in the single review dossier.'}</div>", unsafe_allow_html=True)

    pending_items = []
    # 1. 記事制作課・品質管理課（記事・成果物）- 決裁待ち(Pending Owner Approval)のみ抽出
    for art in workflow.list_articles():
        if art.get("status") == "Pending Owner Approval":
            r_dept = art.get("routed_dept", "qa")
            r_name = art.get("routed_dept_name", "品質管理課 (神崎 玲奈)")
            art_no_tag = f"[{art.get('article_no', 'No.01')}] " if art.get("article_no") else ""
            pending_items.append({
                "unique_key": f"art_{art['id']}",
                "type": "article",
                "id": art["id"],
                "dept": r_name,
                "icon": "📄",
                "title": f"{art_no_tag}{clean_txt(art.get('title', ''))}",
                "date": art.get("created_at", ""),
                "status": art.get("status", "Pending Owner Approval"),
                "data": art
            })
            
    # 2. 市場調査課（企画トピック）- 決裁待ち(Pending Owner Approval)のみ抽出
    for tp in market_manager.list_topics():
        if tp.get("status") == "Pending Owner Approval":
            pending_items.append({
                "unique_key": f"topic_{tp['id']}",
                "type": "topic",
                "id": tp["id"],
                "dept": "市場調査課 (風間 涼)",
                "icon": "🔍",
                "title": clean_txt(tp.get("title", "")),
                "date": tp.get("created_at", ""),
                "status": tp.get("status", "Pending Owner Approval"),
                "data": tp
            })

    if not pending_items:
        st.success("✅ 現在、全社で決裁待ちの案件はありません（すべての部門の案件が承認・処理済みです）。" if lang=="ja" else "✅ All company-wide submissions have been reviewed and approved.")
    else:
        topic_items = [it for it in pending_items if it["type"] == "topic"]
        art_items = [it for it in pending_items if it["type"] == "article"]

        # カテゴリー分類タブ・フィルター
        st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
        c_flt1, c_flt2 = st.columns([3, 1])
        with c_flt1:
            cat_options = []
            if topic_items:
                cat_options.append("topics")
            if art_items:
                cat_options.append("articles")
            if topic_items and art_items:
                cat_options.append("all")

            filter_mode = st.radio(
                "📂 決裁カテゴリーの選択:",
                options=cat_options,
                format_func=lambda x: {
                    "topics": f"🔍 市場調査課・企画決裁 ({len(topic_items)}件)",
                    "articles": f"📄 記事・成果物最終決裁 ({len(art_items)}件)",
                    "all": f"🌐 全社すべての申請 ({len(pending_items)}件)"
                }.get(x, x),
                horizontal=True,
                key="univ_cat_filter"
            )
        with c_flt2:
            st.caption("🛡️ 社内規程【Rule-OPS-AUTO】準拠\n承認完了後は指定先部署へ自動連携されます。")

        filtered_items = topic_items if filter_mode == "topics" else (art_items if filter_mode == "articles" else pending_items)
        if not filtered_items:
            filtered_items = pending_items

        # レコード一覧（ラジオボタン直接組み込み型テーブル）
        st.markdown(f"#### 📋 {'決裁待ち申請レコード一覧（行のラジオボタンで直接選択）' if lang=='ja' else 'Pending Submissions Queue (Direct Radio Selection)'}")

        pending_key_map = {it["unique_key"]: it for it in pending_items}
        valid_options = [it["unique_key"] for it in filtered_items]

        if "univ_record_radio_table" in st.session_state and st.session_state.univ_record_radio_table not in valid_options:
            del st.session_state["univ_record_radio_table"]

        # テーブルヘッダー表示
        st.html("""
        <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid #334155; border-radius: 8px 8px 0 0; padding: 10px 16px; display: flex; align-items: center; font-size: 0.82rem; font-weight: 800; color: #94A3B8; border-bottom: 2px solid #1E293B; letter-spacing: 0.02em;">
            <span style="width: 100px; display: inline-flex; align-items: center; gap: 4px;">🔘 選択 / No.</span>
            <span style="width: 180px;">種別 / 所属</span>
            <span style="flex: 1;">申請件名 / タイトル</span>
            <span style="width: 120px; text-align: right;">申請日時</span>
        </div>
        """)

        def format_table_radio_row(key):
            it = pending_key_map[key]
            idx = valid_options.index(key) + 1
            date_str = f" [{it['date'][5:16]}]" if it.get("date") else ""
            return f"**No.{idx:02d}**　{it['icon']} **[{it['dept']}]**　**{it['title']}**　`{date_str}`"

        captions_list = [
            f"📌 申請ステータス: {it['status']} ｜ 担当部署: {it['dept']}"
            for it in filtered_items
        ]

        selected_key = st.radio(
            "👇 査読・決裁を行う申請を選択してください:",
            options=valid_options,
            format_func=format_table_radio_row,
            captions=captions_list,
            key="univ_record_radio_table",
            label_visibility="collapsed"
        )

        current_item = pending_key_map[selected_key]
        item_type = current_item["type"]
        item_raw = current_item["data"]
        cur_status = current_item["status"]

        # 3. 単一の査読エリア（選択された1件のプレビューを表示 - st.htmlによる完全クリーンレンダリング）
        st.markdown("---")
        st.markdown(f"<div class='section-title'>📄 {'審査書類・プレビュー（査読エリア）' if lang=='ja' else 'Review Dossier (Single Inspection Area)'}</div>", unsafe_allow_html=True)

        if item_type == "article":
            st.html(get_article_dossier_html(item_raw, lang))
        elif item_type == "topic":
            st.html(get_topic_dossier_html(item_raw, lang))

        # 4. 査読エリアの直下に「承認」「✍️ 否認」「拒否」ボタンを表示
        st.markdown("---")
        st.markdown(f"<div class='section-title'>👑 {'オーナー最終決裁欄' if lang=='ja' else 'Executive Decision Gateway'}</div>", unsafe_allow_html=True)

        # 💰 価格変更ウィジェット（記事の場合）
        if item_type == "article":
            cur_price = item_raw.get("price", 300)
            c_pr1, c_pr2 = st.columns([3, 1])
            with c_pr1:
                new_price_val = st.number_input(
                    "💰 販売価格の変更・調整 (note販売価格):",
                    min_value=100,
                    max_value=50000,
                    value=int(cur_price),
                    step=50,
                    key=f"univ_price_input_{item_raw['id']}",
                    help="noteでの販売価格（100円〜50,000円）を設定できます。売上目標や財務試算に即時反映されます。"
                )
            with c_pr2:
                st.write("")
                if st.button("💾 価格を更新", key=f"univ_price_btn_{item_raw['id']}", use_container_width=True):
                    workflow.update_article_price(item_raw["id"], new_price_val)
                    st.success(f"販売価格を ¥{new_price_val:,} に更新しました！")
                    st.rerun()

        st.markdown(f"""
        <div class='approval-box-locked'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <h3 style='color: #FCD34D !important; margin:0;'>🔒 Status: {cur_status}</h3>
                <span style='background:#F59E0B; color:#000; font-weight:800; padding:4px 10px; border-radius:6px;'>{'決裁待ち' if lang=='ja' else 'Pending'}</span>
            </div>
            <div style='margin-top: 10px; font-size: 0.95rem; line-height: 1.6;'>
                {'上記査読エリアの申請内容を確認の上、「承認」「✍️ 否認」「拒否」の決裁を行ってください。' if lang=='ja' else 'Review the dossier above and select Approve, Deny, or Reject.'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_dec1, col_dec2, col_dec3 = st.columns([2, 2, 1])

        with col_dec1:
            if st.button("承認", type="primary", use_container_width=True, key="univ_btn_approve"):
                if item_type == "article":
                    workflow.approve_article(current_item["id"])
                    st.success("🎉 記事を承認しました！投稿ロックを解除しました。")
                else:
                    market_manager.approve_topic(current_item["id"])
                    market_manager.mark_topic_in_production(current_item["id"])
                    st.session_state.prefill_topic = clean_txt(item_raw.get("title", ""))
                    st.session_state.prefill_audience = clean_txt(item_raw.get("target_audience", ""))
                    st.session_state.auto_start_creation = True
                    st.session_state.active_page_id = "content_creation"
                st.session_state.show_univ_rev_form = False
                if "univ_record_radio_table" in st.session_state:
                    del st.session_state["univ_record_radio_table"]
                st.session_state.scroll_trigger += 1
                st.rerun()

        with col_dec2:
            if st.button("✍️ 否認", use_container_width=True, key="univ_btn_toggle_revision"):
                st.session_state.show_univ_rev_form = not st.session_state.show_univ_rev_form
                st.rerun()

        with col_dec3:
            if st.button("拒否", use_container_width=True, key="univ_btn_reject"):
                if item_type == "article":
                    workflow.reject_article(current_item["id"])
                    st.info("記事を拒否（却下・アーカイブ）しました。")
                else:
                    market_manager.reject_topic(current_item["id"])
                    st.info("トピックを拒否（却下）しました。")
                st.session_state.show_univ_rev_form = False
                if "univ_record_radio_table" in st.session_state:
                    del st.session_state["univ_record_radio_table"]
                st.session_state.scroll_trigger += 1
                st.rerun()

        # 否認時の指示入力フォーム
        if st.session_state.show_univ_rev_form:
            with st.container():
                st.markdown(f"#### ✍️ {'否認・修正指示の入力（社内ルール【Rule-OPS-AUTO】）' if lang=='ja' else 'Denial & Revision Directives'}")
                with st.form("univ_revision_form", clear_on_submit=True):
                    univ_target_dept = "content_creation"
                    if item_type == "article":
                        univ_target_dept = st.radio(
                            "🎯 差し戻し・業務送付先を選択してください（社内ルール【Rule-OPS-AUTO】）:",
                            options=["content_creation", "market_research", "pr"],
                            format_func=lambda x: {
                                "content_creation": "✍️ 記事制作課（結城 紬 & 森川 拓真）- 構成案・執筆・有料テンプレートの再修正",
                                "market_research": "🔍 市場調査課（風間 涼）- ターゲット読者層・市場ニーズ・競合ギャップの再調査",
                                "pr": "📢 広報課（佐々木 翼）- 5大SNSプロモーション文・キャッチコピーの再考"
                            }.get(x, x),
                            index=0,
                            help="社内業務連携規程に基づき、否認理由に応じてタスクを再送付する部署を選択します。"
                        )
                    fb_text = st.text_area(
                        "修正・再調査の具体的な指示内容を入力してください:",
                        placeholder="例: 有料部分のテンプレートの具体例をもう1つ追加してください。 / ターゲット層を20代若手社員向けに変更して再調査してください。",
                        key="univ_feedback_input"
                    )
                    submit_univ_rev = st.form_submit_button("📨 否認指示を送信する", type="primary", use_container_width=True)
                    if submit_univ_rev:
                        if fb_text.strip():
                            if item_type == "article":
                                workflow.request_revision(current_item["id"], fb_text, target_dept=univ_target_dept)
                                workflow.auto_revise_and_forward_to_qa(current_item["id"], fb_text, target_dept=univ_target_dept)
                                dept_label = {"content_creation": "記事制作課", "market_research": "市場調査課", "pr": "広報課"}.get(univ_target_dept, "担当課")
                                st.success(f"🎉 社内ルール【Rule-OPS-AUTO】に基づき、{dept_label}がご指摘に基づき加筆・修正を自律完了し、自動で品質管理課へ再送付しました！")
                            else:
                                market_manager.request_revision(current_item["id"], fb_text)
                                st.success("🎉 社内ルール【Rule-OPS-AUTO】に基づき、市場調査課（風間アナリスト）が再調査を自律完了し、決裁待ちへ自動再申請しました！")
                            st.session_state.show_univ_rev_form = False
                            if "univ_record_radio_table" in st.session_state:
                                del st.session_state["univ_record_radio_table"]
                            st.session_state.scroll_trigger += 1
                            st.rerun()
                        else:
                            st.error("指示内容を入力してください。")

    # -------------------------------------------------------------
    # 🔄 担当課にて修正・再執筆対応中の案件 (Revision Queue)
    # -------------------------------------------------------------
    in_revision_items = []
    for art in workflow.list_articles():
        if art.get("status") == "Revision Requested":
            r_dept = art.get("routed_dept", "content_creation")
            r_icon = "🔍" if r_dept == "market_research" else ("📢" if r_dept == "pr" else "✍️")
            r_name = art.get("routed_dept_name", "記事制作課 (結城 紬 & 森川 拓真)")
            art_no_tag = f"[{art.get('article_no', 'No.01')}] " if art.get("article_no") else ""
            in_revision_items.append({
                "id": art["id"],
                "type": "article",
                "dept": r_name,
                "icon": r_icon,
                "title": f"{art_no_tag}{clean_txt(art.get('title', ''))}",
                "feedback": clean_txt(art.get("latest_feedback", "修正対応中")),
                "date": art.get("created_at", "")
            })
    for tp in market_manager.list_topics():
        if tp.get("status") == "Revision Requested":
            in_revision_items.append({
                "id": tp["id"],
                "type": "topic",
                "dept": "市場調査課 (風間 涼)",
                "icon": "🔍",
                "title": clean_txt(tp.get("title", "")),
                "feedback": clean_txt(tp.get("latest_feedback", "再調査対応中")),
                "date": tp.get("created_at", "")
            })

    if in_revision_items:
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.markdown(f"#### 🔄 {'各課にて修正・再調査対応中の案件 (Rule-OPS-AUTO)' if lang=='ja' else 'Revisions In-Progress by Departments'}")
        for rev_it in in_revision_items:
            with st.container():
                c_rv1, c_rv2 = st.columns([4, 1])
                with c_rv1:
                    st.markdown(f"""
                    <div style='background: #1E1B4B; border: 1px solid #6366F1; border-radius: 8px; padding: 14px; margin-bottom: 8px;'>
                        <strong style='color: #A5B4FC; font-size: 0.95rem;'>{rev_it['icon']} [{rev_it['dept']}] {rev_it['title']}</strong>
                        <div style='color: #E0E7FF; font-size: 0.88rem; margin-top: 4px;'><strong>💬 指示内容:</strong> {rev_it['feedback']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with c_rv2:
                    st.write("")
                    st.markdown("""
                    <div style='text-align: center; margin-top: 4px;'>
                        <span style='background: #312E81; color: #A5B4FC; border: 1px solid #6366F1; font-size: 0.76rem; font-weight: 700; padding: 6px 8px; border-radius: 6px; display: inline-block; line-height: 1.3;'>
                            🤖 Rule-OPS-AUTO<br>自律修正中
                        </span>
                    </div>
                    """, unsafe_allow_html=True)



    # -------------------------------------------------------------
    # 💬 社員との直接対話・質問・指示デスク (Employee Consultation Desk)
    # -------------------------------------------------------------
    st.markdown("---")
    st.markdown(f"<div class='section-title'>{t('consult_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='color: #94A3B8; margin-bottom: 14px;'>{t('consult_sub', lang)}</div>", unsafe_allow_html=True)

    # Load dynamic employees from company_info.json
    comp_file = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/company_info.json")
    if os.path.exists(comp_file):
        with open(comp_file, "r", encoding="utf-8") as f:
            all_c_info = json.load(f)
        all_emps = all_c_info.get("employees", [])
    else:
        all_emps = []

    assign_options = [t("consult_assign_auto", lang)]
    assignee_map = {t("consult_assign_auto", lang): "auto"}
    for e in all_emps:
        short_role = e.get("role", "AI").split("/")[0].strip()
        opt_str = f"{e.get('icon', '👤')} {e['name']} ({short_role})"
        assign_options.append(opt_str)
        assignee_map[opt_str] = e["id"]

    with st.form("office_consultation_form", clear_on_submit=True):
        c_in_q1, c_in_q2 = st.columns([4, 1])
        with c_in_q1:
            user_inquiry = st.text_input(
                t("consult_input_label", lang),
                placeholder=t("consult_placeholder", lang)
            )
        with c_in_q2:
            target_assignee = st.selectbox(t("consult_assign_label", lang), assign_options)
        submit_inquiry = st.form_submit_button(t("consult_submit_btn", lang), type="primary", use_container_width=True)

    if submit_inquiry and user_inquiry.strip():
        chosen_emp = assignee_map.get(target_assignee, "auto")

        with st.spinner("担当者がデスクで回答を作成中..." if lang == "ja" else "Specialist is drafting the response..."):
            response_data = chat_manager.generate_response(user_inquiry, chosen_emp)
            st.session_state.office_chat_history.append({
                "user": user_inquiry,
                "response": response_data,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()

    if st.session_state.office_chat_history:
        st.markdown(f"#### {t('consult_log_title', lang)}")
        for item in reversed(st.session_state.office_chat_history):
            resp = item["response"]
            st.markdown(f"""
            <div class='user-query-card'>
                <div style='font-size: 0.8rem; color: #94A3B8;'>🕒 {item.get('timestamp', '')} | <strong>{t('consult_user_prefix', lang)}</strong></div>
                <div style='font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-top: 4px;'>{clean_txt(item['user'])}</div>
            </div>
            <div class='chat-bubble'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                    <div style='font-weight: 800; color: #FFFFFF; font-size: 1.1rem;'>
                        {resp.get('icon', '🧑‍💼')} {resp.get('name', '担当社員')} <span style='font-size: 0.85rem; color: #93C5FD; font-weight: 600;'>（{resp.get('role', '')} / {resp.get('department', '')}）</span>
                    </div>
                    <span class='status-live'><span class='pulse-dot'></span>{t('consult_status_done', lang)}</span>
                </div>
                <div style='white-space: pre-wrap; font-size: 0.95rem; line-height: 1.6; color: #F8FAFC;'>{clean_txt(resp.get('content', ''))}</div>
            </div>
            """, unsafe_allow_html=True)

            if resp.get("emp_id") == "ayase" or any(k in item.get("user", "") for k in ["雇用", "採用", "増員", "連れて", "雇", "hire", "recruit", "ライター", "社員"]):
                u_txt = item.get("user", "").lower()
                avail = st.session_state.hr_manager.get_candidate_presets(include_hired=False)
                suggested_hires = []
                if any(w in u_txt for w in ["女性", "女", "female", "girl"]) and any(w in u_txt for w in ["ライター", "執筆", "writer", "記事"]):
                    suggested_hires = [p for p in avail if p["id"] in ["sakurai", "shirakawa"]]
                elif any(w in u_txt for w in ["ライター", "執筆", "writer"]):
                    suggested_hires = [p for p in avail if p["id"] in ["sakurai", "shirakawa", "kiryu"]]
                elif any(w in u_txt for w in ["マーケ", "sns", "海外", "英語"]):
                    suggested_hires = [p for p in avail if p["id"] in ["stewart"]]

                if suggested_hires:
                    st.markdown(f"""
                    <div style='background: #0F172A; border: 1px solid #38BDF8; border-radius: 8px; padding: 10px 14px; margin-top: 10px; margin-bottom: 8px;'>
                        <div style='color: #38BDF8; font-weight: 700; font-size: 0.92rem;'>🎯 綾瀬七海が選考した即戦力候補（今すぐこのオフィスに連れてくることができます）:</div>
                    </div>
                    """, unsafe_allow_html=True)
                    for s_cand in suggested_hires:
                        sc_1, sc_2 = st.columns([3, 2])
                        with sc_1:
                            st.markdown(f"**{s_cand['icon']} {s_cand['name']}**<br><span style='color: #94A3B8; font-size: 0.83rem;'>{s_cand['role']}</span>", unsafe_allow_html=True)
                        with sc_2:
                            if st.button(f"🤝 {s_cand['name'].split(' ')[0]} を連れてくる (0円)", key=f"btn_chat_hire_{s_cand['id']}_{item.get('timestamp')}", type="primary", use_container_width=True):
                                try:
                                    hired_emp = st.session_state.hr_manager.hire_employee(s_cand)
                                    st.balloons()
                                    st.success(f"🎉 新規AI社員【{s_cand['name']}】を正式雇用し、2Dオフィスフロアに配属しました！")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"雇用エラー: {e}")

                c_jump1, c_jump2 = st.columns([2, 1])
                with c_jump2:
                    if st.button("👉 🤝 人事課（HR）の採用・雇用デスクへ移動", key=f"btn_jump_hr_{item.get('timestamp')}", use_container_width=True, type="secondary"):
                        st.session_state.active_page_id = "hr"
                        st.rerun()

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

    # -------------------------------------------------------------
    # ✨ 新規配属・増員スペシャリストデスク (Newly Recruited AI Specialists)
    # -------------------------------------------------------------
    base_9_ids = {"ichijo", "tachibana", "ayase", "kazama", "yuki", "morikawa", "kanzaki", "sasaki", "shiraishi"}
    new_hired = [e for e in all_emps if e.get("id") not in base_9_ids]

    if new_hired:
        st.markdown(f"#### ✨ {'新規配属・増員スペシャリストデスク (稼働中)' if lang=='ja' else 'Reinforcement & Newly Recruited Specialists (Active)'}")
        cols_nh = st.columns(min(len(new_hired), 3))
        for idx, emp in enumerate(new_hired):
            c_nh = cols_nh[idx % len(cols_nh)]
            with c_nh:
                st.markdown(f"""
                <div class='desk-card' style='border: 1px solid #38BDF8; box-shadow: 0 4px 12px rgba(56, 189, 248, 0.15); border-left: 5px solid {emp.get("color", "#38BDF8")};'>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='font-size: 1.6rem;'>{emp.get('icon', '👤')}</span>
                        <span class='status-live' style='color: #38BDF8; border-color: #38BDF8;'><span class='pulse-dot' style='background: #38BDF8;'></span>{'即時稼働中' if lang=='ja' else 'Active'}</span>
                    </div>
                    <div style='font-weight: 800; font-size: 1.15rem; color: #FFFFFF; margin-top: 4px;'>{emp.get('name')}</div>
                    <div style='font-size: 0.85rem; color: #38BDF8; font-weight: 700;'>{emp.get('role')}</div>
                    <div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>📍 {emp.get('department')}（増員配属ブース）</div>
                    <div style='font-size: 0.85rem; color: #F8FAFC; margin-top: 6px; background: #0F172A; padding: 10px; border-radius: 6px; border: 1px solid #334155;'>💬 「{clean_txt(emp.get('motto', '業務稼働中'))}」</div>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# 3. 🔍 Market Research Division
# ==========================================
elif page_id == "market_research":
    st.markdown(f"<div class='main-header'>{t('mr_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('mr_sub', lang)}</div>", unsafe_allow_html=True)
    
    st.info(t("mr_mission", lang))
    
    # =============================================================
    # 📋 社内就業規則【Rule-RES-10】常時10本ストック自律維持プロトコル
    # =============================================================
    stock_info = market_manager.get_stock_status(target_stock_count=10)
    cur_stock = stock_info["current_count"]
    stock_ratio = min(1.0, cur_stock / 10.0)

    rule_title = "社内業務規定【Rule-RES-10】常時10本ストック自律維持プロトコル" if lang == "ja" else "Company Policy [Rule-RES-10]: Autonomous 10-Slot Topic Stock Active"
    rule_sub = "担当: 市場調査課 風間 涼 ｜ 運用モード: 完全自律（オーナー操作不要）" if lang == "ja" else "Analyst: Ryo Kazama (Research) | Mode: Fully Autonomous (Zero Owner Effort)"
    rule_badge_status = "自律稼働中" if lang == "ja" else "AUTONOMOUS"
    rule_badge_stock = f"📦 {cur_stock} / 10 本（充足率 100%）" if lang == "ja" else f"📦 {cur_stock} / 10 Topics (100%)"
    rule_meter_label = "📈 企画ストック充填状況: 満タン維持（空き枠 0本）" if lang == "ja" else "📈 Stock Status: Fully Maintained (0 Slots Vacant)"
    rule_meter_pct = f"{cur_stock} / 10 SLOTS FILLED (100%)"
    rule_desc = (
        "💡 <strong>【完全自動運用の仕組み】</strong> 企画が記事制作課へ引き渡されたり、オーナーによって却下（拒否）された場合、社内ルールに基づき風間アナリストが即座に最新note市場から自律起票し、常に10本のストックを満タン維持します。オーナーによる補充ボタンのクリック操作は一切不要です。"
        if lang == "ja" else
        "💡 <strong>[Autonomous Operation Protocol]</strong> Whenever a topic is sent to drafting or rejected, Analyst Ryo Kazama instantly analyzes note market trends and replenishes new topics autonomously to guarantee 10 full topic stocks at all times without manual button clicks."
    )

    st.html(f"""
    <div style="background: linear-gradient(135deg, #091E19 0%, #0F172A 100%); border: 1.5px solid #10B981; border-radius: 12px; padding: 18px 22px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15); box-sizing: border-box; width: 100%;">
        <!-- Top Row: Title & Active Badge -->
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 14px; border-bottom: 1px solid rgba(16, 185, 129, 0.25); padding-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 10px; min-width: 260px; flex: 1;">
                <span style="font-size: 1.4rem;">📋</span>
                <div>
                    <div style="color: #6EE7B7; font-size: 1.08rem; font-weight: 800; letter-spacing: 0.02em; line-height: 1.4;">
                        {rule_title}
                    </div>
                    <div style="color: #94A3B8; font-size: 0.8rem; margin-top: 2px;">
                        {rule_sub}
                    </div>
                </div>
            </div>
            <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px;">
                <span style="background: rgba(16, 185, 129, 0.18); color: #6EE7B7; border: 1px solid #10B981; font-weight: 800; font-size: 0.82rem; padding: 4px 12px; border-radius: 20px; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap;">
                    <span style="display: inline-block; width: 7px; height: 7px; background: #10B981; border-radius: 50%; box-shadow: 0 0 6px #10B981;"></span>
                    {rule_badge_status}
                </span>
                <span style="background: #10B981; color: #022C22; font-weight: 900; font-size: 0.84rem; padding: 4px 12px; border-radius: 20px; white-space: nowrap; box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);">
                    {rule_badge_stock}
                </span>
            </div>
        </div>

        <!-- Middle: Built-in Custom Progress Meter -->
        <div style="margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #CBD5E1; margin-bottom: 6px; font-weight: 600;">
                <span>{rule_meter_label}</span>
                <span style="color: #6EE7B7; font-weight: 800; font-family: monospace;">{rule_meter_pct}</span>
            </div>
            <div style="background: #1E293B; border-radius: 8px; height: 8px; overflow: hidden; border: 1px solid #334155;">
                <div style="width: 100%; height: 100%; background: linear-gradient(90deg, #059669 0%, #10B981 50%, #34D399 100%); box-shadow: 0 0 8px rgba(52, 211, 153, 0.5);"></div>
            </div>
        </div>

        <!-- Bottom: Informative description with employee role -->
        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(51, 65, 85, 0.7); border-radius: 8px; padding: 10px 14px; font-size: 0.84rem; color: #E2E8F0; line-height: 1.6;">
            {rule_desc}
        </div>
    </div>
    """)

    # Rule-OPS-AUTO: 品質管理課から市場調査課へ差し戻された案件の自動再調査と品質管理課への自動再送付
    mr_rev_articles = [a for a in workflow.list_articles() if a.get("status") == "Revision Requested" and a.get("routed_dept") == "market_research"]
    if mr_rev_articles:
        with st.status("⚡ **社内ルール【Rule-OPS-AUTO】**: 市場調査課（風間 涼）が差し戻し案件の再調査・ペルソナ分析を自律実行中...", expanded=True) as status_box:
            for rev_a in mr_rev_articles:
                st.write(f"🔍 『{clean_txt(rev_a.get('title'))}』の再調査を実施中...")
                workflow.auto_revise_and_forward_to_qa(rev_a["id"], rev_a.get("latest_feedback", "再調査"), target_dept="market_research")
            status_box.update(label="✅ **社内ルール【Rule-OPS-AUTO】**: 再調査が完了し、品質管理課へ自動再送付しました！", state="complete")
        st.success("🎉 市場調査課での再調査が自律完了し、社内ルール【Rule-OPS-AUTO】に基づき品質管理課へ自動再送付されました。")
        st.rerun()

    with st.expander(f"➕ 手動でキーワードを指定して調査する（手動リサーチ）", expanded=False):
        c_rs1, c_rs2 = st.columns([3, 2])
        with c_rs1:
            rs_kw = st.text_input(t("mr_keyword_label", lang), placeholder=t("mr_keyword_ph", lang))
        with c_rs2:
            rs_aud = st.text_input(t("mr_audience_label", lang), placeholder=t("mr_audience_ph", lang))
        
        if st.button(t("mr_btn_research", lang), type="primary", use_container_width=True):
            if rs_kw.strip():
                with st.spinner("風間アナリストがnote市場・競合ギャップを調査中..."):
                    new_tp = market_manager.conduct_research(rs_kw, rs_aud)
                    st.success(f"🎉 新規トピック『{clean_txt(new_tp['title'])}』の市場調査が完了し、承認待ちとして登録されました！")
                    st.rerun()
            else:
                st.warning("調査キーワードを入力してください。")

    st.markdown("---")

    st.markdown(f"<div class='section-title'>{t('mr_topic_list_header', lang)}</div>", unsafe_allow_html=True)
    topics = market_manager.list_topics()
    
    if not topics:
        st.info("調査トピックがありません。上記フォームから新規調査を指示してください。")
    else:
        topic_titles = [f"[{tp.get('status', 'Pending Owner Approval')}] {clean_txt(tp.get('category', ''))} | {clean_txt(tp.get('title', ''))}" for tp in topics]
        sel_tp_idx = st.selectbox(t("mr_select_topic_label", lang), range(len(topics)), format_func=lambda x: topic_titles[x])
        tp = topics[sel_tp_idx]
        tp_status = tp.get("status", "Pending Owner Approval")
        tp_locked = tp_status in ["Pending Owner Approval", "Revision Requested"]

        # 📄 査読エリア（st.htmlによる完全クリーンレンダリング）
        st.html(get_topic_dossier_html(tp, lang))

        # 👑 企画決裁欄（プレビューのあとに配置）
        st.markdown("---")
        st.markdown(f"<div class='section-title'>👑 {'企画決裁ゲートウェイ' if lang=='ja' else 'Topic Approval Gateway'}</div>", unsafe_allow_html=True)

        if tp_locked:
            st.markdown(f"""
            <div class='approval-box-locked'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <h3 style='color: #FCD34D !important; margin:0;'>🔒 Status: {tp_status}</h3>
                    <span style='background:#F59E0B; color:#000; font-weight:800; padding:4px 10px; border-radius:6px;'>企画承認待ち</span>
                </div>
                <div style='margin-top: 10px; font-size: 0.95rem; line-height: 1.6;'>
                    {'🔒 【企画ロック中】「承認」を押すと、追加ボタン操作不要で記事作成課が自動的に記事作成を開始します。' if lang=='ja' else '🔒 [Topic Locked] Approving will automatically start article creation.'}
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
                    {'✅ オーナー承認完了。記事制作課へ業務が自動移行されています。' if lang=='ja' else '✅ Topic approved and transitioned to Content Creation.'}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 👑 トピック決裁アクションボタン
        if tp_locked:
            col_tpa1, col_tpa2, col_tpa3 = st.columns([2, 2, 1])
            with col_tpa1:
                btn_app_label = "承認" if lang == "ja" else "Approve"
                if st.button(btn_app_label, type="primary", use_container_width=True, key="mr_btn_app_topic"):
                    market_manager.approve_topic(tp["id"])
                    market_manager.mark_topic_in_production(tp["id"])
                    st.session_state.prefill_topic = clean_txt(tp.get("title", ""))
                    st.session_state.prefill_audience = clean_txt(tp.get("target_audience", ""))
                    st.session_state.auto_start_creation = True
                    st.session_state.active_page_id = "content_creation"
                    st.session_state.scroll_trigger += 1
                    st.rerun()

            with col_tpa2:
                if st.button("✍️ 否認", use_container_width=True, key="mr_toggle_tp_rev"):
                    st.session_state.show_mr_tp_rev = not st.session_state.show_mr_tp_rev
                    st.rerun()

            with col_tpa3:
                if st.button("拒否", use_container_width=True, key="mr_btn_rej_topic"):
                    market_manager.reject_topic(tp["id"])
                    st.info("トピックを拒否（却下）しました。社内規定【Rule-RES-10】に基づき風間アナリストが代替トピックを自律起票しました。")
                    st.rerun()

            if st.session_state.show_mr_tp_rev:
                with st.container():
                    st.markdown(f"#### ✍️ {'否認・再調査指示の入力' if lang=='ja' else 'Topic Revision Directives'}")
                    with st.form("mr_page_topic_revision_form", clear_on_submit=True):
                        rev_fb = st.text_area(t("mr_topic_feedback_label", lang), placeholder=t("mr_topic_feedback_ph", lang), key="mr_rev_tp_fb")
                        submit_mr_rev = st.form_submit_button("📨 否認指示を送信する", type="primary", use_container_width=True)
                        if submit_mr_rev:
                            if rev_fb.strip():
                                market_manager.request_revision(tp["id"], rev_fb)
                                st.session_state.show_mr_tp_rev = False
                                st.warning("風間アナリストに再調査・切り口変更指示を伝達しました。")
                                st.rerun()
                            else:
                                st.error("指示内容を入力してください。")
        else:
            st.info("💡 この企画は既にオーナー承認済みです。記事制作課（結城・森川）にて本格執筆が進行しています。" if lang == "ja" else "💡 This topic has already been approved and transitioned to production.")

        st.markdown("##### ⏱️ 企画ステータス遷移タイムスタンプ履歴")
        history = tp.get("status_history", [])
        for h in reversed(history):
            note_str = f" - <em>{clean_txt(h.get('note'))}</em>" if h.get('note') else ""
            st.markdown(f"- 🕒 **{h.get('timestamp')}** ➔ `[{h.get('status')}]` ({clean_txt(h.get('actor', ''))}){note_str}", unsafe_allow_html=True)

# ==========================================
# 4. ✍️ Content Creation Division
# ==========================================
elif page_id == "content_creation":
    st.markdown(f"<div class='main-header'>{t('cc_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('cc_sub', lang)}</div>", unsafe_allow_html=True)

    # Rule-OPS-AUTO: 品質管理課から記事制作課へ差し戻された案件の自動加筆修正と品質管理課への自動再送付
    cc_rev_articles = [a for a in workflow.list_articles() if a.get("status") == "Revision Requested" and a.get("routed_dept", "content_creation") == "content_creation"]
    if cc_rev_articles:
        with st.status("⚡ **社内ルール【Rule-OPS-AUTO】**: 記事制作課（結城 紬 & 森川 拓真）が差し戻し案件の加筆・修正を自律実行中...", expanded=True) as status_box:
            for rev_a in cc_rev_articles:
                st.write(f"✍️ 『{clean_txt(rev_a.get('title'))}』の加筆・修正を実施中...")
                workflow.auto_revise_and_forward_to_qa(rev_a["id"], rev_a.get("latest_feedback", "ブラッシュアップ"), target_dept="content_creation")
            status_box.update(label="✅ **社内ルール【Rule-OPS-AUTO】**: 全案件の加筆・修正が完了し、品質管理課へ自動再送付しました！", state="complete")
        st.success("🎉 記事制作課での加筆・修正が自律完了し、社内ルール【Rule-OPS-AUTO】に基づき品質管理課へ自動再送付されました。")
        st.rerun()

    auto_started = st.session_state.get("auto_start_creation", False)
    if auto_started:
        st.session_state.auto_start_creation = False

    if st.session_state.prefill_topic:
        if auto_started:
            st.info(f"⚡ **企画承認に基づき、記事作成課が『{clean_txt(st.session_state.prefill_topic)}』の作成を自動開始しました。**" if lang=='ja' else f"⚡ **Topic approved! Article creation automatically initiated for '{clean_txt(st.session_state.prefill_topic)}'.**")
        else:
            st.success(f"📥 **市場調査課の申請承認に伴い、業務が自動移行しました:** 『{clean_txt(st.session_state.prefill_topic)}』\n\nターゲット読者と価格設定を確認の上、そのまま執筆を開始できます。")

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
        price_opts = [t("cc_price_opt_300", lang), t("cc_price_opt_500", lang), t("cc_price_opt_prem", lang), t("cc_price_opt_auto", lang)]
        price_input = st.selectbox(t("cc_price_label", lang), price_opts)
        st.write("")
        start_btn = st.button(t("cc_start_btn", lang), type="primary", use_container_width=True)

    if start_btn or auto_started:
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
                    status_text.markdown(f"⏳ **{clean_txt(event.get('message'))}**")
                elif event.get("status") == "done":
                    log = event.get("log", {})
                    with meeting_container:
                        st.markdown(f"""
                        <div class='chat-bubble'>
                            <div style='font-weight: 800; color: #FFFFFF;'>{log.get('icon')} {log.get('name')} <span style='font-size: 0.8rem; color: #94A3B8;'>({log.get('role')})</span></div>
                            <div style='white-space: pre-wrap; margin-top: 6px; font-size: 0.95rem; color: #F8FAFC;'>{clean_txt(log.get('content'))}</div>
                        </div>
                        """, unsafe_allow_html=True)
                elif event.get("status") == "completed":
                    completed_article = event.get("article")
                    progress_bar.progress(1.0)
                    status_text.markdown("🔒 **全工程完了！社内ルール【Rule-OPS-AUTO】に基づき、品質管理課へ自動送付しています...**")
            
            if completed_article:
                st.session_state.prefill_topic = ""
                st.session_state.prefill_audience = ""
                st.session_state.auto_start_creation = False
                st.session_state.auto_transferred_to_qa = True
                st.session_state.qa_selected_art_id = completed_article["id"]
                st.session_state.just_sent_to_qa_title = clean_txt(completed_article["title"])
                st.session_state.active_page_id = "qa"
                st.session_state.scroll_trigger += 1
                st.rerun()

# ==========================================
# 5. 📢 Public Relations Division
# ==========================================
elif page_id == "pr":
    st.markdown(f"<div class='main-header'>{t('pr_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('pr_sub', lang)}</div>", unsafe_allow_html=True)

    # Rule-OPS-AUTO: 品質管理課から広報課へ差し戻された案件の自動プロモーション改定と品質管理課への自動再送付
    pr_rev_articles = [a for a in workflow.list_articles() if a.get("status") == "Revision Requested" and a.get("routed_dept") == "pr"]
    if pr_rev_articles:
        with st.status("⚡ **社内ルール【Rule-OPS-AUTO】**: 広報課（佐々木 翼）が差し戻し案件の5大SNSプロモーション改定を自律実行中...", expanded=True) as status_box:
            for rev_a in pr_rev_articles:
                st.write(f"📢 『{clean_txt(rev_a.get('title'))}』のSNSプロモーション文を改定中...")
                workflow.auto_revise_and_forward_to_qa(rev_a["id"], rev_a.get("latest_feedback", "SNSプロモーション改定"), target_dept="pr")
            status_box.update(label="✅ **社内ルール【Rule-OPS-AUTO】**: SNSプロモーション改定が完了し、品質管理課へ自動再送付しました！", state="complete")
        st.success("🎉 広報課でのプロモーション改定が自律完了し、社内ルール【Rule-OPS-AUTO】に基づき品質管理課へ自動再送付されました。")
        st.rerun()

    st.markdown(f"#### 📝 {'note公式販売アカウント設定 ＆ 投稿ハブ' if lang=='ja' else 'note Official Creator Account & Publishing Hub'}")
    cfg_path = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/sns_config.json")
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            sns_cfg = json.load(f)
    else:
        sns_cfg = {}
    
    note_cfg = sns_cfg.get("note", {})
    c_nt1, c_nt2 = st.columns([3, 2])
    with c_nt1:
        note_brand = st.text_input("🏢 note販売者名 / ブランド名", value=note_cfg.get("brand_name", "noteone"), help="会社法・商号規制に準拠した対外ブランド名")
        note_url = st.text_input("🔗 noteクリエイターページURL", value=note_cfg.get("creator_url", "https://note.com/noteone"), placeholder="https://note.com/あなたのnoteID")
    with c_nt2:
        note_id = st.text_input("🆔 noteクリエイターID", value=note_cfg.get("account_id", "noteone"), placeholder="あなたのnote ID")
        st.write("")
        st.link_button("🚀 note新規投稿画面を開く (note.com)", "https://note.com/notes/new", use_container_width=True)

    st.caption("🛡️ **投稿手順**: 承認済み記事の「Markdown Source」をコピーし、上記ボタンから開くnote投稿画面に貼り付けて有料ラインを設定してください。")

    st.markdown("---")
    st.markdown(f"#### 📢 {'5大SNSマルチプロモーション設定' if lang=='ja' else '5 Major SNS Syndication Settings'}")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        x_acc = st.text_input("🐦 X (Twitter) Account", value=sns_cfg.get("x", {}).get("account_name", "@NoteOneSystems"))
        ig_acc = st.text_input("📸 Instagram Profile", value=sns_cfg.get("instagram", {}).get("account_name", "@noteonesystems_official"))
        th_acc = st.text_input("🧵 Threads Username", value=sns_cfg.get("threads", {}).get("account_name", "@noteonesystems_official"))
    with col_s2:
        bs_handle = st.text_input("🦋 Bluesky Handle", value=sns_cfg.get("bluesky", {}).get("handle", "noteonesystems.bsky.social"))
        mast_inst = st.text_input("🐘 Mastodon Instance URL", value=sns_cfg.get("mastodon", {}).get("instance", "https://mstdn.jp"))
    
    if st.button(t("pr_save_btn", lang), type="primary"):
        sns_cfg["note"] = {
            "brand_name": note_brand,
            "creator_url": note_url,
            "account_id": note_id
        }
        sns_cfg["x"] = {"account_name": x_acc}
        sns_cfg["instagram"] = {"account_name": ig_acc}
        sns_cfg["threads"] = {"account_name": th_acc}
        sns_cfg["bluesky"] = {"handle": bs_handle}
        sns_cfg["mastodon"] = {"instance": mast_inst}
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(sns_cfg, f, ensure_ascii=False, indent=2)
        st.success("note販売アカウントおよび各SNSの設定を保存しました！" if lang == "ja" else "note account and social media configuration saved successfully.")

    # -------------------------------------------------------------
    # 📢 承認済み記事の5大SNS投稿文 ワンクリックコピーデスク
    # -------------------------------------------------------------
    st.markdown("---")
    st.markdown(f"#### 📢 {'承認済み記事の5大SNS投稿文 ワンクリックコピーデスク' if lang=='ja' else '5-Platform Promotional Copy Desk'}")
    st.markdown(f"<div style='color: #94A3B8; font-size: 0.88rem; margin-bottom: 14px;'>{'広報課（佐々木 翼）が作成した各SNS向けプロモーション文です。ワンクリックでコピーして各SNSへの告知投稿に活用してください。' if lang=='ja' else 'Syndicated promotional copies generated by PR Specialist Tsubasa Sasaki. Copy and paste directly into your social platforms.'}</div>", unsafe_allow_html=True)

    pr_approved_articles = [a for a in workflow.list_articles() if a.get("status") in ["Approved", "Published"]]
    if not pr_approved_articles:
        st.info("💡 承認済みの記事がまだありません。品質管理課または全社統合決裁センターで記事を承認すると、ここに5大SNS投稿文が表示されます。" if lang == "ja" else "No approved articles yet.")
    else:
        pr_art_titles = [f"[{a.get('article_no', 'No.01')}] {clean_txt(a.get('title', ''))}" for a in pr_approved_articles]
        sel_pr_art_idx = st.selectbox("📢 プロモーション文を表示する承認済み記事を選択:", range(len(pr_approved_articles)), format_func=lambda x: pr_art_titles[x], key="pr_art_selector")
        target_pr_art = pr_approved_articles[sel_pr_art_idx]

        pr_marketing_raw = clean_txt(target_pr_art.get("marketing", ""))

        def extract_pr_text(raw, key):
            parts = raw.split("【")
            for p in parts:
                if not p.strip():
                    continue
                if key.lower() in p.lower():
                    lines = ("【" + p.strip()).split("\n", 1)
                    return lines[1].strip() if len(lines) > 1 else lines[0].strip()
            return ""

        x_text = extract_pr_text(pr_marketing_raw, "X (Twitter)") or pr_marketing_raw
        ig_text = extract_pr_text(pr_marketing_raw, "Instagram") or pr_marketing_raw
        th_text = extract_pr_text(pr_marketing_raw, "Threads") or pr_marketing_raw
        bs_text = extract_pr_text(pr_marketing_raw, "Bluesky") or pr_marketing_raw
        mast_text = extract_pr_text(pr_marketing_raw, "Mastodon") or pr_marketing_raw

        pr_tabs = st.tabs([
            "🐦 X (Twitter)",
            "📸 Instagram",
            "🧵 Threads",
            "🦋 Bluesky",
            "🐘 Mastodon",
            "📋 全文一括表示"
        ])
        with pr_tabs[0]:
            st.caption("🐦 **X (Twitter) 向け短文告知ポスト**")
            st.text_area("X投稿文", value=x_text, height=140, key=f"copy_x_{target_pr_art['id']}")
        with pr_tabs[1]:
            st.caption("📸 **Instagram カルーセルスライド構成 ＆ キャプション**")
            st.text_area("Instagram投稿文", value=ig_text, height=180, key=f"copy_ig_{target_pr_art['id']}")
        with pr_tabs[2]:
            st.caption("🧵 **Threads 思考ログ・ストーリー型ポスト**")
            st.text_area("Threads投稿文", value=th_text, height=140, key=f"copy_th_{target_pr_art['id']}")
        with pr_tabs[3]:
            st.caption("🦋 **Bluesky 要約告知ポスト**")
            st.text_area("Bluesky投稿文", value=bs_text, height=140, key=f"copy_bs_{target_pr_art['id']}")
        with pr_tabs[4]:
            st.caption("🐘 **Mastodon トピック告知ポスト**")
            st.text_area("Mastodon投稿文", value=mast_text, height=140, key=f"copy_mast_{target_pr_art['id']}")
        with pr_tabs[5]:
            st.caption("📋 **5大SNSプロモーションパッケージ 全文**")
            st.text_area("全文", value=pr_marketing_raw, height=260, key=f"copy_all_{target_pr_art['id']}")

# ==========================================
# 6. ✨ Quality Assurance Division
# ==========================================
elif page_id == "qa":
    st.markdown(f"<div class='main-header'>{t('qa_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('qa_sub', lang)}</div>", unsafe_allow_html=True)

    if st.session_state.get("auto_transferred_to_qa"):
        st.session_state.auto_transferred_to_qa = False
        st.html(f"""
        <div style="background: linear-gradient(135deg, #091E19 0%, #0F172A 100%); border: 1.5px solid #10B981; border-radius: 12px; padding: 16px 20px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(16, 185, 129, 0.25);">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 1.8rem;">🚀</span>
                <div>
                    <div style="color: #6EE7B7; font-weight: 800; font-size: 1.05rem;">
                        【Rule-OPS-AUTO 自動連携】記事作成課（結城 紬・森川 拓真）より自動送付されました
                    </div>
                    <div style="color: #E2E8F0; font-size: 0.9rem; margin-top: 4px;">
                        対象記事: <strong>『{st.session_state.get('just_sent_to_qa_title', '')}』</strong> の執筆が完了し、品質管理課（神崎 玲奈）へ自動引き渡しされました。内容を査読の上、承認または否認（担当課への差し戻し）を行ってください。
                    </div>
                </div>
            </div>
        </div>
        """)

    # Rule-OPS-AUTO 規程バナー表示
    qa_rule_title = "社内業務連携規程【Rule-OPS-AUTO: 3課自律連携・品質管理ルーティング規程】" if lang == "ja" else "Operational Protocol [Rule-OPS-AUTO: 3-Division Autonomous Hand-off & Routing]"
    qa_rule_sub = "制定: 統括役員室 / 所管: note ONE システムズ全課 / 目的: 完全自動化パイプライン及び厳格な品質管理"
    st.html(f"""
    <div style="background: linear-gradient(135deg, #091E19 0%, #0F172A 100%); border: 1.5px solid #10B981; border-radius: 12px; padding: 18px 22px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15); box-sizing: border-box; width: 100%;">
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 14px; border-bottom: 1px solid rgba(16, 185, 129, 0.25); padding-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 10px; min-width: 260px; flex: 1;">
                <span style="font-size: 1.4rem;">📜</span>
                <div>
                    <div style="color: #6EE7B7; font-size: 1.08rem; font-weight: 800; letter-spacing: 0.02em; line-height: 1.4;">
                        {qa_rule_title}
                    </div>
                    <div style="color: #94A3B8; font-size: 0.8rem; margin-top: 2px;">
                        {qa_rule_sub}
                    </div>
                </div>
            </div>
            <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px;">
                <span style="background: rgba(16, 185, 129, 0.18); color: #6EE7B7; border: 1px solid #10B981; font-weight: 800; font-size: 0.82rem; padding: 4px 12px; border-radius: 20px; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap;">
                    <span style="display: inline-block; width: 7px; height: 7px; background: #10B981; border-radius: 50%; box-shadow: 0 0 6px #10B981;"></span>
                    社内規程施行中
                </span>
                <span style="background: #10B981; color: #022C22; font-weight: 900; font-size: 0.84rem; padding: 4px 12px; border-radius: 20px; white-space: nowrap; box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);">
                    自律連携パイプライン
                </span>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px;">
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 8px; padding: 12px 14px;">
                <div style="color: #38BDF8; font-weight: 800; font-size: 0.88rem;">1️⃣ 市場調査課 ➔ 記事作成課 (自動移行)</div>
                <div style="color: #CBD5E1; font-size: 0.82rem; margin-top: 4px; line-height: 1.5;">市場調査課で企画承認された案件は、追加ボタン操作不要で自動的に記事作成課へ引き渡され、即時執筆を開始します。</div>
            </div>
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 8px; padding: 12px 14px;">
                <div style="color: #34D399; font-weight: 800; font-size: 0.88rem;">2️⃣ 記事作成課 ➔ 品質管理課 (自動送付)</div>
                <div style="color: #CBD5E1; font-size: 0.82rem; margin-top: 4px; line-height: 1.5;">記事作成課での執筆・推敲・リーガルチェック完了後、自動で品質管理課へ仕事が送付され、査読画面へ遷移します。</div>
            </div>
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(245, 158, 11, 0.35); border-radius: 8px; padding: 12px 14px;">
                <div style="color: #FBBF24; font-weight: 800; font-size: 0.88rem;">3️⃣ 品質管理課 ➔ 3課ルーティング (否認時)</div>
                <div style="color: #CBD5E1; font-size: 0.82rem; margin-top: 4px; line-height: 1.5;">品質管理課で否認された場合、指摘内容に応じて【市場調査課】【記事制作課】【広報課】を選択して送付します。</div>
            </div>
        </div>
    </div>
    """)

    all_articles = workflow.list_articles()
    
    if not all_articles:
        st.info(t("qa_no_articles", lang))
    else:
        selected_idx = 0
        if st.session_state.get("qa_selected_art_id"):
            for idx, art_item in enumerate(all_articles):
                if art_item.get("id") == st.session_state.qa_selected_art_id:
                    selected_idx = idx
                    break

        article_titles = [f"[{art.get('article_no', f'No.{idx+1:02d}')}] [{art.get('status', 'Pending Owner Approval')}] {clean_txt(art.get('title', ''))}" for idx, art in enumerate(all_articles)]
        selected_idx = st.selectbox(t("qa_select_label", lang), range(len(all_articles)), index=selected_idx, format_func=lambda x: article_titles[x])
        art = all_articles[selected_idx]
        cur_status = art.get("status", "Pending Owner Approval")
        is_locked = cur_status in ["Pending Owner Approval", "Revision Requested"]

        # 📄 査読エリア（st.htmlによる完全クリーンレンダリング）
        st.html(get_article_dossier_html(art, lang))

        # 👑 オーナー決裁欄（プレビューの直後に配置）
        st.markdown("---")
        st.markdown(f"<div class='section-title'>{t('qa_approval_header', lang)}</div>", unsafe_allow_html=True)

        # 💰 価格変更ウィジェット
        cur_qa_price = art.get("price", 300)
        c_qa_p1, c_qa_p2 = st.columns([3, 1])
        with c_qa_p1:
            qa_new_price = st.number_input(
                "💰 販売価格の変更・調整 (note販売価格):",
                min_value=100,
                max_value=50000,
                value=int(cur_qa_price),
                step=50,
                key=f"qa_price_input_{art['id']}",
                help="noteでの販売価格（100円〜50,000円）を設定できます。売上目標や財務試算に即時反映されます。"
            )
        with c_qa_p2:
            st.write("")
            if st.button("💾 価格を更新", key=f"qa_price_btn_{art['id']}", use_container_width=True):
                workflow.update_article_price(art["id"], qa_new_price)
                st.success(f"販売価格を ¥{qa_new_price:,} に更新しました！")
                st.rerun()

        if is_locked:
            st.markdown(f"""
            <div class='approval-box-locked'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <h3 style='color: #FCD34D !important; margin:0;'>🔒 Status: {cur_status}</h3>
                    <span style='background:#F59E0B; color:#000; font-weight:800; padding:4px 10px; border-radius:6px;'>{'決裁待ち' if lang=='ja' else 'Pending'}</span>
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
                    <span style='background:#10B981; color:#000; font-weight:800; padding:4px 10px; border-radius:6px;'>{'承認済み' if lang=='ja' else 'Approved'}</span>
                </div>
                <div style='margin-top: 10px; font-size: 0.95rem; line-height: 1.6;'>
                    {t('qa_unlocked_success', lang)}
                </div>
            </div>
            """, unsafe_allow_html=True)

        if is_locked:
            app_col1, app_col2, app_col3 = st.columns([2, 2, 1])
            with app_col1:
                if st.button("承認", type="primary", use_container_width=True, key="qa_btn_app_main"):
                    workflow.approve_article(art["id"])
                    st.success("🎉 オーナー最終承認が完了し、投稿ロックを解除しました！" if lang == "ja" else "🎉 Approved by owner! Publishing lock has been released.")
                    st.rerun()

            with app_col2:
                if st.button("✍️ 否認", use_container_width=True, key="qa_toggle_art_rev"):
                    st.session_state.show_qa_art_rev = not st.session_state.show_qa_art_rev
                    st.rerun()

            with app_col3:
                if st.button("拒否", use_container_width=True, key="qa_btn_rej_main"):
                    workflow.reject_article(art["id"])
                    st.info("記事を拒否（却下・アーカイブ）しました。" if lang == "ja" else "Article rejected and archived.")
                    st.rerun()

            if st.session_state.show_qa_art_rev:
                with st.container():
                    st.markdown(f"#### ✍️ {'否認・修正指示の入力（社内ルール【Rule-OPS-AUTO】ルーティング）' if lang=='ja' else 'Article Revision Directives'}")
                    with st.form("qa_page_article_revision_form", clear_on_submit=True):
                        target_dept_choice = st.radio(
                            "🎯 差し戻し・業務送付先を選択してください（社内ルール）:",
                            options=["content_creation", "market_research", "pr"],
                            format_func=lambda x: {
                                "content_creation": "✍️ 記事制作課（結城 紬 & 森川 拓真）- 構成案・執筆・有料テンプレートの再修正",
                                "market_research": "🔍 市場調査課（風間 涼）- ターゲット読者層・市場ニーズ・競合ギャップの再調査",
                                "pr": "📢 広報課（佐々木 翼）- 5大SNSプロモーション文・キャッチコピーの再考"
                            }.get(x, x),
                            index=0,
                            help="品質管理課での否認時、修正が必要な専門部署を選択してタスクを自動ルーティングします。"
                        )
                        feedback_txt = st.text_area(t("qa_feedback_label", lang), placeholder="例: ターゲット層のペルソナが曖昧なため、20代若手社員向けにニーズを再調査してください / 有料部分のテンプレート実例をもう1つ追加してください。", key="qa_rev_main_fb")
                        submit_qa_rev = st.form_submit_button("📨 否認指示を送信し、指定課へ送付する", type="primary", use_container_width=True)
                        if submit_qa_rev:
                            if feedback_txt.strip():
                                workflow.request_revision(art["id"], feedback_txt, target_dept=target_dept_choice)
                                workflow.auto_revise_and_forward_to_qa(art["id"], feedback_txt, target_dept=target_dept_choice)
                                st.session_state.show_qa_art_rev = False
                                target_name_map = {
                                    "content_creation": "記事制作課（結城・森川）",
                                    "market_research": "市場調査課（風間）",
                                    "pr": "広報課（佐々木）"
                                }
                                st.success(f"🎉 社内ルール【Rule-OPS-AUTO】に基づき、{target_name_map.get(target_dept_choice)}がご指摘に基づき加筆・修正を自律完了し、品質管理課へ自動で再送付しました！")
                                st.rerun()
                            else:
                                st.error("修正指示内容を入力してください。")
        else:
            st.info("💡 この記事は既にオーナー承認済みです。広報課（PR）またはnote本番環境への展開準備が完了しています。" if lang == "ja" else "💡 This article is already approved. Ready for PR promotion and note publishing.")

        st.markdown("---")

        st.markdown(f"##### {t('qa_history_title', lang)}")
        history = art.get("status_history", [])
        for h in reversed(history):
            note_str = f" - <em>{clean_txt(h.get('note'))}</em>" if h.get('note') else ""
            st.markdown(f"- 🕒 **{h.get('timestamp')}** ➔ `[{h.get('status')}]` ({clean_txt(h.get('actor', ''))}){note_str}", unsafe_allow_html=True)
        
        st.divider()

        st.markdown(f"#### {t('qa_markdown_title', lang)}")
        if is_locked:
            st.warning("🔒 【ロック中】オーナー承認が出るまでnoteへの貼り付けコードは保護されています。")
            st.code("🔒 LOCKED: Awaiting Owner Final Approval (承認ボタンを押すとロックが解除されます)", language="text")
        else:
            st.success("✅ 【ロック解除済】以下のマークダウンをnoteの記事エディタにそのまま貼り付けて公開できます！")
            st.text_area("Markdown Source (note editor ready)", value=clean_content, height=300, key="qa_md_source_main")

# ==========================================
# 7. 🤝 Human Resources Division
# ==========================================
elif page_id == "hr":
    st.markdown(f"<div class='main-header'>{t('hr_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('hr_sub', lang)}</div>", unsafe_allow_html=True)

    # 📄 Departmental Document Link
    org_file = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/org_chart_and_job_descriptions.json")
    if os.path.exists(org_file):
        with open(org_file, "r", encoding="utf-8") as f:
            org_data = json.load(f)
    else:
        org_data = {"departments": []}

    with st.expander(f"📄 {'社内文書: 組織体制図 ＆ 詳細職務分掌規程 (Ver 1.0 正式運用版)' if lang=='ja' else 'Internal Document: Org Chart & Job Descriptions (Ver 1.0)'}", expanded=False):
        st.write(f"**{'制定者:' if lang=='ja' else 'Authorized by:'}** {org_data.get('author')} | **{'バージョン:' if lang=='ja' else 'Version:'}** {org_data.get('version')} | **{'施行日:' if lang=='ja' else 'Effective:'}** {org_data.get('effective_date')}")
        for dept in org_data.get("departments", []):
            st.markdown(f"**{dept['icon']} {dept['name']}** ({'統括:' if lang=='ja' else 'Lead:'} {dept['head']})")
            for role in dept.get("roles", []):
                st.write(f"- **{role['role_name']} ({role['member']})**: {', '.join(role['responsibilities'][:2])}")

    st.markdown("---")
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
        st.markdown(f"#### 🚨 {'過負荷検知 ＆ 社内増員提案（即時雇用承認デスク）' if lang=='ja' else 'Overload Detection & Staffing Proposals (Instant Approval)'}")
        st.markdown(f"<div style='color: #94A3B8; font-size: 0.88rem; margin-bottom: 12px;'>{'綾瀬人事責任者が社員の業務負荷を常時検知し、ボトルネック解消のための増員を起案しています。オーナー承認により即時配属（費用0円）され、過負荷が緩和されます。' if lang=='ja' else 'HR detected elevated workload and proposed autonomous AI reinforcement. Approval executes 0-cost onboarding.'}</div>", unsafe_allow_html=True)
        for prop in proposals:
            with st.container():
                st.markdown(f"""
                <div style='background: #1E293B; border: 1px solid #F59E0B; border-left: 5px solid #F59E0B; border-radius: 8px; padding: 14px; margin-bottom: 12px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <strong style='color: #F59E0B; font-size: 1.05rem;'>⚡ 【増員提案】{prop['target_role']}（{prop['target_name']}）の業務負荷: {prop['workload_score']}%</strong>
                        </div>
                        <span style='background: #0F172A; color: #10B981; font-weight: 700; font-size: 0.8rem; padding: 3px 8px; border-radius: 4px; border: 1px solid #10B981;'>
                            費用: {prop['cost']}
                        </span>
                    </div>
                    <div style='margin-top: 8px; color: #E2E8F0; font-size: 0.9rem; line-height: 1.5;'>
                        {prop['reason']}
                    </div>
                    <div style='margin-top: 8px; color: #38BDF8; font-size: 0.88rem;'>
                        👤 <strong>推薦配属候補:</strong> {prop['recommended_candidate']}（{prop['proposed_role']}）
                    </div>
                </div>
                """, unsafe_allow_html=True)
                c_pr1, c_pr2 = st.columns([3, 2])
                with c_pr2:
                    if st.button(f"🤝 この増員提案を承認して即時雇用する (0円)", key=f"btn_hire_prop_{prop['id']}", use_container_width=True, type="primary"):
                        try:
                            hired_emp = st.session_state.hr_manager.hire_from_proposal(prop["id"])
                            emp_name = hired_emp.get("name", prop.get("recommended_candidate", "新規AI社員")) if isinstance(hired_emp, dict) else prop.get("recommended_candidate", "新規AI社員")
                            emp_role = hired_emp.get("role", prop.get("proposed_role", "")) if isinstance(hired_emp, dict) else prop.get("proposed_role", "")
                            st.balloons()
                            st.success(f"🎉 新規AI社員【{emp_name}（{emp_role}）】を正式雇用・配属しました！（費用0円）\n{prop['target_name']}の業務負荷スコアが半減しました。")
                            st.rerun()
                        except Exception as e:
                            st.error(f"雇用処理エラー: {e}")

    # 🚪 AI社員 在籍管理 ＆ 解雇・オフボーディングデスク
    st.markdown("---")
    st.markdown(f"#### 🚪 {'AI社員 在籍管理 ＆ 解雇・オフボーディングデスク' if lang=='ja' else 'AI Employee Roster & Offboarding Desk'}")
    st.markdown(f"<div style='color: #94A3B8; font-size: 0.88rem; margin-bottom: 14px;'>{'【就業規則 第18条】に基づき、代表者（オーナー）は増員したAI社員を即時かつ0円（退職金・手当なし）で解雇（オフボーディング）できます。解雇されたAI社員は直ちに2Dオフィス、相談デスク、社内名簿から退場します。<br>※基幹コア社員（創業9名）は会社の自律執筆・品質保証パイプラインのシステム保全のため解雇不可（保護対象）となっています。' if lang=='ja' else 'Under Article 18, the owner can offboard supplementary AI employees at 0 cost. Core 9 members are protected.'}</div>", unsafe_allow_html=True)

    comp_info_path = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/company_info.json")
    cur_employees = []
    if os.path.exists(comp_info_path):
        with open(comp_info_path, "r", encoding="utf-8") as f:
            cur_employees = json.load(f).get("employees", [])

    for emp in cur_employees:
        e_id = emp["id"]
        e_name = emp["name"]
        e_role = emp.get("role", "AI社員")
        e_icon = emp.get("icon", "👤")
        e_dept = emp.get("department", "事業部")
        is_core = not st.session_state.hr_manager.is_offboardable(e_id)

        col_info, col_act = st.columns([4, 1.5])
        with col_info:
            status_badge = "<span style='background: #1E3A8A; color: #93C5FD; font-size: 0.78rem; padding: 2px 8px; border-radius: 4px; border: 1px solid #3B82F6;'>🛡️ 基幹コア社員 (保護対象)</span>" if is_core else "<span style='background: #064E3B; color: #34D399; font-size: 0.78rem; padding: 2px 8px; border-radius: 4px; border: 1px solid #10B981;'>🤝 増員AI社員 (解雇可能)</span>"
            st.markdown(f"""
            <div style='background: #0F172A; border: 1px solid #334155; border-radius: 6px; padding: 8px 12px; margin-bottom: 6px;'>
                <span style='font-size: 1.1rem;'>{e_icon}</span>
                <strong style='color: #F8FAFC; margin-left: 6px;'>{e_name}</strong>
                <span style='color: #94A3B8; font-size: 0.85rem; margin-left: 8px;'>（{e_role} / {e_dept}）</span>
                <span style='margin-left: 10px;'>{status_badge}</span>
            </div>
            """, unsafe_allow_html=True)
        with col_act:
            st.write("")
            if is_core:
                st.button("🔒 解雇不可 (コア保護)", key=f"btn_offboard_disabled_{e_id}", disabled=True, use_container_width=True)
            else:
                if st.button(f"❌ 解雇・オフボーディング (0円)", key=f"btn_offboard_{e_id}", type="secondary", use_container_width=True):
                    try:
                        record = st.session_state.hr_manager.offboard_employee(e_id, reason="代表者の経営判断による人員整理")
                        r_name = record.get("name", e_id) if isinstance(record, dict) else e_id
                        r_role = record.get("role", "") if isinstance(record, dict) else ""
                        st.warning(f"🚪 AI社員【{r_name}（{r_role}）】を解雇・オフボーディングしました（費用0円）。\n2Dオフィスから退場し、全社名簿から抹消されました。")
                        st.rerun()
                    except Exception as e:
                        st.error(f"オフボーディング処理エラー: {e}")

    # 🤝 新規AI社員 募集・採用管理デスク
    st.markdown("---")
    st.markdown(f"#### 🤝 {'新規AI専門社員 募集・採用管理デスク (即時雇用・費用0円)' if lang=='ja' else 'AI Employee Recruitment & Onboarding Desk (Zero Cost)'}")
    st.markdown(f"<div style='color: #94A3B8; font-size: 0.88rem; margin-bottom: 14px;'>{'オーナーの経営判断により、事業拡大や特定業務補佐のためのAIスペシャリストを即座に雇用・配属できます。完全無料API枠・純Python設計のため、何名採用しても追加費用は永久に0円です。' if lang=='ja' else 'Deploy specialized AI agents on-demand with zero additional marginal cost.'}</div>", unsafe_allow_html=True)

    presets = st.session_state.hr_manager.get_candidate_presets(include_hired=False)
    preset_count = len(presets)
    preset_tab_title = f"🎯 人事課おすすめの即戦力スペシャリスト (未採用{preset_count}名)" if preset_count > 0 else "🎯 人事課おすすめの即戦力スペシャリスト (全員採用済み)"
    if lang != 'ja':
        preset_tab_title = f"🎯 Recommended Specialists ({preset_count} Available)" if preset_count > 0 else "🎯 Recommended Specialists (All Hired)"

    tab_preset, tab_scout, tab_custom = st.tabs([
        preset_tab_title,
        "🗣️ 綾瀬七海への採用オーダー（AIスカウト）" if lang=="ja" else "🗣️ Scout Order Desk",
        "✍️ オーナー自由指定 採用フォーム (完全カスタムAI社員)" if lang=="ja" else "✍️ Custom Recruitment Form"
    ])

    with tab_preset:
        if not presets:
            st.markdown(f"""
            <div style='background: #0F172A; border: 1px solid #10B981; border-radius: 8px; padding: 18px; text-align: center; margin-bottom: 14px;'>
                <div style='font-size: 1.25rem; margin-bottom: 8px; color: #10B981;'>🎉 <strong>おすすめ即戦力スペシャリストは全員採用・配属済みです！</strong></div>
                <div style='color: #E2E8F0; font-size: 0.9rem; line-height: 1.6;'>
                    現在、人事課が推薦する即戦力AI社員（桐生 蓮、美咲 華、早乙女 律花、桜井 葵、白河 結月 等）はすべて雇用され、各部署および2Dオフィスフロアでフル稼働しています。<br>
                    現在の在籍状況の確認やオフボーディング（解雇・0円）は上部の「🚪 AI社員 在籍管理デスク」から行えます。<br>
                    別領域のAI社員をさらに増員したい場合は、隣の「🗣️ 綾瀬七海への採用オーダー」または「✍️ 自由指定 採用フォーム」より自由な役職名・スキルで何名でも即時採用（永久0円）可能です。
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for idx, cand in enumerate(presets):
                c_card, c_btn = st.columns([3, 1])
                with c_card:
                    st.markdown(f"""
                    <div style='background: #0F172A; border: 1px solid #334155; border-left: 4px solid {cand["color"]}; border-radius: 8px; padding: 12px; margin-bottom: 10px;'>
                        <div style='display: flex; justify-content: space-between;'>
                            <div>
                                <span style='font-size: 1.2rem;'>{cand["icon"]}</span>
                                <strong style='color: #FFFFFF; font-size: 1.05rem; margin-left: 6px;'>{cand["name"]}</strong>
                                <span style='color: #93C5FD; font-size: 0.85rem; margin-left: 8px;'>（{cand["role"]} / {cand["department"]}）</span>
                            </div>
                            <span style='color: #10B981; font-weight: 700; font-size: 0.8rem;'>費用: ¥0</span>
                        </div>
                        <div style='margin-top: 6px; color: #E2E8F0; font-size: 0.88rem;'>
                            <strong>モットー:</strong> <em>「{cand['motto']}」</em>
                        </div>
                        <div style='margin-top: 4px; color: #94A3B8; font-size: 0.82rem;'>
                            💡 <strong>採用メリット:</strong> {cand['recommendation_reason']}
                        </div>
                        <div style='margin-top: 4px; color: #64748B; font-size: 0.78rem;'>
                            🛠️ スキル: {', '.join(cand['skills'])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with c_btn:
                    st.write("")
                    if st.button(f"🤝 採用する (0円)", key=f"btn_hire_preset_{cand['id']}_{idx}", use_container_width=True, type="primary"):
                        try:
                            hired_emp = st.session_state.hr_manager.hire_employee(cand)
                            emp_name = hired_emp.get("name", cand.get("name", "新規AI社員")) if isinstance(hired_emp, dict) else cand.get("name", "新規AI社員")
                            emp_role = hired_emp.get("role", cand.get("role", "")) if isinstance(hired_emp, dict) else cand.get("role", "")
                            st.balloons()
                            st.success(f"🎉 新規AI社員【{emp_name}（{emp_role}）】を正式雇用・配属しました！（費用0円）")
                            st.rerun()
                        except Exception as e:
                            st.error(f"雇用処理エラー: {e}")

    with tab_scout:
        st.markdown(f"##### {'🗣️ 綾瀬七海（人事責任者）への採用オーダーデスク' if lang=='ja' else '🗣️ AI Scout Order Desk'}")
        st.markdown(f"<div style='color: #94A3B8; font-size: 0.88rem; margin-bottom: 12px;'>{'「女性ライターを雇いたい」「読者の共感を呼ぶ女性ストーリーテラー」「ノウハウ図解ライター」など、欲しい人材のイメージを伝えるだけで、綾瀬七海が即座に社内規程に適合するスペシャリストをスカウト・選考し、候補者プロファイルを作成します。' if lang=='ja' else 'Tell HR what kind of agent you want, and Ayase will scout and prepare them for instant onboarding.'}</div>", unsafe_allow_html=True)
        
        c_sc1, c_sc2 = st.columns([4, 1])
        with c_sc1:
            order_query = st.text_input(
                "採用したいAI社員のイメージ・条件（自由入力）",
                placeholder="例: 女性ライターを雇いたい / 読者の共感を呼ぶ女性執筆者 / ノウハウ図解ライター",
                key="input_hr_scout_order"
            )
        with c_sc2:
            st.write("")
            btn_do_scout = st.button("🔍 スカウト依頼", key="btn_exec_scout", type="primary", use_container_width=True)

        if btn_do_scout and order_query.strip():
            with st.spinner("綾瀬七海が条件に適合するAI社員をスカウト中..."):
                scouted_res = st.session_state.hr_manager.scout_custom_candidate(
                    order_query,
                    ai_client=st.session_state.ai_client
                )
                st.session_state.last_scouted_candidate = scouted_res

        if st.session_state.get("last_scouted_candidate"):
            sc = st.session_state.last_scouted_candidate
            st.markdown(f"""
            <div style='background: #0F172A; border: 2px solid {sc.get("color", "#F43F5E")}; border-radius: 8px; padding: 14px; margin-top: 10px; margin-bottom: 12px;'>
                <div style='display: flex; justify-content: space-between;'>
                    <div>
                        <span style='font-size: 1.4rem;'>{sc.get("icon", "👩‍💻")}</span>
                        <strong style='color: #FFFFFF; font-size: 1.1rem; margin-left: 8px;'>{sc.get("name", "スカウト候補")}</strong>
                        <span style='color: #93C5FD; font-size: 0.88rem; margin-left: 8px;'>（{sc.get("role", "")} / {sc.get("department", "")}）</span>
                    </div>
                    <span style='color: #10B981; font-weight: 700; font-size: 0.85rem;'>スカウト費用: ¥0</span>
                </div>
                <div style='margin-top: 8px; color: #E2E8F0; font-size: 0.9rem;'>
                    <strong>モットー:</strong> <em>「{sc.get("motto", "")}」</em>
                </div>
                <div style='margin-top: 6px; color: #38BDF8; font-size: 0.85rem;'>
                    💡 <strong>綾瀬七海の選考・推薦理由:</strong> {sc.get("recommendation_reason", "")}
                </div>
                <div style='margin-top: 6px; color: #94A3B8; font-size: 0.82rem;'>
                    🛠️ スキル: {', '.join(sc.get("skills", []))}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🤝 【{sc.get('name')}】を正式雇用してオフィスに連れてくる (0円)", key="btn_hire_scouted", type="primary", use_container_width=True):
                try:
                    hired_emp = st.session_state.hr_manager.hire_employee(sc)
                    st.session_state.last_scouted_candidate = None
                    st.balloons()
                    st.success(f"🎉 新規AI社員【{hired_emp.get('name')}（{hired_emp.get('role')}）】を正式雇用し、2Dオフィスフロアに配属しました！（費用0円）")
                    st.rerun()
                except Exception as e:
                    st.error(f"雇用処理エラー: {e}")

    with tab_custom:
        with st.form("form_custom_hire"):
            st.markdown(f"##### {'自由指定 AI社員採用スペック策定' if lang=='ja' else 'Custom AI Employee Specifications'}")
            col_h1, col_h2 = st.columns(2)
            with col_h1:
                custom_name = st.text_input("社員名 (氏名)", placeholder="例: 桐生 蓮 / 桜井 葵")
                custom_role = st.text_input("役職名", placeholder="例: TikTok動画プロモーター / GAS自動化エンジニア")
                dept_choices = [
                    "コンテンツ制作本部",
                    "マーケティング・リサーチ本部",
                    "広報・宣伝本部",
                    "経営企画本部",
                    "内部統制・ガバナンス本部",
                    "財務・経理統括本部"
                ]
                custom_dept = st.selectbox("配属部署", dept_choices)
            with col_h2:
                custom_icon = st.text_input("アイコン (絵文字)", value="👤", help="Slack風の社員アイコン（絵文字1字）")
                custom_motto = st.text_input("プロフェッショナルモットー", placeholder="例: 迅速丁寧な作業で読者に最高の価値を届けます。")
                custom_skills = st.text_input("主要スキル (カンマ区切り)", placeholder="例: ショート動画台本制作, トレンド分析, リライト")

            custom_prompt = st.text_area(
                "システムプロンプト (行動規範・役割定義)",
                placeholder="あなたはNoteOneSystems株式会社の専門AI社員です。...",
                height=100
            )

            submit_custom_hire = st.form_submit_button("🤝 この内容でAI社員を雇用・配属する (費用0円)", type="primary", use_container_width=True)
            if submit_custom_hire:
                if custom_name.strip() and custom_role.strip():
                    new_cand_data = {
                        "id": f"custom_{int(datetime.now().timestamp())}",
                        "name": custom_name.strip(),
                        "role": custom_role.strip(),
                        "icon": custom_icon.strip() or "👤",
                        "color": "#38BDF8",
                        "department": custom_dept,
                        "motto": custom_motto.strip() or "読者のために誠実に行動します。",
                        "skills": [s.strip() for s in custom_skills.split(",") if s.strip()] or ["業務迅速化"],
                        "prompt": custom_prompt.strip() or f"あなたはNoteOneSystems株式会社の{custom_role}『{custom_name}』です。"
                    }
                    try:
                        hired_emp = st.session_state.hr_manager.hire_employee(new_cand_data)
                        emp_name = hired_emp.get("name", new_cand_data.get("name", "新規AI社員")) if isinstance(hired_emp, dict) else new_cand_data.get("name", "新規AI社員")
                        emp_role = hired_emp.get("role", new_cand_data.get("role", "")) if isinstance(hired_emp, dict) else new_cand_data.get("role", "")
                        st.balloons()
                        st.success(f"🎉 新規AI社員【{emp_name}（{emp_role}）】を正式雇用・配属しました！（費用0円）")
                        st.rerun()
                    except Exception as e:
                        st.error(f"雇用処理エラー: {e}")
                else:
                    st.error("社員名と役職名は必須入力です。")

    hiring_history = st.session_state.hr_manager.get_hiring_history()
    if hiring_history:
        st.markdown("---")
        st.markdown(f"#### 📜 {'AI社員 人事異動・雇用・解雇台帳 (全社公式記録)' if lang=='ja' else 'AI Employee Personnel, Hiring & Offboarding Ledger'}")
        ledger_df_data = []
        for h in reversed(hiring_history):
            action_label = h.get("action", "採用・配属")
            action_tag = "🚪 解雇・退場" if "解雇" in action_label else "🤝 採用・配属"
            ledger_df_data.append({
                "区分" if lang=="ja" else "Action": action_tag,
                "日時" if lang=="ja" else "Timestamp": h.get("timestamp"),
                "社員名" if lang=="ja" else "Name": f"{h.get('icon', '👤')} {h.get('name')}",
                "役職" if lang=="ja" else "Role": h.get("role"),
                "配属部署" if lang=="ja" else "Department": h.get("department"),
                "費用・手当" if lang=="ja" else "Cost/Severance": h.get("cost", "¥0"),
                "決裁者" if lang=="ja" else "Authorized By": h.get("authorized_by"),
                "異動・退場詳細" if lang=="ja" else "Details": h.get("impact")
            })
        st.dataframe(pd.DataFrame(ledger_df_data), use_container_width=True)

    st.markdown("---")
    # 📮 全社10万通り・社内目安箱（社員の本音ボヤキ＆関係性パトロール）
    st.markdown(f"#### 📮 {'社内目安箱・本音ボヤキ巡回デスク（全社9万通り・関係性パトロール）' if lang=='ja' else 'Internal Suggestion Box & Sentiment Patrol (90,000+ Combinations)'}")
    st.markdown(f"<div style='color: #94A3B8; margin-bottom: 12px;'>{'綾瀬人事責任者が各社員の現場の本音・他部署への不満・業務摩擦を吸い上げています（1人あたり10,000通りのユニークなボヤキからランダム抽出）。会社の業務フロー改善にお役立てください。' if lang=='ja' else 'Nanami Ayase gathers authentic sentiments, inter-departmental friction, and operational bottlenecks across all specialists.'}</div>", unsafe_allow_html=True)

    c_hr_btn1, c_hr_btn2 = st.columns([3, 1])
    with c_hr_btn2:
        if st.button("🔄 本音を吸い上げる (再巡回)", key="hr_btn_refresh_grumbles", use_container_width=True):
            st.rerun()

    from companies.note_one_systems.dialogue_engine import EmployeeDialogueEngine
    hr_engine = EmployeeDialogueEngine()

    emp_list = [
        {"id": "morikawa", "name": "森川 拓真", "role": "記事制作課 (ライター)", "icon": "✍️", "color": "#EA580C"},
        {"id": "yuki", "name": "結城 紬", "role": "記事制作課 (編集長)", "icon": "📑", "color": "#D97706"},
        {"id": "kanzaki", "name": "神崎 玲奈", "role": "品質管理課 (QA)", "icon": "🛡️", "color": "#DC2626"},
        {"id": "sasaki", "name": "佐々木 翼", "role": "広報課", "icon": "📢", "color": "#2563EB"},
        {"id": "tachibana", "name": "橘 律", "role": "法務コンプライアンス課", "icon": "⚖️", "color": "#475569"},
        {"id": "shiraishi", "name": "白石 葵", "role": "財務課 ＆ 経理課", "icon": "📊", "color": "#7C3AED"},
        {"id": "kazama", "name": "風間 涼", "role": "市場調査課", "icon": "🔍", "color": "#0D9488"},
        {"id": "ayase", "name": "綾瀬 七海", "role": "人事課", "icon": "🤝", "color": "#059669"},
        {"id": "ichijo", "name": "一条 蓮", "role": "代表取締役CEO", "icon": "👩‍💼", "color": "#1E3A8A"},
    ]

    for emp in emp_list:
        grumble_data = hr_engine.get_random_grumble(emp["id"], lang=lang)
        with st.container():
            st.markdown(f"""
            <div style='background: #0F172A; border: 1px solid #334155; border-left: 5px solid {emp["color"]}; border-radius: 8px; padding: 14px; margin-bottom: 12px;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <span style='font-size: 1.3rem;'>{emp["icon"]}</span>
                        <strong style='color: #FFFFFF; font-size: 1.05rem; margin-left: 6px;'>{emp["name"]}</strong>
                        <span style='color: #94A3B8; font-size: 0.85rem; margin-left: 8px;'>({emp["role"]})</span>
                    </div>
                    <span style='background: #1E293B; color: #38BDF8; font-size: 0.78rem; font-weight: 700; padding: 3px 8px; border-radius: 4px; border: 1px solid #334155;'>
                        パターン #{grumble_data['combination_id']:,} / 全{grumble_data['total_variations']:,}通り
                    </span>
                </div>
                <div style='margin-top: 6px; font-size: 0.82rem; color: #F59E0B;'>
                    ⚡ <strong>検知された摩擦対象:</strong> {grumble_data['target']}
                </div>
                <div style='margin-top: 8px; font-size: 0.95rem; color: #F8FAFC; background: #1E293B; padding: 10px 14px; border-radius: 6px; border-left: 3px solid #F43F5E; line-height: 1.6;'>
                    {grumble_data['text']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# 8. 📚 Legal & Compliance Division
# ==========================================
elif page_id == "legal":
    st.markdown(f"<div class='main-header'>{t('legal_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('legal_sub', lang)}</div>", unsafe_allow_html=True)

    # 📄 Departmental Document Link
    legal_file = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/legal_investigations.json")
    if os.path.exists(legal_file):
        with open(legal_file, "r", encoding="utf-8") as f:
            legal_inv = json.load(f)
    else:
        legal_inv = {"investigations": []}

    with st.expander(f"📄 {'社内文書: 法務コンプライアンス調査台帳 ＆ 審査規程' if lang=='ja' else 'Internal Document: Legal Investigations & Compliance Ledger'}", expanded=False):
        for inv in legal_inv.get("investigations", []):
            st.markdown(f"""
            <div style='background-color: #1E293B; border: 1px solid #334155; border-left: 4px solid #38BDF8; border-radius: 8px; padding: 16px; margin-bottom: 14px; color: #F8FAFC;'>
                <div style='display: flex; justify-content: space-between;'>
                    <strong style='font-size: 1.1rem; color: #FFFFFF;'>📋 {clean_txt(inv['category'])} (ID: {inv['id']})</strong>
                    <span>{inv['status']}</span>
                </div>
                <div style='font-size: 0.8rem; color: #94A3B8; margin: 4px 0;'>
                    🕒 {'受付' if lang=='ja' else 'Received'}: {inv['received_at']} | {'調査開始' if lang=='ja' else 'Review Started'}: {inv['started_at']} | {'完了' if lang=='ja' else 'Completed'}: {inv['completed_at']}
                </div>
                <div style='font-size: 0.9rem; color: #E2E8F0;'><strong>{'相談元:' if lang=='ja' else 'Originating Unit:'}</strong> {clean_txt(inv['requester_dept'])}</div>
                <div style='font-size: 0.9rem; color: #E2E8F0; margin-top: 4px;'><strong>{'受付内容:' if lang=='ja' else 'Inquiry Summary:'}</strong> {clean_txt(inv['inquiry_content'])}</div>
                <div style='background-color: #0F172A; border: 1px solid #334155; padding: 12px; border-radius: 6px; margin-top: 10px; font-size: 0.9rem; color: #F8FAFC;'>
                    <strong style='color: #38BDF8;'>⚖️ {'橘 律 法的な見解:' if lang=='ja' else 'Formal Legal Opinion:'}</strong> {clean_txt(inv['legal_opinion'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 📄 社内就業規則・業務連携規程の閲覧
    emp_reg_file = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/employment_regulations.json")
    if os.path.exists(emp_reg_file):
        with open(emp_reg_file, "r", encoding="utf-8") as f:
            emp_reg_data = json.load(f)
    else:
        emp_reg_data = {}

    with st.expander(f"📄 {'社内文書: AI社員就業規則 ＆ 業務連携規程 (Ver 1.0 正式運用版)' if lang=='ja' else 'Internal Document: AI Employee Regulations & Operations Manual (Ver 1.0)'}", expanded=False):
        st.write(f"**{'制定者:' if lang=='ja' else 'Authorized by:'}** {emp_reg_data.get('author')} | **{'施行日:' if lang=='ja' else 'Effective Date:'}** {emp_reg_data.get('effective_date')} | **{'ステータス:' if lang=='ja' else 'Status:'}** {emp_reg_data.get('status')}")
        st.info(f"📜 **前文 (Preamble):** {emp_reg_data.get('preamble', '')}")
        for chap in emp_reg_data.get("chapters", []):
            st.markdown(f"#### {chap['chapter']}")
            for art in chap.get("articles", []):
                st.markdown(f"""
                <div style='background-color: #0F172A; border: 1px solid #334155; border-left: 3px solid #38BDF8; border-radius: 6px; padding: 10px 14px; margin-bottom: 8px;'>
                    <strong style='color: #38BDF8;'>{art['article']}</strong>
                    <div style='color: #E2E8F0; font-size: 0.9rem; margin-top: 4px; line-height: 1.6;'>{art['content']}</div>
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
        daily_req = int(new_target / 300 / 30)
        if lang == "ja":
            st.info(f"""
            **【財務逆算プラン（社内規定 Rule-PRC-300 準拠）】**
            - 🎯 **日別必要販売数:** 約 **{max(1, daily_req)}部**（基本単価300円想定）
            - 📝 **推奨リリース頻度:** 月 **{target_arts}本**
            - 💡 **財務アドバイス:** 300円の衝動買いしやすい基本価格で購買ハードルを極限まで下げて読者基盤を急拡大し、月末に1,480円等のマガジンを投入するモデルが最も高収益かつLTVを最大化します。
            """)
        else:
            st.info(f"""
            **[Financial Strategy Blueprint (Rule-PRC-300 Compliant)]**
            - 🎯 **Required Daily Unit Sales:** approx. **{max(1, daily_req)} copies** (at ¥300 base price)
            - 📝 **Recommended Publication Cadence:** **{target_arts} articles / month**
            - 💡 **Strategic Advice:** Maximize conversion with ¥300 impulse-purchase entry pricing, then cross-sell higher-ticket ¥1,480 monthly premium bundles.
            """)

# ==========================================
# 10. 💳 Accounting & Operations Division
# ==========================================
elif page_id == "accounting":
    st.markdown(f"<div class='main-header'>{t('acc_title', lang)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{t('acc_sub', lang)}</div>", unsafe_allow_html=True)

    acc_file = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/accounting_data.json")
    if os.path.exists(acc_file):
        with open(acc_file, "r", encoding="utf-8") as f:
            acc_data = json.load(f)
    else:
        acc_data = {"monthly_total_cost_yen": 0, "cost_items": []}
    
    st.success(f"**{t('acc_total_cost_prefix', lang)}** :green[**{t('acc_total_cost_val', lang)}**]")
    
    # 📄 Departmental Document Link
    with st.expander(f"📄 {'社内文書: 月次経理・コスト監査台帳 ＆ ゼロコスト管理規程' if lang=='ja' else 'Internal Document: Monthly Cost Audit Ledger'}", expanded=False):
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

    # 📄 Departmental Document Link (Clean Inline Link)
    spec_file = os.path.join(os.path.dirname(__file__), "companies/note_one_systems/system_specifications.json")
    if os.path.exists(spec_file):
        with open(spec_file, "r", encoding="utf-8") as f:
            spec_data = json.load(f)
    else:
        spec_data = {}

    with st.expander(f"📄 {'社内文書: Note One Systems 会社システム仕様書 (Ver 3.0.0 正式運用版)' if lang=='ja' else 'Internal Document: System Architecture Specifications (Ver 3.0.0)'}", expanded=False):
        st.markdown(f"### 🏢 {spec_data.get('system_name', 'Note One Systems Platform')}")
        st.caption(f"**Version**: {spec_data.get('version', '3.0.0')} | **Last Updated**: {spec_data.get('last_updated', '2026-09-05')} | **Holding**: {spec_data.get('holding_company', 'Studio 0% Holdings')} | **Managed By**: {spec_data.get('author', 'IT Helpdesk')}")

        # 1. Executive Summary & 0-Cost Stack
        exec_sum = spec_data.get("executive_summary", {})
        st.markdown(f"""
        <div class='content-box' style='border-left: 5px solid #38BDF8;'>
            <h4 style='color: #38BDF8; margin-top:0;'>💡 システム基本理念 ＆ 固定費0円事業モデル</h4>
            <p style='color: #F8FAFC; margin-bottom: 8px;'><strong>事業目的:</strong> {exec_sum.get('purpose', '')}</p>
            <p style='color: #F8FAFC; margin-bottom: 8px;'><strong>対外ブランド / 屋号:</strong> <span style='background: #0284C7; color: #FFF; padding: 2px 8px; border-radius: 4px;'>{exec_sum.get('brand_name', 'noteone')}</span></p>
            <div style='background: #064E3B; border: 1px solid #10B981; border-radius: 6px; padding: 12px; margin-top: 10px;'>
                <strong style='color: #4ADE80;'>🛡️ 完全無料（固定費0円）運用の仕組み:</strong>
                <div style='color: #E2E8F0; font-size: 0.92rem; margin-top: 4px;'>{exec_sum.get('zero_cost_principle', '')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 1.5. Corporate Rules
        corp_rules = spec_data.get("corporate_rules", [])
        if corp_rules:
            st.markdown(f"#### 📜 {'全社制定業務規程 (Corporate Operating Rules)' if lang=='ja' else 'Corporate Operating Rules'}")
            for cr in corp_rules:
                st.markdown(f"""
                <div style='background-color: #0F172A; border: 1px solid #38BDF8; border-left: 4px solid #38BDF8; border-radius: 8px; padding: 14px 18px; margin-bottom: 10px;'>
                    <strong style='color: #38BDF8; font-size: 1.0rem;'>📋 {cr.get('rule_id')}: {cr.get('name')}</strong>
                    <div style='color: #E2E8F0; font-size: 0.9rem; margin-top: 6px; line-height: 1.6;'>{cr.get('description')}</div>
                </div>
                """, unsafe_allow_html=True)

        # 2. Architecture Layers
        st.markdown(f"#### 🏗️ {'システムアーキテクチャ4層構造' if lang=='ja' else 'System Architecture Layers'}")
        for layer in spec_data.get("architecture_layers", []):
            st.markdown(f"""
            <div style='background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 16px; margin-bottom: 12px;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <strong style='color: #38BDF8; font-size: 1.05rem;'>{layer.get('layer')}</strong>
                    <span style='background: #0F172A; color: #94A3B8; font-size: 0.8rem; padding: 3px 8px; border-radius: 4px; border: 1px solid #334155;'>Tech: {layer.get('tech_stack')}</span>
                </div>
                <div style='color: #E2E8F0; font-size: 0.92rem; margin-top: 8px; line-height: 1.6;'>{layer.get('description')}</div>
            </div>
            """, unsafe_allow_html=True)

        # 3. AI Agent Matrix
        st.markdown(f"#### 👥 {'9名の自律型AI社員とプロンプト連携マトリクス' if lang=='ja' else 'AI Agent & Prompt Engineering Matrix'}")
        agent_df = []
        for ag in spec_data.get("agent_matrix", []):
            agent_df.append({
                "社員名 / 役職": f"{ag['name']} ({ag['role']})",
                "担当部署": ag["dept"],
                "プロンプト設計 & 主要責務": ag["prompt_feature"]
            })
        st.dataframe(pd.DataFrame(agent_df), use_container_width=True)

        # 4. End-to-End Workflow & Governance Gateways
        st.markdown(f"#### 🔄 {'全社業務ワークフロー ＆ 決裁ゲートウェイ' if lang=='ja' else 'Workflow & Approval Gateways'}")
        for wf in spec_data.get("workflow_steps", []):
            st.markdown(f"""
            <div style='background-color: #1E293B; border: 1px solid #334155; border-left: 4px solid #F59E0B; border-radius: 8px; padding: 14px 18px; margin-bottom: 10px;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <strong style='color: #FFFFFF; font-size: 1rem;'>Step {wf.get('step')}: {wf.get('title')}</strong>
                    <span style='background: #2A1711; color: #FCD34D; font-size: 0.8rem; font-weight: 700; padding: 3px 8px; border-radius: 4px; border: 1px solid #F59E0B;'>Gate: {wf.get('gate')}</span>
                </div>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 6px; font-size: 0.88rem;'>
                    <div style='color: #94A3B8;'><strong>担当:</strong> <span style='color: #E2E8F0;'>{wf.get('owner')}</span></div>
                    <div style='color: #94A3B8;'><strong>成果物:</strong> <span style='color: #38BDF8;'>{wf.get('output')}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 5. Security & Compliance
        sec = spec_data.get("security_and_compliance", {})
        st.markdown(f"""
        <div style='background: #0F172A; border: 1px solid #334155; border-radius: 8px; padding: 16px; margin-top: 18px;'>
            <strong style='color: #10B981; font-size: 1rem;'>🔒 セキュリティ ＆ コンプライアンス規程</strong>
            <ul style='color: #E2E8F0; font-size: 0.9rem; margin-top: 8px; line-height: 1.7;'>
                <li><strong>APIキー保護:</strong> {sec.get('api_key_protection', '')}</li>
                <li><strong>商用コンプライアンス:</strong> {sec.get('commercial_compliance', '')}</li>
                <li><strong>データ所有権:</strong> {sec.get('data_ownership', '')}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Metrics
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

    st.markdown(f"<div class='section-title'>{t('it_ledger_title', lang)}</div>", unsafe_allow_html=True)
    
    for err in err_data.get("errors", []):
        with st.container():
            st.markdown(f"""
            <div style='background-color: #1E293B; border: 1px solid #334155; border-left: 5px solid #38BDF8; border-radius: 10px; padding: 18px; margin-bottom: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.25); color: #F8FAFC;'>
                <div style='display: flex; justify-content: space-between;'>
                    <strong style='font-size: 1.15rem; color: #FFFFFF;'>⚠️ {clean_txt(err['module'])} (ID: {err['id']})</strong>
                    <span style='color: #4ADE80; font-weight: 700;'>{err['status']}</span>
                </div>
                <div style='font-size: 0.8rem; color: #94A3B8; margin: 4px 0;'>🕒 {'発生日時' if lang=='ja' else 'Occurred'}: {err['occurred_at']}</div>
                <div style='background-color: #450A0A; border: 1px solid #991B1B; padding: 10px; border-radius: 6px; font-family: monospace; font-size: 0.85rem; color: #FCA5A5; margin: 8px 0;'>
                    {clean_txt(err['error_message'])}
                </div>
                <div style='font-size: 0.9rem; color: #E2E8F0;'><strong>🔍 {'原因分析:' if lang=='ja' else 'Root Cause Analysis:'}</strong> {clean_txt(err['root_cause'])}</div>
                <div style='font-size: 0.9rem; color: #4ADE80; margin-top: 4px;'><strong>🛠️ {'対処手順・解決法:' if lang=='ja' else 'Resolution Procedure:'}</strong> {clean_txt(err['solution'])}</div>
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
                st.code(clean_txt(emp['prompt']), language="text")

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
        1. Visit [GitHub](https://github.com/)
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
