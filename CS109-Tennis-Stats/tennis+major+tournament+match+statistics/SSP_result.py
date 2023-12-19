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
                         'SSP.1': float,
                         'SSP.2': float,
                         'Result': int
                     })
    all_matches = pd.concat([all_matches, df], ignore_index=True)

def calculate_general_ssp_win_relationship(df):
    higher_ssp_wins = (df['SSP.1'] > df['SSP.2']) & (df['Result'] == 1) | (
        df['SSP.2'] > df['SSP.1']) & (df['Result'] == 0)
    probability_higher_ssp_wins = higher_ssp_wins.mean()
    return probability_higher_ssp_wins


probability_ssp = calculate_general_ssp_win_relationship(all_matches)
print(
    f"The overall probability of winning with a higher SSP across the specified Grand Slams is: {probability_ssp:.2f}"
    # 0.39
)
