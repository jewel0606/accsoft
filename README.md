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
"""
accsoft — SQL-Based Accounting System

Purpose:
This Streamlit application connects to Supabase PostgreSQL and displays
live accounting reports in a web browser.

The accounting calculations are performed inside Supabase SQL views.
This Python file only:

1. Connects to Supabase through the imported supabase client.
2. Loads data from selected report views.
3. Converts the returned data into pandas DataFrames.
4. Displays the reports in separate Streamlit tabs.

Main report views:
- view_account_summary
- view_balance_sheet
- view_trial_balance
- view_reconciliation
- view_income_statement
- view_full_financial_statement
- view_chart_of_accounts
- view_journal_register
"""


# Import pandas for converting Supabase data into DataFrames.
import pandas as pd

# Import Streamlit for creating the browser-based application.
import streamlit as st

# Import the existing Supabase connection from db.py.
from db import supabase


# Configure the Streamlit page.
#
# page_title:
# Sets the title shown in the browser tab.
#
# layout="wide":
# Uses the full browser width so reports with many columns have more space.
st.set_page_config(
    page_title="accsoft — Accounting System",
    layout="wide",
)


# Display the main application heading and description.
#
# st.markdown allows HTML formatting because unsafe_allow_html=True.
# The HTML below:
# - displays the main title
# - displays a short description
# - adds a horizontal line
st.markdown(
    """
    <h1 style="color:#2c3e50;">accsoft — SQL-Based Accounting System</h1>
    <p>All reports load live from Supabase PostgreSQL views.</p>
    <hr>
    """,
    unsafe_allow_html=True,
)


def show_report(view_name: str) -> None:
    """
    Fetch and display a Supabase report view.

    Parameters
    ----------
    view_name : str
        The name of the Supabase table or view that should be loaded.

    Process
    -------
    1. Query all columns from the selected Supabase view.
    2. Check whether data was returned.
    3. Convert the returned records into a pandas DataFrame.
    4. Display the DataFrame as an interactive Streamlit table.
    5. Show a message when no data is available.
    6. Show an error message if the query fails.
    """

    try:
        # Query every column from the selected Supabase view.
        #
        # table(view_name):
        # Selects the Supabase table or view.
        #
        # select("*"):
        # Requests all available columns.
        #
        # execute():
        # Sends the request to Supabase and returns the result.
        result = supabase.table(view_name).select("*").execute()

        # Check whether Supabase returned one or more records.
        if result.data:
            # Convert the list of returned records into a pandas DataFrame.
            df = pd.DataFrame(result.data)

            # Display the DataFrame as an interactive Streamlit table.
            #
            # use_container_width=True:
            # Makes the table use the available page width.
            #
            # height=600:
            # Sets the visible table height to 600 pixels.
            st.dataframe(df, use_container_width=True, height=600)

        else:
            # Display this message when the selected view has no records.
            st.info("No data found.")

    except Exception as exc:
        # Display an error message if the Supabase query or table display fails.
        #
        # view_name identifies the report that caused the error.
        # exc contains the original error message.
        st.error(f"Error loading {view_name}: {exc}")


# Create eight navigation tabs.
#
# Each tab represents one accounting report.
# The returned tab objects are stored inside the tabs list.
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


# ---------------------------------------------------------------------------
# TAB 1: ACCOUNT SUMMARY
# ---------------------------------------------------------------------------
#
# Displays:
# - direct account balances
# - rolled-up account balances
# - account hierarchy information
#
# Supabase view:
# view_account_summary
with tabs[0]:
    # Display the report heading.
    st.subheader("Account Summary")

    # Load the report only when the user clicks the button.
    #
    # key="account_summary":
    # Gives the button a unique Streamlit identifier.
    if st.button("Load Account Summary", key="account_summary"):
        # Fetch and display the Account Summary view.
        show_report("view_account_summary")


