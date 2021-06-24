from bs4 import BeautifulSoup
import requests
import feedparser

channels = {}
name_channel = ""
group_id = "188254964"
user_token = "ab983c74fb9103daac4df335621a41a824014322a828ed3a7229e6f3366180b67aeab33fe9b88edda4395"


def l():
    return sum(1 for l in open("channels.txt", "r", encoding="utf-8"))


def re():
    global channels
    fin = open("channels.txt", "r", encoding="utf-8")
    for i in range(l()):
        line = fin.readline().split(", ")
        if list(line[0])[0] != "#":
            channels[line[0][list(line[0]).index("..") + 1::]] = [line[1], line[2], line[3].rstrip()]
    fin.close()


def create_album(title):
    params = (
        ("title", title),
        ('group_id', '188254964'),
        ("v", "5.103"),
        ('access_token', user_token),
    )
    response = requests.get('https://api.vk.com/method/video.addAlbum', params=params)
    return response.text[24:-2]


def wr():
    global channels
    k = 1
    fout = open("channels.txt", "w", encoding="utf-8")
    for m, n in channels.items():
        fout.write(str(k) + "." + m + ", " + n[0] + ", " + n[1] + ", " + n[2] + "\n")
        k += 1
    fout.close()


def copy():
    r = open("../reserve.txt", "w", encoding="utf-8")
    c = open("channels.txt", "r", encoding="utf-8")
    for i in range(l()):
        z = c.readline()
        r.write(z)


copy()
re()

print("Я готов")

while name_channel != "1":
    name_channel = input()
    if name_channel != "1":
        url = 'https://www.youtube.com/' + name_channel
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        channel_id = soup.findAll("link")[4]["href"][32:]
        ChannelFeed = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=" + channel_id)
        s = ChannelFeed.entries[0]
        channels[s.author] = [channel_id, s.yt_videoid, create_album(s.author)]
        print("Еще")

print("Все")

wr()
