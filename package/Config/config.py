import configparser


class RecentPlay:
    def __init__(self):
        pass

    class BackGround:
        def __init__(self):
            config = configparser.ConfigParser()
            path = r'D:\IDEAproject\Python\oloctools\config\RecentPlay.ini'
            config.read(path)
            self.config = config

        def bgifnon(self) -> str:
            return self.config.get('Background', 'bgifnon')

        def dim(self) -> float:
            return self.config.getfloat('Background', 'dim')

        def blur(self) -> int:
            return self.config.getint('Background', 'blur')

    class AutoSave:
        def __init__(self):
            config = configparser.ConfigParser()
            path = r'D:\IDEAproject\Python\oloctools\config\RecentPlay.ini'
            config.read(path)
            self.config = config

        def rankAutoSave(self, rank):
            return self.config.getboolean('AutoSave', f'{rank}''_AutoSave')

        def askPerGenerate(self):
            return self.config.getboolean('AutoSave', 'askPerGenerate')

        def accAutoSave(self):
            return self.config.getboolean('AutoSave', 'acc_AutoSave')


if __name__ == '__main__':
    bg = RecentPlay().BackGround()
    print(bg.dim())
    print(bg.bgifnon())
    print(bg.blur())
