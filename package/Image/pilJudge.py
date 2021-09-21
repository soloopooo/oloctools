from PIL import Image


def pilJudge(im):
    """
    判断是否为pil图像，不是则变为pil图像
    :param im: 图像路径或pil图像
    :return: pil图像
    """
    if type(im) == 'PIL.PngImagePlugin.PngImageFile':
        im = im
    elif type(im) == 'str':
        im = Image.open(im)
    return im
