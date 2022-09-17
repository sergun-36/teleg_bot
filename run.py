from  logic.TelegBot import TelegBot

url = "https://webhook.site/8f1131e8-1848-42bf-873a-fd25e918f204"

bot=TelegBot()
#bot.get_updates()
#bot.polling()
print(bot.webhook(url))
print(bot.get_webhook_info(url))