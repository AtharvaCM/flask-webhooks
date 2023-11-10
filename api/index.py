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
    
    # Create an embed message for Discord
    discord_message = {
        "username": "English BT Bot",
        "avatar_url": "https://media.licdn.com/dms/image/D5603AQGJODmUg3akSw/profile-displayphoto-shrink_100_100/0/1689862148982?e=1704931200&v=beta&t=qHp1mmsBg6d97LoAg6KxwXFvzq6Y62WIJjL17jMcppo",
        "embeds": [
            {
                "title": "Status Update",
                "description": status_description,
                "color": 0x00ff00 if new_status == "operational" else 0xff0000,
                "fields": [
                    {
                        "name": "Component",
                        "value": component_name,
                        "inline": True
                    },
                    {
                        "name": "New Status",
                        "value": new_status,
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "OpenAI Status Update"
                },
                "timestamp": data.get('component_update', {}).get('created_at')
            }
        ]
    }

    # Post the message to Discord
    response = requests.post(DISCORD_WEBHOOK_URL, json=discord_message)
    if response.status_code == 204:
        return jsonify({"message": "Success"}), 200
    else:
        return jsonify({"message": "Failed to post to Discord"}), 500

if __name__ == '__main__':
    app.run()
