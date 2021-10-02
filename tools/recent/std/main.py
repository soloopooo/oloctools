import os
from re import X
from package.info.std import StdInfo
from package.info.std import MapInfo
from loguru import logger
from .bgMaker import BgMaker
from PIL import Image, ImageOps, ImageDraw, ImageFont
from package.Image.pilJudge import pilJudge
from package.Image.chart import lineChart
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
        logger.info('展示图片...')
        im = output(im, info)
        im.convert('RGB').show()
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
    jsonInfo = ujson.load(open(r'model/RecentPlay/model.json'))

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

        i = jsonInfo['info']['playTime']['playTimeDay']
        color = (i['color']['r'], i['color']['g'], i['color']['b'])
        im = info_print(im, time[0], i['size'], i['font'],
                        i['location']['x'], i['location']['y'],
                        color, i['align'])

        i = jsonInfo['info']['playTime']['playTimeMin']
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
        i = jsonInfo['info']['normal']
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

    def rankStatus(im, info):
        """[summary]
        输出铺面状态图标

        unknown 0
        unsubmitted 1
        pending/wip/graveyard 2
        unused 3
        ranked 4
        approved 5
        qualified 6
        loved 7

        Args:
            im: pil格式图片
            info: gosu信息

        Returns:
            [pil image]: 输出完状态图标的pil图片
        """
        statusIcon = jsonInfo['rankStatusIcon']
        status = info.map_status()
        status_list = [statusIcon['unknown'],
                       statusIcon['unsubmitted'],
                       statusIcon['pending_wip_graveyard'],
                       statusIcon['unused'],
                       statusIcon['ranked'],
                       statusIcon['approved'],
                       statusIcon['qualified'],
                       statusIcon['loved']
                       ]
        status_img = status_list[status]
        status_img = Image.open(status_img)
        status_img.resize((jsonInfo['info']['mapStatus']['size']['w'],
                           jsonInfo['info']['mapStatus']['size']['h']))
        im.paste(status_img, (jsonInfo['info']['mapStatus']['location']['x'],
                              jsonInfo['info']['mapStatus']['location']['y']), status_img)
        return im

    def rankIcon(im, info):
        """输出成绩评分图标

        Args:
            im (pil图像): pil格式图像
            info (gosu): gosu的信息
        Return:
            im (pil图像): pil格式图像
        """
        rankIcon = jsonInfo['scoreRankIcon']
        rank = info.rank_result()
        rank = str(rank)

        if info.state() == 2:
            rank = Image.open(rankIcon['F'])
        elif info.state() == 7:
            if rank == 'SSH':
                rank = Image.open(rankIcon['SSH'])
            elif rank == 'SS':
                rank = Image.open(rankIcon['SS'])
            elif rank == 'SH':
                rank = Image.open(rankIcon['SH'])
            elif rank == 'S':
                rank = Image.open(rankIcon['S'])
            elif rank == 'A':
                rank = Image.open(rankIcon['A'])
            elif rank == 'B':
                rank = Image.open(rankIcon['B'])
            elif rank == 'C':
                rank = Image.open(rankIcon['C'])
            elif rank == 'D':
                rank = Image.open(rankIcon['D'])

        rank = rank.resize((rankIcon['info']['size']['w'], rankIcon['info']['size']['h'])).convert('RGBA')
        im.paste(rank, (rankIcon['info']['location']['x'], rankIcon['info']['location']['y']), rank)
        return im

    def innormal(im, info):
        """打印需要简单处理的信息

        Args:
            im (pil image): 要打印的图像
            info (gosu): gosu信息

        Returns:
            im: 打印完毕的图像
        """

        def textJudge(key, info):
            if key == 'bpm':
                text = str(info.bpm_max()) if info.bpm_min() == info.bpm_max() else str(info.bpm_min()) + '-' + str(
                    info.bpm_max())
            elif key == 'mapper':
                text = str('mapped by ' + str({0}).format(info.mapper()))
            elif key == ('key_count_k1' or 'key_count_k2' or 'key_count_m1' or 'key_count_m2'):
                text = str(eval(f'info.{key}()') if eval(f'info.{key}()') != 0 else key[:-2])
            elif key == 'score':
                text = '{:,}'.format(info.score())
            elif key == 'max_combo':
                text = '{:,}'.format(info.max_combo()) + 'x'
            elif key == 'accuracy':
                text = str({0}).format(info.accuracy()) + '%'
            elif key == 'ur':
                text = round(float(str({0}).format(info.ur())), 2)
            elif key == 'time_length':
                now = info.time_length_now() / 1000
                now_min = int(now / 60)
                now_sec = int(now % 60)

                full = info.time_length_full() / 1000
                full_min = int(full / 60)
                full_sec = int(full % 60)
                if info.state() == 2:
                    text = f'{now_min}:{now_sec}/{full_min}:{full_sec}'
                else:
                    text = f'{full_min}:{full_sec}'
            else:
                text = eval(f'info.{key}()')
            return text

        i = jsonInfo['info']['innormal']
        keys = list(i.keys())
        n = 0
        for a in i:
            x = keys[n]
            text = textJudge(x, info)

            color = (i[f'{a}']['color']['r'], i[f'{a}']['color']['g'], i[f'{a}']['color']['b'])
            im = info_print(im, text, i[f'{a}']['size'], i[f'{a}']['font'], i[f'{a}']['location']['x'],
                            i[f'{a}']['location']['y'], color, i[f'{a}']['align'])
            n += 1
        return im

    def mod(im, info):
        """
        打印mod图标
        """
        logger.info('输出mod图标')
        modJson = jsonInfo['info']['mod']
        mods_str = str.lower(info.mod_str())  # 把所有字符中的大写字母转换成小写字母
        if mods_str == 'nm':  # 判断是否无mod
            logger.info('无mod，跳过')
            a = ''
        else:
            logger.info(f'拆分mod字符串{mods_str}')
            a = []
            i = 0
            tmp = ""
            for v in mods_str:
                tmp += v
                i += 1
                if i % 2 == 0:
                    a.append(tmp)
                    tmp = ""
        x = modJson['location']['x']
        y = modJson['location']['y']
        size = (modJson['size']['w'], modJson['size']['h'])
        logger.info(f'mod图标大小为{size}, 排列打印图标')
        if modJson['direction'] != ('down' or 'right'):
            logger.error(r'请查看model/RecentPlay/model.json内info->mod->direction是否为right或down')
            logger.error(r'采用默认right横向排列mod图标')
        for a in a:  # 循环打印
            logger.info(f'打印{a.upper()}')
            img = eval(f'modJson[\'icon\'][\'{a}\']')
            img = Image.open(img)
            img = img.resize(size)
            im.paste(img, (x, y), img)
            if modJson['direction'] == 'down':
                y += modJson['spacing']
            elif modJson['direction'] == 'right':
                x += modJson['spacing']
            else:
                x += modJson['spacing']
        return im

    def avatar(im, info):
        """
        打印头像，使用模板文件内的shapeModel路径裁剪头像
        :param im:
        :param info:
        :return:
        """
        avatarJson = jsonInfo['avatar']
        if info.player_name() == 'osu!':
            avatar = Image.open(avatarJson['osu'])
        else:
            avatar = Image.open(avatarJson['avatar'])
        size = (avatarJson['size']['w'], avatarJson['size']['h'])
        avatar = avatar.resize(size)
        if avatarJson['shapeModel'] is not None:
            border = Image.open(avatarJson['shapeModel'])
            border = border.resize(size).convert('L')
            invert = ImageOps.invert(border)
            avatar.putalpha(invert)
        im.paste(avatar, (avatarJson['location']['x'], avatarJson['location']['y']), avatar)
        return im

    def pp(im, info):
        """
        打印获得的pp
        :param im:图
        :param info:信息
        :return: 图
        """
        pp = info.pp_current()
        ppJson = jsonInfo['info']['pp']
        pp_width, pp_height = ImageFont.truetype(ppJson['pp_num']['font'], ppJson['pp_num']['size']).getsize(str(pp))
        str_width, str_height = ImageFont.truetype(ppJson['pp_str']['font'], ppJson['pp_str']['size']).getsize(str(pp))
        im_width = pp_width + str_width
        im_height = max(pp_height, str_height) + str_height + ppJson['pp_str']['y_offset']

        i = Image.new("RGBA", (im_width, im_height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(i)
        ppJson_a = ppJson['pp_num']
        fill = (ppJson_a['color']['r'], ppJson_a['color']['g'], ppJson_a['color']['b'])
        draw.text((0, 0), str(pp), fill=fill,
                  font=ImageFont.truetype(ppJson_a['font'], ppJson_a['size']))

        ppJson_b = ppJson['pp_str']
        location = (pp_width, max(pp_height, str_height) + ppJson['pp_str']['y_offset'] - str_height)
        fill = (ppJson_b['color']['r'], ppJson_b['color']['g'], ppJson_b['color']['b'])
        draw.text(location, 'pp', fill=fill,
                  font=ImageFont.truetype(ppJson_b['font'], ppJson_b['size']))
        # 打印
        align = ppJson['align']
        locations = ppJson['location']
        if align == 'left':
            location = (locations['x'], locations['y'])
        elif align == 'right':
            location = (locations['x'] - i.width, locations['y'])
        elif align == 'centre':
            location = (int(locations['x'] - (i.width / 2)), locations['y'])
        im.paste(i, location, i)

        return im

    def chart(im, info):
        urJson = jsonInfo['info']['lineChart']['ur']
        ur = info.ur_strains()
        leftTop = (urJson['location']['leftTop']['x'], urJson['location']['leftTop']['y'])
        rightBelow = (urJson['location']['rightBelow']['x'], urJson['location']['rightBelow']['y'])
        lineWidth = urJson['line']['width']
        lineColor = (urJson['line']['color']['r'], urJson['line']['color']['g'], urJson['line']['color']['b'])
        im = lineChart(im, ur, leftTop, rightBelow, lineWidth, lineColor, align=1)

        ppJson = jsonInfo['info']['lineChart']['pp']
        pp = info.pp_strains()
        leftTop = (ppJson['location']['leftTop']['x'], ppJson['location']['leftTop']['y'])
        rightBelow = (ppJson['location']['rightBelow']['x'], ppJson['location']['rightBelow']['y'])
        lineWidth = ppJson['line']['width']
        lineColor = (ppJson['line']['color']['r'], ppJson['line']['color']['g'], ppJson['line']['color']['b'])
        im = lineChart(im, pp, leftTop, rightBelow, lineWidth, lineColor, align=1)
        return im

    def outputMain(im, info):
        """
        主函数，运行以上所有函数
        :param im: 图
        :param info: 信息
        :return: 图
        """
        im = playTime(im)
        im = normalInfo(im, info)
        im = rankStatus(im, info)
        im = rankIcon(im, info)
        im = innormal(im, info)
        im = mod(im, info)
        im = avatar(im, info)
        im = pp(im, info)
        im = chart(im, info)
        return im

    im = outputMain(im, info)

    return im


def ifSave(im, info):
    """
    由程序最后部分调用，根据配置文件内的配置，选择性保存成绩图
    若某成绩设置了保存，则
    :param im: 程序图像
    :param info: 传入
    :return: 无
    """

    def save(im, time):
        """
        尝试保存，无路径创建路径
        :param im: pil图片
        :param time: 图片名
        :return:
        """
        try:
            logger.info(f'正在保存成绩图，名称为:{time}.jpg')
            im.save(r'data/recentPlay/'f'{time}.jpg', 'JPEG')
        except FileNotFoundError as e:
            logger.warning(f'出现错误:{e}')
            logger.info('判断目录是否存在')
            isExists = os.path.exists(r'data/recentPlay/')
            if not isExists:
                logger.info('目录不存在,创建目录')
                os.makedirs(r'data/recentPlay/')
            isExists = os.path.exists(r'data/recentPlay/')
            if isExists:
                logger.info('目录已创建')
                try:
                    logger.info(f'正在保存成绩图，名称为:{time}.jpg')
                    im.save(r'data/recentPlay/'f'{time}.jpg', 'JPEG')
                except Exception as e:
                    logger.error(f'保存图片失败:{e}')
            else:
                logger.error('创建失败')
                logger.error('保存图片失败')
        except Exception as e:
            logger.error(f'保存图片失败:{e}')

    allConfig = configs.RecentPlay()
    autoSaveConfig = allConfig.AutoSave()

    im = im.convert('RGB')
    time = strftime("%Y-%m-%d_%H-%M", localtime())

    if autoSaveConfig.rankAutoSave(info.rank_result()):
        logger.info('达到指定rank，自动保存')
        save(im, time)
        im.close()
    elif autoSaveConfig.accAutoSave() <= info.accuracy():
        logger.info('达到指定acc，自动保存')
        save(im, time)
        im.close()
    else:
        sec = input('是否保存成绩图？(Y/N)')
        if sec == 'Y' or sec == 'y':
            save(im, time)
            logger.info('尝试保存完毕')
            im.close()
        else:
            pass
