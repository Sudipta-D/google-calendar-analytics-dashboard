
-- Preview first few rows
SELECT * FROM calendar_events LIMIT 5;

-- Total events and total time spent by event type
SELECT 
    event_type,
    COUNT(*) AS total_events,
    SUM((julianday(end_time) - julianday(start_time)) * 24 * 60) AS total_minutes
FROM calendar_events
GROUP BY event_type
ORDER BY total_minutes DESC;

-- Events per week (usage trend)
SELECT 
    strftime('%Y-%W', start_time) AS week,
    COUNT(*) AS events
FROM calendar_events
GROUP BY week
ORDER BY week;

-- % focus time (project work) vs other events
SELECT
    ROUND(
        SUM(CASE WHEN event_type = 'Project Work' THEN 
            (julianday(end_time) - julianday(start_time)) * 24 * 60 ELSE 0 END) * 100.0 /
        SUM((julianday(end_time) - julianday(start_time)) * 24 * 60), 2
    ) AS focus_percent
FROM calendar_events;

-- Days with more than 8 hours of events (overutilized)
SELECT 
    DATE(start_time) AS date,
    ROUND(SUM((julianday(end_time) - julianday(start_time)) * 24), 2) AS total_hours
FROM calendar_events
GROUP BY DATE(start_time)
HAVING total_hours > 6
ORDER BY total_hours DESC;

-- Days with 3-8 hours of events (healthy)
SELECT 
    DATE(start_time) AS date,
    ROUND(SUM((julianday(end_time) - julianday(start_time)) * 24), 2) AS total_hours
FROM calendar_events
GROUP BY DATE(start_time)
HAVING total_hours between 3 and 6
ORDER BY total_hours DESC;

-- Days with less than 3 hours of events (underutilized)
SELECT 
    DATE(start_time) AS date,
    ROUND(SUM((julianday(end_time) - julianday(start_time)) * 24), 2) AS total_hours
FROM calendar_events
GROUP BY DATE(start_time)
HAVING total_hours < 3
ORDER BY total_hours DESC;


-- Status breakdown (completed, rescheduled, etc.)
SELECT 
    status,
    COUNT(*) AS count
FROM calendar_events
GROUP BY status;

-- Daily meeting count trend
SELECT 
    DATE(start_time) AS date,
    COUNT(*) AS meeting_count
FROM calendar_events
WHERE event_type = 'Client Meeting'
GROUP BY DATE(start_time)
ORDER BY date;

-- Billed vs Unbilled Hours
SELECT 
    status,
    ROUND(SUM((julianday(end_time) - julianday(start_time)) * 24), 2) AS total_hours
FROM calendar_events
GROUP BY status;

-- Hours Spent in Meetings

SELECT 
    DATE(start_time) AS date,
    ROUND(SUM((julianday(end_time) - julianday(start_time)) * 24), 2) AS meeting_hours
FROM calendar_events
WHERE event_type = 'Client Meeting'
GROUP BY DATE(start_time)
ORDER BY date;

-- Meetings Breakdown by Status (Pie Chart)
SELECT 
    status,
    COUNT(*) AS meeting_count
FROM calendar_events
WHERE event_type = 'Client Meeting'
GROUP BY status;

-- Task Line: Events in a Day
SELECT 
    title,
    start_time,
    end_time,
    event_type,
    status
FROM calendar_events
WHERE DATE(start_time) = '2024-09-01' -- change date dynamically
ORDER BY start_time;


