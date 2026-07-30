# accsoft — SQL-Based Accounting System (MSc Project)

## What This Project Is

**accsoft** is a double-entry accounting system built primarily with SQL and developed as an MSc Computer Science project at Comilla University.

The system uses:

- **Supabase PostgreSQL** for accounting data, tables, views, and report calculations
- **SQL** for account hierarchy, debit and credit aggregation, financial statements, and reconciliation
- **Python and Streamlit** for the read-only web interface
- **GitHub** for source-code storage
- **Streamlit Community Cloud** for online hosting

The frontend does not calculate accounting results. It reads live report views from Supabase and displays them as browser-based tables.

**Live App:** https://accsoft.streamlit.app  
**GitHub Repository:** https://github.com/jewel0606/accsoft  
**Database:** Supabase PostgreSQL — `accsoft` project

---

## Project Features

- Double-entry journal structure
- Recursive multi-level chart-of-accounts hierarchy
- Direct account balances
- Rolled-up parent account balances
- Account Summary
- Trial Balance
- Income Statement
- Balance Sheet
- Financial Reconciliation
- Full Financial Statement
- Chart of Accounts report
- Journal Register
- Live report updates from Supabase
- Read-only Streamlit frontend

---

## Project Stack

| Layer | Technology | Purpose |
|---|---|---|
| Database | Supabase PostgreSQL | Stores accounting tables, transactions, and views |
| Accounting Logic | SQL | Builds hierarchy, calculates balances, and generates reports |
| Frontend | Streamlit | Displays live reports in the browser |
| Data Handling | pandas | Converts Supabase results into DataFrames |
| Code Storage | GitHub | Stores project files and documentation |
| Hosting | Streamlit Community Cloud | Runs the application online |

---

## Live Application Reports

Open the application:

**https://accsoft.streamlit.app**

The application contains the following report tabs:

| Tab | Supabase View | Description |
|---|---|---|
| Account Summary | `view_account_summary` | Direct and rolled-up balances for each account |
| Balance Sheet | `view_balance_sheet` | Assets, liabilities, equity, and balance-sheet check |
| Trial Balance | `view_trial_balance` | Debit, credit, and final balance by account |
| Reconciliation | `view_reconciliation` | Income Statement, Balance Sheet, and accounting-equation checks |
| Income Statement | `view_income_statement` | Income, expenses, and Net Income |
| Full Financial Statement | `view_full_financial_statement` | All account types and hierarchy levels |
| Chart of Accounts | `view_chart_of_accounts` | Complete account structure |
| Journal Register | `view_journal_register` | Detailed journal transaction lines |

Each report is generated from the latest database data whenever Streamlit queries the related Supabase view.

---

## How the System Works

```text
Accounting data is entered
            ↓
Supabase PostgreSQL tables
            ↓
Recursive SQL hierarchy and calculations
            ↓
Supabase report views
            ↓
Python Supabase client
            ↓
Streamlit report tabs
            ↓
Browser displays live reports
```

### Data Entry

Accounting data is entered directly into Supabase using:

- Supabase Table Editor
- SQL `INSERT` statements
- Imported data
- Future data-entry forms

The current Streamlit application is read-only and is designed mainly for report presentation.

### Streamlit Responsibilities

Streamlit only:

1. Connects to Supabase
2. Queries a selected view
3. Converts returned rows into a pandas DataFrame
4. Displays the DataFrame in the browser

### Supabase Responsibilities

Supabase PostgreSQL performs:

- Debit and credit aggregation
- Recursive account-hierarchy construction
- Direct account-balance calculation
- Parent and descendant balance roll-up
- Trial Balance generation
- Income Statement calculation
- Net Income calculation
- Balance Sheet generation
- Balance Sheet check
- Financial reconciliation

---

## Double-Entry Accounting

Each accounting transaction should contain at least one debit line and one credit line.

The same `transaction_id` links all journal lines belonging to the same transaction.

Example — rent payment:

```text
Dr Rent Expense       1,000
Cr Cash               1,000
```

The complete reconciliation equation used by the project is:

```text
Assets - Liabilities - Equity - Income + Expense = 0
```

A result of zero confirms that the accounting equation is balanced.

---

## Why This Architecture

