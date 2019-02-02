from django.shortcuts import render
from django.http import HttpResponse
import os
import json


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
    songs = os.listdir(songs_path)
    name_or_singer = [song.replace(".mp3", '').split('-') for song in songs]
    name = [name[1].strip() for name in name_or_singer]
    singer = [name[0].strip() for name in name_or_singer]
    bgp_path = os.path.realpath(os.path.join(__file__, "../../static/music_data/images/"))
    bgp = os.listdir(bgp_path)
    resp_data = {"songs": songs,
                 "bgp": bgp,
                 "name": name,
                 "singer": singer}
    resp = {'status_code': 200, 'data': resp_data}
    print(resp)
    # return resp
    return HttpResponse(json.dumps(resp), content_type="application/json")


if __name__ == '__main__':
    print(get_songs(111))