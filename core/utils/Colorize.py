class Colorize:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    LIGHT_PURPLE = '\033[94m'
    PURPLE = '\033[95m'
    END = '\033[0m'

    @classmethod
    def red(cls, s):
        return cls.RED + s + cls.END

    @classmethod
    def green(cls, s):
        return cls.GREEN + s + cls.END

    @classmethod
    def yellow(cls, s):
        return cls.YELLOW + s + cls.END

    @classmethod
    def light_purple(cls, s):
        return cls.LIGHT_PURPLE + s + cls.END

    @classmethod
    def purple(cls, s):
        return cls.PURPLE + s + cls.END
