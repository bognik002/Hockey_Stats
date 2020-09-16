import quanthockey_parser as parser
import pandas as pd
from random import randint


def paginate(league, year, st, page_n):
    year = str(year)
    if st != 'tournament':
        year = '{0}-{1}'.format(year, int(year[2:]) + 1)
    st_code = {
        'tournament': 'int',
        'regular': 'reg',
        'playoff': 'ply'
    }
    params = {
        'cat': 'Season',
        'pos': 'Players',
        'SS': year,
        'af': 0,
        'nat': year,
        'st': st_code[st],
        'sort': 'P',
        'so': 'DESC',
        'page': page_n,
        'league': league,
        'lang': 'en',
        'rnd': randint(10**8, 10**9),
        'dt': 1,
        'sd': 'undefined',
        'ed': 'undefined'
    }
    return params


def to_dict(columns, contents):
    result = []
    for row in contents:
        new_row = dict()
        if len(columns) != len(row):
            print('to_dict: the length of contents and columns is different, i.e. {0} columns and {1} contents'.format(
                len(columns), len(row)
            ))
        for i in range(len(columns)):
            new_row[columns[i]] = row[i]
        result.append(new_row)
    return result


quantum_url = 'https://www.quanthockey.com/scripts/AjaxPaginate.php'
Competition_df = pd.read_excel('QuantHockey_Competition.xlsx', 'Sheet1')

if __name__ == '__main__':
    writer = pd.ExcelWriter('QuantHockey_PlayerStats.xlsx', engine='xlsxwriter')
    for competition in Competition_df.iterrows():
        print('Collecting {0} for {1} year ({2})...'.format(competition[1]['league_id'],
              competition[1]['season_id'], competition[1]['type']))
        CompetitionStats_df = pd.DataFrame()
        params = paginate(competition[1]['league_id'], competition[1]['season_id'], competition[1]['type'], 1)
        page = parser.get_page(quantum_url, params=params)
        page_f = parser.get_number_of_pages(page)
        for page_n in range(1, page_f + 1):
            print('page {0} of {1}'.format(page_n, page_f))
            params = paginate(competition[1]['league_id'], competition[1]['season_id'], competition[1]['type'], page_n)
            page = parser.get_page(quantum_url, params)
            table = parser.get_table(page)
            if table is None:
                break
            columns = parser.get_columns(table)
            contents = parser.get_contents(table)
            Page_df = pd.DataFrame(to_dict(columns, contents))
            CompetitionStats_df = CompetitionStats_df.append(Page_df, ignore_index=True)
        print('Collected {0} from {league} in {year} ({type})'.format(CompetitionStats_df.shape[0],
                                                                      league=competition[1]['league_id'],
                                                                      year=competition[1]['season_id'],
                                                                      type=competition[1]['type']))
        CompetitionStats_df.to_excel(excel_writer=writer,
                                     sheet_name=('{league}_{year}_{type}'.format(league=competition[1]['league_id'],
                                                                                 year=competition[1]['season_id'],
                                                                                 type=competition[1]['type'])))
    writer.save()