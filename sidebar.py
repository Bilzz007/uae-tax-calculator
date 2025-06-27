# sidebar.py

import streamlit as st

def get_user_inputs():
    st.sidebar.header("📋 Business Information")

    entity_type = st.sidebar.selectbox("Are you a legal entity or a natural person?", ["Legal Entity", "Natural Person"])
    free_zone = st.sidebar.radio("Are you registered in a UAE Free Zone?", ["Yes", "No"])
    qualifying_fz = st.sidebar.radio("If yes, do you meet conditions of a Qualifying Free Zone Person (Article 18)?", ["Yes", "No", "Not Applicable"])
    exempt_type = st.sidebar.multiselect(
        "Select any exemption that applies to you (if any):",
        [
            "Government Entity",
            "Extractive Business",
            "Non-Extractive Natural Resource Business",
            "Qualifying Public Benefit Entity",
            "Qualifying Mutual Fund",
            "Public or Private Pension Fund"
        ]
    )

    st.sidebar.header("💰 Financial Data")

    revenue = st.sidebar.number_input("Total Revenue (AED)", min_value=0.0, step=1000.0)
    deductions = st.sidebar.number_input("Deductible Expenses (AED)", min_value=0.0, step=100.0)
    exempt_income = st.sidebar.number_input("Exempt Income (AED)", min_value=0.0, step=100.0)
    small_business_relief = inputs["revenue"] <= 3_000_000  # auto

    return {
        "entity_type": entity_type,
        "free_zone": free_zone,
        "qualifying_fz": qualifying_fz,
        "exempt_type": exempt_type,
        "revenue": revenue,
        "deductions": deductions,
        "exempt_income": exempt_income,
        "small_business_relief": small_business_relief
    }
