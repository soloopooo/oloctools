import configparser


class RecentPlay:
    def __init__(self):
        pass

    class BackGround:
        def __init__(self):
            config = configparser.ConfigParser()
            path = r'config\RecentPlay.ini'
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
            path = r'config\RecentPlay.ini'
            config.read(path)
            self.config = config

        def rankAutoSave(self, rank):
            return self.config.getboolean('AutoSave', f'{rank}''_AutoSave')

        def askPerGenerate(self):
            return self.config.getboolean('AutoSave', 'askPerGenerate')

        def accAutoSave(self):
            return self.config.getint('AutoSave', 'acc_AutoSave')


class Proxy:
    def __init__(self):
        config = configparser.ConfigParser()
        path = r'config\Proxy.ini'
        config.read(path)
        self.config = config

    def httpProxy(self):
        return self.config.get('proxy', 'httpProxy')

    def switch_ppPlus(self):
        return self.config.getboolean('proxySwitch', 'ppPlusGet')


class User:
    def __init__(self):
        config = configparser.ConfigParser()
        path = r'config\User.ini'
        config.read(path)
        self.config = config

    def username(self):
        return self.config.get('User', 'username')

    def userid(self):
        return self.config.get('User', 'userid')


if __name__ == '__main__':
    bg = RecentPlay().BackGround()
    print(bg.dim())
    print(bg.bgifnon())
    print(bg.blur())
