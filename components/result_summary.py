# components/result_summary.py
"""
Summary display component for UAE Corporate Tax Calculator.
"""

import streamlit as st

def show_summary(inputs: dict, result: dict):
    """
    Display a summary of the financial inputs and tax calculation results.
    Args:
        inputs (dict): User input data.
        result (dict): Tax calculation results.
    """
    st.subheader("📊 Financial Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📈 Revenue", f"AED {inputs['revenue']:,.2f}")
        st.metric("📉 Deductions", f"AED {inputs['deductions']:,.2f}")
    with col2:
        st.metric("🧾 Exempt Income", f"AED {inputs['exempt_income']:,.2f}")
        st.metric("💼 Taxable Income", f"AED {result['taxable_income']:,.2f}")
    st.divider()
    st.subheader("💰 Corporate Tax Payable")
    st.metric("🧮 Total Tax", f"AED {result['tax_payable']:,.2f}")
    if inputs["free_zone"] == "Yes" and inputs["qualifying_fz"] == "Yes":
        st.markdown("### 🏗️ Free Zone Income Breakdown")
        st.markdown(f"• ✅ **Qualifying Income (0% Tax)**: AED {inputs['qualifying_income']:,.2f}")
        st.markdown(f"• ⚠️ **Non-Qualifying Income (9%)**: AED {inputs['non_qualifying_income']:,.2f}")
    st.markdown("---")
    # Show compliance notes and references
    if "notes" in result and result["notes"]:
        st.subheader("📋 Compliance & Law References")
        for note in result["notes"]:
            if note:
                st.markdown(f"- {note}")
    st.markdown("🔍 *This summary is based on UAE Corporate Tax law and is for informational purposes only. For details, see [FTA Corporate Tax Portal](https://tax.gov.ae/en/corporate.tax.aspx) and [MoF Corporate Tax](https://mof.gov.ae/tax-legislation/corporate-tax/).*\n")
