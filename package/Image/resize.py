from .pilJudge import pilJudge


def stretchZoom(im, width, height):
    """
    对传入图片进行拉伸截取至指定大小
    若和目标比例不一则截取中间部分
    :param im: 传入pil图像
    :param width: 要输出的宽度
    :param height: 要输出的高度
    :return: 输出pil图像
    """
    '''im = pilJudge(im)
    modelScale = width/height
    imgScale = im.width/im.height

    if imgScale > modelScale:  # 如果图片比指定比例宽
        scale = height/im.height

        im = im.crop((0, (im.height / 2) - (height / 2), im.width, (im.height / 2) + (height / 2)))
    elif imgScale < modelScale:  # 如果图片比指定比例高
        scale = width/im.width
        im = im.crop(((im.width / 2) - (width / 2), 0, (im.width / 2) + (width / 2), im.height))
    else:  # 如果图片符合指定比例
        scale = width/im.width

    # im = im.resize(im.width*scale, im.height*scale)
    im = im.resize((width, height))'''

    scale = max(width / im.width, height / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)))
    im = im.crop(((im.width - width) / 2, (im.height - height) / 2, (im.width + width) / 2, (im.height + height) / 2))
    return im

