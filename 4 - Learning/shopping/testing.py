# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 21:34:48 2022

@author: Rohan
"""

from shopping import *


# Load data from spreadsheet and split into train and test sets
evidence, labels = load_data("shopping.csv")
X_train, X_test, y_train, y_test = train_test_split(
    evidence, labels, test_size=TEST_SIZE
)

# Train model and make predictions
model = train_model(X_train, y_train)
predictions = model.predict(X_test)
sensitivity, specificity = evaluate(y_test, predictions)

# Print results
print(f"Correct: {(y_test == predictions).sum()}")
print(f"Incorrect: {(y_test != predictions).sum()}")
print(f"True Positive Rate: {100 * sensitivity:.2f}%")
print(f"True Negative Rate: {100 * specificity:.2f}%")