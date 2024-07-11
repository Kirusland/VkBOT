import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import *
from datetime import datetime
from config import TOKEN, GROUPTOKEN


session = vk_api.VkApi(token=TOKEN)
vk = session.get_api()

sessiongroup = vk_api.VkApi(token=GROUPTOKEN)
vkgroup = sessiongroup.get_api()


def get_user_status(user_id):
    status = session.method("status.get", {"user_id": user_id})
    return(status['text'])

def get_my_status():
    status = vk.status.get()
    return(status['text'])

def set_user_status(text):
    session.method("status.set", {"text": text})

def get_user_friends():
    friends = vk.friends.get()
    return friends['items']

def get_friends_online():
    online_friends = vk.friends.getOnline()
    return(online_friends)

def get_fname_by_id(id, name_case):
    return(vk.users.get(user_id=id, name_case=name_case)[0]['first_name'])

def get_lname_by_id(id, name_case):
    return(vk.users.get(user_id=id, name_case=name_case)[0]['last_name'])

def get_profie_info(user_id):
    return(vk.account.getInfo(user_id=user_id))

def add_friend_by_id(user_id, chat_id):
    try:
        vk.friends.add(user_id=user_id)
        send_message_by_peer_id(f"Отправил запрос на добавление в друзья: {lname} {fname}", chat_id)
    except vk_api.exceptions.ApiError as e:
        send_message_by_peer_id(e, chat_id)
        print(e)

# def send_message_by_chat_id(message, chat_id):
#     vkgroup.messages.send(
#                     random_id=0,
#                     chat_id=chat_id,
#                     message=message
#                     )

def send_message_by_peer_id(message, chat_id):
    vkgroup.messages.send(
        random_id=0,
        chat_id=chat_id,
        message=message
    )

def delete_message_4all_by_id(id, peer_id):
    vk.messages.delete(cmids=id, peer_id = peer_id, delete_for_all=True)


for event in VkLongPoll(sessiongroup).listen():

    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        set_user_status(f"VK API Кодер❤️ Последний заход в сеть: {datetime.now()}")
        text = event.text.lower()

        if text[0] == '!':
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

                if arg == isinstance(arg, str):
                    send_message_by_peer_id(f"Команда не найдена, чтобы вывести список команд, напишите: !help",
                                            chat_id)
                    continue

                else:
                    fname = get_fname_by_id(arg,
                                            'dat')
                    lname = get_lname_by_id(arg,
                                            'dat')

                    if prefix == '!друзья':
                        add_friend_by_id(arg,
                                         chat_id)

                    elif prefix == '!инфо':
                        # info = get_profie_info(arg)
                        send_message_by_peer_id(f"Команда недоступна из-за политики VK API:"
                                                f"\n(vk_api.exceptions.ApiError: [914] Message is too long)",
                                                chat_id)
                        #vk_api.exceptions.ApiError: [914] Message is too long
                    elif prefix == '!статус':
                        status = get_user_status(arg)
                        send_message_by_peer_id(status,
                                                chat_id)

                    else:
                        send_message_by_peer_id(f"Команда не найдена, чтобы вывести список команд, напишите: !help",
                                                chat_id)

            else:
                if text == '!статус':
                    status = get_my_status()
                    send_message_by_peer_id(status,
                                            chat_id)

                elif text == '!онлайн':
                    online_friends = get_friends_online()
                    if online_friends == []:
                        send_message_by_peer_id(f"Никого нет онлайн",
                                                chat_id)
                    else:
                        send_message_by_peer_id(f"Онлайн: {online_friends}",
                                                chat_id)
                    print(online_friends)

                elif text == '!помощь' or text == '!help':
                    send_message_by_peer_id(
                                    f"Команды:\n\n!друзья <id> - добавить пользователя в друзья"
                                            f"\n!инфо <id> - получить информацию о пользователе"
                                            f"\n!статус <id> - получить статус пользователя"
                                            f"\n!статус - получить статус текущего пользователя"
                                            f"\n!онлайн - получить список друзей текущего пользователя онлайн"
                                            f"\n!помощь или !help - вывести это сообщение",
                                    chat_id)
                else:
                    send_message_by_peer_id(f"Команда не найдена. Чтобы вывести список команд, напишите: !help", chat_id)




