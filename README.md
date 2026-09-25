\# ⚡ Battery Health \& Safety Predictor



\### Intelligent ML Platform for Battery Health, Remaining Useful Life \& Safety Analytics



> A production-oriented machine learning API for battery health estimation, Remaining Useful Life prediction, and intelligent safety risk assessment.



\*\*SOH Prediction · RUL Estimation · Safety Risk Analysis · ML-Powered Insights\*\*



\---



\## 🚀 Overview



\*\*Battery Health \& Safety Predictor\*\* is an ML-powered backend system designed to analyze battery operating conditions and provide intelligent predictions for battery health, remaining useful life, and safety risk.



The system combines trained machine learning models with a \*\*FastAPI-based REST API\*\* to provide structured, validated and real-time predictions.



\### Core Capabilities



\* 🔋 \*\*State of Health (SOH) Prediction\*\*

\* ⏳ \*\*Remaining Useful Life (RUL) Estimation\*\*

\* 🛡️ \*\*Battery Safety Risk Assessment\*\*

\* ✅ \*\*Input Validation \& Data Integrity Checks\*\*

\* 📊 \*\*Machine Learning-Based Predictive Analytics\*\*

\* ⚡ \*\*RESTful API Architecture\*\*

\* 📖 \*\*Interactive Swagger API Documentation\*\*



\---



\## 🧠 Machine Learning Pipeline



```text

Battery Sensor / Operating Data

&#x20;             │

&#x20;             ▼

&#x20;     Input Validation

&#x20;             │

&#x20;             ▼

&#x20;    Feature Preparation

&#x20;             │

&#x20;       ┌─────┴─────┐

&#x20;       ▼           ▼

&#x20;  SOH Model      RUL Model

&#x20;       │           │

&#x20;       ▼           ▼

&#x20; Battery Health  Remaining

&#x20;   Prediction     Useful Life

&#x20;       │           │

&#x20;       └─────┬─────┘

&#x20;             ▼

&#x20;     Safety Risk Engine

&#x20;             │

&#x20;             ▼

&#x20;       API Response

```



\---



\## 🔋 SOH Prediction



The SOH module estimates the battery's \*\*State of Health\*\* using operational and electrical characteristics.



\### Input Features



\* Cycle

\* Average Voltage

\* Average Current

\* Maximum Temperature

\* Minimum Voltage

\* Discharge Time

\* Capacity

\* Discharge Energy



\### Output



The API returns:



\* Predicted SOH percentage

\* Battery health status

\* Optional model-output warning



\### Health Classification



| SOH      | Status    |

| -------- | --------- |

| ≥ 80     | Healthy   |

| 60–79.99 | Degrading |

| < 60     | Critical  |



\---



\## ⏳ Remaining Useful Life (RUL)



The RUL module estimates the remaining number of battery cycles before the end of its useful operating life.



\### Model Features



```text

Discharge\_Cycle

SOH

Avg\_Voltage

Max\_Temperature

Discharge\_Time

Discharge\_Energy

```



\### Example Response



```json

{

&#x20; "predicted\_rul\_cycles": 63.55,

&#x20; "model\_features": \[

&#x20;   "Discharge\_Cycle",

&#x20;   "SOH",

&#x20;   "Avg\_Voltage",

&#x20;   "Max\_Temperature",

&#x20;   "Discharge\_Time",

&#x20;   "Discharge\_Energy"

&#x20; ],

&#x20; "message": "Estimated Remaining Useful Life of the battery"

}

```



\---



\## 🛡️ Safety Risk Assessment



The safety monitoring module evaluates battery operating conditions and assigns a risk level.



The assessment considers:



\* 🌡️ Temperature

\* ⚡ Current

\* 🔋 Voltage

\* ❤️ Battery SOH



\### Risk Levels



| Risk Score | Risk Level  |

| ---------- | ----------- |

| 0–1        | LOW RISK    |

| 2–3        | MEDIUM RISK |

| ≥ 4        | HIGH RISK   |



