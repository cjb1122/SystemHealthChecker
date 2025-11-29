🖥️ SystemHealthChecker

A lightweight, agent-based server monitoring tool built using Python and Flask.
Designed to help IT Support and System Administrators demonstrate real-world skills in automation, monitoring, Linux administration, REST APIs, and Git.

This project collects metrics from Linux servers using a lightweight Python agent and sends them to a central Aggregator Dashboard running on Flask.

🚀 Features
Agent (Installed on servers)

Collects:

CPU usage

Memory usage

Disk usage

System uptime

Failed SSH login attempts

Hostname + timestamp

Sends metrics securely to the aggregator via HTTP with Basic Auth.

Configurable polling interval (default: 60 seconds).

Aggregator (Central Server)

Receives metrics from multiple agents

Stores metrics in a JSON log file

Provides authenticated REST endpoints:

POST /submit – agents submit data

GET /metrics – view all collected system metrics

GET /health – simple health check

Can be run as a systemd service for production use.