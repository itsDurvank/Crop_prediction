# modelCreation.py
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import joblib
import os

# Create directory for saving models
os.makedirs('models', exist_ok=True)

# Load the dataset
crop_data = pd.read_csv('Crop_recommendation.csv')

# Map crop names to numbers
crop_dict = {
    'rice': 1, 'maize': 2, 'jute': 3, 'cotton': 4, 'coconut': 5, 'papaya': 6, 'orange': 7, 'apple': 8,
    'muskmelon': 9, 'watermelon': 10, 'grapes': 11, 'mango': 12, 'banana': 13, 'pomegranate': 14,
    'lentil': 15, 'blackgram': 16, 'mungbean': 17, 'mothbeans': 18, 'pigeonpeas': 19, 'kidneybeans': 20,
    'chickpea': 21, 'coffee': 22
}
crop_data['crop_num'] = crop_data['label'].map(crop_dict)
crop_data.drop('label', axis=1, inplace=True)

# Separate features and target
x = crop_data.drop('crop_num', axis=1)
y = crop_data['crop_num']

# Split the data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Scale features using MinMaxScaler
ms = MinMaxScaler()
x_train = ms.fit_transform(x_train)
x_test = ms.transform(x_test)

# Standardize the features using StandardScaler
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

# Train the model
gnb = GaussianNB()
gnb.fit(x_train, y_train)

# Predict and evaluate
y_pred = gnb.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: {:.2f}%".format(accuracy * 100))

# Save the model and scalers
joblib.dump(gnb, 'models/crop_recommendation_model.pkl')
joblib.dump(ms, 'models/minmax_scaler.pkl')
joblib.dump(sc, 'models/standard_scaler.pkl')
print("Model and scalers saved successfully in the 'models' directory.")
