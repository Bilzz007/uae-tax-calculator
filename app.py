# app.py

import streamlit as st
from sidebar import get_user_inputs
from eligibility_logic import check_eligibility
from tax_calculator import calculate_tax
from ui_components import show_summary, show_header

st.set_page_config("🇦🇪 UAE Corporate Tax Calculator", layout="wide")
show_header()

# Step 1: Get inputs from sidebar
user_inputs = get_user_inputs()

# Step 2: Check eligibility
eligibility_result = check_eligibility(user_inputs)

if not eligibility_result["is_taxable"]:
    st.warning(eligibility_result["message"])
else:
    st.success("✅ You are subject to UAE Corporate Tax. Please review the summary below.")
    
    # Step 3: Calculate tax
    tax_result = calculate_tax(user_inputs)
    
    # Step 4: Display summary
    show_summary(user_inputs, tax_result)
