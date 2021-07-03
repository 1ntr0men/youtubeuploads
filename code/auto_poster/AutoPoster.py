import requests
import json
import os
import feedparser
import youtube_dl

# вк токен
user_token = "b30732fb32903e93bc8721645cac119be3a7f3d62e399eed73c86d910e33cd98a7ff1b46af442e5f07e74"

# создание словаря
channels = {}

print("Поехали")
print()

# реклама в описании
advertising = ""


def edit_description(id_vk, name_vk):
    params = (
        ("owner_id", -188254964),
        ("video_id", id_vk),
        ("name", name_vk),
        ("desc", advertising),
        ('access_token', user_token),
        ("v", "5.120")
    )
    requests.post('https://api.vk.com/method/video.edit', params=params)


def re():
    global channels
    fin = open("channels.txt", "r", encoding="utf-8")
    for i in range(sum(1 for l in open("channels.txt", "r", encoding="utf-8"))):
        line = fin.readline().split(", ")
        channels[line[0]] = [line[1], line[2].rstrip(), int(line[3])]
    fin.close()


def wr():
    global channels
    fout = open("channels.txt", "w", encoding="utf-8")
    for m, n in channels.items():
        fout.write(m + ", " + n[0] + ", " + n[1] + ", " + str(n[2]) + "\n")
    fout.close()


# функция выгрузки в вк
def upload(name_vk, path, album_id):
    params = (
        ("name", name_vk),
        ("description", ""),
        ("wallpost", 1),
        ('group_id', 188254964),
        ('access_token', user_token),
        ("v", "5.103"),
        ("album_id", album_id)
    )
    response = requests.get('https://api.vk.com/method/video.save', params=params)
    # print(response.text)
    upload_server = json.loads(response.text)['response']['upload_url']
    id_vk = json.loads(response.text)['response']['video_id']
    files = {'video_file': open(path, 'rb')}
    requests.post(upload_server, files=files)
    return id_vk, name_vk


# загрузка и выгрузка в вк кидео
def auto_poster(url, author, album_id, quiet=True):
    print(url)
    ydl_opts = {
        'outtmpl': "..\\..\\video\\%(title)s.%(ext)s",
        'quiet': quiet,
        'merge_output_format': 'mp4'}

    # загрузка
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        result = ydl.extract_info(url, download=False)
        outfile = ydl.prepare_filename(result)

    # выгрузка в вк
    path = outfile
    id_vk, name_vk = upload("{" + author + "} " + "".join(list(path)[9:len(path) - 4]), path, album_id)
    os.remove(path)
    return id_vk, name_vk


# чтение файла channels
re()

# запуск цикла
while True:
    for j, i in channels.items():
        # print(i, j)
        # получение RSS канала и взятие оттуда id последнего видео
        ChannelFeed = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=" + i[0])
        last_video = ChannelFeed.entries[0]
        video_id = last_video.yt_videoid
        # проверка что видео не равно последнему видео записанному в файл
        if video_id != i[1]:
            print("Вышло видео у", last_video.author)
            # изменение последнего видео в файле
            channels[j][1] = video_id
            # сохранение
            wr()
            try:
                id_vk, name_vk = auto_poster('https://www.youtube.com/watch?v=' + video_id, last_video.author, i[2])
                edit_description(id_vk, name_vk)
                print("Запостил " + last_video.title)
                print()
            except Exception as e:
                print("ОШИБКА " + str(e))
                print()
