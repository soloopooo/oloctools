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

    limit = float(input('请输入下载量，建议200以内:'))
    i = input('是否下载无视频版本(y/n):')

    if i == "Y" or i == "y":
        no_video = True
    else:
        no_video = False

    loader = Downloader(limit, no_video, proxy)
    # asyncio.run(loader.run())
    input('按下回车返回')


DOWNLOAD_PATH = songsDir()


# 部分引用自vincentmathis/osu-beatmap-downloader
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

        
        self.remove_existing_beatmapsets()

    def scrape_beatmapsets(self, limit, local_offset=0):
        """
        从sayo镜像站获取热门铺面信息，并添加铺面json至self.beatmapsets
        :return: 铺面信息添加至self.beatmapsets
        """
        url = "https://api.sayobot.cn/beatmaplist"

        if limit > 200:  # 如果要搜的图大于200
            offset = local_offset  # 初始化偏移
            while limit > 200:  # 当大于200  循环进行200个铺面的搜索
                params = {
                    "O": offset,  # 从偏移位置搜索
                    "L": 200,
                    "T": 1,  # type hot
                    "M": 1,  # mode std
                    "C": 1,  # class Ranked&Approved
                }
                r = self.session.get(url, params=params)
                r = r.json()
                # 遍历 输入所有搜索到的铺面信息
                for i in r['data']:
                    self.beatmapsets.append(i)
                limit -= 200  # 数量-200，准备下一轮
                offset += 200  # 偏移+200，准备下一轮

            if limit > 0:  # while结束，如果还有大于0小于200的图未搜索
                params = {
                    "O": offset,  # 从offset开始
                    "L": limit,  # 搜索剩余量的图
                    "T": 1,  # type hot
                    "M": 1,  # mode std
                    "C": 1,  # class Ranked&Approved
                }   
                r = self.session.get(url, params=params)
                r = r.json()
                # 遍历 输入所有搜索到的铺面信息
                for i in r['data']:
                    self.beatmapsets.append(i)
                offset += limit  # offset添加，为查重后再次搜索做准备
                
        else:  # 如果要搜的图小于200
            params = {
                "L": limit,  # 目标数量的图
                "T": 1,  # type hot
                "M": 1,  # mode std
                "C": 1,  # class Ranked&Approved
            }
            if local_offset > 0:  # 如果大于0，也就是筛图后的搜图
                params['O'] = local_offset  # 添加offset参数
            r = self.session.get(url, params=params)
            r = r.json()
            # 遍历 输入所有搜索到的铺面信息
            for i in r['data']:
                self.beatmapsets.append(i)
            offset = limit
        num_beatmapsets = len(self.beatmapsets)
        logger.success(f"获取到了 {num_beatmapsets} beatmapsets")
        return offset  # 返回搜索完的位置

    def remove_existing_beatmapsets(self):
        """
        移除已经存在于Songs文件夹的铺面
        读取osu!.db数据库
        :return: 修改self.beatmapsets
        """
        # 获取已经存在的所有铺面 输出列表
        offset = self.scrape_beatmapsets(self.limit)  # 先获取再查重嘛, offset是为筛掉图做准备
        origin_maps = len(self.beatmapsets)  # 筛掉之前的铺面量
        logger.info('铺面查重')
        logger.info('导出osu!.db')
        osu_db_export(osuDirGet() + 'osu!.db')  # 导出当前osu!.db为sqlite3
        database = OsuDB()
        logger.info('获取sid')
        bmset = database.beatmapset()

        n = 0
        map_to_del = []  # 要删的图
        for i in self.beatmapsets:
            if i['sid'] in bmset:
                logger.info(f"铺面 sid:{i['sid']}--{i['title']} 已经下载过了.")
                map_to_del.append(n)  # 添加的是该图的索引
            n += 1

        map_to_del.sort(reverse=True)  # 反向排序，从最后删，否则索引会变
        for i in map_to_del:
            self.beatmapsets.pop(i)  # 按照索引删图
            
        now_maps = len(self.beatmapsets)  # 筛选后的map量
        logger.info(f'目前有{now_maps}张铺面进入预下载队列')
        while self.limit > len(self.beatmapsets):  # 如果筛掉了map，循环，直到够量
            logger.info('不够量，再次获取！')
            limit = origin_maps - now_maps  # 筛掉的图的量
            origin_maps = len(self.beatmapsets)
            offset = self.scrape_beatmapsets(limit, offset)  # 搜索筛掉的图的量，从上次搜索的最后开始，顺便更新offset

            # 新一轮筛图
            n = 0
            map_to_del = []  # 要删的图
            for i in self.beatmapsets:
                if i['sid'] in bmset:
                    logger.info(f"铺面 sid:{i['sid']}--{i['title']} 已经下载过了.")
                    map_to_del.append(n)  # 添加的是该图的索引
                n += 1

            map_to_del.sort(reverse=True)  # 反向排序，从最后删，否则索引会变
            for i in map_to_del:
                self.beatmapsets.pop(i)  # 按照索引删图
                
            now_maps = len(self.beatmapsets)  # 筛选后的map量
            logger.info(f'目前有{now_maps}张铺面进入预下载队列')

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
        logger.success(f"文件{filename}写入成功")

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
