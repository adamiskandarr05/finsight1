"""
FinSight Scraper Agent
Uses Gemini to gather: SEC filings, earnings data,
recent news, and analyst commentary for a given company/query.
"""

import os
import json
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

SCRAPER_SYSTEM = """
You are the FinSight Scraper Agent. Your role is to gather raw financial intelligence.

For the given query, collect:
- Recent earnings reports (revenue, EPS, guidance)
- SEC filings highlights (10-K, 10-Q if relevant)
- Recent news (last 30 days) affecting the company or sector
- Analyst ratings and price targets
- Key financial metrics (P/E, market cap, debt levels)

Return ONLY a JSON object with keys:
  earnings: {...}
  filings_summary: "..."
  recent_news: ["...", "..."]
  analyst_ratings: [{analyst, rating, target}]
  key_metrics: {revenue, eps, pe_ratio, market_cap, debt_to_equity}

No markdown. No preamble. Valid JSON only.
"""

def run_scraper(query: str) -> dict:
    """Run the scraper agent, returns raw financial data as dict."""
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=SCRAPER_SYSTEM
    )
    response = model.generate_content(
        f"Research this financial query and gather all available data: {query}"
    )
    raw = response.text.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw, "error": "parse_failed"}


if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "Apple AAPL latest earnings"
    result = run_scraper(q)
    print(json.dumps(result, indent=2))
