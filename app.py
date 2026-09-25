
import streamlit as st
import joblib
import pandas as pd
from xgboost import XGBRegressor

# Load model
model = XGBRegressor()
model.load_model("final_battery_soh_model.json")

feature_names = joblib.load("final_feature_names.pkl")

st.title("🔋 Battery Health & Safety Predictor")

st.write("Predict Battery State of Health (SOH) and Safety Risk")

st.subheader("Enter Battery Features")

input_data = {}

for feature in feature_names:
    input_data[feature] = st.number_input(
        feature,
        value=0.0
    )


def battery_safety_risk(temperature, current, voltage, soh):

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


if st.button("Predict SOH & Safety Risk"):

    input_df = pd.DataFrame([input_data])

    prediction = model.predict(input_df)[0]

    st.success(f"Predicted SOH: {prediction:.2f}%")

    if prediction >= 80:
        st.success("Battery Status: Healthy")
    elif prediction >= 60:
        st.warning("Battery Status: Degrading")
    else:
        st.error("Battery Status: Critical")

    # Safety Risk Detection
    temperature = input_data["Max_Temperature"]
    current = input_data["Avg_Current"]
    voltage = input_data["Avg_Voltage"]

    risk, risk_score, warnings = battery_safety_risk(
        temperature,
        current,
        voltage,
        prediction
    )

    st.subheader("⚠️ Battery Safety Risk")

    if risk == "HIGH RISK":
        st.error(f"🔴 {risk}")

    elif risk == "MEDIUM RISK":
        st.warning(f"🟡 {risk}")

    else:
        st.success(f"🟢 {risk}")

    st.write(f"Risk Score: {risk_score}")

    if warnings:

        st.write("Warnings:")

        for warning in warnings:
            st.write(f"- {warning}")

    else:
        st.info("No abnormal condition detected.")

    # Safety Recommendation
    st.subheader("🛡️ Safety Recommendation")

    if risk == "HIGH RISK":

        st.error(
            "🚨 Immediate Inspection Recommended. "
            "Stop using the battery if unsafe conditions "
            "are suspected."
        )

    elif risk == "MEDIUM RISK":

        st.warning(
            "⚠️ Check battery temperature, voltage, "
            "and current. Further inspection is recommended."
        )

    else:

        st.success(
            "✅ Continue monitoring battery parameters."
        )

    st.caption(
        "Prototype warning only. This system cannot guarantee "
        "accident or thermal runaway prediction."
    )