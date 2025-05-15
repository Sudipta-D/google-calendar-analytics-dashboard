# 📅 Google Calendar Analytics Dashboard

A data-driven Streamlit dashboard that analyzes calendar usage for freelancers and professionals — visualize your time distribution, meeting load, and productivity trends.

## 🎯 Project Objective

This project helps individuals understand:
- Where their time is going
- How often meetings occur
- How balanced, underutilized or overutilized their days are
- What types of events dominate their schedule

It is an attempt to develop a monetizable feature concept for Google Calendar targeted at freelancers especially.

---

## 🛠️ Features

✅ Interactive filters for date and status  
✅ KPI cards showing focus time, event count, and overutilized days  
✅ Weekly trend visualizations  
✅ Utilization breakdown (under/healthy/over) with charts  
✅ Meeting type and status analysis (bar + pie)  
✅ Dynamic task timeline for selected dates  

---

## 📊 Tech Stack

| Tool       | Purpose                     |
|------------|-----------------------------|
| Python     | Core logic and data wrangling |
| Streamlit  | Web app and dashboard UI     |
| SQLite     | Data storage                 |
| Faker      | Mock data generation         |
| Matplotlib | Custom plotting              |
| Pandas     | Data manipulation            |
| Seaborn    | (Optional) visuals           |

---

## 📂 Folder Structure
google-calendar-analytics/
├── dashboard/              # Streamlit app
│   └── app.py
├── data/
│   └── calendar_events.db
├── sql/
│   └── calendar_analysis.sql
├── notebooks/              # EDA, data generation
│   ├── generate_calendar_data.py
│   ├── eda_visuals.ipynb
│   └── sql_analysis.ipynb
├── images/                 # Screenshots or visuals
│   └── sample_dashboard.png
├── .streamlit/
│   └── config.toml
├── .gitignore
├── requirements.txt
└── README.md

---
## 🚀 Live Demo

👉 [Click here to view the live app](https://sudipta-d-calendar-analytics.streamlit.app/)

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Sudipta-D/google-calendar-analytics-dashboard.git
cd google-calendar-analytics
---

## Install dependencies

pip install -r requirements.txt

## Run the app
streamlit run dashboard/app.py

