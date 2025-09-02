from utilities.load_schedule import fetch_schedule

# load the schedule for the year
schedule = fetch_schedule([2025])

schedule.to_csv(
    '2025_schedule.csv',
    index=False
)