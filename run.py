from  logic.TelegBot import TelegBot
from logic.settings import TELEG_ROOT_URL

if __name__ == "__main__":
	bot=TelegBot()
	bot.polling()