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

    if inputs["free_zone"] == "Yes" and inputs["qualifying_fz"] == "Yes":
        st.markdown("**📁 Free Zone Income Breakdown:**")
        st.write(f"• Qualifying Income (0% Tax): AED {inputs['qualifying_income']:,.2f}")
        st.write(f"• Non-Qualifying Income (9% Tax Slab Applies): AED {inputs['non_qualifying_income']:,.2f}")

    st.markdown("---")
    st.markdown("**Note:** This tool is based on UAE Tax Law and is for guidance only. Always consult your tax advisor.")
