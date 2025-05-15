import pandas as pd
from faker import Faker
import random
from datetime import timedelta, datetime
import os


# Ensure data folder exists
os.makedirs("data", exist_ok=True)


fake = Faker()
Faker.seed(42)
random.seed(42)


locations = ["Zoom", "Google Meet", "Office", "Home", "Cafe"]


descriptions_map = {
    "Break": [
        "Coffee break", "Lunch break", "Take a short walk", "Mindfulness time"
    ],
    "Project Work": [
        "Write project documentation", "Implement module features", "Test new codebase", "Fix reported bugs"
    ],
    "Client Meeting": [
        "Discuss contract terms", "Review progress with client", "Demo completed features", "Align on next steps"
    ],
    "Admin": [
        "Update invoices", "Log expenses", "Respond to internal emails", "Submit weekly report"
    ],
    "Email & Communication": [
        "Reply to client emails", "Sort inbox", "Follow up on proposals", "Schedule meetings"
    ]
}


event_templates = [
    {"event_type": "Project Work", "duration_range": (60, 120), "prob": 0.9},
    {"event_type": "Client Meeting", "duration_range": (30, 60), "prob": 0.6},
    {"event_type": "Break", "duration_range": (15, 30), "prob": 0.8},
    {"event_type": "Admin", "duration_range": (20, 40), "prob": 0.7},
    {"event_type": "Email & Communication", "duration_range": (15, 30), "prob": 0.5}
]


data = []
reschedule_pool = []


start_date = datetime(2024, 9, 1)
end_date = datetime(2025, 5, 1)
user_id = 1
event_id = 1000
current_date = start_date
today = datetime.now()


while current_date < end_date:
    current_hour = random.randint(8, 10)
    events_today = []


    for template in event_templates:
        if random.random() < template["prob"]:
            duration_mins = random.randint(*template["duration_range"])
            event_start = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=current_hour)
            event_end = event_start + timedelta(minutes=duration_mins)


            # Determine event status
            if event_start > today:
                status = "upcoming"
            elif template["event_type"] == "Break":
                status = "completed" if random.random() > 0.1 else "upcoming"
            else:
                status = random.choices(
                    ["completed", "to be rescheduled", "canceled"],
                    weights=[0.65, 0.2, 0.15],
                    k=1
                )[0]


            with_whom = fake.name() if template["event_type"] == "Client Meeting" else ""
            description = random.choice(descriptions_map[template["event_type"]])


            event = {
                "event_id": event_id,
                "user_id": user_id,
                "title": f"{template['event_type']} - {description}",
                "start_time": event_start,
                "end_time": event_end,
                "status": status,
                "description": description,
                "location": random.choice(locations),
                "event_type": template["event_type"],
                "with_whom": with_whom
            }


            data.append(event)


            # If cancelled or rescheduled, clone as a completed one later
            if status in ["canceled", "to be rescheduled","upcoming"]:
                if template["event_type"] != "Break":
                    clone_date = current_date + timedelta(days=random.randint(1, 5))
                    if clone_date < end_date:
                         event_id += 1
                         event_clone = event.copy()
                         event_clone["event_id"] = event_id
                         event_clone["start_time"] = event_start + timedelta(days=random.randint(1, 3))
                         event_clone["end_time"] = event_clone["start_time"] + (event_end - event_start)
                         event_clone["status"] = "completed"
                         data.append(event_clone)
                   
               


            current_hour += duration_mins // 60 + 1
            event_id += 1


    current_date += timedelta(days=1)


# Save to CSV
df = pd.DataFrame(data)
df = df.sort_values(by="start_time")  # ✅ sort chronologically

df.to_csv("data/calendar_events.csv", index=False)

print(f"✅ Realistic calendar_events.csv created with {len(df)} records.")
