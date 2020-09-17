from pytube import YouTube, exceptions
import requests
import json
import os
import feedparser
import sys

user_token = "799900f75b07c42aea8ecee5648f85a6e240ae525fb382c30f45b4356107ad24fa1eb3f16fb279349c851"
channels = {}
dev = False
if len(sys.argv) > 1:
    dev = sys.argv[1]
print(dev)

print("Поехали")
print()


def re():
    global channels
    fin = open("channels.txt", "r", encoding="utf-8")
    for i in range(sum(1 for l in open("channels.txt", "r", encoding="utf-8"))):
        line = fin.readline().split(", ")
        channels[line[0][list(line[0]).index(".") + 1::]] = [line[1], line[2].rstrip(), int(line[3])]
    fin.close()


def wr():
    global channels
    k = 1
    fout = open("channels.txt", "w", encoding="utf-8")
    for m, n in channels.items():
        fout.write(str(k) + "." + m + ", " + n[0] + ", " + n[1] + ", " + str(n[2]) + "\n")
        k += 1
    fout.close()


def upload(name, f, album_id):
    params = (
        ("name", name),
        ("description", ""),
        ("wallpost", 1),
        ('group_id', '188254964'),
        ('access_token', user_token),
        ("v", "5.103"),
        ("album_id", album_id)
    )

    response = requests.get('https://api.vk.com/method/video.save', params=params)
    # print(response.text)
    upload_server = json.loads(response.text)['response']['upload_url']
    # vid = json.loads(response.text)['response']['video_id']
    files = {'video_file': open(f, 'rb')}
    requests.post(upload_server, files=files)


def autoposter(v, author, album_id):
    if not dev:
        try:
            a = YouTube('https://www.youtube.com/watch?v=' + v).streams.get_by_itag('22').download(
                output_path="D:\\Autoposter\\video\\")

            # b = YouTube('https://www.youtube.com/watch?v=' + v)
            # videos = b.streams.all()
            # for v in videos:
            #     print(v)

            n = a.title()
            # print(n)
            upload("{" + author + "} " + "".join(list(n)[20:len(n) - 4]), n, album_id)
            os.remove(n)
            return 0
        except exceptions.LiveStreamError as E:
            return 1
        except KeyError:
            return 2
    else:
        a = YouTube('https://www.youtube.com/watch?v=' + v).streams.get_by_itag('22').download(
            output_path="D:\\Autoposter\\video\\")
        n = a.title()
        upload("{" + author + "} " + "".join(list(n)[20:len(n) - 4]), n, album_id)
        os.remove(n)


re()
# print(channels)
while True:
    for j, i in channels.items():
        # print(i, j)
        ChannelFeed = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=" + i[0])
        s = ChannelFeed.entries[0]
        if s.yt_videoid != i[1]:
            print("Вышло видео у", s.author)
            channels[j][1] = s.yt_videoid
            wr()
            if autoposter(s.yt_videoid, s.author, i[2]) == 0:
                print("Запостил " + s.title)
                print()
            elif autoposter(s.yt_videoid, s.author, i[2]) == 1:
                print("Стрим")
                print()
            else:
                print("ОШИБКА")
                print()