# ---------------------------------------------------------------------------
# TAB 2: BALANCE SHEET
# ---------------------------------------------------------------------------
#
# Displays:
# - assets
# - liabilities
# - equity
# - Balance Sheet check
#
# Supabase view:
# view_balance_sheet
with tabs[1]:
    # Display the report heading.
    st.subheader("Balance Sheet")

    # Generate the Balance Sheet when the button is clicked.
    if st.button("Generate Balance Sheet", key="balance_sheet"):
        # Fetch and display the Balance Sheet view.
        show_report("view_balance_sheet")


# ---------------------------------------------------------------------------
# TAB 3: TRIAL BALANCE
# ---------------------------------------------------------------------------
#
# Displays:
# - debit balances
# - credit balances
# - final account balances
#
# Supabase view:
# view_trial_balance
with tabs[2]:
    # Display the report heading.
    st.subheader("Trial Balance")

    # Generate the Trial Balance when the button is clicked.
    if st.button("Generate Trial Balance", key="trial_balance"):
        # Fetch and display the Trial Balance view.
        show_report("view_trial_balance")


# ---------------------------------------------------------------------------
# TAB 4: RECONCILIATION
# ---------------------------------------------------------------------------
#
# Displays:
# - Income Statement calculation
# - Balance Sheet calculation
# - complete accounting-equation check
#
# Supabase view:
# view_reconciliation
with tabs[3]:
    # Display the report heading.
    st.subheader("Reconciliation")

    # Generate the Reconciliation report when the button is clicked.
    if st.button("Generate Reconciliation", key="reconciliation"):
        # Fetch and display the Reconciliation view.
        show_report("view_reconciliation")


# ---------------------------------------------------------------------------
# TAB 5: INCOME STATEMENT
# ---------------------------------------------------------------------------
#
# Displays:
# - income accounts
# - expense accounts
# - Net Income
#
# Supabase view:
# view_income_statement
with tabs[4]:
    # Display the report heading.
    st.subheader("Income Statement")

    # Generate the Income Statement when the button is clicked.
    if st.button("Generate Income Statement", key="income_statement"):
        # Fetch and display the Income Statement view.
        show_report("view_income_statement")


# ---------------------------------------------------------------------------
# TAB 6: FULL FINANCIAL STATEMENT
# ---------------------------------------------------------------------------
#
# Displays:
# - assets
# - liabilities
# - equity
# - income
# - expenses
# - account hierarchy paths
#
# Supabase view:
# view_full_financial_statement
with tabs[5]:
    # Display the report heading.
    st.subheader("Full Financial Statement")

    # Generate the full financial report when the button is clicked.
    if st.button("Generate Full Financial Statement", key="full_financial_statement"):
        # Fetch and display the Full Financial Statement view.
        show_report("view_full_financial_statement")


# ---------------------------------------------------------------------------
# TAB 7: CHART OF ACCOUNTS
# ---------------------------------------------------------------------------
#
# Displays the complete account structure used by the accounting system.
#
# Supabase view:
# view_chart_of_accounts
with tabs[6]:
    # Display the report heading.
    st.subheader("Chart of Accounts")

    # Load the Chart of Accounts when the button is clicked.
    if st.button("Load Chart of Accounts", key="chart_of_accounts"):
        # Fetch and display the Chart of Accounts view.
        show_report("view_chart_of_accounts")


# ---------------------------------------------------------------------------
# TAB 8: JOURNAL REGISTER
# ---------------------------------------------------------------------------
#
# Displays every journal transaction line stored in the system.
#
# Supabase view:
# view_journal_register
with tabs[7]:
    # Display the report heading.
    st.subheader("Journal Register")

    # Load the Journal Register when the button is clicked.
    if st.button("Load Journal Register", key="journal_register"):
        # Fetch and display the Journal Register view.
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

# SQL Financial Report Codes

The following SQL codes use one recursive master query to build the complete chart-of-accounts hierarchy and calculate direct and rolled-up account balances.

