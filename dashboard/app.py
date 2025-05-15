import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="📅 Calendar Analytics", layout="wide")

# --- Light theme background ---
st.markdown("""
    <style>
        .main {
            background-color: #F1F3F4;
        }
        h1, h2, h3, .stMetricLabel {
            color: #4285F4;
        }
        .st-bb {
            background-color: white;
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)


# --- Database Connection ---
conn = sqlite3.connect("data/calendar_events.db")

# --- Load Queries from SQL File ---
def get_queries():
    with open("sql/calendar_analysis.sql", "r") as f:
        sql = f.read()
    return [q.strip() for q in sql.split(";") if q.strip()]

queries = get_queries()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")
selected_date = st.sidebar.date_input("📅 Select a Date", pd.to_datetime("2024-09-01"))

# --- Main Header ---
st.title("📅 Calendar Analytics Dashboard")
st.markdown("Monitor how your day is utilized, track meetings, and evaluate productivity.")

# --- Load Key Query Results ---
df_preview = pd.read_sql(queries[0], conn)
df_focus = pd.read_sql(queries[3], conn)
df_status = pd.read_sql(queries[7], conn)

# --- KPI Cards ---
col1, col2,= st.columns(2)
col1.metric("🧠 Focus Time %", f"{df_focus.iloc[0]['focus_percent']}%")
col2.metric("🔁 Total Events", len(df_preview))
st.subheader("📈 Daily Meeting Count")
df_meeting_count = pd.read_sql(queries[8], conn)
st.line_chart(df_meeting_count.set_index("date")["meeting_count"])

st.subheader("🕓 Time Spent in Client Meetings")
df_meeting_hours = pd.read_sql(queries[10], conn)
st.line_chart(df_meeting_hours.set_index("date")["meeting_hours"])


st.subheader("🧩 Client Meetings by Status")

df_meeting_status = pd.read_sql(queries[11], conn)

if not df_meeting_status.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.write("### Bar Chart")
        st.bar_chart(df_meeting_status.set_index("status")["meeting_count"])

    with col2:
        st.write("### Pie Chart")
        import matplotlib.pyplot as plt

        labels = df_meeting_status["status"]
        sizes = df_meeting_status["meeting_count"]
        colors = ["#34A853", "#FBBC05", "#EA4335"]  # ✅ Google green, yellow, red

        fig, ax = plt.subplots(figsize=(6, 6))
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=None,  # Remove labels from inside the chart
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            textprops=dict(color="black")
        )

        # Add legend instead of inline labels
        ax.legend(wedges, labels, title="Status", loc="center left", bbox_to_anchor=(1, 0.5))
        ax.set_title("Meeting Status Breakdown")
        ax.axis('equal')

        st.pyplot(fig)

else:
    st.info("No meeting status data available.")


# 📊 Side-by-side bar and pie
st.markdown("## 🧠 Daily Utilization Summary")

# Step 1: Query daily hours
query_util = """
SELECT DATE(start_time) AS date,
       ROUND(SUM((julianday(end_time) - julianday(start_time)) * 24), 2) AS total_hours
FROM calendar_events
GROUP BY DATE(start_time)
"""
df_util_all = pd.read_sql(query_util, conn)

# Step 2: Classify days
def classify_utilization(hours):
    if hours < 3:
        return "Underutilized"
    elif hours <= 6:
        return "Healthy"
    else:
        return "Overutilized"

df_util_all["category"] = df_util_all["total_hours"].apply(classify_utilization)

# Step 3: Count days per category (and preserve missing categories)
categories = ["Underutilized", "Healthy", "Overutilized"]
util_counts = df_util_all["category"].value_counts().reindex(categories, fill_value=0)

# Step 4: Side-by-side charts
col1, col2 = st.columns(2)

with col1:
    st.write("### Bar Chart")
    st.bar_chart(util_counts)

with col2:
    st.write("### Pie Chart")
    import matplotlib.pyplot as plt

    # Google Material colors
    slice_colors = ["#34A853", "#FBBC05", "#EA4335"]  # blue, yellow, green

    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        util_counts.values,
        labels=None,  # move labels to legend
        autopct='%1.1f%%',
        startangle=140,
        colors=slice_colors,
        textprops={'fontsize': 12, 'color': "black"}
    )

    # Add external legend for cleaner view
    ax.legend(
        wedges,
        util_counts.index,
        title="Category",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=11
    )
    ax.set_title("Utilization Breakdown", fontsize=14)
    ax.axis("equal")  # keep circle shape

    st.pyplot(fig)

# --- 📊 Step 1: Time by Event Type ---
st.subheader("🕒 Time Spent by Event Type")
df_event_time = pd.read_sql(queries[1], conn)
st.bar_chart(df_event_time.set_index("event_type")["total_minutes"])

# --- 📈 Step 2: Weekly Event Trend ---
st.subheader("📅 Weekly Event Trend")
df_weekly = pd.read_sql(queries[2], conn)
st.line_chart(df_weekly.set_index("week")["events"])


# --- 📋 Step 4: Status Filter View ---
st.sidebar.markdown("---")
status_filter = st.sidebar.selectbox("Filter Events by Status", df_status["status"].unique().tolist())

st.subheader(f"📄 Events with Status: {status_filter}")
query_status = f"""
SELECT title, start_time, end_time, event_type, status
FROM calendar_events
WHERE status = '{status_filter}'
ORDER BY start_time DESC
"""
df_status_events = pd.read_sql(query_status, conn)
st.dataframe(df_status_events)

# --- 📅 Task Timeline ---
st.subheader(f"📋 Task Line for {selected_date}")
q_taskline = queries[12].replace("2024-09-01", selected_date.strftime('%Y-%m-%d'))
df_taskline = pd.read_sql(q_taskline, conn)

if not df_taskline.empty:
    st.write(df_taskline[["title", "start_time", "end_time", "event_type", "status"]])
else:
    st.info("No events for this date.")

# --- Close DB Connection ---
conn.close()

