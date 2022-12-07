from collections import defaultdict
from pathlib import Path

import pandas as pd
import requests

year = 2022
leaderboard_id = 976545
token_path = Path.home() / '.config/aocd/token'

with open(token_path) as f:
    token = f.read().strip()

def load_json(leaderboard_id=leaderboard_id, year=year, token=token):
    cookies = {'session': token}
    headers = {'User-Agent': 'github.com/attoPascal'}
    return requests.get(f'https://adventofcode.com/{year}/leaderboard/private/view/{leaderboard_id}.json', cookies=cookies, headers=headers).json()

def load_data():
    json = load_json()
    time_diffs = defaultdict(lambda: defaultdict(str))

    for id, member in json['members'].items():
        name = member['name'] if member['name'] else id
        for day, times in member['completion_day_level'].items():
            if '1' in times and '2' in times:
                time_diffs[name][int(day)] = times['2']['get_star_ts'] - times['1']['get_star_ts']

    df = pd.DataFrame.from_dict(time_diffs, orient='index', dtype='Int64')
    return df.sort_index(key=lambda x: x.str.lower()).sort_index(axis=1)

data = load_data()

def points(data=data):
    num_members, num_days = data.shape
    points = pd.Series(0, index=data.index, dtype=int)

    for day in range(num_days):
        points_awarded = num_members
        for name, time in data[day+1].sort_values().items():
            if not pd.isna(time):
                points[name] += points_awarded
                points_awarded -= 1

    points = points.sort_values(ascending=False).to_frame().reset_index()
    points.index += 1
    points.columns = ['name', 'pts']
    return points[['pts', 'name']]

def seconds_latest_day(data=data):
    return data.iloc[:, -1].dropna().sort_values().to_frame()

def seconds_all_days(data=data):
    return data.sum(axis=1, skipna=False).dropna().sort_values().to_frame()
