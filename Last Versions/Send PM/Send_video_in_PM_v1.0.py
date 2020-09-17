from pytube import YouTube
import requests
import json
import os
import random

user_token = "3edd95bd76f97fe72d795a5ccb63e510a3dee144a1ce8d74d33941e4cdda64008ab49636f817e30cb3b3f"
community_token = "045bfce905f92adf30fd9bb77ff4a29dd91269bdadd19af65f30fcb81e5a92d043b345991a918ac6918ce"

print("Готов к отсылке видео")
print()

test_group_id = 193181102
main_group_id = 188254964


def send_video(id, reciever):
    params = (
        ("user_id", reciever),
        ("random_id", random.randint(0, 10000)),
        ("message", "Дождитесь обработки видео ВК и наслаждайтесь просмотром"),
        ("attachment", "video-193181102_" + str(id)),
        ('access_token', community_token),
        ("v", "5.103")
    )
    response = requests.post('https://api.vk.com/method/messages.send', params=params)


def edit_desciption(id, name):
    params = (
        ("owner_id", test_group_id * -1),
        ("video_id", id),
        ("name", name),
        ("desc",
         ""),
        ('access_token', user_token),
        ("v", "5.103")
    )
    response = requests.post('https://api.vk.com/method/video.edit', params=params)
    return id


def upload(name, f):
    params = (
        ("name", name),
        ("description", ""),
        ("wallpost", 1),
        ('group_id', test_group_id),
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
        output_path="D:\\Autoposter\\video\\")
    n = a.title()
    id, name = upload("".join(list(n)[20:len(n) - 4]), n)
    os.remove(n)
    return id, name


video = input()
receiver = input()
id, name = autoposter(video)
id_vk = edit_desciption(id, name)
send_video(id_vk, receiver)

print("Видео в паблике")
