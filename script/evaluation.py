from sklearn.metrics import classification_report
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from joblib import load

def evaluate_model():
    digits = load_digits()
    _, X_test, _, y_test = train_test_split(
        digits.data, digits.target, test_size=0.2, random_state=42
    )

    model = load("model/mnist_model.joblib")
    y_pred = model.predict(X_test)

    print("📊 Evaluation Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    evaluate_model()
