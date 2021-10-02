from tools.recent.std import main as re_std


def main():
    try:
        re_std.main()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
    input('按下回车退出')
