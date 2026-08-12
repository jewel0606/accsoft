import pandas as pd
import streamlit as st

from db import supabase

st.set_page_config(
    page_title="accsoft — Accounting System",
    layout="wide",
)

st.markdown(
    """
    <h1 style="color:#2c3e50;">accsoft — SQL-Based Accounting System</h1>
    <p>All reports load live from Supabase PostgreSQL views.</p>
    <hr>
    """,
    unsafe_allow_html=True,
)


def show_report(view_name: str) -> None:
    """Fetch and display a Supabase report view."""
    try:
        result = supabase.table(view_name).select("*").execute()

        if result.data:
            df = pd.DataFrame(result.data)
            st.dataframe(df, use_container_width=True, height=600)
        else:
            st.info("No data found.")

    except Exception as exc:
        st.error(f"Error loading {view_name}: {exc}")


tabs = st.tabs([
    "Account Summary",
    "Balance Sheet",
    "Trial Balance",
    "Reconciliation",
    "Income Statement",
    "Full Financial Statement",
    "Chart of Accounts",
    "Journal Register",
])


with tabs[0]:
    st.subheader("Account Summary")
    if st.button("Load Account Summary", key="account_summary"):
        show_report("view_account_summary")

with tabs[1]:
    st.subheader("Balance Sheet")
    if st.button("Generate Balance Sheet", key="balance_sheet"):
        show_report("view_balance_sheet")

with tabs[2]:
    st.subheader("Trial Balance")
    if st.button("Generate Trial Balance", key="trial_balance"):
        show_report("view_trial_balance")

with tabs[3]:
    st.subheader("Reconciliation")
    if st.button("Generate Reconciliation", key="reconciliation"):
        show_report("view_reconciliation")

with tabs[4]:
    st.subheader("Income Statement")
    if st.button("Generate Income Statement", key="income_statement"):
        show_report("view_income_statement")

with tabs[5]:
    st.subheader("Full Financial Statement")
    if st.button("Generate Full Financial Statement", key="full_financial_statement"):
        show_report("view_full_financial_statement")

with tabs[6]:
    st.subheader("Chart of Accounts")
    if st.button("Load Chart of Accounts", key="chart_of_accounts"):
        show_report("view_chart_of_accounts")

with tabs[7]:
    st.subheader("Journal Register")
    if st.button("Load Journal Register", key="journal_register"):
        show_report("view_journal_register")
