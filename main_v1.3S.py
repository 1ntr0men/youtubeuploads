import requests
import json
import os
import feedparser
import youtube_dl

user_token_starui = "3edd95bd76f97fe72d795a5ccb63e510a3dee144a1ce8d74d33941e4cdda64008ab49636f817e30cb3b3f"  # Хирошима
user_token_ak = "f42192a74ce719b76b79971f6905be446373022406ee0544797fa52d5fe094b09d2390ddf58b4b3c2b5d1"  # Акакий
user_token_intromen = "ab983c74fb9103daac4df335621a41a824014322a828ed3a7229e6f3366180b67aeab33fe9b88edda4395"
user_token = "ce9b9828b611e1993be1cb4e37383cb4d52c2bf250947661fecb530780d318f92038ce6fccc73bee4db47"


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


def auto_poster(url, author, album_id, quiet=True):
    print(url)
    ydl_opts = {}
    ydl_opts['outtmpl'] = "D:\\AutoPoster\\video\\%(title)s.%(ext)s"
    ydl_opts['quiet'] = quiet
    ydl_opts['merge_output_format'] = 'mp4'

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        result = ydl.extract_info(url, download=False)
        outfile = ydl.prepare_filename(result)

    path = outfile
    id_vk, name_vk = upload("{" + author + "} " + "".join(list(path)[20:len(path) - 4]), path, album_id)
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
                id_vk, name_vk = auto_poster('https://www.youtube.com/watch?v=' + video_id, last_video.author, i[2])
                edit_description(id_vk, name_vk)
                print("Запостил " + last_video.title)
                print()
            except:
                print("ОШИБКА")
                print()
