"""
FinSight API Server
A lightweight Flask server that bridges the web frontend and the agent swarm.
Deploy on Google Cloud Run.
"""

import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orchestrator import run_orchestrator

app = Flask(__name__)
CORS(app)  # Allow frontend to call the API


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "FinSight API"})


@app.route("/research", methods=["POST"])
def research():
    """
    POST /research
    Body: { "query": "Analyze Tesla TSLA earnings" }
    Returns: Full investment brief JSON
    """
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' field"}), 400

    query = data["query"].strip()
    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    if len(query) > 500:
        return jsonify({"error": "Query too long (max 500 chars)"}), 400

    try:
        brief = run_orchestrator(query)
        return jsonify({"success": True, "brief": brief})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/demo", methods=["GET"])
def demo():
    """Returns a mock brief for UI testing without burning API calls."""
    mock = {
        "title": "Apple Inc: Strong Quarter, Services Shine",
        "ticker": "AAPL",
        "rating": "BUY",
        "summary": (
            "Apple delivered a strong Q1 2025 with iPhone revenue beating expectations "
            "and Services reaching record highs. The company's AI integration strategy "
            "positions it well for the next product cycle."
        ),
        "key_metrics": [
            {"label": "Revenue", "value": "$124.3B", "trend": "up"},
            {"label": "EPS", "value": "$2.40", "trend": "up"},
            {"label": "P/E Ratio", "value": "28.5x", "trend": "flat"},
            {"label": "Market Cap", "value": "$3.2T", "trend": "up"}
        ],
        "risks": [
            "China market headwinds and regulatory scrutiny",
            "Slowing hardware upgrade cycles",
            "Intensifying AI competition from Google and Samsung"
        ],
        "signals": [
            "Services revenue grew 14% YoY to $26.3B",
            "Apple Intelligence driving iPhone 16 upgrade cycle",
            "$110B buyback authorization signals confidence"
        ],
        "verdict": "Solid foundation with AI tailwinds — initiate at BUY with $215 target.",
        "generated_at": "2025-03-14T12:00:00+00:00"
    }
    return jsonify({"success": True, "brief": mock})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)


@app.route("/")
def index():
    return send_from_directory(".", "index.html")
