"""
FinSight Orchestrator Agent
Receives a user query, fans out to scraper/analyst/reporter agents,
and returns a structured investment brief.
"""

import os
import json
import asyncio
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

ORCHESTRATOR_SYSTEM = """
You are the FinSight Orchestrator. Your job is to coordinate a financial research swarm.

Given a user query about a company or market topic, you will:
1. Identify the company/ticker and research scope
2. Delegate: raw data gathering → synthesis → report writing
3. Return a final JSON brief with keys: title, summary, key_metrics, risks, signals, verdict

Always respond with valid JSON only. No markdown, no preamble.
"""

def run_orchestrator(query: str) -> dict:
    """Entry point: takes a query string, returns the full brief as a dict."""

    # Step 1: Scrape raw data
    from scraper import run_scraper
    raw_data = run_scraper(query)

    # Step 2: Analyst synthesizes raw data
    from analyst import run_analyst
    analysis = run_analyst(query, raw_data)

    # Step 3: Reporter structures the brief
    from reporter import run_reporter
    brief = run_reporter(query, analysis)

    return brief


if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "Analyze Apple Inc (AAPL) for Q1 2025"
    result = run_orchestrator(q)
    print(json.dumps(result, indent=2))