The API also provides specific warnings such as:



```text

High Temperature

Abnormal Current

Abnormal Voltage

Low Battery Health

```



\---



\## ⚙️ Technology Stack



\### Machine Learning



\* Python

\* XGBoost

\* Scikit-learn

\* Pandas

\* NumPy



\### Backend



\* FastAPI

\* Pydantic

\* Uvicorn



\### Model Management



\* Joblib

\* Serialized ML models

\* Feature-name persistence



\### API Documentation



\* OpenAPI

\* Swagger UI



\---



\## 🌐 API Endpoints



| Method | Endpoint       | Purpose                |

| ------ | -------------- | ---------------------- |

| `GET`  | `/`            | API overview           |

| `GET`  | `/health`      | Service health check   |

| `POST` | `/predict-soh` | Battery SOH prediction |

| `POST` | `/predict-rul` | RUL estimation         |

| `POST` | `/safety-risk` | Safety risk assessment |



\---



\## 📖 API Documentation



After starting the server, interactive API documentation is available at:



```text

http://127.0.0.1:8000/docs

```



The Swagger interface allows users to:



\* Inspect available endpoints

\* View request schemas

\* Validate input parameters

\* Execute API requests

\* Inspect real-time responses



\---



\## ▶️ Running the Project



\### 1. Clone the repository



```bash

git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

cd Battery\_SOH\_predictor

```



\### 2. Install dependencies



```bash

pip install fastapi uvicorn pandas joblib xgboost scikit-learn

```



\### 3. Start the API server



```bash

uvicorn main:app --reload

```



\### 4. Open Swagger UI



```text

http://127.0.0.1:8000/docs

```



\---



\## 📂 Project Structure



```text

Battery\_SOH\_predictor/

│

├── main.py

│

├── final\_battery\_soh\_model.json

├── final\_feature\_names.pkl

│

├── final\_rul\_model.pkl

├── final\_rul\_feature\_names.pkl

│

├── app.py

├── README.md

└── requirements.txt

```



\---



\## 🔐 Validation \& Reliability



The API includes structured validation using \*\*Pydantic\*\* to prevent invalid battery measurements from entering the prediction pipeline.



Examples include:



\* Voltage range validation

\* Temperature range validation

\* Current range validation

\* Non-negative cycle validation

\* SOH range validation

\* Battery measurement consistency checks



This helps improve API reliability and prevents malformed requests from reaching the ML models.



\---



\## 📊 Example Workflow



```text

Client Application

&#x20;      │

&#x20;      ▼

&#x20;  FastAPI

&#x20;      │

&#x20;      ▼

Input Validation

&#x20;      │

&#x20;      ├──────────────┐

&#x20;      ▼              ▼

&#x20;  SOH Model       RUL Model

&#x20;      │              │

&#x20;      ▼              ▼

&#x20;Battery Health   Remaining Life

&#x20;      │              │

&#x20;      └──────┬───────┘

&#x20;             ▼

&#x20;      Safety Analysis

&#x20;             │

&#x20;             ▼

&#x20;       JSON Response

```



\---



\## 🎯 Project Objectives



The system is designed to demonstrate how machine learning can be integrated into a structured backend service for:



\* Predictive battery health monitoring

\* Remaining useful life estimation

\* Automated safety assessment

\* Machine learning model serving

\* REST API development

\* Data validation and reliable prediction workflows



\---



\## ⚠️ Disclaimer



This project is a \*\*machine-learning prototype for predictive analytics and educational/research purposes\*\*.



Safety-risk outputs are advisory predictions and should not be treated as guaranteed accident, failure, or safety predictions.



\---



\## 👩‍💻 Author



\*\*Meghna Mukherjee\*\*



B.Tech Engineering

Institute of Engineering \& Management, Kolkata



\---



\### ⭐ Project Focus



\*\*Machine Learning · Predictive Maintenance · Battery Analytics · FastAPI · XGBoost · REST API · Predictive Safety Monitoring\*\*



