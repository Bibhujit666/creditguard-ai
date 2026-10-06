##  Project Highlights

- Exploratory Data Analysis (EDA) on the UCI Credit Card Default dataset
- Data cleaning and preprocessing
- Handling of categorical and numerical features
- Train/validation/test split
- Comparison of multiple machine learning models
- ROC-AUC and PR-AUC evaluation
- Classification-threshold tuning for the final model
- CatBoost selected as the final model
- Saved trained models using `joblib`
- Flask REST endpoint for predictions
- Interactive web interface for customer risk assessment
- Real-time default probability and risk classification

---

##  Objective

The goal is to predict the target variable:

```text
default.payment.next.month
```

where:

- `0` → Customer is unlikely to default next month
- `1` → Customer is likely to default next month

The application accepts customer/account information and estimates the probability of next-month credit card default.

---

##  Dataset

This project uses the **UCI Credit Card Default** dataset.

🔗 **Kaggle Dataset:**  
https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset

### Dataset size

- **30,000 observations**
- **25 original columns**
- **23 predictive features** after removing the `ID` column and separating the target
- Binary classification problem
- Default rate: approximately **22.1%**

The original dataset contains information about:

- Credit limit
- Demographic characteristics
- Previous payment status
- Bill statement amounts
- Previous payment amounts

### Input features

| Feature | Description |
|---|---|
| `LIMIT_BAL` | Credit limit |
| `SEX` | Gender code |
| `EDUCATION` | Education level code |
| `MARRIAGE` | Marital status code |
| `AGE` | Customer age |
| `PAY_0` | Most recent repayment status |
| `PAY_2` – `PAY_6` | Previous repayment statuses |
| `BILL_AMT1` – `BILL_AMT6` | Recent bill statement amounts |
| `PAY_AMT1` – `PAY_AMT6` | Recent payment amounts |

---

##  Data Preprocessing

The notebook performs data inspection, cleaning, exploratory analysis, and feature preparation before model training.

### Categorical features

The following features are treated as categorical:

```text
SEX
EDUCATION
MARRIAGE
PAY_0
PAY_2
PAY_3
PAY_4
PAY_5
PAY_6
```

### Numerical features

```text
LIMIT_BAL
AGE
BILL_AMT1
BILL_AMT2
BILL_AMT3
BILL_AMT4
BILL_AMT5
BILL_AMT6
PAY_AMT1
PAY_AMT2
PAY_AMT3
PAY_AMT4
PAY_AMT5
PAY_AMT6
```

### Data cleaning

The final application reproduces the notebook's documented category cleaning:

```text
EDUCATION: 0 and 6 → 5
MARRIAGE: 0 → 3
```

The `ID` column is excluded from the model.

---

##  Models Compared

The project evaluates five classification algorithms:

1. Logistic Regression
2. K-Nearest Neighbors (KNN)
3. Support Vector Machine (SVM)
4. XGBoost
5. CatBoost

### Model comparison

The notebook reports the following test-set results:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.7754 | 0.4935 | 0.5678 | 0.5280 | 0.7594 | 0.5279 |
| KNN | 0.8069 | 0.6452 | 0.2825 | 0.3929 | 0.7375 | 0.4942 |
| SVM | 0.8033 | 0.5696 | 0.4548 | 0.5058 | 0.7567 | 0.4977 |
| XGBoost | 0.8171 | 0.6586 | 0.3597 | 0.4653 | 0.7735 | 0.5341 |
| **CatBoost** | **0.8200** | **0.6701** | 0.3672 | 0.4745 | **0.7794** | **0.5426** |

###  Final model

**CatBoost** was selected as the final model based on its overall validation/test performance, particularly its ROC-AUC and PR-AUC.

Reported final metrics:

```text
Accuracy : 0.8200
Precision: 0.6701
Recall   : 0.3672
F1       : 0.4745
ROC-AUC  : 0.7794
PR-AUC   : 0.5426
```

---

##  Classification Threshold

Instead of relying on the default classification threshold of `0.50`, the project tunes the decision threshold using validation data.

The selected threshold is:

```text
0.28
```

At this threshold, the notebook reports:

