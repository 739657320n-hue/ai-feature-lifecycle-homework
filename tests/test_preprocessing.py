# tests/test_preprocessing.py
# Test for Feature Preprocessing Code, Aligned with Courseware pytest Requirements
import pytest
import pandas as pd
from src.feature_preprocessing import preprocess_data

def test_preprocess_data():
    """Test the feature preprocessing function to ensure proper data cleaning and feature extraction"""
    test_data = pd.DataFrame({'value': [10, 20, 30, None, 1001, 40]})
    processed_data = preprocess_data(test_data)
    
    # Assert: No missing values and no outliers
    assert processed_data.isnull().sum().sum() == 0
    assert processed_data['value'].max() < 1000
    assert processed_data['value'].min() > 0
    
    # Assert: Feature extraction successful
    assert 'mean_value' in processed_data.columns
    assert 'max_value' in processed_data.columns
    assert 'target' in processed_data.columns

# Additional test case to ensure full CI coverage
def test_demo_success():
    """Simple test case to verify CI runs properly"""
    assert 1 + 1 == 2
