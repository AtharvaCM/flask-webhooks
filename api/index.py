from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# This is your Discord webhook URL
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1172028599994429520/zl7CK3NToCJgnHVSL5Ea4PKpRYNAgRJ57mwVYWPwE8qG0j8qUh7Gl40KRESDmuhcKPwX'

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/openai-webhook', methods=['POST'])
def openai_webhook():
    data = request.json  # Get the JSON data POSTed to the endpoint

    # Extract information from OpenAI's webhook data
    status_description = data['page']['status_description']
    component_name = data.get('component', {}).get('name', 'Component')
    new_status = data.get('component_update', {}).get('new_status', 'status')
    
    # Format the message for Discord
    discord_message = {
        "content": f"{component_name} status updated: {new_status}\n{status_description}"
    }

    # Post the message to Discord
    response = requests.post(DISCORD_WEBHOOK_URL, json=discord_message)
    if response.status_code == 204:
        return jsonify({"message": "Success"}), 200
    else:
        return jsonify({"message": "Failed to post to Discord"}), 500

if __name__ == '__main__':
    app.run()
