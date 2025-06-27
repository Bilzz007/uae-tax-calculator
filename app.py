# app.py

import streamlit as st
from components.input_form import get_user_inputs
from components.result_summary import show_summary
from utils.tax_calculator import calculate_tax

# ---------------------- Page Setup ---------------------- #
st.set_page_config("UAE Corporate Tax Calculator", layout="centered")
st.title("UAE Corporate Tax Calculator")

# ---------------------- Input Form ---------------------- #
submitted, user_inputs = get_user_inputs()

# ---------------------- Tax Logic ----------------------- #
if submitted:
    st.markdown("### 🧾 Eligibility Result")

    # Exempt check
    if user_inputs["exempt_type"]:
        st.warning(f"❌ You are exempt from UAE Corporate Tax due to: {', '.join(user_inputs['exempt_type'])}.")
    elif user_inputs["revenue"] <= 3_000_000:
        st.info("✅ Small Business Relief applies (Revenue ≤ AED 3M). No corporate tax this period.")
    else:
        st.success("✅ Based on your inputs, corporate tax applies.")
        result = calculate_tax(user_inputs)

        st.markdown("### 💼 Tax Summary")
        show_summary(user_inputs, result)
