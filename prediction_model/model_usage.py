import torch
import torch.nn as nn
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import json
from pathlib import Path


class InsuranceModel(nn.Module):
    def __init__(self, input_size=9):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.2),

            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(0.1),

            nn.Linear(32, 1),
            nn.ReLU()
        )

    def forward(self, x):
        return self.model(x)


def save_test_model():
    """Create and save a test model with proper components"""
    model = InsuranceModel(input_size=9)

    # Create and fit scaler with dummy data
    scaler = StandardScaler()
    dummy_data = np.array([
        [35, 800000, 8000000, 22857, 0.15, 1, 1, 1, 0],  # Sample feature vector
        [40, 1000000, 10000000, 25000, 0.12, 0, 2, 0, 1]  # Another sample
    ])
    scaler.fit(dummy_data)

    # Save encoders classes for validation
    encoders = {
        'Gender': ['Male', 'Female'],
        'Health_Status': ['Good', 'Average', 'Poor'],
        'Marital_Status': ['Single', 'Married', 'Divorced'],
        'Claim_History': ['No Claims', 'Low Claims', 'High Claims']
    }

    # Save encoder classes separately
    Path('encoders.json').write_text(json.dumps(encoders))

    # Save model state
    torch.save({
        'model_state_dict': model.state_dict(),
        'input_size': 9,
        'scaler_mean_': scaler.mean_,
        'scaler_scale_': scaler.scale_,
        'feature_names': [
            'Age', 'Annual_Income', 'Sum_Assured',
            'Income_to_Age', 'Premium_to_Income',
            'Gender', 'Health_Status', 'Marital_Status',
            'Claim_History'
        ]
    }, 'insurance_model.pth')

    print("Model components saved successfully")


def load_model():
    """Load model with proper error handling"""
    try:
        # Load model components
        model_path = Path('insurance_model.pth')
        encoders_path = Path('encoders.json')

        if not model_path.exists() or not encoders_path.exists():
            raise FileNotFoundError("Model or encoder files not found")

        # Load model state
        checkpoint = torch.load(
            model_path, map_location='cpu', weights_only=False)
        model = InsuranceModel(input_size=checkpoint['input_size'])
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()

        # Recreate scaler
        scaler = StandardScaler()
        scaler.mean_ = checkpoint['scaler_mean_']
        scaler.scale_ = checkpoint['scaler_scale_']

        # Load encoders
        encoders = json.loads(encoders_path.read_text())

        return model, scaler, encoders

    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None, None, None


def calculate_sum_assured(age, annual_income):
    """Calculate recommended sum assured based on age and income"""
    if age < 30:
        multiplier = 15
    elif age < 40:
        multiplier = 12
    elif age < 50:
        multiplier = 8
    else:
        multiplier = 5
    return min(annual_income * multiplier, 30000000)  # Cap at 3 Cr


def recommend_policy_type(age, annual_income, marital_status):
    """Recommend suitable insurance policy"""
    if age < 35 and marital_status == 'Single':
        return "Term Insurance Plan"
    elif annual_income > 1000000:  # > 10L
        return "ULIP"
    elif age > 45:
        return "Retirement Plan"
    elif marital_status == 'Married':
        return "Endowment Plan"
    else:
        return "Term Insurance Plan"


def calculate_term(age):
    """Calculate recommended policy term"""
    max_term = min(70 - age, 30)  # Max 30 years or till age 70
    if age < 30:
        return max_term
    elif age < 40:
        return min(max_term, 25)
    elif age < 50:
        return min(max_term, 20)
    else:
        return min(max_term, 15)


def calculate_conversion_likelihood(age, annual_income, health_status, claim_history):
    """Calculate likelihood of conversion as percentage"""
    score = 0

    # Age factor (younger = higher likelihood)
    if age < 30:
        score += 30
    elif age < 40:
        score += 25
    elif age < 50:
        score += 20
    else:
        score += 15

    # Income factor
    if annual_income > 1000000:  # > 10L
        score += 30
    elif annual_income > 500000:  # > 5L
        score += 25
    else:
        score += 20

    # Health status
    health_scores = {
        'Good': 25,
        'Average': 20,
        'Poor': 10
    }
    score += health_scores.get(health_status, 15)

    # Claims history
    claims_scores = {
        'No Claims': 15,
        'Low Claims': 10,
        'High Claims': 5
    }
    score += claims_scores.get(claim_history, 7)

    return min(score, 100)  # Cap at 100%


def make_prediction(customer_data):
    """Make prediction with validation"""
    try:
        model, scaler, encoders = load_model()
        if not all([model, scaler, encoders]):
            return "Error: Model components not loaded properly"

        # Validate input data
        required_fields = ['age', 'gender', 'health_status', 'marital_status',
                           'annual_income', 'claim_history']
        if not all(field in customer_data for field in required_fields):
            return "Error: Missing required customer data fields"

        # Prepare features
        features = np.array([[
            customer_data['age'],
            customer_data['annual_income'],
            calculate_sum_assured(
                customer_data['age'], customer_data['annual_income']),
            customer_data['annual_income'] / customer_data['age'],
            0,  # Premium to income ratio (will be updated)
            encoders['Gender'].index(customer_data['gender']),
            encoders['Health_Status'].index(customer_data['health_status']),
            encoders['Marital_Status'].index(customer_data['marital_status']),
            encoders['Claim_History'].index(customer_data['claim_history'])
        ]])

        # Scale features
        scaled_features = scaler.transform(features)
        features_tensor = torch.FloatTensor(scaled_features)

        # Make prediction
        with torch.no_grad():
            prediction = model(features_tensor)
            predicted_premium = max(prediction.item(), 1000)

        return {
            'recommended_policy': recommend_policy_type(
                customer_data['age'],
                customer_data['annual_income'],
                customer_data['marital_status']
            ),
            'sum_assured': f"₹{calculate_sum_assured(customer_data['age'], customer_data['annual_income']):,.2f}",
            'premium_per_year': f"₹{predicted_premium:,.2f}",
            'recommended_term': f"{calculate_term(customer_data['age'])} years",
            'conversion_likelihood': f"{calculate_conversion_likelihood(
                customer_data['age'],
                customer_data['annual_income'],
                customer_data['health_status'],
                customer_data['claim_history']
            ):.1f}%"
        }

    except Exception as e:
        return f"Error making prediction: {str(e)}"


if __name__ == "__main__":
    save_test_model()

    sample_customer = {
        'age': 35,
        'gender': 'Male',
        'health_status': 'Good',
        'marital_status': 'Married',
        'annual_income': 800000,
        'claim_history': 'No Claims'
    }

    result = make_prediction(sample_customer)
    print("\nInsurance Recommendation:")
    print("-" * 50)
    if isinstance(result, dict):
        for key, value in result.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    else:
        print(result)