The original SQL query logic, names, calculations, columns, spelling, and report structure have not been changed. Additional comments have only been added to explain how each section works.

---

# Code 1: Master code (Master code for generate all report)

```sql
/*
===============================================================================
CODE 1: MASTER CODE
===============================================================================

Purpose:
- Builds a complete multi-level account hierarchy.
- Calculates each account's direct debit, credit and final balance.
- Rolls child-account balances into all parent accounts.
- Produces the final reusable CTE named "summery".
- Acts as the base query for Codes 2 to 7.

Main data sources:
- chart_of_accounts
- jnl

Main hierarchy fields:
- sorting:
  Shows the account depth.
  Root account = 1
  Child account = 2
  Grandchild account = 3
  Additional descendants continue increasing.

- path:
  Shows the readable account hierarchy.

  Example:
  Loan > Loan Payable > Mortgage Payable

- path_codes:
  Stores every account code in the hierarchy path.

  Example:
  {102,126,128}

Balance fields:
- old_debit:
  Debit posted directly to the account.

- old_credit:
  Credit posted directly to the account.

- old_final_balance:
  Final balance from transactions posted directly to the account.

- debit:
  Debit posted to the account and all descendant accounts.

- credit:
  Credit posted to the account and all descendant accounts.

- final_balance:
  Final balance of the account and all descendant accounts.

Important:
- The final CTE ends with a comma because additional report CTEs can be
  appended after the master code.
===============================================================================
*/

WITH RECURSIVE account_hierarchy AS (
    /*
      Builds the complete account hierarchy.


      sorting:
      Shows the account level. Root = 1, child = 2, etc.


      path:
      Creates a readable hierarchy such as:
      Loan > Loan Payable > Mortgage Payable


      path_codes:
      Stores the account codes of every parent and the current account.
      Example: {102,126,128}
    */


    /*
      Root-account selection.

      A root account is an account without a parent account.
      Therefore, account_sub1 must be NULL.

      Each root account starts with:
      - sorting = 1
      - path containing its own account name
      - path_codes containing its own account code
    */

    -- Root accounts: accounts without a parent
    SELECT
        coa.account_category,
        coa.account_type,
        coa.account_code,
        1 AS sorting,
        coa.account_name,
        coa.account_sub1,
        coa.account_name::text AS path,
        ARRAY[coa.account_code] AS path_codes
    FROM chart_of_accounts AS coa
    WHERE coa.account_sub1 IS NULL


    UNION ALL


    /*
      Recursive child-account selection.

      Each child account is connected to its immediate parent using:

      coa.account_sub1 = ah.account_name

      For every child account:
      - sorting increases by 1
      - the account name is added to path
      - the account code is added to path_codes

      The recursive query continues until no additional child accounts exist.
    */

    -- Recursively attach child accounts to their parent accounts
    SELECT
        coa.account_category,
        coa.account_type,
        coa.account_code,
        ah.sorting + 1,
        coa.account_name,
        coa.account_sub1,
        CONCAT(ah.path, ' > ', coa.account_name) AS path,
        ah.path_codes || coa.account_code
    FROM chart_of_accounts AS coa
    JOIN account_hierarchy AS ah
        ON coa.account_sub1 = ah.account_name
),


account_hierarchy_map AS (
    /*
      Converts path_codes into parent-account relationships.


      Example:
      path_codes = {102,126,128}
      account_code = 128


      Result:
      102 | 128
      126 | 128
      128 | 128


      This allows every account balance to roll up to all parents.
    */


    /*
      UNNEST converts each path_codes array into separate rows.

      For the path:
      {102,126,128}

      The current account 128 is mapped to:
      - parent account 102
      - parent account 126
      - itself, account 128

      This mapping is later used to add every descendant balance to each
      parent account.
    */

    SELECT
        UNNEST(path_codes) AS parent_account_code,
        account_code
    FROM account_hierarchy
),


sum_per_account AS (
    /*
      Calculates each account's own debit, credit and final balance.


      Asset and expense:
      final balance = debit - credit


      Liability, equity and income:
      final balance = credit - debit
    */


    /*
      This CTE calculates only transactions posted directly to each account.

      It does not perform hierarchy roll-up.

      total_debit:
      Adds journal amounts where dc = debit.

      total_credit:
      Adds journal amounts where dc = credit.

      final_balance:
      Uses the normal balance rule based on account_type.
    */

    SELECT
        coa.account_code,
        coa.account_name,


        /*
          Calculate total debit posted directly to the account.

          Credit rows contribute zero to total_debit.
        */

        SUM(
            CASE
                WHEN jnl.dc::text = 'debit'::text
                THEN jnl.amount
                ELSE 0::double precision
            END
        ) AS total_debit,


        /*
          Calculate total credit posted directly to the account.

          Debit rows contribute zero to total_credit.
        */

        SUM(
            CASE
                WHEN jnl.dc::text = 'credit'::text
                THEN jnl.amount
                ELSE 0::double precision
            END
        ) AS total_credit,


        /*
          Calculate the direct final balance.

          Asset and expense accounts normally have debit balances:
          debit - credit

          Liability, equity and income accounts normally have credit balances:
          credit - debit
        */

        CASE
            WHEN coa.account_type::text = ANY (
                ARRAY['asset', 'expense']::text[]
            )
            THEN SUM(
                CASE
                    WHEN jnl.dc::text = 'debit'::text
                    THEN jnl.amount
                    ELSE -jnl.amount
                END
            )
            ELSE SUM(
                CASE
                    WHEN jnl.dc::text = 'credit'::text
                    THEN jnl.amount
                    ELSE -jnl.amount
                END
            )
        END AS final_balance


    /*
      Join every journal line to its chart-of-accounts record using
      account_code.
    */

    FROM jnl
    JOIN chart_of_accounts AS coa
        ON jnl.account_code = coa.account_code


    /*
      One result row is created for each individual account.
    */

    GROUP BY
        coa.account_code,
        coa.account_name,
        coa.account_type
),


combine AS (
    /*
      Joins the account hierarchy with each account's own balance.


      COALESCE changes NULL balances to zero for accounts without
      journal transactions.
    */


    /*
      The hierarchy contains all accounts, including accounts without
      journal transactions.

      The LEFT JOIN keeps those accounts in the report.

      COALESCE converts missing balances to zero.
    */

    SELECT
        COALESCE(ab.total_debit, 0.0) AS debit,
        COALESCE(ab.total_credit, 0.0) AS credit,
        COALESCE(ab.final_balance, 0.0) AS final_balance,
        ah.*
    FROM account_hierarchy AS ah
    LEFT JOIN sum_per_account AS ab
        ON ab.account_code = ah.account_code
),


account_balance AS (
    /*
      Rolls account balances upward through the hierarchy.


      Each parent receives:
      - its own balance
      - direct child balances
      - all lower descendant balances
    */


    /*
      account_hierarchy_map identifies all parent and descendant
      relationships.

      combine contains each account's direct balances.

      The GROUP BY parent_account_code calculates one rolled-up balance for
      every account.

      Each account receives:
      - its own direct balance
      - all direct child balances
      - all lower descendant balances
    */

    SELECT
        am.parent_account_code,
        SUM(com.debit) AS new_debit,
        SUM(com.credit) AS new_credit,
        SUM(com.final_balance) AS new_final_balance
    FROM account_hierarchy_map AS am
    JOIN combine AS com
        ON com.account_code = am.account_code
    GROUP BY
        am.parent_account_code
),


summery AS (
    /*
      Final master report dataset.


      old_debit, old_credit, old_final_balance:
      Amounts posted directly to the account.


      debit, credit, final_balance:
      Rolled-up amounts including all child accounts.
    */


    /*
      This is the final reusable master-report dataset.

      Direct balance columns:
      - old_debit
      - old_credit
      - old_final_balance

      Rolled-up hierarchy columns:
      - debit
      - credit
      - final_balance

      The direct columns come from combine.

      The rolled-up columns come from account_balance.
    */

    SELECT
        com.account_category,
        com.account_type,
        com.account_code,
        com.sorting,
        com.account_name,
        com.account_sub1,
        com.path,
        com.path_codes,


        /*
          Preserve each account's own direct transaction amounts.
        */

        com.debit AS old_debit,
        com.credit AS old_credit,
        com.final_balance AS old_final_balance,


        /*
          Add balances that include the current account and all descendants.
        */

        ab.new_debit AS debit,
        ab.new_credit AS credit,
        ab.new_final_balance AS final_balance


    FROM combine AS com
    LEFT JOIN account_balance AS ab
        ON ab.parent_account_code = com.account_code


    /*
      Sort accounts using the complete hierarchy path.
    */

    ORDER BY
        com.path
),	
```

