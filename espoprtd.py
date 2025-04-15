from flask import Flask, request
import requests  # For API calls


app = Flask(__name__)

@app.route('/tournaments', methods=['GET'])
def get_tournaments():
    # Example: Call an esports API
    api_key = "YOUR_API_KEY"
    response = requests.get("https://api.abiosgaming.com/v2/tournaments", 
                           headers={"Authorization": f"Bearer {api_key}"})
    return response.json()

if __name__ == "__main__":
    app.run(debug=True)