```text
F1       : 0.5414
Precision: 0.5262
Recall   : 0.5574
Accuracy : 0.7910
```

The Flask application uses the saved threshold:

```python
prediction = int(probability >= BEST_THRESHOLD)
```

This makes the deployed application's classification behavior consistent with the trained pipeline.

---

##  Web Application

The project includes a Flask-based web application called **CreditGuard**.

The interface allows users to enter:

- Customer profile information
- Credit limit
- Payment history
- Recent bill amounts
- Recent payment amounts

The application then returns:

- Estimated default probability
- Risk level
- Prediction status
- Decision message
- Model threshold used for classification

### Prediction flow

```text
User Input
    ↓
Flask /predict API
    ↓
Input Validation
    ↓
Data Cleaning
    ↓
Feature DataFrame
    ↓
CatBoost Model
    ↓
Default Probability
    ↓
Threshold = 0.28
    ↓
Risk Classification
    ↓
Web UI Result
```

---



##  Project Structure

```text
Credit Card Default Prediction/
│
├── app.py
├── requirements.txt
├── README.md
│
├── UCI Credit Card Default Prediction.ipynb
├── UCI_Credit_Card.csv
│
├── saved_models/
│   ├── best_model_name.pkl
│   ├── best_threshold.pkl
│   ├── catboost.pkl
│   ├── xgboost.pkl
│   ├── svm.pkl
│   ├── logistic_regression.pkl
│   ├── knn.pkl
│   └── preprocessor.pkl
│
├── templates/
│   └── index.html
│
├── static/
│   ├── app.js
│   └── style.css
│
└── catboost_info/
    └── ... training logs and CatBoost artifacts
```

---

##  API

The Flask application exposes a prediction endpoint:

```http
POST /predict
```

### Request

Send a JSON object containing the 23 model features:

```json
{
  "LIMIT_BAL": 50000,
  "SEX": 2,
  "EDUCATION": 2,
  "MARRIAGE": 2,
  "AGE": 35,
  "PAY_0": 0,
  "PAY_2": 0,
  "PAY_3": 0,
  "PAY_4": 0,
  "PAY_5": 0,
  "PAY_6": 0,
  "BILL_AMT1": 5000,
  "BILL_AMT2": 6000,
  "BILL_AMT3": 4500,
  "BILL_AMT4": 4200,
  "BILL_AMT5": 4000,
  "BILL_AMT6": 3800,
  "PAY_AMT1": 2000,
  "PAY_AMT2": 1500,
  "PAY_AMT3": 1200,
  "PAY_AMT4": 1000,
  "PAY_AMT5": 900,
  "PAY_AMT6": 800
}
```

### Response

A successful response has the following structure:

```json
{
  "success": true,
  "prediction": 0,
  "status": "Likely to Repay",
  "risk": "Lower Risk",
  "probability": 18.42,
  "threshold": 28.0,
  "message": "The model estimates a lower likelihood of next-month payment default."
}
```

---

##  Technologies Used

### Machine Learning

- Python
- Pandas
- NumPy
- Scikit-learn
- CatBoost
- XGBoost
- Joblib

### Web Development

- Flask
- HTML
- CSS
- JavaScript

### Development & Analysis

- Jupyter Notebook
- Matplotlib
- Seaborn

---

##  Notebook

The complete machine learning workflow is available in:

```text
UCI Credit Card Default Prediction.ipynb
```

The notebook covers:

1. Dataset loading
2. Data inspection
3. Missing-value analysis
4. Exploratory data analysis
5. Distribution analysis
6. Outlier analysis
7. Feature preparation
8. Train/validation/test splitting
9. Model training
10. Model comparison
11. Threshold optimization
12. Final model selection
13. Model serialization

---

##  Saved Models

The `saved_models/` directory contains serialized models and supporting artifacts.

The Flask application currently loads:

```text
saved_models/catboost.pkl
saved_models/best_threshold.pkl
```

Other trained models are retained for comparison and reproducibility:

```text
logistic_regression.pkl
knn.pkl
svm.pkl
xgboost.pkl
catboost.pkl
```

---

##  Author

**Bibhujit Panigrahi**


---

