from  logic.TelegBot import TelegBot
from flask import Flask, request
from logic.settings import bot_token

secret = bot_token
bot=TelegBot()
bot.webhook()

app = Flask(__name__)

@app.route(f"/{secret}", methods=["POST"])
def webhook():
	#bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	updates = request.json
	bot.handling_message(updates)
	return "ok", 200

if __name__ == "__main__":
	app.run()