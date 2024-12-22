import joblib
import pandas as pd


# Load all the saved components
categorical_values = joblib.load('p_sa/categorical_values.pkl')
numerical_columns = joblib.load('p_sa/numerical_columns.pkl')
target_columns = joblib.load('p_sa/target_columns.pkl')

# Load models
models = {}
for column in target_columns:
    models[column] = joblib.load(f'p_sa/model_{column.lower()}.pkl')

# Example prediction function
def predict_insurance(user_data):
    predictions = {}
    for column, model in models.items():
        predictions[column] = model.predict(user_data)[0]
    return predictions

# Example usage
new_user_data = pd.DataFrame({
    'Age': [65],
    'Gender': ['Female'],
    'Health_Status': ['Excellent'],
    'Marital_Status': ['Widowed'],
    'Insurance_Type': ['None'],
    'Claims_Count': [5],
    'Retirement_Status': ['Retired']
})

predictions = predict_insurance(new_user_data)
for target, value in predictions.items():
    print(f"{target}: {value:.2f}")