| Reason | Explanation |
|---|---|
| SQL-focused | Accounting calculations remain inside PostgreSQL |
| Dynamic | Reports reflect the latest journal data |
| Low cost | Supabase, GitHub, and Streamlit offer free tiers |
| Online | Reports are available through a browser |
| Simple frontend | Streamlit displays SQL results with limited Python code |
| Multi-level hierarchy | Recursive SQL supports flexible account depth |
| Academic value | Demonstrates accounting, SQL, databases, Python, and cloud deployment |
| Clear separation | SQL calculates reports while Streamlit presents them |

---

# Level 1 — Platform Setup

## Step 1: Create the Supabase Project

1. Go to Supabase and create a free account.
2. Create a project named `accsoft`.
3. Select the nearest available region.
4. Save the database password securely.
5. Wait for the project to finish provisioning.

---

## Step 2: Create Database Tables

Open:

```text
Supabase Dashboard
→ SQL Editor
→ New Query
```

Create the tables in this order:

```text
1. currency
2. chart_of_accounts
3. contact
4. department
5. location
6. item
7. budget
8. user
9. jnl
```

The `jnl` table must be created last because it depends on supporting tables through foreign keys.

---

## Step 3: Insert Minimum Currency Data

```sql
INSERT INTO public.currency (currency_id)
VALUES ('USD');
```

---

## Step 4: Create Supabase Views

Create these views:

```text
view_account_summary
view_balance_sheet
view_trial_balance
view_reconciliation
view_income_statement
view_full_financial_statement
view_chart_of_accounts
view_journal_register
```

Recommended creation order:

```text
1. view_account_summary
2. view_balance_sheet
3. view_trial_balance
4. view_reconciliation
5. view_income_statement
6. view_full_financial_statement
7. view_chart_of_accounts
8. view_journal_register
```

The main report views depend on:

```text
jnl
+
chart_of_accounts
```

---

## Step 5: Configure Row Level Security

Row Level Security applies to tables, not views.

Enable RLS on the underlying tables:

```sql
ALTER TABLE public.jnl
ENABLE ROW LEVEL SECURITY;

ALTER TABLE public.chart_of_accounts
ENABLE ROW LEVEL SECURITY;
```

Create read policies:

```sql
DROP POLICY IF EXISTS "anon_read_only"
ON public.jnl;

CREATE POLICY "anon_read_only"
ON public.jnl
FOR SELECT
TO anon, authenticated
USING (true);
```

```sql
DROP POLICY IF EXISTS "anon_read_only"
ON public.chart_of_accounts;

CREATE POLICY "anon_read_only"
ON public.chart_of_accounts
FOR SELECT
TO anon, authenticated
USING (true);
```

Do not run `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` against a view.

---

## Step 6: Configure View Security

Use security-invoker views so the views respect the RLS policies of the underlying tables.

```sql
ALTER VIEW public.view_account_summary
SET (security_invoker = true);

ALTER VIEW public.view_balance_sheet
SET (security_invoker = true);

ALTER VIEW public.view_trial_balance
SET (security_invoker = true);

ALTER VIEW public.view_reconciliation
SET (security_invoker = true);

ALTER VIEW public.view_income_statement
SET (security_invoker = true);

ALTER VIEW public.view_full_financial_statement
SET (security_invoker = true);

ALTER VIEW public.view_chart_of_accounts
SET (security_invoker = true);

ALTER VIEW public.view_journal_register
SET (security_invoker = true);
```

Grant read access:

```sql
GRANT SELECT ON
    public.view_account_summary,
    public.view_balance_sheet,
    public.view_trial_balance,
    public.view_reconciliation,
    public.view_income_statement,
    public.view_full_financial_statement,
    public.view_chart_of_accounts,
    public.view_journal_register
TO anon, authenticated;
```

---

## Step 7: Test the Views

```sql
SELECT *
FROM public.view_account_summary
LIMIT 5;
```

```sql
SELECT *
FROM public.view_trial_balance
LIMIT 5;
```

```sql
SELECT *
FROM public.view_income_statement
LIMIT 5;
```

```sql
SELECT *
FROM public.view_balance_sheet
LIMIT 5;
```

If these queries run successfully, the main Supabase reports are ready.

---

## Step 8: Create the GitHub Repository

1. Create a GitHub account.
2. Create a new public repository.
3. Name the repository `accsoft`.
4. Add a README file.
5. Commit the project files.

Recommended repository structure:

```text
accsoft/
├── README.md
├── requirements.txt
├── db.py
├── app.py
└── database.sql
```

---

## Step 9: Create requirements.txt

```text
streamlit
supabase
pandas
```

---

## Step 10: Create db.py

```python
import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
)
```

