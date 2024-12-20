import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F  # Add this import
from sklearn.preprocessing import StandardScaler, LabelEncoder, RobustScaler
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")


def verify_columns(df):
    """Verify and print available columns"""
    print("\nAvailable columns in dataset:")
    for col in df.columns:
        print(f"- {col}")
    return df.columns.tolist()


def preprocess_data(df):
    """Preprocess data with proper type conversion"""
    df = df.copy()

    # 1. Handle categorical features
    cat_cols = ['Gender', 'Health_Status', 'Marital_Status', 'Claim_History']
    label_encoders = {}

    for col in cat_cols:
        label_encoders[col] = LabelEncoder()
        df[col] = label_encoders[col].fit_transform(df[col].astype(str))

    # 2. Handle numeric columns with proper error handling
    numeric_cols = ['Age', 'Annual_Income', 'Sum_Assured', 'Premium']
    for col in numeric_cols:
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Fill numeric nulls with median
            df[col] = df[col].fillna(df[col].median())
        except Exception as e:
            print(f"Error converting {col}: {str(e)}")

    # 3. Drop problematic columns
    cols_to_drop = [
        'Current_Insurance',
        'Previous_Policies',
        'Family_Details'  # Will handle family details separately if needed
    ]
    df = df.drop(columns=cols_to_drop, errors='ignore')

    # 4. Feature engineering (only after numeric conversion)
    df['Income_to_Age'] = df['Annual_Income'] / df['Age']
    df['Premium_to_Income'] = df['Premium'] / df['Annual_Income']

    # 5. Scale numeric features
    num_cols_to_scale = [
        'Age',
        'Annual_Income',
        'Sum_Assured',
        'Income_to_Age',
        'Premium_to_Income'
    ]

    # Replace infinities before scaling
    df = df.replace([np.inf, -np.inf], np.nan)
    df[num_cols_to_scale] = df[num_cols_to_scale].fillna(
        df[num_cols_to_scale].median())

    scaler = RobustScaler()
    df[num_cols_to_scale] = scaler.fit_transform(df[num_cols_to_scale])

    return df, scaler, label_encoders


class InsuranceDataset(Dataset):
    def __init__(self, features, targets):
        # Ensure all inputs are float32
        self.features = torch.FloatTensor(features.astype(np.float32))
        self.targets = torch.FloatTensor(
            targets.astype(np.float32)).reshape(-1, 1)

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.targets[idx]


class ImprovedInsuranceModel(nn.Module):
    def __init__(self, input_size):
        super().__init__()

        # Print input size for debugging
        print(f"Model input size: {input_size}")

        # Layer architecture
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 16)
        self.fc4 = nn.Linear(16, 1)

        # Batch normalization
        self.bn1 = nn.BatchNorm1d(64)
        self.bn2 = nn.BatchNorm1d(32)
        self.bn3 = nn.BatchNorm1d(16)

        # Dropout for regularization
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        # First layer
        x1 = self.fc1(x)
        x1 = self.bn1(x1)
        x1 = F.relu(x1)
        x1 = self.dropout(x1)

        # Second layer with residual
        x2 = self.fc2(x1)
        x2 = self.bn2(x2)
        x2 = F.relu(x2)
        x2 = self.dropout(x2)
        x2 = x2 + x1[:, :32]  # Residual connection

        # Third layer
        x3 = self.fc3(x2)
        x3 = self.bn3(x3)
        x3 = F.relu(x3)
        x3 = self.dropout(x3)

        # Output layer
        out = self.fc4(x3)
        return F.relu(out)  # Ensure positive output


def train_model(model, train_loader, val_loader, criterion, optimizer, device, scaler, encoders, epochs=1000):
    model = model.to(device)
    best_val_loss = float('inf')
    patience = 15
    counter = 0

    for epoch in range(epochs):
        # Training
        model.train()
        train_loss = 0
        for batch_X, batch_y in train_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)

            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)
            optimizer.step()

            train_loss += loss.item()

        # Validation
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch_X, batch_y in val_loader:
                batch_X, batch_y = batch_X.to(device), batch_y.to(device)
                outputs = model(batch_X)
                val_loss += criterion(outputs, batch_y).item()

        val_loss /= len(val_loader)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            counter = 0
            torch.save({
                'model_state_dict': model.state_dict(),
                'scaler': scaler,
                'encoders': encoders,
                'input_size': model.fc1.in_features
            }, 'insurance_model.pth')
        else:
            counter += 1

        if counter >= patience:
            print(f"Early stopping at epoch {epoch}")
            break

        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Train Loss: {train_loss /
                  len(train_loader):.4f}, Val Loss: {val_loss:.4f}")


def calculate_sum_assured(age, annual_income):
    """More conservative sum assured calculation"""
    if age < 30:
        multiplier = 15
    elif age < 40:
        multiplier = 12
    elif age < 50:
        multiplier = 8
    else:
        multiplier = 5
    return min(annual_income * multiplier, 30000000)  # Cap at 3 Cr


def main():
    try:
        # Load data with proper encoding
        df = pd.read_csv(
            'K:/Insurance-Prediction/insurance_data.csv', encoding='utf-8')

        # Print data info for debugging
        print("\nDataset Info:")
        print(df.info())

        processed_df, scaler, encoders = preprocess_data(df)

        # Verify processed data
        print("\nProcessed columns:", processed_df.columns.tolist())
        print("Processed dtypes:", processed_df.dtypes)

        # Split features and target
        X = processed_df.drop('Premium', axis=1).values  # Convert to numpy
        y = processed_df['Premium'].values  # Convert to numpy

        print(f"Features shape: {X.shape}")
        print(f"Target shape: {y.shape}")

        # Train/val split
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Create datasets
        train_dataset = InsuranceDataset(X_train, y_train)
        val_dataset = InsuranceDataset(X_val, y_val)

        # Create loaders
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=32)

        # Initialize model
        model = ImprovedInsuranceModel(input_size=X.shape[1])
        criterion = nn.MSELoss()
        optimizer = torch.optim.AdamW(
            model.parameters(), lr=0.001, weight_decay=0.01
        )

        # Train model
        train_model(model, train_loader, val_loader,
                    criterion, optimizer, device, scaler, encoders)

        # Save model components
        torch.save({
            'model_state_dict': model.state_dict(),
            'scaler': scaler,
            'encoders': encoders
        }, 'insurance_model.pth')

        return model, scaler, encoders

    except Exception as e:
        print(f"Error in main(): {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None, None


if __name__ == "__main__":
    model, scaler, encoders = main()
