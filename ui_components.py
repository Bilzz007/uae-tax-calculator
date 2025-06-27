# ui_components.py

import streamlit as st

def show_header():
    st.title("🇦🇪 UAE Corporate Tax Calculator")
    st.caption("Built using Federal Decree-Law No. 47 of 2022")

def show_summary(inputs: dict, result: dict):
    st.header("📊 Corporate Tax Summary")

    st.metric("Total Revenue", f"AED {inputs['revenue']:,.2f}")
    st.metric("Deductible Expenses", f"AED {inputs['deductions']:,.2f}")
    st.metric("Exempt Income", f"AED {inputs['exempt_income']:,.2f}")
    st.metric("Taxable Income", f"AED {result['taxable_income']:,.2f}")
    st.metric("Corporate Tax Payable", f"AED {result['tax_payable']:,.2f}")

    st.markdown("---")
    st.markdown("**Note:** This tool is based on publicly available UAE tax laws and is for informational purposes only.")