---

# Code 2: account_summary - raw report (Master code + select query)

```sql
/*
===============================================================================
CODE 2: ACCOUNT SUMMARY
===============================================================================

Purpose:
- Displays the complete account hierarchy.
- Shows both direct and rolled-up account balances.
- Removes accounts where all rolled-up amounts are zero.

Required:
- Paste this SELECT after Code 1.
- Code 1 must end with the summery CTE.

Output:
- Account type
- Account category
- Account code
- Account name
- Hierarchy path
- Direct debit, credit and final balance
- Rolled-up debit, credit and final balance
===============================================================================
*/

SELECT
    account_type,
    account_category,
    account_code,
    account_name,
    path,

    /*
      Direct amounts posted only to the individual account.
    */

    old_debit,
    old_credit,
    old_final_balance,

    /*
      Rolled-up amounts containing the account and all descendants.
    */

    debit,
    credit,
    final_balance
FROM summery

/*
  Remove accounts where all rolled-up amounts are zero.
*/

WHERE debit <> 0 OR credit <> 0 OR final_balance <> 0

/*
  Display accounts in hierarchy-path order.
*/

ORDER BY path;
```

---

# Code 3: balance_sheet - report (Master code + select query)

```sql
/*
===============================================================================
CODE 3: BALANCE SHEET
===============================================================================

Purpose:
- Displays asset, liability and equity accounts.
- Uses rolled-up balances from summery.
- Adds a Balance Sheet Check row.

Balance Sheet Check:
Assets - Liabilities - Equity

Important:
- The calculation uses sorting = 1.
- Root accounts already include all descendant balances.
- Using every hierarchy row would double-count parent and child balances.

Required:
- Paste this CTE and final SELECT after Code 1.
===============================================================================
*/

balance_sheet as (
    /*
      Select Balance Sheet account types from the master report.

      Included account types:
      - asset
      - liability
      - equity
    */

    SELECT
            account_type,
            account_category,
            account_code,
            sorting,
            account_name,
            account_sub1,
            path,
            debit,
            credit,
            final_balance
        FROM summery
        WHERE account_type IN ('asset', 'liability', 'equity')


        UNION ALL


        /*
          Add one calculated report-total row.

          account_type:
          TOTAL

          account_name:
          Balance Sheet Check

          Calculation:
          Assets - Liabilities - Equity

          FILTER and sorting = 1 ensure that only root-level rolled-up
          balances are used.
        */

        SELECT
            'TOTAL'::varchar AS account_type,
            NULL::varchar AS account_category,
            NULL::bigint AS account_code,
            0 AS sorting,
            'Balance Sheet Check'::varchar AS account_name,
            NULL::varchar AS account_sub1,
            NULL::text AS path,
            NULL::double precision AS debit,
            NULL::double precision AS credit,
            COALESCE(SUM(final_balance) FILTER (WHERE account_type = 'asset' AND sorting = 1), 0)
            - COALESCE(SUM(final_balance) FILTER (WHERE account_type = 'liability' AND sorting = 1), 0)
            - COALESCE(SUM(final_balance) FILTER (WHERE account_type = 'equity' AND sorting = 1), 0)
            AS final_balance
        FROM summery
)


/*
  Return the final Balance Sheet report.
*/

SELECT
    account_type,
    account_category,
    account_code,
    account_name,
    path,
    debit,
    credit,
    final_balance
FROM balance_sheet

/*
  Always retain the TOTAL row.

  For normal account rows, remove rows where debit, credit and final balance
  are all zero.
*/

WHERE account_type = 'TOTAL'
   OR debit <> 0
   OR credit <> 0
   OR final_balance <> 0

/*
  Sort the report by account type and hierarchy path.
*/

ORDER BY
    account_type,
    path;
```

