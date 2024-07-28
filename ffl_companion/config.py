# LEAGUE_ID = None
#
#
# def get_league_id():
#     return globals()["LEAGUE_ID"]
#
#
# def set_league_id(league_id: str):
#     globals()["LEAGUE_ID"] = league_id
#

# class ModelConfig:
#     __config = {
#         "LeagueSettingsManager": "SUCCESS"
#     }
#
#     def __getitem__(self, item):
#         return ModelConfig.__config[item]


class App:
    __KEY = "dataset"
    __conf = {__KEY: "Demo"}
    __UNLOCK = False

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
