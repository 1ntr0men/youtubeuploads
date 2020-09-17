import vk_api
import requests
from vk_api import VkUpload
from random import randint
from vk_api.longpoll import VkLongPoll, VkEventType

user_token = "ce9b9828b611e1993be1cb4e37383cb4d52c2bf250947661fecb530780d318f92038ce6fccc73bee4db47"
community_token = "cdeb54a462b6478564a177204d712e2bb1bc0d3725c3fb3aa93f11c159feac77ad46e0c074955bd544c33"

session = requests.Session()
vk_session = vk_api.VkApi(token=community_token)
upload = VkUpload(vk_session)

try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

vk.messages.send(
    user_id=253830804,
    message='Пришли, что ты хочешь разослать',
    random_id=randint(0, 19999),
)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.from_user and event.user_id == 253830804:
            message = event.text
            att = 0

            vk.messages.send(
                user_id=253830804,
                message="Ты уверен?",
                random_id=randint(0, 19999),
            )
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    if event.from_user and event.user_id == 253830804 and event.text.lower() == "да":
                        if event.from_user:
                            vk.messages.send(
                                user_id=event.user_id,
                                #attachment=','.join(attachments),
                                message="Лови " + message,
                                random_id=randint(0, 19999)
                            )
                    break
