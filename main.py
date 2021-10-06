from tools.recent.std.main import main as re_std
from tools.pp_plus.ppPlusGet import main as pp_plus_get
from tools.map_download.hotMap.hotMapDownloader import main as hot_map_download
from tools.map_download.mapReferDownload.mapReferDownload import main as refer_map_download
from loguru import logger
import os


def tryDefine(str):
    try:
        eval(str)
    except Exception as e:
        logger.error(e)


def main():
    text = ("1.`+`recent成绩图生成\n"
            "2.`-`pp+获取\n"
            "3.`-`热门铺面下载(from sayo)\n"
            "4.`-`指定参数铺面下载(from sayo)")
    while True:
        print(" _____   _       _____   _____   _____   _____   _____   _       _____  "
              "/  _  \ | |     /  _  \ /  ___| |_   _| /  _  \ /  _  \ | |     /  ___/ "
              "| | | | | |     | | | | | |       | |   | | | | | | | | | |     | |___  "
              "| | | | | |     | | | | | |       | |   | | | | | | | | | |     \___  \ "
              "| |_| | | |___  | |_| | | |___    | |   | |_| | | |_| | | |___   ___| | "
              "\_____/ |_____| \_____/ \_____|   |_|   \_____/ \_____/ |_____| /_____/ "
              "                                                       -----by Adsicmes")
        print("""\n\n全本地功能标`+`，涉及到网络的功能标`-`""")
        print("""目前已有功能:\n""")
        print(text)
        sec = input('\n请输入要使用的功能:')
        if sec == '1':
            tryDefine('re_std()')
        elif sec == '2':
            tryDefine('pp_plus_get()')
        elif sec == '3':
            tryDefine('hot_map_download()')
        elif sec == '4':
            tryDefine('refer_map_download()')
        input('按下回车返回主界面')
        os.system('cls')


if __name__ == '__main__':
    main()
