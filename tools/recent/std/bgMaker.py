import package.Config.config as configs
from PIL import Image
from PIL import ImageFilter
from loguru import logger
from package.Image.resize import stretchZoom
import ujson


class BgMaker:
    """
    background处理
    """
    def __init__(self, info):
        self.bgconfig = configs.RecentPlay().BackGround()
        logger.info('获取模板设置信息')

        bg_dir = str(info.bg_dir())  # 获取now listening背景
        logger.info('获取now listening背景图片')

        if bg_dir[-3:] == 'png' or bg_dir[-3:] == 'jpg':  # 判断后缀做背景
            bg = bg_dir
        else:
            bg = self.bgconfig.bgifnon()  # 没有背景的话使用设置里设置的背景
            logger.warning('获取失败，使用自定义背景')

        self.bg = Image.open(bg).convert('RGB')
        logger.info('转换背景格式')

    def bg(self):
        """
        对background进行处理并返回
        :return: pil图像
        """
        dim = self.bgconfig.dim()
        blur = self.bgconfig.blur()
        model = ujson.load(r'model\RecentPlay\model.json')
        weight = model['imgSize']['weight']
        height = model['imgSize']['height']

        im = self.bg()

        im = im.filter(ImageFilter.GaussianBlur(radius=blur))  # 高斯模糊
        logger.info(f'对背景进行{blur}像素半径高斯模糊')
        im = im.point(lambda p: p * dim)  # 背景暗化
        logger.info(f'对背景进行{dim}暗化')
        im = stretchZoom(im, weight, height)
        logger.info('对背景图片进行等比拉伸')
        return im

