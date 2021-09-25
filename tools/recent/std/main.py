from re import X
from package.info.std import StdInfo
from loguru import logger
from .bgMaker import BgMaker
from PIL import Image
from package.Image.pilJudge import pilJudge
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
        ifSave(im, info)
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
        x = Image.open(model)
        logger.info('合并背景图与模板')
        x = x.convert('RGBA')
        bg = bg.convert('RGBA')
        # im = bg.paste(x, (0, 0, bg.width, bg.height)).convert('RGB')
        bg.paste(x, (0, 0), x)
        return bg

    logger.info('处理背景图片')
    bgMaker = BgMaker(info)
    bg = bgMaker.bgMake()
    logger.info('背景图片处理完毕')

    modelJson = ujson.load(open(r'model/RecentPlay/model.json'))
    im = paste(modelJson['modelBg'], bg)
    im = output(im, info)
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
    jsonInfo = ujson.load(open(r'model/RecentPlay/model.json'))['info']

    def playTime(im):
        """
        打印时间
        时间采用本地时间
        :return: pil格式图像
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

        '''try:
            logger.info('读取本地时间')
            time_str = strftime("%Y/%m/%d %H:%M", localtime())
            time = time_str.split(' ')
            time[1] = time[1].split(':')[0] + ':' + time[1].split(':')[1]
        except Exception as e:
            logger.error('本地时间读取失败，错误:{e}')
            return'''

        i = jsonInfo['playTime']['playTimeDay']
        color = (i['color']['r'], i['color']['g'], i['color']['b'])
        im = info_print(im, time[0], i['size'], i['font'],
                        i['location']['x'], i['location']['y'],
                        color, i['align'])
        
        i = jsonInfo['playTime']['playTimeMin']
        color = (i['color']['r'], i['color']['g'], i['color']['b'])
        im = info_print(im, time[1], i['size'], i['font'],
                        i['location']['x'], i['location']['y'],
                        color, i['align'])
        return im

    def normalInfo(im, info):
        """[summary]
        打印一般的，不需要或只需要简单处理的信息
        Args:
            im (pil图像): pil图像
            info (gosu信息): gosu信息

        Returns:
            [im]: pil格式图像
        """
        i = jsonInfo['normal']
        keys = list(i.keys())
        n = 0
        for a in i:
            x = keys[n]
            text = eval(f'info.{x}()')
            color = (i[f'{a}']['color']['r'], i[f'{a}']
                    ['color']['g'], i[f'{a}']['color']['b'])
            im = info_print(im, text, i[f'{a}']['size'], i[f'{a}']['font'], i[f'{a}']['location']
                            ['x'], i[f'{a}']['location']['y'], color, i[f'{a}']['align'])
            n += 1
        return im
    
    im = playTime(im)
    im = normalInfo(im, info)

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

