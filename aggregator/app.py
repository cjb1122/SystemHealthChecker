#!/usr/bin/env python3

from flask import Flask, request, jsonify
from functools import wraps
import os
import json
from datetime import datetime

app = Flask(__name__)

# ====================================================
# Configuration
# ====================================================
AGGREGATOR_USER = os.getenv("AGG_USER", "admin")
AGGREGATOR_PASS = os.getenv("AGG_PASS", "SuperSecurePassword123")

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

# ====================================================
# Authentication
# ====================================================
def check_auth(username, password):
    return username == AGGREGATOR_USER and password == AGGREGATOR_PASS

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper

# ====================================================
# Basic Health Check
# ====================================================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})

# ====================================================
# Receive Metrics from Agents
# ====================================================
@app.route("/metrics", methods=["POST"])
@require_auth
def receive_metrics():
    data = request.json

    if not data:
        return jsonify({"error": "No JSON payload"}), 400

    hostname = data.get("hostname", "unknown")
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")

    filename = f"{hostname}_{timestamp}.json"
    filepath = os.path.join(DATA_FOLDER, filename)

    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        return jsonify({"status": "saved", "file": filename}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ====================================================
# Return All Saved Metrics
# ====================================================
@app.route("/metrics", methods=["GET"])
@require_auth
def list_metrics():
    files = sorted(os.listdir(DATA_FOLDER))
    entries = []

    for file in files:
        try:
            with open(os.path.join(DATA_FOLDER, file)) as f:
                entries.append(json.load(f))
        except:
            pass
    
    return jsonify(entries), 200

# ====================================================
# Run Server
# ====================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
