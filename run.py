from  logic.TelegBot import TelegBot
from flask import Flask, request

url = "https://fb37-46-53-248-212.eu.ngrok.io"

secret = "JHDLHIudshfoishoIHUL"
bot=TelegBot()
#bot.get_updates()
#bot.polling()
bot.webhook(f"{url}/{secret}")
print(bot.get_webhook_info(url))

app = Flask(__name__)

@app.route(f"/{secret}", methods=["POST"])
def webhook():
	#bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	updates = request.json
	print(updates)
	pass
	return "ok"

if __name__ == "__main__":
	app.run()