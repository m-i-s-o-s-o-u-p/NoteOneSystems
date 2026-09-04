import os
import json
from companies.note_one_systems.workflow import NoteOneWorkflow
from core.ai_client import AIClient
from companies.note_one_systems.market_research_manager import MarketResearchManager

ai_client = AIClient()
wf = NoteOneWorkflow(ai_client)
mm = MarketResearchManager(ai_client)

articles = wf.list_articles()
pending_arts = [a for a in articles if a.get("status") == "Pending Owner Approval"]
print(f"Total articles: {len(articles)}")
print(f"Pending Owner Approval articles: {len(pending_arts)}")
for a in pending_arts:
    print(f"  - [{a['id']}] {a['title'][:30]}... ({len(a.get('content',''))} chars)")

topics = mm.list_topics()
pending_tps = [t for t in topics if t.get("status") == "Pending Owner Approval"]
print(f"\nTotal topics: {len(topics)}")
print(f"Pending Owner Approval topics: {len(pending_tps)}")

