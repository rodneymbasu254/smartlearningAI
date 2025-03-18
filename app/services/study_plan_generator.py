from datetime import datetime, timedelta

def generate_study_plan(course_data, start_date=None, duration_weeks=14):
    weekly_topics = course_data.get("weekly_topics", [])
    title = course_data.get("course_title", "Unknown Course")
    code = course_data.get("course_code", "CODE000")

    if not start_date:
        start_date = datetime.today()

    plan = []
    for i, topic in enumerate(weekly_topics):
        week = i + 1
        if week > duration_weeks:
            break
        week_start = start_date + timedelta(weeks=i)
        week_end = week_start + timedelta(days=6)
        plan.append({
            "unit": code,
            "title": title,
            "week": week,
            "topic": topic,
            "start_date": week_start.strftime('%Y-%m-%d'),
            "end_date": week_end.strftime('%Y-%m-%d'),
        })

    return plan
