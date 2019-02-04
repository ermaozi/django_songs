from django.shortcuts import render
from django.http import HttpResponse
import os
import json
import random


def index(req):
    """
    返回首页
    :param req:
    :return:
    """
    return render(req, 'index.html')


def get_songs(req):
    """
    返回音乐列表
    :param req:
    :return:
    """
    songs_path = os.path.realpath(os.path.join(__file__, "../../static/music_data/songs/"))
    songs_list = os.listdir(songs_path)
    name_or_singer = [song.replace(".mp3", '').split('-') for song in songs_list]
    lis1 = [name for name in name_or_singer if len(name) == 3]
    lis2 = [name for name in name_or_singer if len(name) < 3]
    rspid1 = [1, 2, 3, 4]
    name1 = ["我的歌声里", "爱情转移", "曾经", "越单纯越幸福"]
    singer1 = ["曲婉婷", "陈奕迅", "陈晓东", "王筝"]
    songs1 =["曲婉婷 - 我的歌声里 - 1.mp3",
             "陈奕迅 - 爱情转移 - 2.mp3", 
             "陈晓东 - 曾经 - 3.mp3", 
             "王筝 - 越单纯越幸福 - 4.mp3"]
    rspid2 = [i+len(rspid1)+1 for i in range(len(lis2))]
    name2 = [name[1].strip() for name in lis2]
    singer2 = [name[0].strip() for name in lis2]
    songs2 = ["-".join(song)+".mp3" for song in lis2]
    rspid = rspid1 + rspid2
    name = name1 + name2
    singer = singer1 + singer2
    songs = songs1 + songs2
    bgp_path = os.path.realpath(os.path.join(__file__, "../../static/music_data/images/"))
    bgp_file = os.listdir(bgp_path)
    bgp = []
    for i in range(len(songs)):
        bgp.append(bgp_file[random.randint(0, len(bgp_file) - 1)])
    resp_data = {"rspid": rspid,
                 "songs": songs,
                 "bgp": bgp,
                 "name": name,
                 "singer": singer}
    resp = {'status_code': 200, 'data': resp_data}
    print(resp)
    return HttpResponse(json.dumps(resp), content_type="application/json")


if __name__ == '__main__':
    print(get_songs(111))
