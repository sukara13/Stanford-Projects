import os
import pandas as pd
import numpy as np

csv_filenames = [
    'AusOpen-men-2013.csv', 'FrenchOpen-men-2013.csv', 'USOpen-men-2013.csv',
    'Wimbledon-men-2013.csv'
]

folder_path = '/Users/sukara/Downloads/tennis+major+tournament+match+statistics/'

all_matches = pd.DataFrame()
for filename in csv_filenames:
    file_path = os.path.join(folder_path, filename)
    df = pd.read_csv(file_path,
                     dtype={
                         'FSW.1': float,
                         'FSW.2': float,
                         'Result': int
                     })
    all_matches = pd.concat([all_matches, df], ignore_index=True)

def calculate_general_fsw_win_relationship(df):
    higher_fsw_wins = (df['FSW.1'] > df['FSW.2']) & (df['Result'] == 1) | (
        df['FSW.2'] > df['FSW.1']) & (df['Result'] == 0)
    probability_higher_fsw_wins = higher_fsw_wins.mean()
    return probability_higher_fsw_wins

probability_fsw = calculate_general_fsw_win_relationship(all_matches)
print(
    f"The overall probability of winning with a higher FSW across the specified Grand Slams is: {probability_fsw:.2f}"
    # 0.69
)
