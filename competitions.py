import pandas as pd

leagues = ['NHL', 'KHL', 'Liiga', 'SHL', 'AHL', 'ECHL', 'OHL', 'QMJHL', 'WHL', 'WJC-U20', 'WJC-U18', 'Olympics', 'WHC']
years = {
    'NHL': list(range(1917, 2020)),
    'KHL': list(range(2008, 2020)),
    'Liiga': list(range(1933, 2020)),
    'SHL': list(range(1975, 2020)),
    'AHL': list(range(1993, 2020)),
    'ECHL': list(range(1988, 2020)),
    'OHL': list(range(1980, 2020)),
    'QMJHL': list(range(1969, 2020)),
    'WHL': list(range(1978, 2020)),
    'WJC-U20': list(range(1977, 2020)),
    'WJC-U18': list(range(1999, 2020)),
    #'Olympics': list(range(1920, 2020, 4)),
    'Olympics': list(range(1920, 1937, 4)) + list(range(1948, 1993, 4)) + list(range(1994, 2020, 4)),
    'WHC': [1982, 1984] + list(range(1985, 1988)) + list(range(1989, 2020))
}
types = {
    'NHL': ['regular', 'playoff'],
    'KHL': ['regular', 'playoff'],
    'Liiga': ['regular', 'playoff'],
    'SHL': ['regular', 'playoff'],
    'AHL': ['regular', 'playoff'],
    'ECHL': ['regular', 'playoff'],
    'OHL': ['regular', 'playoff'],
    'QMJHL': ['regular', 'playoff'],
    'WHL': ['regular', 'playoff'],
    'WJC-U20': ['tournament'],
    'WJC-U18': ['tournament'],
    'Olympics': ['tournament'],
    'WHC': ['tournament']
}

writer = pd.ExcelWriter('QuantHockey_Competition.xlsx')
Competitions_df = pd.DataFrame(columns=['league_id', 'season_id', 'type'])
for league_id in leagues:
    for tp in types[league_id]:
        for season_id in years[league_id]:
            if tp == 'playoff' and season_id == 2019:
                pass
            else:
                Competitions_df.loc[len(Competitions_df)] = [league_id, season_id, tp]
Competitions_df.to_excel(excel_writer=writer)
writer.save()