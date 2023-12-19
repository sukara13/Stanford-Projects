import numpy as np
import pandas as pd

# Read the CSV file
df = pd.read_csv('Djoker vs Nadal All Matches Stats - Sheet1.csv')

# Discretize 'Consistency' and 'FSW'
df['Consistency'] = (df['WNR.1'] - df['UFE.1']) > (df['WNR.2'] - df['UFE.2'])
df['FSW'] = df['FSW.1'] > df['FSW.2']
df['Consistency'] = df['Consistency'].astype(int)
df['FSW'] = df['FSW'].astype(int)

# Split the data (simple split)
split_index = int(len(df) * 0.98305085)
train_data = df.iloc[:split_index]
test_data = df.iloc[split_index:]

X_train = train_data[['Consistency', 'FSW']].values
y_train = train_data['Result'].values
X_test = test_data[['Consistency', 'FSW']].values
y_test = test_data['Result'].values

# Naive Bayes implementation
labels, counts = np.unique(y_train, return_counts=True)
prob_Y = counts / y_train.size
num_features = X_train.shape[1]
num_labels = 2
prob_X_given_Y = np.zeros((num_labels, num_features, 2))

for label_index, label_val in enumerate(labels):
    labels_subset = X_train[y_train == label_val]
    feature_counts = np.sum(labels_subset, axis=0)
    prob_X_given_Y[label_index, :,
                   1] = (feature_counts + 1) / (labels_subset.shape[0] + 2)
    prob_X_given_Y[label_index, :, 0] = 1 - prob_X_given_Y[label_index, :, 1]


def predict(X):
    log_prob_Y = np.log(prob_Y)
    log_probs = np.zeros((X.shape[0], num_labels))
    for label_index in range(num_labels):
        log_probs[:, label_index] = X.dot(np.log(prob_X_given_Y[label_index, :, 1])) + \
                                    (1 - X).dot(np.log(prob_X_given_Y[label_index, :, 0])) + \
                                    log_prob_Y[label_index]
    return np.argmax(log_probs, axis=1)


# Predictions and accuracy
predicted_labels = predict(X_test)
accuracy = np.mean(predicted_labels == y_test)
print(f"Classification accuracy: {accuracy}")

# Convert to pandas Series for easy manipulation
predicted_series = pd.Series(predicted_labels, name='Predicted')
actual_series = pd.Series(y_test, name='Actual')

# Reset index of test_data to align with the series
test_data_reset = test_data.reset_index(drop=True)

# Combine actual outcomes, predictions, and test data into one DataFrame
results_df = pd.concat([test_data_reset, actual_series, predicted_series],
                       axis=1)

# Display the DataFrame
print(results_df)
