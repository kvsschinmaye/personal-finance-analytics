
# Personal Finance Analytics Platform

A full-stack data analytics platform that analyzes personal spending patterns, detects anomalies using a rules-based alerts engine, and visualizes insights through an interactive dashboard.

The project is designed with a clean, layered architecture inspired by real-world fintech and analytics systems.

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

MySQL Database
       ↓
Analytics Layer
       ↓
Rules & Alerts Engine
       ↓
Flask REST APIs
       ↓
Streamlit Dashboard


This layered approach ensures scalability, maintainability, and easy extensibility.

---

## 🛠️ Tech Stack

- **Programming Language:** Python  
- **Backend Framework:** Flask  
- **Database:** MySQL  
- **Frontend / Visualization:** Streamlit  
- **Data Processing:** Pandas  
- **API Style:** REST (JSON)  

---

## ▶️ Running the Project Locally

### Start the Backend API
```bash
python -m api.app
The API will be available at:

cpp
Copy code
http://127.0.0.1:5000
Start the Dashboard
bash
Copy code
streamlit run ui/dashboard.py
The dashboard will open automatically in your default browser.

🌐 Deployment
Backend API: Render

Dashboard UI: Streamlit Cloud

(Live deployment links will be added after deployment.)

📌 Future Enhancements
Budget recommendations based on spending patterns

Anomaly detection using statistical and ML techniques

Authentication and role-based access control

Advanced filters (date range, category-wise filtering)

👤 Author
K V Sai Sri Chinmaye
Computer Science Engineering Student
Focused on Backend Development, Data Analytics, and Scalable System Design