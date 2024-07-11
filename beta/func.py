import vk_api
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

