from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
import os, shutil
import json
import random
from plugins.music_dl.__main__ import Music
from django.utils.encoding import escape_uri_path


songs_path = os.path.realpath(os.path.join(__file__, "../../static/music_data/songs/"))
back_path = os.path.realpath(os.path.join(__file__, "../../static/music_data/songs_back/"))


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
    # 遍历songs目录, 获取所有歌曲文件名并区分歌曲名与歌手名
    songs_list = os.listdir(songs_path)
    name_or_singer = [song.replace(".mp3", '').split('-') for song in songs_list]

    # 如果目录下存在有两个"-"的文件名则视为强制置顶排序歌曲(表白用的), 下面举个例子
    # 李宗盛 - 我终于失去了你 - 1.mp3
    # 陈奕迅 - 爱情转移 - 2.mp3
    # 王力宏 - 你是我心内的一首歌 - 3.mp3
    list1 = [name for name in name_or_singer if len(name) == 3]
    list2 = [name for name in name_or_singer if len(name) < 3]

    list1.sort(key=lambda x: int(x[2]))

    rspid1 = [name[2].strip() for name in list1]
    name1 = [name[1].strip() for name in list1]
    singer1 = [name[0].strip() for name in list1]
    songs1 = ["-".join(song) + ".mp3" for song in list1]

    rspid2 = [i + len(rspid1) + 1 for i in range(len(list2))]
    name2 = [name[1].strip() for name in list2]
    singer2 = [name[0].strip() for name in list2]
    songs2 = ["-".join(song) + ".mp3" for song in list2]

    # 将置顶歌曲与其他歌曲合并
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


music_dic = {}


def search_songs(req):
    if req.method == 'POST':
        music_dic['music'] = Music()
        req_data = req.POST
        song_name = req_data.get('song_name')
        resp_data = music_dic['music'].search(song_name)
        # resp_data = [song_name]
        status_code = 200
    elif req.method == 'GET':
        idx = req.GET.get('idx', default='0')
        music_dic['music'].downlod_songs(idx)
        resp_data = ['下载成功']
        status_code = 200
    else:
        resp_data = ['123']
        status_code = 400
    resp = {'status_code': status_code, 'data': resp_data}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def delete_song(req):
    if req.method == 'DEL':
        song_name = req.DEL.get('song')
        song_path = os.path.join(songs_path, song_name)
        if os.path.exists(song_path):
            shutil.move(song_path, os.path.join(back_path, song_name))


def download_song(req):
    # do something...

    def file_iterator(file_name, chunk_size=512):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    if req.method == 'GET':
        song_name = req.GET.get('song').split('/')[-1]
        the_file_name = os.path.join(songs_path, song_name)
        response = StreamingHttpResponse(file_iterator(the_file_name))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(escape_uri_path(song_name))
        return response


if __name__ == '__main__':
    print(get_songs(111))
