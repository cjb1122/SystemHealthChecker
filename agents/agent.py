#!/usr/bin/env python3

import time
import socket
import psutil
import requests
from datetime import datetime, timezone

# -------------------------------
# CONFIG — EDIT ONLY THESE VALUES
# -------------------------------
AGGREGATOR_URL = "http://3.129.210.216:5000/metrics"
AGG_USER = "admin"
AGG_PASS = "SuperSecurePassword123"
INTERVAL_SECONDS = 60

# -------------------------------
# Collect system metrics
# -------------------------------
def collect_metrics():
    return {
        "hostname": socket.gethostname(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
    }

# -------------------------------
# Send metrics to aggregator
# -------------------------------
def send_metrics():
    payload = collect_metrics()

    try:
        response = requests.post(
            AGGREGATOR_URL,
            json=payload,
            auth=(AGG_USER, AGG_PASS),
            timeout=10
        )

        if response.status_code == 200:
            print("[+] Metrics sent successfully")
        else:
            print(f"[!] Failed to send metrics: HTTP {response.status_code} → {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to send metrics: {e}")

# -------------------------------
# Main loop
# -------------------------------
def main():
    print("Linux HostHealthCheck Agent started...")
    while True:
        send_metrics()
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    main()

