import joblib
import pandas as pd
import numpy as np
import os
from datetime import datetime

def load_specific_model(model_dir='policy'):
    """
    Load insurance model components.
    """
    try:
        version = '20241221_181106'  # Version from your saved files
        
        model = joblib.load(f'{model_dir}/insurance_model_components.joblib')
        scaler = joblib.load(f'{model_dir}/scaler.joblib')
        encoders = joblib.load(f'{model_dir}/encoders.joblib')
        metadata = joblib.load(f'{model_dir}/metadata.joblib')
        
        print("Model components loaded successfully!")
        print("\nModel metadata:")
        for key, value in metadata.items():
            print(f"{key}: {value}")
            
        return {
            'model': model,
            'scaler': scaler,
            'encoders': encoders,
            'metadata': metadata
        }
    except Exception as e:
        raise RuntimeError(f"Error loading model: {str(e)}")

def prepare_claim_history(value):
    """Convert claim history string to numeric value"""
    if isinstance(value, str):
        try:
            return int(value.split()[0].replace('+', ''))
        except (ValueError, IndexError):
            return 0
    return value

def prepare_family_ages(value):
    """Convert family ages string to numeric value"""
    if isinstance(value, str):
        try:
            ages = [int(age.split(':')[1]) for age in value.split(', ') if ':' in age]
            return sum(ages) if ages else 0
        except ValueError:
            return 0
    return value

def predict_insurance_policy(test_cases, model_components):
    """
    Make predictions using the loaded model components
    
    Parameters:
    -----------
    test_cases : list of dict
        List of test cases with user information
    model_components : dict
        Dictionary containing model, scaler, and encoders
    """
    results = []
    
    for test_case in test_cases:
        # Create DataFrame with single row
        df = pd.DataFrame([test_case])
        
        # Process claim history and family ages
        df['Claim_History'] = df['Claim_History'].apply(prepare_claim_history)
        df['Family_Ages'] = df['Family_Ages'].apply(prepare_family_ages)
        
        # Process categorical variables
        categorical_columns = ['Gender', 'Health_Status', 'Marital_Status', 
                             'Current_Insurance', 'Retirement_Status']
        
        encoded_data = df.copy()
        for col in categorical_columns:
            if col in df.columns and col in model_components['encoders']:
                encoded_data[col] = model_components['encoders'][col].transform(df[col])
        
        # Process family details as binary
        encoded_data['Family_Details'] = df['Family_Details'].apply(
            lambda x: 1 if isinstance(x, str) and ('child' in x.lower() or 'spouse' in x.lower()) else 0
        )
        
        # Ensure all columns are numeric
        numeric_data = encoded_data.select_dtypes(include=['number'])
        
        # Scale the features
        scaled_data = model_components['scaler'].transform(numeric_data)
        
        # Make prediction
        pred = model_components['model'].predict(scaled_data)
        pred_proba = model_components['model'].predict_proba(scaled_data)
        
        # Get the predicted policy name
        predicted_policy = model_components['encoders']['Recommended_Policy'].inverse_transform(pred)[0]
        
        # Get probabilities for all classes
        class_probabilities = dict(zip(
            model_components['encoders']['Recommended_Policy'].inverse_transform(range(len(pred_proba[0]))),
            pred_proba[0]
        ))
        
        results.append({
            'profile': test_case,
            'recommended_policy': predicted_policy,
            'probabilities': class_probabilities
        })
        
    return results

# Test cases
test_cases = [
    {
        'Age': 53,
        'Gender': 'Female',
        'Health_Status': 'Excellent',
        'Marital_Status': 'Divorced',
        'Current_Insurance': 'Retirement Insurance',
        'Previous_Policies': 4,
        'Annual_Income': 616416,
        'Claim_History': '2 claim',
        'Retirement_Status': 'Nearing Retirement',
        'Premium': 21176.71,
        'Sum_Assured': 924624,
        'Family_Details': '1 child',
        'Family_Ages': 'Child: 19'
    },
    {
        'Age': 24,
        'Gender': 'Male',
        'Health_Status': 'Good',
        'Marital_Status': 'Single',
        'Current_Insurance': 'Term Life',
        'Previous_Policies': 1,
        'Annual_Income': 403599,
        'Claim_History': '0 claim',
        'Retirement_Status': 'Not Retired',
        'Premium': 19685.92,
        'Sum_Assured': 403599,
        'Family_Details': 'No dependents',
        'Family_Ages': 'None'
    }
]

def main():
    # Load the model
    print("Loading model components...")
    model_components = load_specific_model()
    
    # Make predictions
    print("\nPredictions for Different User Profiles:")
    results = predict_insurance_policy(test_cases, model_components)
    
    # Print results
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Profile {i}:")
        print("Input characteristics:")
        print(f"Age: {result['profile']['Age']}")
        print(f"Gender: {result['profile']['Gender']}")
        print(f"Health Status: {result['profile']['Health_Status']}")
        print(f"Current Insurance: {result['profile']['Current_Insurance']}")
        print(f"Retirement Status: {result['profile']['Retirement_Status']}")
        print(f"Family Details: {result['profile']['Family_Details']}")
        print(f"Annual Income: {result['profile']['Annual_Income']:,}")
        
        print(f"\nRecommended Policy: {result['recommended_policy']}")
        print("Top 3 Policy Probabilities:")
        for policy_name, prob in sorted(result['probabilities'].items(), key=lambda x: x[1], reverse=True)[:3]:
            print(f"{policy_name}: {prob:.2%}")

if __name__ == "__main__":
    main()