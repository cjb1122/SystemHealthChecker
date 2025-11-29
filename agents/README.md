🖥️ **SystemHealthChecker**



A lightweight, agent-based server monitoring tool built using Python and Flask.

Designed to help IT Support and System Administrators demonstrate real-world skills in automation, monitoring, Linux administration, REST APIs, and Git.



This project collects metrics from Linux servers using a lightweight Python agent and sends them to a central Aggregator Dashboard running on Flask.



🚀 **Features**

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



**Aggregator (Central Server)**



Receives metrics from multiple agents



Stores metrics in a JSON log file



Provides authenticated REST endpoints:



POST /submit – agents submit data



GET /metrics – view all collected system metrics



GET /health – simple health check



Can be run as a systemd service for production use.



📁 **Project Structure**



SystemHealthChecker/

│

├── aggregator/

│   ├── app.py             # Flask API server

│   ├── config.py          # Credentials + settings

│   ├── requirements.txt   # Python dependencies

│   └── systemd.service    # Optional: run aggregator as a service

│

├── agents/

│   └── linux/

│       ├── agent.py       # Linux monitoring agent

│       ├── config.json    # Agent settings (URL, credentials, interval)

│

└── README.md





INSTRUCTIONS:

⚙️ 1. Install the Aggregator (Flask API)



On the aggregator EC2 instance (Amazon Linux or Ubuntu):



sudo yum install python3 git -y   # or apt install on Ubuntu

git clone https://github.com/cjb1122/SystemHealthChecker.git

cd SystemHealthChecker/aggregator



pip3 install -r requirements.txt



Set aggregator credentials using environment variables

export AGG\_USER="admin"

export AGG\_PASS="SuperSecurePassword123"





(These match the values used by the agents.)



Start the server

python3 app.py





Aggregator will run at:



http://<aggregator-ip>:5000



🖥️ 2. Install the Agent on a Linux Server



On each monitored Linux EC2 instance:



sudo yum install python3 curl -y

mkdir -p /opt/systemhealth/agent

cd /opt/systemhealth/agent



curl -O https://raw.githubusercontent.com/cjb1122/SystemHealthChecker/main/agents/linux/agent.py

curl -O https://raw.githubusercontent.com/cjb1122/SystemHealthChecker/main/agents/linux/config.json



⚙️ 3. Configure the Agent



Edit config.json:



{

&nbsp;   "aggregator\_url": "http://<aggregator-ip>:5000/submit",

&nbsp;   "username": "admin",

&nbsp;   "password": "SuperSecurePassword123",

&nbsp;   "interval\_seconds": 60

}





Save the file.



▶️ 4. Run the Agent

python3 agent.py





You should see:



Linux agent started...

\[+] Sent metrics (200)



📡 Aggregator Endpoints

POST /submit



Agent sends metrics.



GET /metrics



View all collected metrics (requires auth).



GET /health



Check API status.



🔧 5. Running Aggregator as a systemd service



Create:



sudo nano /etc/systemd/system/systemhealth.service





Paste:



\[Unit]

Description=System Health Aggregator

After=network.target



\[Service]

User=ec2-user

WorkingDirectory=/home/ec2-user/SystemHealthChecker/aggregator

ExecStart=/usr/bin/python3 app.py

Restart=always

Environment="AGG\_USER=admin"

Environment="AGG\_PASS=SuperSecurePassword123"



\[Install]

WantedBy=multi-user.target





Start service:



sudo systemctl daemon-reload

sudo systemctl enable systemhealth

sudo systemctl start systemhealth

sudo systemctl status systemhealth



🎯 Why This Project Helps IT Professionals



This project demonstrates real-world technical skills:



✔ Linux system administration

✔ Python scripting

✔ REST API communication

✔ Monitoring and automation

✔ GitHub + version control

✔ Service deployment on EC2

✔ Building a working infrastructure tool end-to-end



It’s an excellent project to showcase on your resume or LinkedIn portfolio.



🏁 Next Step: Write your LinkedIn Post



Once you're ready, I’ll craft a polished LinkedIn post explaining:



The value of this project



What you learned



How aspiring IT support professionals can build similar tools



Just say “write the LinkedIn post”.

