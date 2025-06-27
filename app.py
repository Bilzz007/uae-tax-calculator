# app.py

import streamlit as st
from input_form import get_user_inputs
from eligibility_logic import check_eligibility
from tax_calculator import calculate_tax
from ui_components import show_summary, show_header

# ------------------------ Page Settings ------------------------

st.set_page_config("🇦🇪 UAE Corporate Tax Calculator", layout="centered")
show_header()

# ------------------------ Input Form ------------------------

submitted, user_inputs = get_user_inputs()

# ------------------------ Eligibility + Calculation ------------------------

if submitted:
    st.markdown("### 🧾 Eligibility Result")

    eligibility = check_eligibility(user_inputs)

    if eligibility["is_taxable"]:
        st.success(eligibility["message"])
        result = calculate_tax(user_inputs)

        st.markdown("---")
        st.markdown("### 💼 Tax Calculation Summary")
        show_summary(user_inputs, result)
    else:
        st.warning(eligibility["message"])
