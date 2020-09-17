import vk_api
import requests
from vk_api import VkUpload
from random import randint
from vk_api.longpoll import VkLongPoll, VkEventType
import json
import os
import random
import youtube_dl
import datetime

print("Введите количество видео, которое уже есть в пабле за сегодня от 0-50")
limit = int(input())
day = datetime.datetime.now().day

user_token_starui = "3edd95bd76f97fe72d795a5ccb63e510a3dee144a1ce8d74d33941e4cdda64008ab49636f817e30cb3b3f"
user_token = "ab983c74fb9103daac4df335621a41a824014322a828ed3a7229e6f3366180b67aeab33fe9b88edda4395"
community_token_starui = "045bfce905f92adf30fd9bb77ff4a29dd91269bdadd19af65f30fcb81e5a92d043b345991a918ac6918ce"
community_token = "9c5be8ddc5e47f9ca79237524e339fa832fb46118a5a49dd9cd42d6a1f77eb2133d360a48bbd4baa05da8"
session = requests.Session()
vk_session = vk_api.VkApi(token=community_token)
upload = VkUpload(vk_session)
archive_group_id = 193181102


def try_repeat(func):
    def wrapper(*args, **kwargs):
        count = 3
        while count:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                E = e
                count -= 1
        print('Error:', E)
        vk.messages.send(
            user_id=253830804,
            message=E,
            random_id=randint(0, 19999)
        )

    return wrapper


try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


@try_repeat
def send_video(id, reciever):
    if id:
        message = "Дождитесь обработки видео ВК и наслаждайтесь просмотром"
    else:
        message = "Извините, неплодадки со стороны ютуба, пришлите другое видео))"
    params = (
        ("user_id", reciever),
        ("random_id", random.randint(0, 19999)),
        ("message", message),
        ("attachment", "video-193181102_" + str(id)),
        ('access_token', community_token),
        ("v", "5.103")
    )
    requests.post('https://api.vk.com/method/messages.send', params=params)


@try_repeat
def edit_desciption(args):
    id = args[0]
    name = args[1]
    params = (
        ("owner_id", archive_group_id * -1),
        ("video_id", id),
        ("name", name),
        ("desc",
         "https://vk.com/youtubeupload"),
        ('access_token', user_token),
        ("v", "5.103")
    )
    requests.post('https://api.vk.com/method/video.edit', params=params)
    return id


@try_repeat
def upload_1(name, f, wallpost):
    params = (
        ("name", name),
        ("description", ""),
        ("wallpost", wallpost),
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


@try_repeat
def autoposter(v, quiet=True):
    global limit
    url = 'https://www.youtube.com/watch?v=' + v
    ydl_opts = {}
    ydl_opts['outtmpl'] = "/home/intromenoff/SIPM/video/%(title)s.%(ext)s"
    ydl_opts['quiet'] = quiet
    ydl_opts['merge_output_format'] = 'mp4'

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        result = ydl.extract_info(url, download=False)
        outfile = ydl.prepare_filename(result)
        views = result.get('view_count')
        # duration = result.get('duration')
    if views >= 100000 and limit < 50:
        wallpost = 1
        limit += 1
    else:
        wallpost = 0
    n = outfile
    id_vk, name_vk = upload_1("".join(list(n)[29:len(n) - 4]), n, wallpost)
    os.remove(n)
    return id_vk, name_vk


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.text.lower() == 'хочу видео':
            if event.from_user:
                vk.messages.send(
                    user_id=event.user_id,
                    message='Здравствуйте, вам предоставлена недельная подписка\n'
                            '\nВы можете запросить одно видео в день'
                            '\nДля запроса пришлите ссылку на нужное вам видео. Длинна видео не должна превышать час\n'
                            '\nВ зависимости от длинны видео мы пришлем его вам через 1-180 ми\n'
                            '\nP.S. бот в бета тесте возможны неполадки\n',
                    random_id=randint(0, 19999),
                )

        elif len(event.text) == 43:
            if event.from_user:
                vk.messages.send(
                    user_id=event.user_id,
                    message="Загрузка видео начата, ожидайте",
                    random_id=randint(0, 19999)
                )
                send_video(edit_desciption(autoposter(event.text[32:])), event.user_id)

        elif len(event.text) == 28:
            if event.from_user:
                vk.messages.send(
                    user_id=event.user_id,
                    message="Загрузка видео начата, ожидайте",
                    random_id=randint(0, 19999)
                )
                send_video(edit_desciption(autoposter(event.text[17:])), event.user_id)

        elif len(event.text) == 41:
            if event.from_user:
                vk.messages.send(
                    user_id=event.user_id,
                    message="Загрузка видео начата, ожидайте",
                    random_id=randint(0, 19999)
                )
                send_video(edit_desciption(autoposter(event.text[30:])), event.user_id)

        else:
            if event.from_user:
                vk.messages.send(
                    user_id=event.user_id,
                    message="Я распознаю лишь ссылки",
                    random_id=randint(0, 19999),
                )
    if day != datetime.datetime.now().day:
        day = datetime.datetime.now().day
        limit = 0
