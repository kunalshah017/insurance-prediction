import pandas as pd
import numpy as np
from faker import Faker
import random

# Initialize Faker
fake = Faker()
np.random.seed(42)
random.seed(42)

# Define parameters
n_records = 2000

# Define possible values
health_statuses = ['Excellent', 'Good', 'Fair', 'Poor']
insurance_types = ['None', 'Term Life', 'Whole Life',
                   'ULIP', 'Endowment', 'Health Insurance']
claim_categories = ['No Claims', '1 Claim', '2 Claims', '3+ Claims']
marital_statuses = ['Single', 'Married', 'Divorced', 'Widowed']
relationships = ['Spouse', 'Child', 'Parent', 'Sibling']


def generate_family_details():
    family_size = np.random.randint(0, 5)
    details = []
    for _ in range(family_size):
        relation = random.choice(relationships)
        if relation == 'Child':
            age = np.random.randint(1, 25)
        elif relation == 'Spouse':
            age = np.random.randint(25, 60)
        else:
            age = np.random.randint(45, 80)
        details.append(f"{relation}:{age}")
    return ';'.join(details) if details else 'None'


# Generate base data
data = {
    'Age': np.random.randint(25, 70, n_records),
    'Gender': np.random.choice(['Male', 'Female'], n_records),
    'Health_Status': np.random.choice(health_statuses, n_records, p=[0.3, 0.4, 0.2, 0.1]),
    'Marital_Status': np.random.choice(marital_statuses, n_records),
    'Current_Insurance': np.random.choice(insurance_types, n_records),
    'Previous_Policies': np.random.randint(0, 5, n_records),
    'Claim_History': np.random.choice(claim_categories, n_records)
}

# Create DataFrame
df = pd.DataFrame(data)

# Add correlated and derived fields
df['Annual_Income'] = (30000 + df['Age'] * 1000 +
                       np.random.normal(0, 20000, n_records)).astype(int)
df['Premium'] = (df['Annual_Income'] *
                 np.random.uniform(0.02, 0.05, n_records)).astype(int)
df['Sum_Assured'] = (
    df['Premium'] * np.random.uniform(10, 20, n_records)).astype(int)

# Add family details
df['Family_Details'] = [generate_family_details() for _ in range(n_records)]

# Add noise and missing values
df.loc[np.random.choice(df.index, 50), 'Annual_Income'] = np.nan
df['Premium'] = df['Premium'] * (1 + np.random.normal(0, 0.1, n_records))
df['Sum_Assured'] = df['Sum_Assured'] * \
    (1 + np.random.normal(0, 0.05, n_records))

# Clean up numerical columns
df['Premium'] = df['Premium'].round().astype(int)
df['Sum_Assured'] = df['Sum_Assured'].round().astype(int)
df['Annual_Income'] = df['Annual_Income'].round().astype(float)

# Save to CSV
df.to_csv('insurance_data.csv', index=False)

print("Dataset generated successfully with shape:", df.shape)
print("\nSample of generated data:")
print(df.head())
print("\nDataset statistics:")
print(df.describe())
