# components/precheck_taxable_person.py

import streamlit as st

st.info("📌 Taxable Person Pre-Check Loaded!")

def taxable_person_precheck():
    st.subheader("⚖️ Taxable Person Pre-Check")

    entity_type = st.selectbox("Select your business type", ["Legal Entity", "Natural Person"])

    uae_resident = st.radio("Are you a UAE resident for tax purposes?", ["Yes", "No"])
    conducting_business = st.radio("Are you conducting business in the UAE?", ["Yes", "No"])

    is_taxable = (
        (entity_type == "Legal Entity" and uae_resident == "Yes") or
        (entity_type == "Natural Person" and conducting_business == "Yes")
    )

    return entity_type, is_taxable
