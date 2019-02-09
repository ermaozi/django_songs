#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author: HJK
@file: main.py
@time: 2019-01-08
"""

import sys
import threading
import click
import logging
from plugins.music_dl import config
from plugins.music_dl.core import music_search, music_download, music_list_merge


class Music():
    music_list = []

    def search(self, keyword):
        config.init()
        config.set("keyword", keyword)
        logger = logging.getLogger(__name__)
        thread_pool = []
        errors = []

        # click.echo(
        #     "\nSearching %s from ..." % colorize(config.get("keyword"), "yellow"), nl=False
        # )

        # 多线程搜索
        for source in config.get("source").split():
            t = threading.Thread(target=music_search, args=(source, self.music_list, errors))
            thread_pool.append(t)
            t.start()
        for t in thread_pool:
            t.join()

        # 分割线
        # click.echo("\n---------------------------\n")
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
            # click.echo(music.info)
        return rsp
        #
        # # 分割线
        # click.echo("\n---------------------------")
        # # 用户指定下载序号
        # prompt = "请输入%s，支持形如 %s 的格式，输入 %s 跳过下载\n >>" % (
        #     colorize("下载序号", "yellow"),
        #     colorize("0 3-5 8", "yellow"),
        #     colorize("N", "yellow"),
        # )
        # choices = click.prompt(prompt)
        # while choices.lower() != "n" and not re.match(
        #     r"^((\d+\-\d+)|(\d+)|\s+)+$", choices
        # ):
        #     choices = click.prompt("%s%s" % (colorize("输入有误！", "red"), prompt))
        #
        # selected_list = get_sequence(choices)
        # for idx in selected_list:

    def downlod_songs(self, idx):
        music_download(idx, self.music_list)

        # 下载完后继续搜索
        # keyword = click.prompt("请输入要搜索的歌曲，或Ctrl+C退出\n >>")
        # config.set("keyword", keyword)
        # run()

    # def main(self, keyword):  # source, count, outdir, proxy, merge, verbose
    #     """
    #         Search and download music from netease, qq, kugou, baidu and xiami.
    #         Example: music-dl -k "周杰伦"
    #     """
    #     # 初始化全局变量
    #     config.init()
    #     config.set("keyword", keyword)
    #
    #     try:
    #         self.search()
    #     except (EOFError, KeyboardInterrupt):
    #         sys.exit(0)


if __name__ == "__main__":
    music = Music()
    music.search('嘿嘿黑')
