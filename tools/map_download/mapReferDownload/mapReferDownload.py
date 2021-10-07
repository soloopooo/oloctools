import asyncio
import os
import re
import httpx
import ujson

from package.Config.config import Download as downloadConfig
from package.osuDatabase.osu_db import create_db as osu_db_export
from package.osuDatabase.osu_db import OsuDB
from package.Config.config import Proxy
from package.osuDir import songsDir
from package.osuDir import osuDirGet
from loguru import logger


def main():
    """
    指定参数铺面下载主函数
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

    loader = Downloader(proxy)
    asyncio.run(loader.run())
    input('按下回车返回')


DOWNLOAD_PATH = songsDir()


def postData():
    
    data = {
        'cmd': 'beatmaplist',
        'type': 'search',  # 4: search
        'mode': 1   # 1: std
    }

    print('铺面状态：\n'
          '1 = Ranked & Approved\n'
          '2 = Qualified\n'
          '4 = Loved\n'
          '8 = Pending & WIP\n'
          '16 = Graveyard')
    try:
        mapClass = int(input('请输入要搜刮的铺面状态 (default:1): '))
    except Exception:
        mapClass = None
    data['class'] = mapClass if mapClass is not None else 1

    try:
        starsL = float(input('请输入最低stars (default:0): '))
    except Exception:
        starsL = None
    try:
        starsH = float(input('请输入最高stars (default:1000): '))
    except Exception:
        starsH = None
    data['stars'] = [starsL if starsL is not None else 0.0, starsH if starsH is not None else 1000.0]

    try:
        arL = float(input('请输入最低ar (default:0): '))
    except Exception:
        arL = None
    try:
        arH = float(input('请输入最高ar (default:1000): '))
    except Exception:
        arH = None
    data['ar'] = [arL if arL is not None else 0.0, arH if arH is not None else 1000.0]

    try:
        odL = float(input('请输入最低od (default:0): '))
    except Exception:
        odL = None
    try:
        odH = float(input('请输入最高od (default:1000): '))
    except Exception:
        odH = None
    data['od'] = [odL if odL is not None else 0.0, odH if odH is not None else 1000.0]

    try:
        hpL = float(input('请输入最低hp (default:0): '))
    except Exception:
        hpL = None
    try:
        hpH = float(input('请输入最高hp (default:1000): '))
    except Exception:
        hpH = None
    data['hp'] = [hpL if hpL is not None else 0.0, hpH if hpH is not None else 1000.0]

    try:
        csL = float(input('请输入最低cs (default:0): '))
    except Exception:
        csL = None
    try:
        csH = float(input('请输入最高cs (default:1000): '))
    except Exception:
        csH = None
    data['cs'] = [csL if csL is not None else 0.0, csH if csH is not None else 1000.0]

    try:
        lengthL = float(input('请输入最低length (输入数字，秒数)(default:0): '))
    except Exception:
        lengthL = None
    try:
        lengthH = float(input('请输入最高length (输入数字，秒数)(default:1000): '))
    except Exception:
        lengthH = None
    data['length'] = [lengthL if lengthL is not None else 0.0, lengthH if lengthH is not None else 1000.0]

    try:
        bpmL = float(input('请输入最低bpm (default:0): '))
    except Exception:
        bpmL = None
    try:
        bpmH = float(input('请输入最高bpm (default:1000): '))
    except Exception:
        bpmH = None
    data['bpm'] = [bpmL if bpmL is not None else 0.0, bpmH if bpmH is not None else 1000.0]

    return data


# 引用自vincentmathis/osu-beatmap-downloader
# 部分引用自vincentmathis/osu-beatmap-downloader
class Downloader:
    """
    下载类
    """

    def __init__(self, proxy):
        self.beatmapsets = []
        self.postdata = postData()
        self.dConfig = downloadConfig()
        self.limit = float(input('请输入下载量，建议200以内:'))
        self.offset = 0

        i = input('是否下载无视频版本(y/n):')
        if i == "Y" or i == "y":
            self.no_video = True
        else:
            self.no_video = False

        # 检测代理
        self.proxy = proxy
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

    def scrape_beatmapsets(self, limit):
        """
        从sayo镜像站获取热门铺面信息，并添加铺面json至self.beatmapsets
        :return: 铺面信息添加至self.beatmapsets
        """
        url = "https://api.sayobot.cn/?post"
        data = self.postdata

        if limit > 200:  # 如果要搜的图大于200
            while limit > 200:  # 当大于200  循环进行200个铺面的搜索
                data['limit'] = 200
                data['offset'] = self.offset
                r = self.session.post(url, data=ujson.dumps(data))
                r = r.json()
                # 遍历 输入所有搜索到的铺面信息
                for i in r['data']:
                    self.beatmapsets.append(i)
                limit -= 200  # 数量-200，准备下一轮
                self.offset = r['endid']  # 获取最后的位置偏移

            if limit > 0:  # while结束，如果还有大于0小于200的图未搜索
                data['limit'] = limit
                data['offset'] = self.offset
                r = self.session.post(url, data=ujson.dumps(data))
                r = r.json()
                # 遍历 输入所有搜索到的铺面信息
                for i in r['data']:
                    self.beatmapsets.append(i)
                self.offset = r['endid']  # offset添加，为查重后再次搜索做准备

        else:  # 如果要搜的图小于200
            data['limit'] = limit
            if self.offset > 0:  # 如果大于0
                data['offset'] = self.offset  # 添加offset参数
            r = self.session.post(url, data=ujson.dumps(data))
            r = r.json()
            # 遍历 输入所有搜索到的铺面信息
            for i in r['data']:
                self.beatmapsets.append(i)
            self.offset = r['endid']
        num_beatmapsets = len(self.beatmapsets)
        logger.success(f"获取到了 {num_beatmapsets} beatmapsets")

    def remove_existing_beatmapsets(self):
        """
        移除已经存在于Songs文件夹的铺面
        读取osu!.db数据库
        :return: 修改self.beatmapsets
        """
        # 获取已经存在的所有铺面 输出列表
        self.scrape_beatmapsets(self.limit)  # 先获取再查重嘛
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
            input()
            limit = self.limit - len(self.beatmapsets)  # 筛掉的图的量
            # 搜索筛掉的图的量，从上次搜索的最后开始，顺便更新offset
            self.scrape_beatmapsets(limit)

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
        headers = {
            "Referer": "https://github.com/Adsicmes/oloctools"}  # 项目地址，下载必标
        download_url = r'https://dl.sayobot.cn/beatmaps/download/full/' + \
            str(beatmapset['sid'])
        if self.no_video:
            download_url = r'https://dl.sayobot.cn/beatmaps/download/novideo/' + \
                str(beatmapset['sid'])
        async with sem:  # 限制并发数
            async with httpx.AsyncClient(timeout=self.dConfig.timeout(), headers=headers) as client:
                logger.info(
                    f"下载铺面ing: sid{beatmapset['sid']}--{beatmapset['title']}")
                response = await client.get(download_url)
                if response.status_code == 200:
                    logger.success(
                        f"sid{beatmapset['sid']} code:{response.status_code} - 下载成功")
                    self.write_beatmapset_file(f"{beatmapset['sid']} {beatmapset['artist']}-{beatmapset['title']}",
                                               response.content)
                else:
                    logger.error(
                        f"sid{beatmapset['sid']} code:{response.status_code} - 下载失败")

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
