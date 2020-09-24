import vk_api
import requests
from vk_api import VkUpload
from random import randint
from json import dumps

user_token = "ce9b9828b611e1993be1cb4e37383cb4d52c2bf250947661fecb530780d318f92038ce6fccc73bee4db47"
community_token = "e0c123cc5f0e8b3a3cbe0a114f0a56d9b7183251c955d35fef77fbe263c6607a8bbf508f2825b62a723e1"

user_token_1 = "ab983c74fb9103daac4df335621a41a824014322a828ed3a7229e6f3366180b67aeab33fe9b88edda4395"
community_token_1 = "9c5be8ddc5e47f9ca79237524e339fa832fb46118a5a49dd9cd42d6a1f77eb2133d360a48bbd4baa05da8"
session = requests.Session()
vk_session = vk_api.VkApi(token=community_token)
upload = VkUpload(vk_session)

vk = vk_session.get_api()

knopki = {
    "one_time": True,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "label": "Да"
                },
                "color": "primary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "label": "Нет"
                },
                "color": "primary"
            }
        ]
    ]
}

params = (
    ("count", 200),
    ("filter", "all"),
    ("wallpost", 1),
    ('group_id', 188254964),
    ('access_token', community_token),
    ("v", "5.103")
)
response = requests.get('https://api.vk.com/method/messages.getConversations', params=params)
count = response.json()["response"]["count"]

for i in range(count):
    try:
        user_id = response.json()["response"]["items"][i]["conversation"]["peer"]["id"]
        vk.messages.send(
            user_id=user_id,
            message="У меня появилась возможность восстановить, доработать и улучшить бота\n"
                    "Решил собрать статистику будущих пользователей\n"
                    "\n"
                    "Собираешься ли ты использовать бота??\n"
                    "Ответьте, мне важна активность\n"
                    "\n"
                    "Скажу по секрету, Вас ждут новые функции😉🤫",
            random_id=randint(0, 19999),
            keyboard=dumps(knopki)
        )
    except:
        pass
