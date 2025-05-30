
import pandas as pd
import json
import numpy as np


# Function to fe
import pandas as pd
#Load df
def load_df(file_path):
    df = pd.read_csv(file_path)
    return df
df = load_df("FILE.csv")
df = df.sort_values('date')
# One-hot encoding (for low-cardinality categories)
df = pd.get_dummies(df, columns=['ProductId','Group', 'ZoneId'])


def create_sequences(data, target, window_size):
    X_seq, y_seq = [], []
    for i in range(len(data) - window_size):
        X_seq.append(data[i:i+window_size])
        y_seq.append(target[i+window_size])
    return np.array(X_seq), np.array(y_seq)



window_size = 8
#_seq, y_seq = create_sequences(X_scaled, y_scaled, window_size)
