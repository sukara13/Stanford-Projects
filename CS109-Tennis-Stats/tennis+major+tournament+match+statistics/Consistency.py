import os
import pandas as pd
import numpy as np

# Note: In this code, I calculate consistency by doing UFE - Winners and then finding whichever player has the smaller value.
# When writing the paper, I thought it would be more clear to descibe consistency as Winners - UFE and finding the player
# with the larger value instead. To avoid confusion, I am adding this note for clarity.

# Define CSV filenames to process and define a folder path
# Note, I decide to only focus on men in this project
csv_filenames = [
    'AusOpen-men-2013.csv', 'FrenchOpen-men-2013.csv', 'USOpen-men-2013.csv',
    'Wimbledon-men-2013.csv'
]

folder_path = '/Users/sukara/Downloads/tennis+major+tournament+match+statistics/'

# Read and concatenate files into one DataFrame.
all_matches = pd.DataFrame()
for filename in csv_filenames:
    file_path = os.path.join(folder_path, filename)
    df = pd.read_csv(file_path,
                     dtype={
                         'Result': int,
                         'UFE.1': float,
                         'WNR.1': float,
                         'UFE.2': float,
                         'WNR.2': float
                     })

    # Drop rows where any of the specified columns have NA
    df = df.dropna(subset=['UFE.1', 'WNR.1', 'UFE.2', 'WNR.2'])
    all_matches = pd.concat([all_matches, df], ignore_index=True)


def calculate_consistency_win_relationship(df):
    # Calculate consistency for each player
    df['ErrorRate_P1'] = df['UFE.1'] - df['WNR.1']
    df['ErrorRate_P2'] = df['UFE.2'] - df['WNR.2']

    # Determine which player was more consistent
    df['Consistency'] = (df['ErrorRate_P1'] < df['ErrorRate_P2']).astype(int)

    # Calculate the probability of winning based on consistency
    higher_consistency_wins = (df['Consistency'] == 1) & (
        df['Result'] == 1) | (df['Consistency'] == 0) & (df['Result'] == 0)
    probability_higher_consistency_wins = higher_consistency_wins.mean()

    return probability_higher_consistency_wins


# Calculate the probability for Consistency
probability_consistency = calculate_consistency_win_relationship(all_matches)
print(
    f"The overall probability of winning with higher consistency across the specified Grand Slams is: {probability_consistency:.2f}"
    # 0.86
)
