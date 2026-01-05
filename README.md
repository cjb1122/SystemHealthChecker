🖥️ Distributed System Healthcheck & Security Pipeline
A lightweight, full-stack observability solution designed to monitor Linux server health and security across distributed environments. This project replaces manual "check-ins" with a centralized telemetry hub and real-time alerting.

🚀 The Mission
In production environments, visibility is the difference between a minor blip and a major outage. This pipeline provides a "single pane of glass" for system metrics and potential security breaches (brute-force attempts) across an entire fleet of servers.

Key Capabilities:
Persistent Monitoring: Implemented as a systemd service to ensure the monitor is self-healing, survives reboots, and recovers from crashes.

Security Observability: Parses binary btmp logs to detect failed login attempts, serving as a basic Intrusion Detection System (IDS).

Threshold-Based Alerting: The UI uses conditional logic to trigger visual alerts (Yellow/Red) when resource usage or security risks breach defined limits.

Decoupled Architecture: A Python agent (Producer) ships JSON telemetry to a Flask REST API (Aggregator), which serves a reactive JavaScript frontend (Consumer).


🏗️ Technical Stack
Backend: Python 3.10+, Flask, Flask-CORS
Agent Logic: psutil (hardware), subprocess (log parsing), socket
Frontend: HTML5, CSS3 (Keyframe Animations), JavaScript (ES6 Fetch API)
Infrastructure: Linux (RHEL/Amazon Linux/Ubuntu), Systemd, Bash📊 

Dashboard Visual Logic
The dashboard interprets data using a traffic-light system to reduce "alert fatigue":
Metric    | Green (Healthy)|    Yellow           |  Red (Critical)
CPU Usage | < 70%          |   70% - 89%        | > 90% + Pulsing
RAM Usage | < 70%          | 70% - 89%        | > 90% + Pulsing
Failed Logins | 0 - 5      |   1 - 5          | > 5 + Pulsing




🔧 Installation & Deployment
1. Set Up the Aggregator (Central Server)
# Clone the repository
git clone https://github.com/YOUR_USERNAME/SystemHealthcheck.git
cd SystemHealthcheck/aggregator

# Install requirements
pip install -r requirements.txt

# Start the hub
python3 app.py

# Start the hub
python3 app.py
2. Deploy the Agent (Monitoring Nodes)Bashcd SystemHealthcheck/agent

# Edit config with your Aggregator's IP
vim agent.py

# Install as a systemd service
sudo cp healthcheck-agent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable healthcheck-agent --now

🛠️ L3 Engineering Highlights
Log Ingestion: Designed a custom parser for /var/log/btmp to bridge the gap between low-level Linux logs and high-level dashboard metrics.
Asynchronous Polling: Utilized JavaScript setInterval and fetch to create a live-updating experience without requiring page refreshes.
Resiliency: Configured systemd with a Restart=always policy and a 5-second delay to ensure maximum uptime of the monitoring agent.
Defensive Programming: Implemented robust try/except blocks in the telemetry loop to handle intermittent network failures between nodes.


