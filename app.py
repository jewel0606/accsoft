import streamlit as st
from db import supabase
import pandas as pd

st.set_page_config(page_title="Accounting System", layout="wide")

st.markdown("""
<h1 style='color:#2c3e50;'>Accounting System — MSc Demo</h1>
<p>All reports load live from Supabase PostgreSQL database.</p>
<hr>
""", unsafe_allow_html=True)

# Helper function
def show_report(view_name):
    try:
        result = supabase.table(view_name).select("*").execute()
        if result.data:
            df = pd.DataFrame(result.data)
            st.dataframe(
                df,
                use_container_width=True,
                height=6000
            )
        else:
            st.info("No data found.")
    except Exception as e:
        st.error(f"Error: {e}")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Chart of Accounts",
    "Trial Balance",
    "Income Statement",
    "Balance Sheet",
    "Journal Register"
])

with tab1:
    st.subheader("Chart of Accounts")
    if st.button("Load Accounts"):
        show_report("view_chart_of_accounts")

with tab2:
    st.subheader("Trial Balance")
    if st.button("Generate Trial Balance"):
        show_report("view_trial_balance")

with tab3:
    st.subheader("Income Statement")
    if st.button("Generate Income Statement"):
        show_report("view_income_statement")

with tab4:
    st.subheader("Balance Sheet")
    if st.button("Generate Balance Sheet"):
        show_report("view_balance_sheet")

with tab5:
    st.subheader("Journal Register")
    if st.button("Load Journal Register"):
        show_report("view_journal_register")
