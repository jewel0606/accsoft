import textwrap

import pandas as pd
import streamlit as st

from db import supabase


# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------

st.set_page_config(
    page_title="accsoft — Accounting System",
    layout="wide",
)


# ---------------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------------

st.title("accsoft — SQL-Based Accounting System")

st.write(
    "All reports load live from Supabase PostgreSQL views."
)

st.divider()


# ---------------------------------------------------------
# FUNCTION TO BREAK LONG TEXT INTO MULTIPLE LINES
# ---------------------------------------------------------

def wrap_text(value, width=30):
    """
    Break long text into multiple lines.

    Example:

    Loan > Loan Payable > Mortgage Payable

    becomes:

    Loan > Loan Payable >
    Mortgage Payable
    """

    if value is None:
        return ""

    value = str(value)

    return "\n".join(
        textwrap.wrap(
            value,
            width=width,
        )
    )


# ---------------------------------------------------------
# FUNCTION TO LOAD AND DISPLAY A REPORT
# ---------------------------------------------------------

def show_report(view_name: str) -> None:
    """
    Fetch data from a Supabase view
    and display it as a Streamlit table.
    """

    try:
        # Get all rows and columns from the selected Supabase view
        result = (
            supabase
            .table(view_name)
            .select("*")
            .execute()
        )

        # Stop if the view contains no data
        if not result.data:
            st.info("No data found.")
            return

        # Convert Supabase data into a pandas table
        df = pd.DataFrame(result.data)

        # Replace empty database values with blank text
        df = df.fillna("")

        # -------------------------------------------------
        # WRAP LONG TEXT COLUMNS
        # -------------------------------------------------

        text_columns = [
            "account_type",
            "account_category",
            "account_name",
            "account_sub1",
            "path",
            "description",
            "memo",
            "calculation",
        ]

        for column in text_columns:
            if column in df.columns:
                df[column] = df[column].apply(
                    lambda value: wrap_text(
                        value,
                        width=30,
                    )
                )

        # Make the path column slightly wider before wrapping
        if "path" in df.columns:
            df["path"] = df["path"].apply(
                lambda value: wrap_text(
                    value,
                    width=45,
                )
            )

        # Make calculation text slightly wider
        if "calculation" in df.columns:
            df["calculation"] = df["calculation"].apply(
                lambda value: wrap_text(
                    value,
                    width=45,
                )
            )

        # -------------------------------------------------
        # CONVERT ACCOUNTING COLUMNS TO NUMBERS
        # -------------------------------------------------

        number_columns = [
            "old_debit",
            "old_credit",
            "old_final_balance",
            "debit",
            "credit",
            "final_balance",
            "result",
            "amount",
            "total_amount",
        ]

        for column in number_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce",
                )

        # -------------------------------------------------
        # COLUMN SETTINGS
        # -------------------------------------------------

        column_settings = {}

        if "account_type" in df.columns:
            column_settings["account_type"] = (
                st.column_config.TextColumn(
                    "Account Type",
                    width=140,
                )
            )

        if "account_category" in df.columns:
            column_settings["account_category"] = (
                st.column_config.TextColumn(
                    "Account Category",
                    width=200,
                )
            )

        if "account_code" in df.columns:
            column_settings["account_code"] = (
                st.column_config.NumberColumn(
                    "Account Code",
                    width=120,
                    format="%d",
                )
            )

        if "account_name" in df.columns:
            column_settings["account_name"] = (
                st.column_config.TextColumn(
                    "Account Name",
                    width=250,
                )
            )

        if "account_sub1" in df.columns:
            column_settings["account_sub1"] = (
                st.column_config.TextColumn(
                    "Parent Account",
                    width=220,
                )
            )

        if "path" in df.columns:
            column_settings["path"] = (
                st.column_config.TextColumn(
                    "Account Path",
                    width=450,
                )
            )

        if "description" in df.columns:
            column_settings["description"] = (
                st.column_config.TextColumn(
                    "Description",
                    width=350,
                )
            )

        if "memo" in df.columns:
            column_settings["memo"] = (
                st.column_config.TextColumn(
                    "Memo",
                    width=250,
                )
            )

        if "calculation" in df.columns:
            column_settings["calculation"] = (
                st.column_config.TextColumn(
                    "Calculation",
                    width=450,
                )
            )

        if "transaction_id" in df.columns:
            column_settings["transaction_id"] = (
                st.column_config.TextColumn(
                    "Transaction ID",
                    width=180,
                )
            )

        if "transaction_line_id" in df.columns:
            column_settings["transaction_line_id"] = (
                st.column_config.TextColumn(
                    "Transaction Line ID",
                    width=180,
                )
            )

        if "transaction_date" in df.columns:
            column_settings["transaction_date"] = (
                st.column_config.DateColumn(
                    "Transaction Date",
                    width=140,
                    format="DD-MM-YYYY",
                )
            )

        if "due_date" in df.columns:
            column_settings["due_date"] = (
                st.column_config.DateColumn(
                    "Due Date",
                    width=140,
                    format="DD-MM-YYYY",
                )
            )

        # Apply number formatting
        for column in number_columns:
            if column in df.columns:
                column_settings[column] = (
                    st.column_config.NumberColumn(
                        column.replace("_", " ").title(),
                        width=160,
                        format="%.2f",
                    )
                )

        # -------------------------------------------------
        # DISPLAY REPORT
        # -------------------------------------------------

        st.dataframe(
            df,
            width="stretch",
            height=700,
            row_height=90,
            hide_index=True,
            column_config=column_settings,
        )

    except Exception as exc:
        st.error(
            f"Error loading {view_name}: {exc}"
        )


