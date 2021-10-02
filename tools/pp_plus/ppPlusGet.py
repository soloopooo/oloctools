import os

from package.info.ppPlus import get_self_pp_plus
from ujson import dumps
from loguru import logger


def main():
    """
    pp+获取主程序
    :return: 了个寂寞
    """
    try:
        logger.info('尝试获取pp+')
        pp_plus_json = get_self_pp_plus()
        print(pp_plus_out(pp_plus_json))
        input('按下回车继续...')
        logger.info('保存此次结果')
        save(dumps(pp_plus_json))
    except Exception as e:
        logger.error(f'获取失败，查询本地记录 {e}')
        try:
            with open('data/pp_plus.json', 'r') as f:
                pp_plus_json = f.read()
            print(pp_plus_out(pp_plus_json))
        except Exception:
            logger.error('获取失败')
    input('按下回车返回')


def pp_plus_out(input):
    """
    清屏并获取输出信息
    :param input: pp+信息
    :return: 输出字符串
    """
    os.system('cls')
    out = ('-------------------------------------------------------\n'
           '玩家{UserName}的pp+数据如下\n\n'
           'Total:      {PerformanceTotal:.2f}\n'
           'Aim:        {AimTotal:.2f}\n'
           'Jump:       {JumpAimTotal:.2f}\n'
           'Flow:       {FlowAimTotal:.2f}\n'
           'Precision:  {PrecisionTotal:.2f}\n'
           'Speed:      {SpeedTotal:.2f}\n'
           'Stamina:    {StaminaTotal:.2f}\n'
           'Accuracy:   {AccuracyTotal:.2f}\n'
           '-------------------------------------------------------').format(**input)
    return out


def save(str):
    """
    尝试保存pp+文件以供下次获取不到使用
    :param str:
    :return:
    """
    try:
        logger.info('正在尝试保存')
        with open('data/ppPlus/pp_plus', 'w+') as f:
            f.write(str)
    except FileNotFoundError as e:
        logger.warning(f'出现错误:{e}')
        logger.info('判断目录是否存在')
        isExists = os.path.exists(r'data/ppPlus/')
        if not isExists:
            logger.info('目录不存在,创建目录')
            os.makedirs(r'data/ppPlus/')
        isExists = os.path.exists(r'data/ppPlus/')
        if isExists:
            logger.info('目录已创建')
            try:
                logger.info('正在尝试保存')
                with open('data/ppPlus/pp_plus', 'w+') as f:
                    f.write(str)
            except Exception as e:
                logger.error(f'保存失败:{e}')
        else:
            logger.error('创建失败')
            logger.error('保存pp+失败')
    except Exception as e:
        logger.error(f'保存pp+失败:{e}')


