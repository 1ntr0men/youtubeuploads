from pytube import YouTube
import requests
import json
import os
import feedparser

user_token = "799900f75b07c42aea8ecee5648f85a6e240ae525fb382c30f45b4356107ad24fa1eb3f16fb279349c851"
channels = {}

print("Поехали")
print()

advertising = ""


def edit_description(id_vk, name_vk):
    params = (
        ("owner_id", -188254964),
        ("video_id", id_vk),
        ("name", name_vk),
        ("desc", advertising),
        ('access_token', user_token),
        ("v", "5.103")
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
    upload_server = json.loads(response.text)['response']['upload_url']
    id_vk = json.loads(response.text)['response']['video_id']
    files = {'video_file': open(path, 'rb')}
    requests.post(upload_server, files=files)
    return id_vk, name_vk


def auto_poster(v, author, album_id):
    a = YouTube('https://www.youtube.com/watch?v=' + v).streams.get_by_itag('22').download(
        output_path="D:\\AutoPoster\\video\\")
    path = a.title()
    print(path)
    id_vk, name_vk = upload("{" + author + "} " + "".join(list(path)[22:len(path) - 4]), path, album_id)
    os.remove(path)
    return id_vk, name_vk


re()
while True:
    for j, i in channels.items():
        # print(i, j)
        ChannelFeed = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=" + i[0])
        last_video = ChannelFeed.entries[0]
        video_id = last_video.yt_videoid
        if video_id != i[1]:
            print("Вышло видео у", last_video.author)
            channels[j][1] = video_id
            wr()
            try:
                id_vk, name_vk = auto_poster(video_id, last_video.author, i[2])
                edit_description(id_vk, name_vk)
                print("Запостил " + last_video.title)
                print()
            except:
                print("ОШИБКА")
                print()
