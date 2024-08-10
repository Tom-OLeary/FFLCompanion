from rest_framework.authentication import TokenAuthentication


class App:
    __KEY = "dataset"
    __conf = {__KEY: "Demo"}
    __UNLOCK = True

    @staticmethod
    def config():
        if App.__UNLOCK:
            return {}
        return App.__conf

    @staticmethod
    def set(value):
        App.__conf[App.__KEY] = value

    @staticmethod
    def unlock():
        App.__UNLOCK = True

    @staticmethod
    def lock():
        App.__UNLOCK = False
        App.__conf[App.__KEY] = "Demo"
