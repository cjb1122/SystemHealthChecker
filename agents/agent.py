#!/usr/bin/env python3

import subprocess
import json
import time
import requests
import socket
from datetime import datetime
import os

# =======================
# Load Config
# =======================
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

with open(CONFIG_FILE, "r") as f:
    cfg = json.load(f)

AGGREGATOR_URL = cfg["http://3.12.150.216:5000/submit"]        # e.g. "http://3.15.25.81:5000/submit"
USERNAME       = cfg["username"]
PASSWORD       = cfg["password"]
INTERVAL       = cfg.get("interval_seconds", 60)


# =======================
# Helper to run shell commands
# =======================
def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except:
        return ""


# =======================
# Collect host metrics
# =======================
def collect_metrics():
    return {
        "agent_type": "linux",
        "hostname": socket.gethostname(),
        "timestamp": datetime.utcnow().isoformat() + "Z",

        "uptime": run("uptime -p"),
        "cpu": run("top -bn1 | grep 'Cpu'"),
        "memory": run("free -h | grep Mem"),
        "disk": run("df -h / | tail -1"),

        # RHEL/CentOS failed login check
        "failed_logins": run("grep 'Invalid user' /var/log/secure | wc -l")
    }


# =======================
# Send data to aggregator
# =======================
def post_metrics(metrics):
    try:
        resp = requests.post(
            AGGREGATOR_URL,
            json=metrics,
            auth=(USERNAME, PASSWORD),
            timeout=10
        )
        print(f"[+] Sent metrics → aggregator ({resp.status_code})")
    except Exception as e:
        print(f"[!] Failed to send metrics: {e}")


# =======================
# Main loop
# =======================
if __name__ == "__main__":
    print("Linux HostHealthCheck Agent started...")

    while True:
        metrics = collect_metrics()
        post_metrics(metrics)
        time.sleep(INTERVAL)
