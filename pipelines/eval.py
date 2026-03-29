# pipelines/eval.py
# AI Feature Evaluation Script, Aligned with Courseware Pipeline Requirements
import pandas as pd
import joblib
from sklearn.metrics import r2_score

def evaluate_model(model_path, test_data_path, report_path):
    """Model evaluation function: generate evaluation report and save to the reports directory"""
    # Load model and test data
    model = joblib.load(model_path)
    test_data = pd.read_csv(test_data_path)
    X_test = test_data.drop('target', axis=1)
    y_test = test_data['target']
    
    # Evaluate model (aligned with EvalSpec requirements)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    
    # Generate evaluation report and save to the reports directory
    report = f"Model Evaluation Report\n=============\nTest Data Path: {test_data_path}\nR2 Score: {r2:.4f}\nEvaluation Date: 2026-03-30"
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"Evaluation completed, report saved to: {report_path}")
    return r2

# Example usage
if __name__ == "__main__":
    evaluate_model('src/trained_model.pkl', 'examples/test_data.csv', 'reports/eval_report.md')
