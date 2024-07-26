import pandas as pd

from ffl_companion.api_models.player import PlayerStatsWeekly, Player


def import_weekly_player_stats(csv_dict: dict, year: int):
    """
    Expects dict of:
    {
        "passing": [paths],
        "receiving": [paths],
        "rushing": [paths],
    }
    """
    import_missing_players(csv_dict=csv_dict, year=year)
    for stat_type, csvs in csv_dict.items():
        for path in csvs:
            PlayerStatsWeekly.objects.import_csv_data(path=path, stat_type=stat_type, year=year)


def import_missing_players(csv_dict: dict, year: int):
    """
    Expects dict of:
    {
        "passing": [paths],
        "receiving": [paths],
        "rushing": [paths],
    }
    """
    missing_players = []
    for stat_type, csvs in csv_dict.items():
        for path in csvs:
            data = pd.read_csv(path).to_dict("records")
            players_missing = PlayerStatsWeekly.objects.find_missing(data=data, stat_type=stat_type, year=year)
            missing_players.extend(players_missing)

    if missing_players:
        missing_players_df = pd.DataFrame(missing_players).drop_duplicates()
        missing_players_import = missing_players_df.to_dict("records")
        Player.objects.import_missing_players(missing_players_import)