Store Supabase credentials in Streamlit Secrets. Do not commit private credentials to a public repository.

---

## Step 11: Create app.py

```python
import pandas as pd
import streamlit as st

from db import supabase


st.set_page_config(
    page_title="accsoft — Accounting System",
    layout="wide",
)

st.markdown(
    """
    <h1 style="color:#2c3e50;">
        accsoft — SQL-Based Accounting System
    </h1>
    <p>
        All reports load live from Supabase PostgreSQL views.
    </p>
    <hr>
    """,
    unsafe_allow_html=True,
)


def show_report(view_name: str) -> None:
    """Fetch and display a Supabase report view."""

    try:
        result = (
            supabase
            .table(view_name)
            .select("*")
            .execute()
        )

        if result.data:
            df = pd.DataFrame(result.data)

            st.dataframe(
                df,
                use_container_width=True,
                height=600,
            )
        else:
            st.info("No data found.")

    except Exception as exc:
        st.error(f"Error loading {view_name}: {exc}")


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


with tabs[0]:
    st.subheader("Account Summary")

    if st.button(
        "Load Account Summary",
        key="account_summary",
    ):
        show_report("view_account_summary")


with tabs[1]:
    st.subheader("Balance Sheet")

    if st.button(
        "Generate Balance Sheet",
        key="balance_sheet",
    ):
        show_report("view_balance_sheet")


with tabs[2]:
    st.subheader("Trial Balance")

    if st.button(
        "Generate Trial Balance",
        key="trial_balance",
    ):
        show_report("view_trial_balance")


with tabs[3]:
    st.subheader("Reconciliation")

    if st.button(
        "Generate Reconciliation",
        key="reconciliation",
    ):
        show_report("view_reconciliation")


with tabs[4]:
    st.subheader("Income Statement")

    if st.button(
        "Generate Income Statement",
        key="income_statement",
    ):
        show_report("view_income_statement")


with tabs[5]:
    st.subheader("Full Financial Statement")

    if st.button(
        "Generate Full Financial Statement",
        key="full_financial_statement",
    ):
        show_report("view_full_financial_statement")


with tabs[6]:
    st.subheader("Chart of Accounts")

    if st.button(
        "Load Chart of Accounts",
        key="chart_of_accounts",
    ):
        show_report("view_chart_of_accounts")


with tabs[7]:
    st.subheader("Journal Register")

    if st.button(
        "Load Journal Register",
        key="journal_register",
    ):
        show_report("view_journal_register")
```

---

## Step 12: Configure Streamlit Secrets

Open:

```text
Streamlit Cloud
→ App Settings
→ Secrets
```

Add:

```toml
SUPABASE_URL = "your-supabase-project-url"
SUPABASE_KEY = "your-supabase-anon-key"
```

---

## Step 13: Deploy the Application

1. Sign in to Streamlit Community Cloud using GitHub.
2. Select the repository `jewel0606/accsoft`.
3. Select the `main` branch.
4. Set the main file path to `app.py`.
5. Choose the application URL `accsoft`.
6. Deploy the application.

---

# Level 2 — Code Explanation

## requirements.txt

The file tells Streamlit Cloud which Python packages to install.

| Package | Purpose |
|---|---|
| `streamlit` | Creates the browser interface |
| `supabase` | Connects Python to Supabase |
| `pandas` | Converts query results into tables |

---

## db.py

```python
import streamlit as st
```

Imports Streamlit so the application can access Streamlit Secrets.

```python
from supabase import create_client
```

Imports the Supabase client function.

```python
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
```

Reads the Supabase URL and anon key from Streamlit Secrets.

```python
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
)
```

Creates the connection used by `app.py`.

---

## app.py

```python
def show_report(view_name: str) -> None:
```

Creates one reusable function for all report views.

```python
supabase.table(view_name).select("*").execute()
```

Queries the selected Supabase view.

```python
df = pd.DataFrame(result.data)
```

Converts returned rows into a pandas DataFrame.

```python
st.dataframe(df)
```

Displays the report in the browser.

---

## Adding Another Report Tab

1. Add the report name to the `st.tabs()` list.
2. Add a new `with tabs[index]:` block.
3. Call `show_report("view_name")`.
4. Create the matching Supabase view.
5. Grant `SELECT` access to the view.
6. Commit the updated `app.py`.

---

# Level 3 — SQL and Supabase Structure

## Main Dependency Map

