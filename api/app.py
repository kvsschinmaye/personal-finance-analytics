from flask import Flask, jsonify, request, Response
import json

from analytics.spending import category_wise_spending
from analytics.trends import monthly_spending_trend
from analytics.users import user_wise_spending
from analytics.high_value import high_value_transactions
from rules.alerts import generate_all_alerts
from utils.logger import logger

app = Flask(__name__)

# ------------------------
# Health Check
# ------------------------
@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "service": "Personal Finance Analytics API"
    })


# ------------------------
# Root Endpoint
# ------------------------
@app.route("/")
def home():
    return jsonify({
        "status": "Personal Finance Analytics API running"
    })


# ------------------------
# Analytics Endpoints
# ------------------------
@app.route("/analytics/category")
def category_spending():
    try:
        logger.info("API: Category-wise spending requested")
        data = category_wise_spending()
        return jsonify([
            {"category": c, "total_spent": float(t)}
            for c, t in data
        ])
    except Exception:
        logger.exception("Category analytics failed")
        return jsonify({"error": "Failed to fetch category analytics"}), 500


@app.route("/analytics/monthly")
def monthly_trend():
    try:
        logger.info("API: Monthly spending trend requested")
        data = monthly_spending_trend()
        return jsonify([
            {"month": m, "total_spent": float(t)}
            for m, t in data
        ])
    except Exception:
        logger.exception("Monthly analytics failed")
        return jsonify({"error": "Failed to fetch monthly analytics"}), 500


@app.route("/analytics/users")
def users_spending():
    try:
        logger.info("API: User-wise spending requested")
        data = user_wise_spending()
        return jsonify([
            {"user_id": u, "total_spent": float(t)}
            for u, t in data
        ])
    except Exception:
        logger.exception("User analytics failed")
        return jsonify({"error": "Failed to fetch user analytics"}), 500


@app.route("/analytics/high-value")
def high_value():
    try:
        threshold = request.args.get("threshold", default=5000, type=int)
        logger.info(f"API: High-value transactions requested (>{threshold})")
        data = high_value_transactions(threshold)

        return jsonify([
            {
                "txn_id": tx,
                "user_id": u,
                "amount": float(a),
                "category": c,
                "date": str(d)
            }
            for tx, u, a, c, d in data
        ])
    except Exception:
        logger.exception("High-value analytics failed")
        return jsonify({"error": "Failed to fetch high-value transactions"}), 500


# ------------------------
# Alerts Endpoint (Unicode-safe)
# ------------------------
@app.route("/alerts")
def alerts():
    try:
        logger.info("API: Alerts requested")
        alerts = generate_all_alerts()
        return Response(
            json.dumps({"alerts": alerts}, ensure_ascii=False),
            mimetype="application/json"
        )
    except Exception:
        logger.exception("Alerts generation failed")
        return jsonify({"error": "Failed to generate alerts"}), 500


# ------------------------
# Global Error Handlers
# ------------------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500
