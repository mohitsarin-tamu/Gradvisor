import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import random 
import joblib


gre_scores = {
'Worcester Polytechnic Institute': random.randint(260, 270), 
'Wayne State University': random.randint(320, 330),
'Virginia Polytechnic Institute and State University': random.randint(320, 330),
'University of Wisconsin Madison': random.randint(320, 330),
'University of Washington': random.randint(320, 330),
'University of Utah': random.randint(320, 330),
'University of Texas Dallas': random.randint(320, 330),
'University of Texas Austin': random.randint(310, 320),
'University of Texas Arlington': random.randint(310, 320),
'University of Southern California': random.randint(310, 320),
'University of Pennsylvania': random.randint(310, 320),
'University of North Carolina Charlotte': random.randint(310, 320),
'University of North Carolina Chapel Hill': random.randint(310, 320),
'University of Minnesota Twin Cities': random.randint(310, 320),
'University of Michigan Ann Arbor': random.randint(310, 320),
'University of Massachusetts Amherst': random.randint(300, 310),
'University of Maryland College Park': random.randint(300, 310),
'University of Illinois Urbana-Champaign': random.randint(300, 310),
'University of Illinois Chicago': random.randint(300, 310),
'University of Florida': random.randint(300, 310),
'University of Colorado Boulder': random.randint(300, 310),
'University of Cincinnati': random.randint(300, 310),
'University of California Santa Cruz': random.randint(300, 310),
'University of California Santa Barbara': random.randint(290, 300),
'University of California San Diego': random.randint(290, 300),
'University of California Los Angeles': random.randint(290, 300),
'University of California Irvine': random.randint(290, 300),
'University of California Davis': random.randint(290, 300),
'University of Arizona': random.randint(290, 300),
'Texas A and M University College Station': random.randint(290, 300),
'Syracuse University': random.randint(290, 300),
'SUNY Stony Brook': random.randint(280, 290),
'SUNY Buffalo': random.randint(280, 290),
'Stanford University': random.randint(280, 290),
'Rutgers University New Brunswick/Piscataway': random.randint(280, 290),
'Purdue University': random.randint(280, 290),
'Princeton University': random.randint(280, 290),
'Ohio State University Columbus': random.randint(280, 290),
'Northwestern University': random.randint(280, 290),
'Northeastern University': random.randint(270, 280),
'North Carolina State University': random.randint(270, 280),
'New York University': random.randint(270, 280),
'New Jersey Institute of Technology': random.randint(270, 280),
'Massachusetts Institute of Technology': random.randint(270, 280),
'Johns Hopkins University': random.randint(270, 280),
'Harvard University': random.randint(270, 280),
'Georgia Institute of Technology': random.randint(270, 280),
'George Mason University': random.randint(260, 270),
'Cornell University': random.randint(260, 270),
'Columbia University': random.randint(260, 270),
'Clemson University': random.randint(260, 270),
'Carnegie Mellon University': random.randint(260, 270),
'California Institute of Technology': random.randint(260, 270),
'Arizona State University': random.randint(260, 270)
}

# Step 1: Load data from CSV
file_path = "user_user_wo_toefl_score.csv"
df = pd.read_csv(file_path)

print(df)

# Step 2: Replace infinity values with NaN
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Step 3: Replace NaN with 0
df.fillna(2, inplace=True)

# Step 5: Remove rows where admit = 0
df = df[df['admit'] != 0]

# Print all columns for the selected username
# print(df.head)

# Step 6: Update the DataFrame with the GRE scores based on university names
df['grescore'] = df['univName'].map(gre_scores)
# print(df.head)

df = pd.get_dummies(df, columns=["major"])
print(df.shape)

# Step 15: Split data into features and target
X = df.drop(columns=["univName", "admit", "greV", "greQ"])

y = df["univName"]
print("Number of unique universities:", df['univName'].nunique())
# print('user data:', user_df)

# Step 16: Train-test split
# Step 15: Train-test split (updated)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)# stratify=y)

X_train.drop(columns=['userName'], inplace=True)
X_test.drop(columns=['userName'], inplace=True)

# print("Size of X_train:", X_train.shape)
# print("Size of X_test:", X_test.shape)


# Step 17: Define the parameter grid for GridSearchCV
param_grid = {
    'n_estimators': [100],
    'max_depth': [10],
    'min_samples_split': [10]
}


# Step 18: Perform GridSearchCV to find the best hyperparameters
rf_model = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(rf_model, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Step 19: Get the best hyperparameters and model
best_params = grid_search.best_params_
best_model = grid_search.best_estimator_

# Step 20: Model evaluation (continued)
# Get the predicted probabilities for each class
print(X_test.columns)
y_pred_proba = best_model.predict_proba(X_test)

# Get the classes
classes = best_model.classes_

# Initialize a list to store top five precision predictions and usernames for each row
top_five_predictions_with_username = []

# Iterate over each row in y_pred_proba
for i, row in enumerate(y_pred_proba):
    # Get the indices of the top five classes with the highest probabilities
    top_five_indices = np.argsort(row)[::-1][:5]
    
    # Get the corresponding classes and probabilities
    top_five_classes = classes[top_five_indices]
    top_five_probs = row[top_five_indices]
    
    # Find the row index in the original DataFrame df that matches the current row in X_test
    original_index = X_test.index[i]
    
    # Find the username corresponding to the original index
    username = df.loc[original_index, 'userName']
    
    # Store the top five precision predictions and username for this row
    top_five_predictions_with_username.append((username, list(zip(top_five_classes, top_five_probs))))

# Print the top five precision predictions and username for each row
# for username, prediction in top_five_predictions_with_username:
#     print('\n',f"Username: {username}, Top five precision predictions: {prediction}")

# Calculate accuracy
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Save the best model
joblib.dump(best_model, 'random_forest_model_checkpoint.pkl')