```text
chart_of_accounts
        +
       jnl
        ↓
account_hierarchy
        ↓
account_hierarchy_map
        ↓
sum_per_account
        ↓
combine
        ↓
account_balance
        ↓
summery
        ↓
view_account_summary
        ↓
┌───────────────────────────────────────────────┐
│ view_balance_sheet                            │
│ view_trial_balance                            │
│ view_reconciliation                           │
│ view_income_statement                         │
│ view_full_financial_statement                 │
└───────────────────────────────────────────────┘
```

Additional views:

```text
chart_of_accounts
        ↓
view_chart_of_accounts
```

```text
jnl + chart_of_accounts
        ↓
view_journal_register
```

---

## Recursive Account Hierarchy

The master SQL uses:

```sql
WITH RECURSIVE account_hierarchy AS (...)
```

The hierarchy supports:

```text
Root account
    ↓
Child account
    ↓
Grandchild account
    ↓
Additional descendant accounts
```

The hierarchy is dynamic and is not limited to fixed `main_ledger` and `sub_ledger` columns.

---

## Important Master Columns

| Column | Purpose |
|---|---|
| `sorting` | Account hierarchy level |
| `path` | Readable account hierarchy |
| `path_codes` | Parent codes and current account code |
| `old_debit` | Debit posted directly to the account |
| `old_credit` | Credit posted directly to the account |
| `old_final_balance` | Direct account balance |
| `debit` | Debit including descendants |
| `credit` | Credit including descendants |
| `final_balance` | Balance including descendants |

Example hierarchy path:

```text
Liabilities > Loans > Mortgage Payable
```

Example hierarchy levels:

```text
sorting = 1 → root account
sorting = 2 → child account
sorting = 3 → grandchild account
```

---

## Balance Rules

For Asset and Expense accounts:

```text
Final Balance = Debit - Credit
```

For Liability, Equity, and Income accounts:

```text
Final Balance = Credit - Debit
```

---

## Avoiding Double-Counting

Parent rows already include descendant balances.

Therefore, report-wide totals must not add every displayed hierarchy row together.

Use root rows:

```sql
sorting = 1
```

Root rows already contain all lower-level balances.

---

## Dynamic View Updates

The reports are normal PostgreSQL views.

When `jnl` or `chart_of_accounts` changes, the views do not need to be recreated.

The latest results are returned the next time Streamlit queries a view.

```python
supabase.table(
    "view_trial_balance"
).select("*").execute()
```

---

## Replacing Existing Views

PostgreSQL may reject `CREATE OR REPLACE VIEW` when the new definition changes existing column names, order, or data types.

Example error:

```text
cannot change name of view column
```

Drop and recreate the affected view:

```sql
DROP VIEW IF EXISTS public.view_balance_sheet;
```

Then create the replacement:

```sql
CREATE VIEW public.view_balance_sheet AS
SELECT ...;
```

Recreate dependent views in the correct order when necessary.

---

## Data Requirements

- `account_sub1` must contain the exact immediate parent account name
- `account_name` must remain unique
- Every journal `account_code` must exist in `chart_of_accounts`
- `dc` must contain `debit` or `credit`
- Invoice and bill aging reports require valid `due_date` values
- Cash and bank accounts should use `account_pattern = 'cash'` or `account_pattern = 'bank'`
- Report-wide totals should use root accounts only

---

## SQL Source File

To keep this README readable, store the complete table definitions, recursive master query, report-view definitions, and additional report queries in:

```text
database.sql
```

Recommended `database.sql` order:

```text
1. Table definitions
2. Seed data
3. RLS policies
4. view_account_summary
5. view_balance_sheet
6. view_trial_balance
7. view_reconciliation
8. view_income_statement
9. view_full_financial_statement
10. view_chart_of_accounts
11. view_journal_register
12. Additional invoice, bill, vendor, ledger, and cash-flow reports
```

---

## Future Improvements

- Authentication and user login
- Journal-entry forms
- Invoice and bill forms
- Date filters
- Account filters
- Excel export
- PDF export
- Dashboard charts
- Budget comparison
- Department and location reporting
- Customer and vendor statements
- Automated period closing
- Audit logs
- Role-based access control

---

## Final Architecture

```text
Accounting data
      ↓
Supabase PostgreSQL tables
      ↓
Recursive SQL account hierarchy
      ↓
SQL financial report views
      ↓
Supabase Python client
      ↓
Streamlit report interface
      ↓
GitHub and Streamlit Cloud deployment
```

---

*Built by Jewel (Yaqin) — MSc Computer Science, Comilla University*
