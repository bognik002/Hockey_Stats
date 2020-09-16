import pandas as pd
from numpy import nan
from time import time as time_ns

print('Initializing Data Frames...')
PlayerStats_excel = pd.ExcelFile('data/QuantHockey_PlayerStats.xlsx')


Seasons_df = pd.DataFrame(columns=['year', 'type'])
writer_seasons = pd.ExcelWriter('tables/season.xlsx')
seasons = set()

Players_df = pd.DataFrame(columns=['name', 'league_id', 'birth_date', 'nationality', 'youth_team', 'position', 'shoots', 'height', 'weight'])
writer_players = pd.ExcelWriter('tables/player.xlsx')
players = set()
players_ids = dict()

PlayerStats_df = pd.DataFrame(columns=['season_id', 'team_id', 'player_id', 'league_id',
                                       'games', 'points', 'goals', 'assists', 'penalty', '+/-',
                                       'power_play_goals', 'short_handed_goals', 'game_winning_goals',
                                       'goals_per_games', 'assists_per_games', 'points_per_games'])

writer_player_stats = pd.ExcelWriter('tables/player_stats.xlsx')

for sheet in PlayerStats_excel.sheet_names:
    league, year, season_type = sheet.split('_')
    if year >= '1990':
        Stats = pd.DataFrame(columns=['season_id', 'team_id', 'player_id', 'league_id',
                                       'games', 'points', 'goals', 'assists', 'penalty', '+/-',
                                       'power_play_goals', 'short_handed_goals', 'game_winning_goals',
                                       'goals_per_games', 'assists_per_games', 'points_per_games'])

        print('Collecting data from {0} {1} ({2})'.format(league, year, season_type))
        # Update Seasons_df
        if (year, season_type) not in seasons:
            Seasons_df.loc[len(Seasons_df)] = [year, season_type]
            seasons.add((year, season_type))
        season_id = Seasons_df.loc[(Seasons_df.year == year) & (Seasons_df.type == season_type)].index.tolist()[0]
        # Update Teams_df
        team_id = nan
        t0 = time_ns()
        for ind, row in PlayerStats_excel.parse(sheet).iterrows():
            # Update Players_df
            if (row['Name'], row['Pos'], league) not in players:
                players.add((row['Name'], row['Pos'], league))
                players_ids[(row['Name'], row['Pos'], league)] = len(Players_df)
                Players_df.loc[len(Players_df)] = [row['Name'], league, nan, nan, nan, row['Pos'], nan, nan, nan]

            player_id = players_ids[(row['Name'], row['Pos'], league)]

            # Update PlayerStats_df
            Stats.loc[len(Stats)] = [season_id, team_id, player_id, league,
                                     row['GP'], row['P'], row['G'], row['A'], row['PIM'], row['+/-'],
                                     row['PPG'], row['SHG'], row['GWG'],
                                     row['G/GP'], row['A/GP'], row['P/GP']]
        PlayerStats_df = PlayerStats_df.append(Stats, ignore_index=True)
        print('Currently found {0} players in {1}'.format(Players_df.shape[0], league))

Seasons_df.to_excel(writer_seasons)
PlayerStats_df.to_excel(writer_player_stats)
Players_df.to_excel(writer_players)

writer_seasons.save()
writer_players.save()
writer_player_stats.save()