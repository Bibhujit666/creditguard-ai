
from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "saved_models" / "catboost.pkl"
THRESHOLD_PATH = BASE_DIR / "saved_models" / "best_threshold.pkl"

model = joblib.load(MODEL_PATH)
BEST_THRESHOLD = float(joblib.load(THRESHOLD_PATH))

FEATURE_COLUMNS = [
    "LIMIT_BAL", "SEX", "EDUCATION", "MARRIAGE", "AGE",
    "PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6",
    "BILL_AMT1", "BILL_AMT2", "BILL_AMT3", "BILL_AMT4", "BILL_AMT5", "BILL_AMT6",
    "PAY_AMT1", "PAY_AMT2", "PAY_AMT3", "PAY_AMT4", "PAY_AMT5", "PAY_AMT6"
]

CATEGORICAL_COLUMNS = [
    "SEX", "EDUCATION", "MARRIAGE",
    "PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"
]

INTEGER_COLUMNS = [
    "SEX", "EDUCATION", "MARRIAGE", "AGE",
    "PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"
]

@app.route("/")
def index():
    return render_template("index.html", threshold=BEST_THRESHOLD)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json(force=True)

        missing = [c for c in FEATURE_COLUMNS if c not in payload or payload[c] in ("", None)]
        if missing:
            return jsonify({
                "success": False,
                "error": "Please complete all fields.",
                "missing": missing
            }), 400

        row = {}
        for col in FEATURE_COLUMNS:
            row[col] = float(payload[col])

        # Match the training notebook's data cleaning exactly.
        row["EDUCATION"] = 5 if int(row["EDUCATION"]) in (0, 6) else int(row["EDUCATION"])
        row["MARRIAGE"] = 3 if int(row["MARRIAGE"]) == 0 else int(row["MARRIAGE"])

        for col in INTEGER_COLUMNS:
            row[col] = int(row[col])

        input_df = pd.DataFrame([row], columns=FEATURE_COLUMNS)

        probability = float(model.predict_proba(input_df)[0][1])
        prediction = int(probability >= BEST_THRESHOLD)

        if prediction == 1:
            status = "Likely to Default"
            risk = "High Risk"
            message = "The model estimates a higher likelihood of next-month payment default."
        else:
            status = "Likely to Repay"
            risk = "Lower Risk"
            message = "The model estimates a lower likelihood of next-month payment default."

        return jsonify({
            "success": True,
            "prediction": prediction,
            "status": status,
            "risk": risk,
            "probability": round(probability * 100, 2),
            "threshold": round(BEST_THRESHOLD * 100, 2),
            "message": message
        })

    except Exception as exc:
        return jsonify({
            "success": False,
            "error": str(exc)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
