import func
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import *
from datetime import datetime

for event in VkLongPoll(func.sessiongroup).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        time_=event.raw[4]
        func.set_user_status(f"VK API Кодер❤️ Последний заход в сеть: {datetime.now()}")
        text = event.text.lower()
        if text[0] == '!':
            peer_id = event.peer_id

            if peer_id > 2000000000:
                chat_id = peer_id - 2000000000

            else:
                chat_id = peer_id

            user_id = event.user_id
            message_id = event.message_id

            print(chat_id)
            print(user_id)
            print(message_id)
            print(peer_id)

            if ' ' in text:
                prefix, arg = text.split(' ', 1)
                print(type(arg))
                try:
                    arg = int(arg)
                except ValueError:
                    if (prefix == '!реши'):
                        try:
                            msg = eval(arg)
                            func.send_message_by_peer_id(msg, chat_id)
                        except ZeroDivisionError:
                            func.send_message_by_peer_id("Нельзя делить на ноль!", chat_id)
                            continue
                    else:
                        func.send_message_by_peer_id(f"Аргумент команды не является числом, напишите: !help",
                                                     chat_id)
                    continue


                else:
                    fname = func.get_fname_by_id(arg, 'dat')
                    lname = func.get_lname_by_id(arg, 'dat')

                    if prefix == '!друзья':
                        func.add_friend_by_id(arg, chat_id)

                    elif prefix == '!инфо':
                        # info = func.get_profie_info(arg)
                        func.send_message_by_peer_id(f"Команда недоступна из-за политики VK API:"
                                                     f"\n(vk_api.exceptions.ApiError: [914] Message is too long)",
                                                     chat_id)
                        #vk_api.exceptions.ApiError: [914] Message is too long
                    elif prefix == '!статус':
                        status = func.get_user_status(arg)
                        func.send_message_by_peer_id(status, chat_id)
                        
                    else:
                        func.send_message_by_peer_id(f"Команда не найдена, чтобы вывести список команд, напишите: !help",
                                                     chat_id)

            else:
                if text == '!статус':
                    status = func.get_my_status()
                    func.send_message_by_peer_id(status, chat_id)

                elif text == '!онлайн':
                    online_friends = func.get_friends_online()
                    if online_friends == []:
                        func.send_message_by_peer_id(f"Никого нет онлайн", chat_id)
                    else:
                        func.send_message_by_peer_id(f"Онлайн: {online_friends}", chat_id)
                    print(online_friends)

                elif text == '!ping' or text == '!пинг':
                    ping=f'Пинг: {abs(round(datetime.now().timestamp()-time_, 3))} сек.'
                    func.send_message_by_peer_id(ping, chat_id)
                    print(ping)

                elif text == '!помощь' or text == '!help':
                    func.send_message_by_peer_id(
                        f"Команды:\n\n!друзья <id> - добавить пользователя в друзья"
                        f"\n!инфо <id> - получить информацию о пользователе"
                        f"\n!статус <id> - получить статус пользователя"
                        f"\n!статус - получить статус текущего пользователя"
                        f"\n!онлайн - получить список друзей текущего пользователя онлайн"
                        f"\n!помощь или !help - вывести это сообщение",
                        chat_id)
                else:
                    func.send_message_by_peer_id(f"Команда не найдена. Чтобы вывести список команд, напишите: !help", chat_id)
