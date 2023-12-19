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
                         'FSP.1': float,
                         'FSP.2': float,
                         'Result': int
                     })
    all_matches = pd.concat([all_matches, df], ignore_index=True)

def calculate_general_fsp_win_relationship(df):
    higher_fsp_wins = (df['FSP.1'] > df['FSP.2']) & (df['Result'] == 1) | (
        df['FSP.2'] > df['FSP.1']) & (df['Result'] == 0)
    probability_higher_fsp_wins = higher_fsp_wins.mean()
    return probability_higher_fsp_wins


probability_fsp = calculate_general_fsp_win_relationship(all_matches)
print(
    f"The overall probability of winning with a higher FSP across the specified Grand Slams is: {probability_fsp:.2f}"
    # 0.57
)
