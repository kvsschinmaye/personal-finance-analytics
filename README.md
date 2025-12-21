# Personal Finance Analytics Platform

A full-stack data analytics platform that analyzes personal spending patterns, detects anomalies using a rules-based alerts engine, and visualizes insights through an interactive dashboard.

This project is built with a clean, layered architecture inspired by real-world fintech and analytics systems and is fully deployed on the cloud.

---

## 🚀 Key Features

- 📊 Category-wise spending analysis  
- 📈 Monthly spending trend visualization  
- 👤 User-wise expense aggregation  
- 🚨 Rules-based alerts for high spending and anomalies  
- 🌐 RESTful APIs built using Flask  
- 🖥️ Interactive and responsive Streamlit dashboard  

---

## 🧱 System Architecture

1. SQLite Database  
2. Analytics Layer  
3. Rules & Alerts Engine  
4. Flask REST APIs  
5. Streamlit Dashboard  

This layered design ensures scalability, maintainability, and clear separation of concerns.

---

## 🛠️ Tech Stack

- **Programming Language:** Python  
- **Backend Framework:** Flask (Gunicorn for production)  
- **Database:** SQLite  
- **Frontend / Visualization:** Streamlit  
- **Data Processing:** Pandas  
- **API Style:** REST (JSON)  

---

## ▶️ Running the Project Locally

### 1️⃣ Initialize the SQLite Database
```bash
python data/init_db.py
2️⃣ Start the Backend API
python -m api.app


The API will be available at:

http://127.0.0.1:5000

3️⃣ Start the Dashboard
streamlit run ui/dashboard.py


The dashboard will open automatically in your browser.

🌐 Live Deployment

Backend API (Render):
https://personal-finance-analytics-api.onrender.com

Dashboard (Streamlit Cloud):
https://personal-finance-analytics.streamlit.app

📌 Future Enhancements

Budget recommendations based on spending patterns

Anomaly detection using statistical or ML techniques

Authentication and role-based access control

Advanced filters (date range, category-wise filtering)

👤 Author

K V Sai Sri Chinmaye
Computer Science Engineering Student
Focused on  Backend Development, Data Analytics, and Scalable System Design

