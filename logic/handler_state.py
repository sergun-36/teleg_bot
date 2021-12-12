"""тип кино
из выдираем город
 город есть шлем сообщение
 запонить запрос кино 
 попросить ввести город
 искать город """

 state = { "type": "кино",
 			"city": "Минск"}

if state["type"] and state["city"]:
	if city in settings.CITIES:
		send_message("Ok")
		return True
if state.get("type") == "кино" and not state.get("city"):
	send_message("Enter city")
	check_user_answer("пулить есть ли город")
	if last_messge in СCities :
		apdate( state['city']=city)

def func(state):
	if state["type"] and state["city"]:
		if city in settings.CITIES:
			send_message("Ok")
			return True
	else:
		if state.get("type") == "кино" and not state.get("city"):
			send_message("Enter city")
			pooling("есть ли город")
			if last_messge in СCities :
				state['city'] = last_messge
				func(state)