---

# Code 4: Income_statement - report (Master code + select query)

```sql
/*
===============================================================================
CODE 4: INCOME STATEMENT
===============================================================================

Purpose:
- Displays income and expense accounts.
- Uses rolled-up balances from summery.
- Adds a Net Income row.

Net Income:
Income - Expense

Important:
- The calculation uses sorting = 1.
- Root rows contain all descendant balances.
- This avoids double-counting hierarchy levels.

Required:
- Paste this CTE and final SELECT after Code 1.
===============================================================================
*/

income_statement AS (
    /*
      Select Income Statement account types.

      Included account types:
      - income
      - expense
    */

    SELECT
        account_type,
        account_category,
        account_code,
        sorting,
        account_name,
        account_sub1,
        path,
        debit,
        credit,
        final_balance
    FROM summery
    WHERE account_type IN ('income', 'expense')


    UNION ALL


    /*
      Add the Net Income row.

      Net Income calculation:
      Total root-level income
      minus
      Total root-level expense
    */

    SELECT
        'TOTAL'::varchar AS account_type,
        NULL::varchar AS account_category,
        NULL::bigint AS account_code,
        0 AS sorting,
        'Net Income'::varchar AS account_name,
        NULL::varchar AS account_sub1,
        NULL::text AS path,
        NULL::double precision AS debit,
        NULL::double precision AS credit,
        COALESCE(SUM(final_balance) FILTER (WHERE account_type = 'income' AND sorting = 1), 0)
        - COALESCE(SUM(final_balance) FILTER (WHERE account_type = 'expense' AND sorting = 1), 0)
        AS final_balance
    FROM summery
)


/*
  Return the final Income Statement report.
*/

SELECT
    account_type,
    account_category,
    account_code,
    account_name,
    path,
    debit,
    credit,
    final_balance
FROM income_statement

/*
  Always retain the TOTAL row.

  Remove normal account rows where debit, credit and final balance are zero.
*/

WHERE account_type = 'TOTAL'
   OR debit <> 0
   OR credit <> 0
   OR final_balance <> 0

/*
  Sort the report by account type and hierarchy path.
*/

ORDER BY account_type, path;
```

