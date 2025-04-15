import requests
import schedule
import time

# Your PandaScore API token
API_TOKEN = "Y1VUewV6DpA8BX5hGLyKPfWec0C7_KHZnYjgzz7NLKF63Onc6VY"  # Replace with your actual API token

# API endpoint for upcoming matches
url = "https://api.pandascore.co/matches/upcoming"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# Optional: Filter by game (e.g., VALORANT)
params = {
    "filter[videogame]": "valorant",  # Change this for different games
    "page[size]": 10  # Limit to 10 matches
}

# Function to fetch and display upcoming matches
def fetch_matches():
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        matches = response.json()
        
        for match in matches:
            name = match.get("name", "Unknown Match")
            start_time = match.get("scheduled_at", "Unknown Time")
            tournament = match.get("tournament", {}).get("name", "Unknown Tournament")

            print(f"Match: {name} | Tournament: {tournament} | Starts: {start_time}")

            # Simulating Grok response
            grok_summary = f"Yo, {name} is going down at {tournament} on {start_time}—hype match incoming!"
            print(grok_summary)
    
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Fetch matches immediately on script start
fetch_matches()

# Schedule the function to run every hour
schedule.every(1).hours.do(fetch_matches)

# Keep running the scheduler
while True:
    schedule.run_pending()
    time.sleep(60)
