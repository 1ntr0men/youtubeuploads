import vk_api
import requests
from vk_api import VkUpload
from random import randint
from vk_api.longpoll import VkLongPoll, VkEventType
from pytube import YouTube
import json
import os
import random

user_token = "3edd95bd76f97fe72d795a5ccb63e510a3dee144a1ce8d74d33941e4cdda64008ab49636f817e30cb3b3f"
community_token = "045bfce905f92adf30fd9bb77ff4a29dd91269bdadd19af65f30fcb81e5a92d043b345991a918ac6918ce"
session = requests.Session()
vk_session = vk_api.VkApi(token=community_token)
upload = VkUpload(vk_session)
archive_group_id = 193181102

try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


def send_video(id, reciever):
    params = (
        ("user_id", reciever),
        ("random_id", random.randint(0, 19999)),
        ("message", "Дождитесь обработки видео ВК и наслаждайтесь просмотром"),
        ("attachment", "video-193181102_" + str(id)),
        ('access_token', community_token),
        ("v", "5.103")
    )
    response = requests.post('https://api.vk.com/method/messages.send', params=params)


def edit_desciption(id, name):
    params = (
        ("owner_id", archive_group_id * -1),
        ("video_id", id),
        ("name", name),
        ("desc",
         ""),
        ('access_token', user_token),
        ("v", "5.103")
    )
    response = requests.post('https://api.vk.com/method/video.edit', params=params)
    return id


def upload_1(name, f):
    params = (
        ("name", name),
        ("description", ""),
        ("wallpost", 1),
        ('group_id', archive_group_id),
        ('access_token', user_token),
        ("v", "5.103")
    )
    response = requests.get('https://api.vk.com/method/video.save', params=params)
    upload_server = json.loads(response.text)['response']['upload_url']
    id = json.loads(response.text)['response']['video_id']
    files = {'video_file': open(f, 'rb')}
    requests.post(upload_server, files=files)
    return id, name


def autoposter(v):
    a = YouTube('https://www.youtube.com/watch?v=' + v).streams.get_by_itag('22').download(
        output_path="/home/intromen/ifolder/Send_video_in_PM/video_PM/")
    n = a.title()
    id, name = upload_1("".join(list(a)[49:len(a) - 4]), a)
    os.remove(a)
    return id, name


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:

        if event.text.lower() == 'хочу видео':
            if event.from_user:
                vk.messages.send(
                    user_id=event.user_id,
                    message='ы',
                    random_id=randint(0, 19999),
                )

        elif len(event.text) == 43:
            if event.from_user:
                id, name = autoposter(event.text[32:])
                id_vk = edit_desciption(id, name)
                send_video(id_vk, event.user_id)

        elif len(event.text) == 28:
            if event.from_user:
                id, name = autoposter(event.text[17:])
                id_vk = edit_desciption(id, name)
                send_video(id_vk, event.user_id)

        elif event.text.lower() == "аноним":
            if event.from_user:
                vk.messages.send(
                    user_id=event.user_id,
                    message="Пришли ссылку на получателя",
                    random_id=randint(0, 19999)
                )
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                        if event.from_user:
                            anonim_post_id = vk.users.get(user_ids=''.join(list(event.text)[15:]),
                                                          fields="photo_50",
                                                          name_case="Nom")
                            vk.messages.send(
                                user_id=event.user_id,
                                message="Что отправить?",
                                random_id=randint(0, 19999)
                            )
                            for event in longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                                    if event.from_user:
                                        try:
                                            vk.messages.send(
                                                user_id=str(anonim_post_id[0]["id"]),
                                                message="Вам сообщение от анонима: " + str(event.text),
                                                random_id=randint(0, 19999),
                                            )
                                        except vk_api.exceptions.ApiError:
                                            vk.messages.send(
                                                user_id=event.user_id,
                                                message=str(anonim_post_id[0]["first_name"]) + " " + str(
                                                    anonim_post_id[0][
                                                        "last_name"]) + " не получил(а) твое сообщение, попроси ее(его)"
                                                                        " начать диалог со мной, для начала",
                                                random_id=randint(0, 19999),
                                            )
                                            break
                                    if event.from_user:
                                        vk.messages.send(
                                            user_id=event.user_id,
                                            message=str(anonim_post_id[0]["first_name"]) + " " + str(
                                                anonim_post_id[0]["last_name"]) + " получил твое сообщение",
                                            random_id=randint(0, 19999),
                                        )
                                    break
                        break

        else:
            if event.from_user:
                vk.messages.send(
                    user_id=event.user_id,
                    message="Я распознаю лишь ссылки",
                    random_id=randint(0, 19999),
                )
