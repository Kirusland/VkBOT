# main.py
import func
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import *
from datetime import datetime

for event in VkLongPoll(func.sessiongroup).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        func.set_user_status(f"VK API Кодер❤️ Последний заход в сеть: {datetime.now()}")
        text = event.text.lower()

        if text == '!':
            peer_id = event.peer_id

            if peer_id > 2000000000:
                chat_id = peer_id - 2000000000

            else:
                chat_id = peer_id

            user_id = event.user_id
            message_id = event.message_id

            print(user_id)
            print(message_id)
            print(peer_id)

            if ' ' in text:
                prefix, arg = text.split(' ', 1)
                print(type(arg))

                if isinstance(arg, str):
                    func.send_message_by_peer_id(f"Команда не найдена, чтобы вывести список команд, напишите: !help",
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

                elif text == '!помощь' or text == '!help':
                    func.send_message_by_peer_id(
                        f"Команды:\n\nдрузья <id> - добавить пользователя в друзья"
                        f"\nинфо <id> - получить информацию о пользователе"
                        f"\nстатус <id> - получить статус пользователя"
                        f"\nстатус - получить статус текущего пользователя"
                        f"\nонлайн - получить список друзей текущего пользователя онлайн"
                        f"\nпомощь или !help - вывести это сообщение",
                        chat_id)
                else:
                    func.send_message_by_peer_id(f"Команда не найдена. Чтобы вывести список команд, напишите: !help", chat_id)
