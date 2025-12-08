#!/usr/bin/env python3
import os
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -----------------------------
# Authentication Config
# -----------------------------
USERNAME = "admin"
PASSWORD = "SuperSecurePassword123"

# -----------------------------
# In-Memory Metrics Store
# -----------------------------
metrics_store = {}   # { hostname: { last_update: <iso>, metrics: { ... } } }


# -----------------------------
# Health Check
# -----------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})


# -----------------------------
# Receive Metrics From Agents
# POST /metrics   (agent → server)
# -----------------------------
@app.route("/metrics", methods=["POST"])
def receive_metrics():
    auth = request.authorization

    if not auth or auth.username != USERNAME or auth.password != PASSWORD:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON"}), 400

    hostname = data.get("hostname")
    if not hostname:
        return jsonify({"error": "Missing hostname"}), 400

    metrics_store[hostname] = {
        "last_update": datetime.utcnow().isoformat() + "Z",
        "metrics": data
    }

    return jsonify({"status": "received"}), 200


# -----------------------------
# Fetch All Metrics For Dashboard
# GET /dashboard-data   (browser → server)
# -----------------------------
@app.route("/dashboard-data", methods=["GET"])
def dashboard_data():
    return jsonify(metrics_store)


# -----------------------------
# Dashboard Page (HTML)
# GET /
# -----------------------------
@app.route("/", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")


# -----------------------------
# Run Flask (0.0.0.0 for public)
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

