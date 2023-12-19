import pandas as pd

# In this code, we calculate the probability that each player wins given that they were more consistent, using data from their
# previous 58 matches. We find that the probability that Djokovic wins the next match given that he is more consistent is 0.88
# and that the probability that Nadal wins the next match given that he is more consistent is 0.76. In reality, Nadal won
# their last match and looking at stats for the 59th match he was much more consistent than Djokovic in this game (Winners
# - UFE for Nadal was +24 higher than Djokovic).

# Load Djoker vs Nadal csv file into a dataframe
df_matches = pd.read_csv(
    '/Users/sukara/Downloads/tennis+major+tournament+match+statistics/Djoker vs Nadal All Matches Stats - Sheet1.csv'
)

# Drop the last row which is the French Open 2022 that we don't have data for the calculations
df_matches = df_matches[:-1]

############## Djokovic Wins Given More Consistent #################


# Define the functions for calculating each probability component
def calculate_P_result_given_consistency(df):
    # Calculate consistency for Djokovic (1) and Nadal (2). 'More_Consistent' is 1 if Djokovic had less 
    # UFE - Winners, and is 0 if Nadal did
    df['Consistency_1'] = df['UFE.1'] - df['WNR.1']
    df['Consistency_2'] = df['UFE.2'] - df['WNR.2']
    df['More_Consistent'] = df['Consistency_1'] < df['Consistency_2']

    # Calculate P(Result = 1 and Consistency = 1)
    P_result_and_consistency = ((df['Result'] == 1)
                                & df['More_Consistent']).mean()

    # Calculate P(Result = 1)
    P_result = (df['Result'] == 1).mean()

    # Calculate P(Consistency = 1)
    P_consistency = df['More_Consistent'].mean()

    # Calculate P(Consistency = 1 | Result = 1)
    P_consistency_given_result = P_result_and_consistency / P_result

    # Apply Bayes' Theorem to find P(Result = 1 | Consistency = 1)
    P_result_given_consistency = (P_consistency_given_result *
                                  P_result) / P_consistency

    return P_result_given_consistency


# Calculate the probability P(Result = 1 | Consistency = 1)
probability = calculate_P_result_given_consistency(df_matches)
print(
    f"The probability that Djokovic wins the next match given that he is more consistent is: {probability:.2f}"
)

############ Nadal Wins Given More Consistent ###################


def calculate_P_result_0_given_consistency_0(df):
    df['Consistency_1'] = df['UFE.1'] - df['WNR.1']
    df['Consistency_2'] = df['UFE.2'] - df['WNR.2']
    df['Less_Consistent'] = df['Consistency_1'] > df['Consistency_2']

    P_result_0_and_consistency_0 = ((df['Result'] == 0)
                                    & df['Less_Consistent']).mean()

    P_result_0 = (df['Result'] == 0).mean()

    P_consistency_0 = df['Less_Consistent'].mean()

    P_consistency_0_given_result_0 = P_result_0_and_consistency_0 / P_result_0

    P_result_0_given_consistency_0 = (P_consistency_0_given_result_0 *
                                      P_result_0) / P_consistency_0

    return P_result_0_given_consistency_0


# Calculate the probability P(Result = 0 | Consistency = 0)
probability_0 = calculate_P_result_0_given_consistency_0(df_matches)
print(
    f"The probability that Nadal wins the next match given that he is more consistent is: {probability_0:.2f}"
)
