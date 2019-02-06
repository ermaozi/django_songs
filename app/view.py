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

    list1 = [name for name in name_or_singer if len(name) == 3]
    list2 = [name for name in name_or_singer if len(name) < 3]

    list1.sort(key=lambda x: int(x[2]))

    rspid1 = [name[2].strip() for name in list1]
    name1 = [name[1].strip() for name in list1]
    singer1 = [name[0].strip() for name in list1]
    songs1 = ["-".join(song)+".mp3" for song in list1]

    rspid2 = [i+len(rspid1)+1 for i in range(len(list2))]
    name2 = [name[1].strip() for name in list2]
    singer2 = [name[0].strip() for name in list2]
    songs2 = ["-".join(song)+".mp3" for song in list2]

    rspid = rspid1 + rspid2
    name = name1 + name2
    singer = singer1 + singer2
    songs = songs1 + songs2

    bgp_path = os.path.realpath(os.path.join(__file__, "../../static/music_data/images/"))
    bgp_file = os.listdir(bgp_path)
    bgp = []
    for i in range(len(songs)):
        bgp.append(bgp_file[random.randint(0, len(bgp_file) - 1)])

    resp_data = []
    for i in range(len(rspid)):
        resp_data.append({
            "rspid": rspid[i],
            "songs": songs[i],
            "bgp": bgp[i],
            "name": name[i],
            "singer": singer[i]
        })
    resp = {'status_code': 200, 'data': resp_data}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def search_songs(req):
    if req.method == 'POST':
        req_data = req.POST
        print(req_data)
        song_name = req_data.get('song_name')
        resp_data = [song_name]
        status_code = 200
    else:
        resp_data = ['123']
        status_code = 400
    resp = {'status_code': status_code, 'data': resp_data}
    return HttpResponse(json.dumps(resp), content_type="application/json")


if __name__ == '__main__':
    print(get_songs(111))
