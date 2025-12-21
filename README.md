📊 Personal Finance Analytics Platform

A lightweight Personal Finance Analytics Platform to analyze spending patterns, detect high-risk expenses, and generate actionable insights through an interactive dashboard.

Built using Python, SQLite, Flask, and Streamlit, and deployed on cloud.

🚀 Live Links

Dashboard (Streamlit):
https://personal-finance-analytics.streamlit.app

Backend API (Render):
https://personal-finance-analytics-ac0b.onrender.com

🧠 Architecture
SQLite Database
   ↓
Analytics Layer
   ↓
Rules & Alerts Engine
   ↓
Flask REST API
   ↓
Streamlit Dashboard

✨ Features

Category-wise spending analysis

Monthly and user-wise spending trends

High-value transaction detection

Rule-based alerts

Interactive charts & tables

CSV and PDF report downloads

Mobile-responsive UI

🛠️ Tech Stack

Backend: Python, Flask, SQLite

Frontend: Streamlit, Pandas, Matplotlib

Deployment: Render, Streamlit Cloud

📂 Project Structure
personal-finance-analytics/
├── api/            # Flask API
├── analytics/      # Analytics logic
├── rules/          # Alerts engine
├── db/             # SQLite connection
├── data/           # Database & init script
├── ui/             # Streamlit dashboard
└── requirements.txt

▶️ Run Locally
pip install -r requirements.txt
python data/init_db.py
python -m api.app
streamlit run ui/dashboard.py

👤 Author

K V Sai Sri Chinmaye
GitHub: https://github.com/kvsschinmaye

LinkedIn: https://linkedin.com/in/kvsaisrichinmaye

⭐ If you find this project useful, consider starring the repository.