from flask import Flask, request
from logic.settings import bot_token
from logic.TelegBot import TelegBot


secret = bot_token

bot=TelegBot()
bot.webhook()

app = Flask(__name__)

@app.route(f"/{secret}", methods=["POST"])
def webhook():
	updates = request.json
	bot.handling_message(updates)
	return "ok", 200