# ---------------------------------------------------------
# REPORT TABS
# ---------------------------------------------------------

tabs = st.tabs(
    [
        "Account Summary",
        "Balance Sheet",
        "Trial Balance",
        "Reconciliation",
        "Income Statement",
        "Full Financial Statement",
        "Chart of Accounts",
        "Journal Register",
    ]
)


# ---------------------------------------------------------
# TAB 1 — ACCOUNT SUMMARY
# ---------------------------------------------------------

with tabs[0]:
    st.subheader("Account Summary")

    st.write(
        "Shows direct and rolled-up account balances."
    )

    if st.button(
        "Load Account Summary",
        key="account_summary",
    ):
        show_report(
            "view_account_summary"
        )


# ---------------------------------------------------------
# TAB 2 — BALANCE SHEET
# ---------------------------------------------------------

with tabs[1]:
    st.subheader("Balance Sheet")

    st.write(
        "Shows assets, liabilities, equity and the balance check."
    )

    if st.button(
        "Generate Balance Sheet",
        key="balance_sheet",
    ):
        show_report(
            "view_balance_sheet"
        )


# ---------------------------------------------------------
# TAB 3 — TRIAL BALANCE
# ---------------------------------------------------------

with tabs[2]:
    st.subheader("Trial Balance")

    st.write(
        "Shows debit, credit and final balance for each account."
    )

    if st.button(
        "Generate Trial Balance",
        key="trial_balance",
    ):
        show_report(
            "view_trial_balance"
        )


# ---------------------------------------------------------
# TAB 4 — RECONCILIATION
# ---------------------------------------------------------

with tabs[3]:
    st.subheader("Reconciliation")

    st.write(
        "Shows the accounting equation and report checks."
    )

    if st.button(
        "Generate Reconciliation",
        key="reconciliation",
    ):
        show_report(
            "view_reconciliation"
        )


# ---------------------------------------------------------
# TAB 5 — INCOME STATEMENT
# ---------------------------------------------------------

with tabs[4]:
    st.subheader("Income Statement")

    st.write(
        "Shows income, expenses and Net Income."
    )

    if st.button(
        "Generate Income Statement",
        key="income_statement",
    ):
        show_report(
            "view_income_statement"
        )


# ---------------------------------------------------------
# TAB 6 — FULL FINANCIAL STATEMENT
# ---------------------------------------------------------

with tabs[5]:
    st.subheader(
        "Full Financial Statement"
    )

    st.write(
        "Shows all financial account types and hierarchy levels."
    )

    if st.button(
        "Generate Full Financial Statement",
        key="full_financial_statement",
    ):
        show_report(
            "view_full_financial_statement"
        )


# ---------------------------------------------------------
# TAB 7 — CHART OF ACCOUNTS
# ---------------------------------------------------------

with tabs[6]:
    st.subheader(
        "Chart of Accounts"
    )

    st.write(
        "Shows all accounts in the accounting system."
    )

    if st.button(
        "Load Chart of Accounts",
        key="chart_of_accounts",
    ):
        show_report(
            "view_chart_of_accounts"
        )


# ---------------------------------------------------------
# TAB 8 — JOURNAL REGISTER
# ---------------------------------------------------------

with tabs[7]:
    st.subheader(
        "Journal Register"
    )

    st.write(
        "Shows every journal transaction line."
    )

    if st.button(
        "Load Journal Register",
        key="journal_register",
    ):
        show_report(
            "view_journal_register"
        )
