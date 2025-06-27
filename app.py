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

# ---------------------- Eligibility Logic ---------------------- #
if submitted:
    st.markdown("### 🧾 Eligibility Result")

    if not user_inputs["is_taxable_person"]:
        st.warning("❌ You are not a Taxable Person under UAE Corporate Tax Law. No calculation applicable.")
    elif user_inputs["exempt_type"]:
        st.warning(f"❌ Exempt Person — based on Article 4 categories selected: {', '.join(user_inputs['exempt_type'])}. No corporate tax applies.")
    elif user_inputs["revenue"] <= 3_000_000:
        st.info("✅ Eligible for Small Business Relief (Revenue ≤ AED 3M). Corporate tax is not applicable for this period.")
    else:
        st.success("✅ You are a Taxable Person. Proceeding with tax calculation...")
        result = calculate_tax(user_inputs)

        st.markdown("### 💼 Tax Summary")
        show_summary(user_inputs, result)
