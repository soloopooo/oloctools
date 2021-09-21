from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
from .pilJudge import pilJudge
from loguru import logger
import time


def info_print(im, text, fontsize, font=ImageFont.load_default().font, x=0, y=0, color=(0, 0, 0), align='lb'):
    """
    打印文字，自定义对齐方式
    :param im:传入图像路径或pil格式图像
    :param text:文本，必须可以被格式化成str
    :param fontsize:字体大小
    :param font:字体，默认为系统默认字体
    :param x:左上为基准，默认 0px
    :param y:左上为基准，默认 0px
    :param color:颜色，默认黑色
    :param align:对齐，由两个位置组成字符串
                 第一个位置可填写'l(eft)' 'c(entre)' 'r(ight)'，第二个可填写'a(bove)' 'c(entre)' 'b(elow)'
                 默认为'lb'(left-below 左下为基准)
    :return:pil格式图像
    """
    im = pilJudge(im)
    draw = ImageDraw.Draw(im)
    text = str(text)
    try:
        width, height = ImageFont.truetype(font, fontsize).getsize(text)
    except OSError as e:
        logger.warning(f'字体读取失败:{e}，使用默认字体')
        width, height = ImageFont.truetype(ImageFont.load_default().font, fontsize).getsize(text)

    if align[0] == 'l':
        x = x
    elif align[0] == 'c':
        x = x - (width / 2)
    elif align[0] == 'r':
        x = x - width
    else:
        print('程序发生错误，请上报issue')
        print('程序将在五秒后退出')
        time.sleep(5)
        exit(0)
    if align[1] == 'a':
        y = y
    elif align[1] == 'c':
        y = y - (height / 2)
    elif align[1] == 'b':
        y = y - height
    else:
        print('程序发生错误，请上报issue')
        print('程序将在五秒后退出')
        time.sleep(5)
        exit(0)

    try:
        draw.text((x, y), text, fill=color, font=ImageFont.truetype(font, fontsize))
    except OSError as e:
        logger.warning(f'字体读取失败:{e}，使用默认字体')
        draw.text((x, y), text, fill=color, font=ImageFont.truetype(ImageFont.load_default().font, fontsize))
    return im
