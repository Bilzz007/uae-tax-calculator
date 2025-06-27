# input_form.py

import streamlit as st

def get_user_inputs():
    with st.form("tax_input_form"):
        st.subheader("📋 Business Information")

        entity_type = st.selectbox("Are you a legal entity or a natural person?", ["Legal Entity", "Natural Person"])
        free_zone = st.radio("Are you registered in a UAE Free Zone?", ["Yes", "No"])
        qualifying_fz = st.radio(
            "If yes, do you meet the conditions of a Qualifying Free Zone Person (Article 18)?",
            ["Yes", "No", "Not Applicable"]
        )
        exempt_type = st.multiselect(
            "Any of the following exemptions apply to your entity?",
            [
                "Government Entity",
                "Government Controlled Entity",
                "Extractive Business",
                "Non-Extractive Natural Resource Business",
                "Qualifying Public Benefit Entity",
                "Qualifying Mutual Fund",
                "Public or Private Pension Fund"
            ]
        )

        st.divider()
        st.subheader("💰 Financial Details")

        revenue = st.number_input("Total Revenue (AED)", min_value=0.0, step=1000.0)
        deductions = st.number_input("Deductible Expenses (AED)", min_value=0.0, step=100.0)
        exempt_income = st.number_input("Exempt Income (AED)", min_value=0.0, step=100.0)

        qualifying_income = 0.0
        non_qualifying_income = 0.0

        if free_zone == "Yes" and qualifying_fz == "Yes":
            st.subheader("🏗️ Free Zone Income Breakdown")
            qualifying_income = st.number_input("Qualifying Income (0% Tax)", min_value=0.0, step=100.0)
            non_qualifying_income = st.number_input("Non-Qualifying Income (9% Tax)", min_value=0.0, step=100.0)

        submitted = st.form_submit_button("Check Eligibility and Calculate Tax")

    return submitted, {
        "entity_type": entity_type,
        "free_zone": free_zone,
        "qualifying_fz": qualifying_fz,
        "exempt_type": exempt_type,
        "revenue": revenue,
        "deductions": deductions,
        "exempt_income": exempt_income,
        "qualifying_income": qualifying_income,
        "non_qualifying_income": non_qualifying_income,
    }
