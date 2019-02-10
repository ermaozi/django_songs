#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author: HJK
@file: main.py
@time: 2019-01-08
"""

import threading
import logging
from plugins.music_dl import config
from plugins.music_dl.core import music_search, music_download, music_list_merge


class Music():

    def __init__(self):
        self.music_list = []

    def search(self, keyword):
        try:
            config.init()
            config.set("keyword", keyword)
            logger = logging.getLogger(__name__)
            thread_pool = []
            errors = []

            # 多线程搜索
            for source in config.get("source").split():
                t = threading.Thread(target=music_search, args=(source, self.music_list, errors))
                thread_pool.append(t)
                t.start()
            for t in thread_pool:
                t.join()

            # 分割线
            # 输出错误信息
            for err in errors:
                logger.error("Get %s music list failed." % err[0].upper())
                logger.error(err[1])
            # 对搜索结果排序和去重
            if config.get("merge"):
                self.music_list = music_list_merge(self.music_list)
            # 遍历输出搜索列表
            rsp = []
            for index, music in enumerate(self.music_list):
                music.idx = index
                rsp.append({
                    'title': music.title,
                    'singer': music.singer,
                    'source': music.source,
                    'duration': music.duration,
                    'size': music.size,
                    'url': music._url
                })
            return rsp
        finally:
            pass

    def downlod_songs(self, idx):
        music_download(idx, self.music_list)


if __name__ == "__main__":
    music = Music()
    music.search('嘿嘿黑')
