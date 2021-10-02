from PIL import ImageDraw


def lineChart(im, y, leftTop, rightBelow, lineWidth, lineColor, align=0):
    """
    由指定的y在im的指定区域生成折线图，x平均分配
    :param align: 对齐选项 y有复数输入1，没有输入0
    :param lineColor: rgb元组
    :param lineWidth: 线宽度
    :param im: 传入pil图像
    :param y:点的y值列表
    :param leftTop: 折线区域左上角
    :param rightBelow: 折线区域右下角
    :return: 画完折线的图
    """
    chartWidth = rightBelow[0] - leftTop[0]
    chartHeight = rightBelow[1] - leftTop[1]

    if y is not None:
        if align == 1:
            """
            align = 1 的时候，将列表的所有y加上列表内的最小值转换为正数列表
            """
            # 取y的最小值
            min_y = 0
            for i in y:
                if i < min_y:
                    min_y = i
            # 所有y加上最小值
            y_plus = []
            for i in y:
                i -= min_y
                y_plus.append(i)
            y = y_plus

        # 生成X数列
        x = []
        n = 0
        for i in y:
            n += 1
        m = 0
        for i in range(n):
            x.append(m)
            m += 1

        # 取y的最大值
        max_y = 0
        for i in y:
            if i > max_y:
                max_y = i

        # 等比缩放y
        scale_y = chartHeight / max_y
        new_y = []
        for num in y:
            new_num = num * scale_y
            new_y.append(new_num)

        # 等比缩放x
        max_x = x[-1]
        scale_x = chartWidth / max_x
        new_x = []
        for num in x:
            new_num = num * scale_x
            new_x.append(new_num)

        # 换算成对应坐标
        final_y = []
        for y in new_y:  # 里边有一步轴对称
            new_y_ = rightBelow[1] - y
            final_y.append(new_y_)
        final_x = []
        for x in new_x:
            new_x_ = leftTop[0] + x
            final_x.append(new_x_)
        xy = []
        for i in range(n):
            xy.append((final_x[i], final_y[i]))

        # 画线
        draw = ImageDraw.Draw(im)
        for i in range(n - 1):
            x_y = [xy[i], xy[i + 1]]
            draw.line(x_y, fill=lineColor, width=lineWidth)

        return im



