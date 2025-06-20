from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from joblib import dump
from pathlib import Path
import json
import time

def train_model():
    digits = load_digits()
    X_train, X_test, y_train, y_test = train_test_split(
        digits.data, digits.target, test_size=0.2, random_state=42
    )

    clf = RandomForestClassifier(n_estimators=100)

    start_time = time.time()
    clf.fit(X_train, y_train)
    end_time = time.time()

    train_acc = accuracy_score(y_train, clf.predict(X_train))
    test_acc = accuracy_score(y_test, clf.predict(X_test))

    Path("model").mkdir(exist_ok=True)
    dump(clf, "model/mnist_model.joblib")
    print("✅ Model trained and saved to model/mnist_model.joblib")

    # Create docs directory for GitHub Pages
    Path("docs").mkdir(exist_ok=True)

    training_log = {
        "n_estimators": clf.n_estimators,
        "train_accuracy": train_acc,
        "test_accuracy": test_acc,
        "training_time_seconds": round(end_time - start_time, 4)
    }

    # Save JSON log
    with open("docs/training_log.json", "w") as f:
        json.dump(training_log, f, indent=2)
    print("✅ Training log saved to docs/training_log.json")

    # Auto-generate HTML to render the log
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Training Log</title>
  <style>
    body {{ font-family: Arial, sans-serif; padding: 2rem; }}
    pre {{ background: #f0f0f0; padding: 1rem; border-radius: 5px; }}
  </style>
</head>
<body>
  <h1>Model Training Log</h1>
  <pre id="log">Loading...</pre>
  <script>
    fetch('training_log.json')
      .then(res => res.json())
      .then(data => {{
        document.getElementById('log').textContent = JSON.stringify(data, null, 2);
      }})
      .catch(err => {{
        document.getElementById('log').textContent = 'Error loading log: ' + err;
      }});
  </script>
</body>
</html>
"""

    with open("docs/index.html", "w") as f:
        f.write(html_content.strip())
    print("✅ HTML report generated at docs/index.html")

if __name__ == "__main__":
    train_model()
