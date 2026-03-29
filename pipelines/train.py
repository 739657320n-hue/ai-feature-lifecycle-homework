# pipelines/train.py
# AI Feature Training Script, Aligned with Courseware Pipeline Requirements
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

def train_model(data_path, model_save_path):
    """Model training function: load data, train model, and save the model"""
    # Load data (aligned with DataSpec requirements)
    data = pd.read_csv(data_path)
    X = data.drop('target', axis=1)
    y = data['target']
    
    # Train a baseline model (courseware requirement: start with a simple baseline model)
    model = LinearRegression()
    model.fit(X, y)
    
    # Save the model (aligned with model specification requirements)
    joblib.dump(model, model_save_path)
    print(f"Model training completed, saved to: {model_save_path}")

# Example usage (for subsequent testing)
if __name__ == "__main__":
    train_model('examples/train_data.csv', 'src/trained_model.pkl')
