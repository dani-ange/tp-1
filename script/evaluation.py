from sklearn.metrics import classification_report, accuracy_score, f1_score
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from joblib import load
import json

def evaluate_model():
    digits = load_digits()
    _, X_test, _, y_test = train_test_split(
        digits.data, digits.target, test_size=0.2, random_state=42
    )

    model = load("model/mnist_model.joblib")
    y_pred = model.predict(X_test)

    # Compute metrics
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')

    print("📊 Evaluation Report:")
    print(classification_report(y_test, y_pred))

    results = {
        "accuracy": accuracy,
        "f1_score": f1,
    }

    # Save metrics to results.json
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("✅ Results saved to results.json")

if __name__ == "__main__":
    evaluate_model()
