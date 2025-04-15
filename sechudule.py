import schedule
import time

def fetch_matches():
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        matches = response.json()
        for match in matches:
            print(f"Upcoming: {match['name']} at {match['scheduled_at']}")

# Run every hour
schedule.every(1).hours.do(fetch_matches)

while True:
    schedule.run_pending()
    time.sleep(60)