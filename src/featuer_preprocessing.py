# src/feature_preprocessing.py
# Feature Preprocessing Script, Aligned with Courseware src Folder Requirements
import pandas as pd

def preprocess_data(data):
    """Feature preprocessing function: clean data and extract features"""
    # Data cleaning (aligned with DataSpec requirements)
    data = data.dropna()  # Drop missing values
    data = data[(data['value'] > 0) & (data['value'] < 1000)]  # Remove outliers
    
    # Feature extraction (aligned with courseware feature pipeline requirements)
    data['mean_value'] = data['value'].rolling(window=3).mean()
    data['max_value'] = data['value'].max()
    data['min_value'] = data['value'].min()
    
    # Add target column (for subsequent training)
    data['target'] = data['mean_value'].round(2)
    return data

# Example usage
if __name__ == "__main__":
    test_data = pd.DataFrame({'value': [10, 20, 30, None, 1001, 40]})
    processed_data = preprocess_data(test_data)
    print("Feature preprocessing completed:")
    print(processed_data)
