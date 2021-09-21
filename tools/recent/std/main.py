from package.info.std import StdInfo
from loguru import logger
import bgMaker
from PIL import Image
import ujson
import package.Config.config as configs
from .memPlayTime import get_played_time
from package.Image.infoPrint import info_print
from time import localtime
from time import strftime


def main():
    """
    执行程序，生成成绩图
    :return: 无
    """
    logger.info('获取信息')
    info = StdInfo()

    logger.info('判断游戏状态')
    stat = status(info)
    if stat:
        im = bg(info)
        im.show()
        ifSave(im)
    else:
        logger.error('游戏状态不正确')
        return


def status(info):
    """
    判断游戏状态是否为std的结算或Fail界面
    :param info:gosu已经读取为py对象的json
    :return:True或者False
    """

    def menuState():
        if info.state() == 7 or 2:  # 判断打完图或回放后或者fail的结算或者暂停界面
            logger.info('确认在指定界面')
            return True
        else:
            logger.error('不在指定界面')
            return False

    def modeState():
        if info.mode() == 0:  # 判断mode是否为Std
            logger.info('确认模式为std')
            return True
        else:
            logger.info('模式不为std')
            return False

    try:
        if menuState() and modeState():
            logger.info('通过gosu确认游戏状态正确')
            return True
        else:
            logger.info('通过gosu确认游戏状态失败')
            return False
    except Exception:
        return False


def bg(info):
    """
    获取处理background并做好信息模板
    :param info:gosu已经读取为py对象的json
    :return: pil图像格式的带bg的模板
    """
    def paste(model, bg):
        """
        合并背景和模板，需要大小相同
        :param model: jpg或者png模板路径
        :param bg: pil格式背景
        :return:pil格式的已经合并完背景和模板的图片
        """
        logger.info('合并背景图与模板')
        im = bg.paste(model, (0, 0), model)
        return im

    logger.info('处理背景图片')
    bg = bgMaker.BgMaker(info)
    bg.bg()
    logger.info('背景图片处理完毕')

    modelJson = ujson.load(r'model/RecentPlay/model.json')
    im = paste(modelJson['modelBg'], bg)
    return im


def output(im, info):
    """
    输出各项信息
    :param im:传入带bg的pil格式的模板图片
    :param info: 传入gosu信息
    :return: pil格式图片
    """
    logger.info('准备输出信息')
    logger.info('加载模板文件')
    jsonInfo = ujson.load(r'model/RecentPlay/model.json')['info']

    def playTime(im):
        """
        使用项目根目录下的GameTime.dll对游戏结算界面的游玩时间进行读取
        若因为任何原因读取失败则使用本地实际按
        :return:
        """
        try:
            logger.info('读取游玩时间')
            time_str = eval(str(get_played_time()))[0]
            time = time_str.split(' ')
            time[1] = time[1].split(':')[0] + ':' + time[1].split(':')[1]
        except Exception as e:
            logger.warning('时间读取失败，采用本机时间')
            time_str = strftime("%Y/%m/%d %H:%M", localtime())
            time = time_str.split(' ')
            time[1] = time[1].split(':')[0] + ':' + time[1].split(':')[1]

        i = jsonInfo['playTimeDay']
        im = info_print(im, )
        '''Coding now'''
        '''正在写时间输出模块'''
        return im
    return im


def ifSave(im, info):
    """
    由程序最后部分调用，根据配置文件内的配置，选择性保存成绩图
    若某成绩设置了保存，则
    :param im: 程序图像
    :param info: 传入
    :return: 无
    """
    allConfig = configs.RecentPlay()
    autoSaveConfig = allConfig.AutoSave()

    if autoSaveConfig.rankAutoSave(info.rank_result()):
        im.save(r'data/recentPlay')
        im.close()
    elif autoSaveConfig.accAutoSave() <= info.accuracy():
        im.save(r'data/recentPlay')
        im.close()
    else:
        sec = input('是否保存成绩图？(Y/N)')
        if sec == 'Y' or sec == 'y':
            im.save(r'data/recentPlay')
            im.close()
        else:
            pass


