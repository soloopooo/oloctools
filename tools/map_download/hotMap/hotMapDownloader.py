import asyncio
import os
import re

from package.Config.config import Download as downloadConfig
from package.osuDatabase.osu_db import create_db as osu_db_export
from package.osuDatabase.osu_db import OsuDB
from package.Config.config import Proxy
from package.osuDir import songsDir
from package.osuDir import osuDirGet
from loguru import logger
import httpx


def main():
    """
    热门ranked铺面下载主函数
    :return: 无
    """
    con = Proxy()  # 配置文件代理类
    # 判断代理
    if con.httpProxy() is not None:
        if con.switch_hotMapDownload() is True:
            proxy = f'{con.httpProxy()}'
        else:
            proxy = None
    else:
        proxy = None

    limit = float(input('请输入下载量，建议500以内:'))
    i = input('是否下载无视频版本(y/n):')

    if i == ("Y" or "y"):
        no_video = True
    else:
        no_video = False

    loader = Downloader(limit, no_video, proxy)
    asyncio.run(loader.run())
    input('按下回车返回')


DOWNLOAD_PATH = songsDir()


# 引用自vincentmathis/osu-beatmap-downloader
class Downloader:
    """
    下载类
    """

    def __init__(self, limit, no_video, proxy):
        self.beatmapsets = []
        self.limit = limit
        self.no_video = no_video
        self.proxy = proxy
        self.dConfig = downloadConfig()

        # 检测代理
        proxies = {
            'http://': proxy,  # http://localhost:54433
            'https://': proxy
        }
        headers = {"Referer": "https://github.com/Adsicmes/oloctools"}
        if proxy is not None:
            logger.info(f'检测到代理，设置代理: {proxy}')
            self.session = httpx.Client(proxies=proxies, headers=headers)
        else:
            self.session = httpx.Client(headers=headers)

        self.scrape_beatmapsets()
        self.remove_existing_beatmapsets()

    def scrape_beatmapsets(self):
        """
        从sayo镜像站获取热门铺面信息，并添加铺面json至self.beatmapsets
        :return: 无
        """
        url = "https://api.sayobot.cn/beatmaplist"
        params = {
            "L": self.limit,  # 数量限制
            "T": 1,  # type hot
            "M": 1,  # mode std
            "C": 1,  # class Ranked&Approved
        }
        r = self.session.get(url, params=params)
        r = r.json()
        # 遍历 输入所有搜索到的铺面信息
        for i in r['data']:
            self.beatmapsets.append(i)
        num_beatmapsets = len(self.beatmapsets)
        logger.success(f"获取到了 {num_beatmapsets} beatmapsets")

    def remove_existing_beatmapsets(self):
        """
        移除已经存在于Songs文件夹的铺面
        读取osu!.db数据库
        :return: 无
        """
        # 获取已经存在的所有铺面 输出列表
        logger.info('铺面查重')
        logger.info('导出osu!.db')
        osu_db_export(osuDirGet() + 'osu!.db')  # 导出当前osu!.db为sqlite3
        database = OsuDB()
        logger.info('获取sid')
        bmset = database.beatmapset()
        n = 0
        map_to_del = []
        for i in self.beatmapsets:
            if i['sid'] in bmset:
                logger.info(f"铺面 sid:{i['sid']}--{i['title']} 已经下载过了.")
                map_to_del.append(n)
            n += 1

        map_to_del.sort(reverse=True)
        for i in map_to_del:
            self.beatmapsets.pop(i)
        logger.success(f'筛选出了{len(self.beatmapsets)}张铺面')

    async def download_beatmapset_file(self, beatmapset, sem):
        """
        异步函数，下载铺面
        :param beatmapset: sayo获取到的铺面信息dict{}
        :param sem: 最大并发数
        :return: 无
        """
        headers = {"Referer": "https://github.com/Adsicmes/oloctools"}  # 项目地址，下载必标
        download_url = r'https://dl.sayobot.cn/beatmaps/download/full/' + str(beatmapset['sid'])
        if self.no_video:
            download_url = r'https://dl.sayobot.cn/beatmaps/download/novideo/' + str(beatmapset['sid'])
        async with sem:  # 限制并发数
            async with httpx.AsyncClient(timeout=self.dConfig.timeout(), headers=headers) as client:
                logger.info(f"下载铺面ing: sid{beatmapset['sid']}--{beatmapset['title']}")
                response = await client.get(download_url)
                if response.status_code == 200:
                    logger.success(f"sid{beatmapset['sid']} code:{response.status_code} - 下载成功")
                    self.write_beatmapset_file(f"{beatmapset['sid']} {beatmapset['artist']}-{beatmapset['title']}",
                                               response.content)
                else:
                    logger.error(f"sid{beatmapset['sid']} code:{response.status_code} - 下载失败")

    def write_beatmapset_file(self, filename, data):
        """
        写入文件
        :param filename: 文件名，不能在文件名内出现的字符会被替换
        :param data: 数据
        :return: 无
        """
        ILLEGAL_CHARS = re.compile(r"[\<\>:\"\/\\\|\?*]")  # 非法字符
        fn = ILLEGAL_CHARS.sub("_", filename)  # 正则替换文件名
        file_path = os.path.join(DOWNLOAD_PATH, f"{fn}.osz")  # 构建文件完整路径
        logger.info(f"写入文件: {file_path}")
        with open(file_path, "wb") as outfile:
            outfile.write(data)
        logger.success("文件写入成功")

    async def run(self):
        """
        运行主程序
        :return: 无
        """
        sem = asyncio.Semaphore(self.dConfig.maxDownloadAtSame())  # 并发限制类
        task_list = []
        n = 0
        for i in self.beatmapsets:
            task = asyncio.create_task(self.download_beatmapset_file(i, sem))
            task_list.append(task)
            n += 1
        await asyncio.gather(*task_list)
        logger.info(" 下载结束 ".center(50, "#") + "\n")
