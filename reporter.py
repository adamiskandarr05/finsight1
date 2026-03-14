"""
FinSight Reporter Agent
Takes analyst output and structures it into a clean, final investment brief.
"""

import os
import json
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

REPORTER_SYSTEM = """
You are the FinSight Reporter Agent. You write clear, concise investment briefs
for professional and retail investors.

Given a query and analyst assessment, produce a polished final brief.

Return ONLY a JSON object with these exact keys:
  title: "Company Name: Brief Title (e.g. Strong Quarter, Cautious Outlook)"
  ticker: "TICKER"
  rating: "BUY" | "HOLD" | "SELL" | "WATCH"
  summary: "2-3 sentence executive summary"
  key_metrics: [
    {label: "Revenue", value: "...", trend: "up" | "down" | "flat"},
    {label: "EPS", value: "...", trend: "up" | "down" | "flat"},
    {label: "P/E Ratio", value: "...", trend: "up" | "down" | "flat"},
    {label: "Market Cap", value: "...", trend: "up" | "down" | "flat"}
  ]
  risks: ["...", "...", "..."]
  signals: ["...", "...", "..."]
  verdict: "One punchy sentence with the investment conclusion"
  generated_at: "ISO timestamp placeholder"

No markdown. Valid JSON only.
"""

def run_reporter(query: str, analysis: dict) -> dict:
    """Produce the final structured investment brief."""
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=REPORTER_SYSTEM
    )
    response = model.generate_content(
        f"Original query: {query}\n\n"
        f"Analyst assessment:\n{json.dumps(analysis, indent=2)}\n\n"
        "Generate the final investment brief."
    )
    raw = response.text.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
    try:
        data = json.loads(raw)
        from datetime import datetime, timezone
        data["generated_at"] = datetime.now(timezone.utc).isoformat()
        return data
    except json.JSONDecodeError:
        return {"raw": raw, "error": "parse_failed"}
