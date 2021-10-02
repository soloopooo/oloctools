from tools.recent.std import main as re_std
import os


def recent():
    try:
        re_std.main()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    text = """1.`+`recent成绩图生成"""
    while True:
        print(r""" _____   _       _____   _____   _____   _____   _____   _       _____  
/  _  \ | |     /  _  \ /  ___| |_   _| /  _  \ /  _  \ | |     /  ___/ 
| | | | | |     | | | | | |       | |   | | | | | | | | | |     | |___  
| | | | | |     | | | | | |       | |   | | | | | | | | | |     \___  \ 
| |_| | | |___  | |_| | | |___    | |   | |_| | | |_| | | |___   ___| | 
\_____/ |_____| \_____/ \_____|   |_|   \_____/ \_____/ |_____| /_____/ 
                                                    -----by Adsicmes""")
        print("""\n\n全本地功能标`+`，涉及到网络的功能标`-`""")
        print("""目前已有功能:\n""")
        print(text)
        sec = input('\n请输入要使用的功能:')
        if sec == 1:
            recent()
        input('按下回车返回主界面')
        os.system('clear')


