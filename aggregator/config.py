import os

# -----------------------------
# Basic Auth Credentials
# -----------------------------
AGGREGATOR_USER = os.getenv("AGG_USER", "admin")  
AGGREGATOR_PASS = os.getenv("AGG_PASS", "SuperSecurePassword123")

# -----------------------------
# Server Settings
# -----------------------------
HOST = "0.0.0.0"
PORT = 5000

# -----------------------------
# File where metrics are stored
# -----------------------------
DATA_FILE = "aggregated_results.json"
