# app.py

import streamlit as st
from components.input_form import get_user_inputs
from components.result_summary import show_summary
from utils.tax_calculator import calculate_tax
from eligibility_logic import check_eligibility

# ---------------------- Page Setup ---------------------- #
st.set_page_config("UAE Corporate Tax Calculator", layout="centered")
st.title("UAE Corporate Tax Calculator")

# ---------------------- Input Form ---------------------- #
submitted, user_inputs = get_user_inputs()

# ---------------------- Eligibility Logic ---------------------- #
if submitted:
    st.markdown("### 🧾 Eligibility Result")
    eligibility = check_eligibility(user_inputs)
    st.info(eligibility["message"])

    if eligibility["is_taxable"]:
        st.success("✅ You are a Taxable Person. Proceeding with tax calculation...")
        result = calculate_tax(user_inputs)
        st.markdown("### 💼 Tax Summary")
        show_summary(user_inputs, result)
