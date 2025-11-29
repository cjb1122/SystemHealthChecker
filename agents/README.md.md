README.md — SystemHealthChecker

SystemHealthChecker



A lightweight system monitoring and reporting tool that includes two components:



Aggregator (Server) — collects health data from agents



Agent (Client) — runs on each monitored host and reports system metrics to the aggregator



Features



CPU, memory, disk, and uptime reporting



API endpoints protected by username/password



JSON-based configuration



Systemd support for both aggregator and agent



Easy to deploy on any Linux server or agent machine



Works across networks using HTTP POST



Repository Structure

SystemHealthChecker/

│── aggregator/

│   ├── app.py

│   ├── config.py

│   ├── config.json

│   └── requirements.txt

│

│── agent/

│   ├── agent.py

│   ├── config.py

│   ├── config.json

│   └── requirements.txt

│

└── README.md



Aggregator Setup

1\. Install dependencies

cd aggregator

pip install -r requirements.txt



2\. Configure aggregator credentials



Edit config.json:



{

&nbsp; "AGGREGATOR\_USER": "admin",

&nbsp; "AGGREGATOR\_PASS": "SuperSecurePassword123",

&nbsp; "HOST": "0.0.0.0",

&nbsp; "PORT": 5000

}



3\. Start the aggregator

python3 app.py



Agent Setup

1\. Install dependencies

cd agent

pip install -r requirements.txt



2\. Configure agent



Edit config.json:



{

&nbsp; "AGGREGATOR\_URL": "http://3.12.150.216:5000/report",

&nbsp; "AGG\_USER": "admin",

&nbsp; "AGG\_PASS": "SuperSecurePassword123",

&nbsp; "INTERVAL": 30

}



3\. Start the agent

python3 agent.py



Systemd Installation (Optional)

Aggregator Service



/etc/systemd/system/aggregator.service



\[Unit]

Description=System Health Aggregator

After=network.target



\[Service]

User=root

WorkingDirectory=/opt/SystemHealthChecker/aggregator

ExecStart=/usr/bin/python3 app.py

Restart=always



\[Install]

WantedBy=multi-user.target





Enable + start:



sudo systemctl daemon-reload

sudo systemctl enable aggregator

sudo systemctl start aggregator



Agent Service



/etc/systemd/system/agent.service



\[Unit]

Description=System Health Agent

After=network.target



\[Service]

User=root

WorkingDirectory=/opt/SystemHealthChecker/agent

ExecStart=/usr/bin/python3 agent.py

Restart=always



\[Install]

WantedBy=multi-user.target





Enable + start:



sudo systemctl daemon-reload

sudo systemctl enable agent

sudo systemctl start agent



API Endpoints

POST /report



Agents send system health data.



GET /status



Returns a list of all last-seen agents and their metrics.



Security Notes



Always change default credentials



Use HTTPS or a VPN for production environments



Store secrets in environment variables when possible



License



MIT License

