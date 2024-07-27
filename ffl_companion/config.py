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
    __conf = {
        "LeagueSettingsManager": {
            "league_id": "",
            "name": "Demo",
        }
    }
    __setters = ["LeagueSettingsManager"]

    @staticmethod
    def config(name):
        return App.__conf.get(name, {})

    @staticmethod
    def set(name, value):
        if name in App.__setters:
            App.__conf[name] = value
        else:
            raise NameError("Name not accepted in set() method")

    # @staticmethod
    # def global_filter():
    #     return App.__conf

    @staticmethod
    def unlock():
        for k in App.__setters:
            App.__conf[k] = {}

    # @classmethod
    # def __getitem__(cls, item):
    #     return App.__conf[item]