---

# Code 5: trail_balance - report (Master code + select query)

```sql
/*
===============================================================================
CODE 5: TRAIL BALANCE
===============================================================================

Purpose:
- Displays debit, credit and final balance for all non-zero accounts.
- Uses the rolled-up hierarchy balances from summery.
- Includes each account's readable hierarchy path.

Important:
- The report name and original spelling "trail_balance" have been preserved.
- debit, credit and final_balance contain the current account and descendants.

Required:
- Paste this SELECT after Code 1.
===============================================================================
*/

SELECT
    account_type,
    account_category,
    account_code,
    account_name,
    path,

    /*
      Rolled-up debit, credit and final balance.
    */

    debit,
    credit,
    final_balance
FROM summery

/*
  Remove accounts where every reported amount is zero.
*/

WHERE debit <> 0
   OR credit <> 0
   OR final_balance <> 0

/*
  Display accounts in hierarchy-path order.
*/

ORDER BY path;
```

---

# Code 6: RECONCILIATION - report (Master code + select query)

```sql
/*
===============================================================================
CODE 6: RECONCILIATION
===============================================================================

Purpose:
- Produces three financial calculation checks.
- Uses root-level rolled-up balances from summery.

Calculations:
1. Income Statement = Income - Expense
2. Balance Sheet = Asset - Liability - Equity
3. Asset - Liability - Equity - Income + Expense = 0

Important:
- sorting = 1 restricts calculations to root accounts.
- Root accounts already contain all descendant balances.
- This prevents double-counting across hierarchy levels.

Required:
- Paste this CTE and final SELECT after Code 1.
===============================================================================
*/

reconciliation AS (
    /*
      Calculation 1:
      Income Statement result.

      Formula:
      Income - Expense
    */

    SELECT
        'Income Statement = Income - Expense'::varchar AS calculation,
        COALESCE(SUM(final_balance) FILTER (WHERE account_type = 'income' AND sorting = 1), 0)
        - COALESCE(SUM(final_balance) FILTER (WHERE account_type = 'expense' AND sorting = 1), 0)
        AS result
    FROM summery


    UNION ALL


    /*
      Calculation 2:
      Balance Sheet result.

      Formula:
      Asset - Liability - Equity
    */

    SELECT
        'Balance Sheet = Asset - Liability - Equity'::varchar,
        COALESCE(SUM(final_balance) FILTER (WHERE account_type = 'asset' AND sorting = 1), 0)
        - COALESCE(SUM(final_balance) FILTER (WHERE account_type = 'liability' AND sorting = 1), 0)
        - COALESCE(SUM(final_balance) FILTER (WHERE account_type = 'equity' AND sorting = 1), 0)
    FROM summery


    UNION ALL


    /*
      Calculation 3:
      Complete accounting-equation reconciliation.

      Formula:
      Asset - Liability - Equity - Income + Expense

      Expected result:
      0
    */

    SELECT
        'Asset - Liability - Equity - Income + Expense = 0'::varchar,
        COALESCE(SUM(final_balance) FILTER (WHERE account_type = 'asset' AND sorting = 1), 0)
        - COALESCE(SUM(final_balance) FILTER (WHERE account_type = 'liability' AND sorting = 1), 0)
        - COALESCE(SUM(final_balance) FILTER (WHERE account_type = 'equity' AND sorting = 1), 0)
        - COALESCE(SUM(final_balance) FILTER (WHERE account_type = 'income' AND sorting = 1), 0)
        + COALESCE(SUM(final_balance) FILTER (WHERE account_type = 'expense' AND sorting = 1), 0)
    FROM summery
)


/*
  Return all reconciliation calculations.
*/

SELECT * FROM reconciliation;
```

---

# Code 7: full_financial_statement - report (Master code + select query)

```sql
/*
===============================================================================
CODE 7: FULL FINANCIAL STATEMENT
===============================================================================

Purpose:
- Displays every non-zero account from all account types.
- Includes assets, liabilities, equity, income and expenses.
- Shows each account's hierarchy path.
- Uses rolled-up balances from summery.

Required:
- Paste this SELECT after Code 1.
===============================================================================
*/

SELECT
    account_type,
    account_category,
    account_code,
    account_name,
    path,

    /*
      Rolled-up debit, credit and final balance.
    */

    debit,
    credit,
    final_balance
FROM summery

/*
  Remove accounts where all reported amounts are zero.
*/

WHERE debit <> 0 OR credit <> 0 OR final_balance <> 0

/*
  Group the report by account type and then hierarchy path.
*/

ORDER BY account_type, path;
```


---

*Built by Jewel (Yaqin) — MSc Computer Science, Comilla University*
