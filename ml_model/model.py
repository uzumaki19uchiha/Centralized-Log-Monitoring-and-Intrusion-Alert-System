# model.py

from sklearn.ensemble import IsolationForest
import numpy as np

# Create model globally
model = IsolationForest(contamination=0.1)

def train_model():
    # Fake normal traffic for initial training
    normal_data = np.array([
        [10, 1, 0.1, 3],
        [12, 2, 0.2, 4],
        [8, 1, 0.05, 2],
        [15, 0, 0.1, 3],
        [9, 1, 0.15, 2]
    ])
    
    model.fit(normal_data)

def predict(features):
    features_array = np.array([features])
    prediction = model.predict(features_array)
    score = model.decision_function(features_array)

    return prediction[0], score[0]