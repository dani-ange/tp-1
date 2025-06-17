from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from joblib import dump
import os

def train_model():
    digits = load_digits()
    X_train, X_test, y_train, y_test = train_test_split(
        digits.data, digits.target, test_size=0.2, random_state=42
    )

    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X_train, y_train)

    os.makedirs("model", exist_ok=True)
    dump(clf, "model/mnist_model.joblib")
    print("✅ Model trained and saved to model/mnist_model.joblib")

if __name__ == "__main__":
    train_model()
