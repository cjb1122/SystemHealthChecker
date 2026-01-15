#!/usr/bin/env python3
import os
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

#!/usr/bin/env python3
import os
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -----------------------------
# Config & Thresholds
# -----------------------------
USERNAME = "admin"
PASSWORD = "SuperSecurePassword123"
BLOCK_THRESHOLD = 5  # New: Threshold for auto-remediation

# -----------------------------
# In-Memory Metrics Store
# -----------------------------
metrics_store = {}  # { hostname: { last_update: <iso>, metrics: { ... } } }
failed_attempts_tracker = {} # New: Tracks failed logins per IP

# -----------------------------
# Health Check
# -----------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})


# -----------------------------
# Receive Metrics From Agents
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

    # 1. Standard Update for Dashboard
    metrics_store[hostname] = {
        "last_update": datetime.utcnow().isoformat() + "Z",
        "metrics": data
    }

    # ---------------------------------------------------------
    # NEW: REMEDIATION LOGIC
    # ---------------------------------------------------------
    # Check if the agent reported a failed SSH attempt
    # (Assuming your agent sends 'last_failed_ip' in its payload)
    source_ip = data.get("last_failed_ip") 
    
    if source_ip:
        # Increment failure count
        failed_attempts_tracker[source_ip] = failed_attempts_tracker.get(source_ip, 0) + 1
        
        # If threshold hit, return the BLOCK instruction
        if failed_attempts_tracker[source_ip] >= BLOCK_THRESHOLD:
            return jsonify({
                "status": "remediate",
                "action": "BLOCK",
                "target_ip": source_ip,
                "reason": f"Exceeded {BLOCK_THRESHOLD} failed attempts"
            }), 201 # 201 indicates a new remediation 'resource' was created
    # ---------------------------------------------------------

    return jsonify({"status": "received"}), 200


@app.route("/dashboard-data", methods=["GET"])
def dashboard_data():
    return jsonify(metrics_store)


@app.route("/", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
