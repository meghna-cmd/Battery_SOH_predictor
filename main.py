from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator
import joblib
import pandas as pd
from xgboost import XGBRegressor


app = FastAPI(
    title="Battery Health & Safety Predictor API",
    description="API for Battery SOH Prediction, RUL Estimation and Safety Monitoring",
    version="1.0"
)


# =========================================================
# LOAD SOH MODEL
# =========================================================

soh_model = XGBRegressor()
soh_model.load_model("final_battery_soh_model.json")

soh_feature_names = joblib.load(
    "final_feature_names.pkl"
)


# =========================================================
# LOAD RUL MODEL
# =========================================================

rul_model = joblib.load(
    "final_rul_model.pkl"
)

# IMPORTANT:
# Use the exact features stored inside the trained model.
# Do NOT use final_rul_feature_names.pkl because that file
# contains a different feature list.

if hasattr(rul_model, "feature_names_in_"):
    rul_feature_names = list(rul_model.feature_names_in_)
else:
    rul_feature_names = [
        "Discharge_Cycle",
        "SOH",
        "Avg_Voltage",
        "Max_Temperature",
        "Discharge_Time",
        "Discharge_Energy"
    ]

print("RUL model expects features:")
print(rul_feature_names)


# =========================================================
# INPUT VALIDATION - SOH
# =========================================================

class BatteryInput(BaseModel):

    Cycle: float = Field(ge=0)

    Avg_Voltage: float = Field(
        gt=0,
        le=10
    )

    Avg_Current: float = Field(
        ge=-100,
        le=100
    )

    Max_Temperature: float = Field(
        ge=-50,
        le=150
    )

    Min_Voltage: float = Field(
        gt=0,
        le=10
    )

    Discharge_Time: float = Field(
        ge=0
    )

    Capacity: float = Field(
        gt=0
    )

    Discharge_Energy: float = Field(
        ge=0
    )

    @model_validator(mode="after")
    def validate_voltage(self):

        if self.Min_Voltage > self.Avg_Voltage:
            raise ValueError(
                "Min_Voltage cannot be greater than Avg_Voltage"
            )

        return self


# =========================================================
# INPUT VALIDATION - RUL
# =========================================================

# These are the EXACT 6 features used by the saved RUL model.

class RULInput(BaseModel):

    Discharge_Cycle: float = Field(
        ge=0
    )

    SOH: float = Field(
        ge=0,
        le=100
    )

    Avg_Voltage: float = Field(
        gt=0,
        le=10
    )

    Max_Temperature: float = Field(
        ge=-50,
        le=150
    )

    Discharge_Time: float = Field(
        ge=0
    )

    Discharge_Energy: float = Field(
        ge=0
    )


# =========================================================
# SAFETY RISK FUNCTION
# =========================================================

def battery_safety_risk(
    temperature,
    current,
    voltage,
    soh
):

    risk_score = 0
    warnings = []

    if temperature > 45:
        risk_score += 2
        warnings.append("High Temperature")

    if abs(current) > 5:
        risk_score += 2
        warnings.append("Abnormal Current")

    if voltage < 2.5 or voltage > 4.3:
        risk_score += 2
        warnings.append("Abnormal Voltage")

    if soh < 60:
        risk_score += 1
        warnings.append("Low Battery Health")

    if risk_score >= 4:
        risk = "HIGH RISK"

    elif risk_score >= 2:
        risk = "MEDIUM RISK"

    else:
        risk = "LOW RISK"

    return risk, risk_score, warnings


# =========================================================
# SOH PREDICTION HELPER
# =========================================================

def get_soh_prediction(data):

    input_data = data.model_dump()

    input_df = pd.DataFrame(
        [input_data]
    )

    # Arrange features exactly as SOH model expects
    input_df = input_df[
        soh_feature_names
    ]

    raw_prediction = float(
        soh_model.predict(
            input_df
        )[0]
    )

    prediction_warning = None

    if (
        raw_prediction < 0
        or raw_prediction > 100
    ):

        prediction_warning = (
            "Model output is outside the expected "
            "SOH range. Please verify the input values."
        )

    prediction = max(
        0,
        min(
            100,
            raw_prediction
        )
    )

    return (
        prediction,
        raw_prediction,
        prediction_warning
    )


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message":
        "Battery Health & Safety Predictor API is running"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():

    return {
        "status":
        "healthy"
    }


# =========================================================
# SOH PREDICTION
# =========================================================

@app.post("/predict-soh")
def predict_soh(
    data: BatteryInput
):

    (
        prediction,
        raw_prediction,
        prediction_warning
    ) = get_soh_prediction(
        data
    )

    if prediction >= 80:
        status = "Healthy"

    elif prediction >= 60:
        status = "Degrading"

    else:
        status = "Critical"

    response = {

        "predicted_soh":
        round(
            prediction,
            2
        ),

        "battery_status":
        status
    }

    if prediction_warning:

        response[
            "prediction_warning"
        ] = prediction_warning

        response[
            "raw_prediction"
        ] = round(
            raw_prediction,
            2
        )

    return response


# =========================================================
# RUL PREDICTION
# =========================================================

@app.post("/predict-rul")
def predict_rul(
    data: RULInput
):

    input_data = data.model_dump()

    input_df = pd.DataFrame(
        [input_data]
    )

    # Make sure API data contains every feature
    # required by the trained RUL model.

    missing_features = [
        feature
        for feature in rul_feature_names
        if feature not in input_df.columns
    ]

    if missing_features:

        return {
            "error": "Missing RUL features",
            "missing_features": missing_features,
            "model_features": rul_feature_names
        }

    # Select EXACT model features
    input_df = input_df[
        rul_feature_names
    ]

    predicted_rul = float(
        rul_model.predict(
            input_df
        )[0]
    )

    # RUL cannot be negative
    predicted_rul = max(
        0,
        predicted_rul
    )

    return {

        "predicted_rul_cycles":
        round(
            predicted_rul,
            2
        ),

        "model_features":
        rul_feature_names,

        "message":
        "Estimated Remaining Useful Life of the battery"
    }


# =========================================================
# SAFETY RISK
# =========================================================

@app.post("/safety-risk")
def safety_risk(
    data: BatteryInput
):

    (
        prediction,
        raw_prediction,
        prediction_warning
    ) = get_soh_prediction(
        data
    )

    (
        risk,
        risk_score,
        warnings
    ) = battery_safety_risk(

        data.Max_Temperature,

        data.Avg_Current,

        data.Avg_Voltage,

        prediction
    )

    response = {

        "predicted_soh":
        round(
            prediction,
            2
        ),

        "safety_risk":
        risk,

        "risk_score":
        risk_score,

        "warnings":
        warnings,

        "disclaimer":
        (
            "Prototype warning only. "
            "This is not a guaranteed accident "
            "prediction system."
        )
    }

    if prediction_warning:

        response[
            "prediction_warning"
        ] = prediction_warning

        response[
            "raw_prediction"
        ] = round(
            raw_prediction,
            2
        )

    return response