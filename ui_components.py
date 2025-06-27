# ui_components.py

import streamlit as st

def show_header():
    st.title("UAE Corporate Tax Calculator")

def show_summary(inputs: dict, result: dict):
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
        st.markdown(f"• ✅ **Qualifying Income (0%)**: AED {inputs['qualifying_income']:,.2f}")
        st.markdown(f"• ⚠️ **Non-Qualifying Income (9%)**: AED {inputs['non_qualifying_income']:,.2f}")

    st.markdown("---")
    st.markdown("🔍 *This calculator is for informational purposes only. Always consult a qualified tax advisor.*")
