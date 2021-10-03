import os


def fileSearch_2(dir_path, string):
    """
    二级文件查找
    :param dir_path: 要查找的目录
    :param string: 文件包含的字符串
    :return: 文件路径列表
    """
    file = []
    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            file.append(dir_path + filename)
        for dirname in dirs:
            for root2, dirs2, files2 in os.walk((dir_path + dirname)):
                for filename in files2:
                    file.append(dir_path + dirname + filename)
    print(file)
    final = []
    length = len(string)
    for i in file:
        if string in i:
            final.append(i)
    return final


if __name__ == '__main__':
    print(fileSearch_2(r'D:\OSU\Songs', '.osu'))

