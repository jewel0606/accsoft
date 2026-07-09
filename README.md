# accsoft — SQL-Based Accounting System (MSc Project)

## What This Project Is

This is a **double-entry accounting system** built entirely on SQL, 
developed as a final-year MSc Computer Science project at Comilla University.

The core idea is simple:
- All accounting data lives in **Supabase (PostgreSQL)** — a free cloud database
- All accounting logic — journal entries, ledger, trial balance, 
  income statement, balance sheet — is written purely in **SQL views and queries**
- A simple **Python frontend (Streamlit)** connects to the database 
  and displays the reports as live tables in a browser
- GitHub stores the Python code and Streamlit Cloud hosts it free online

**Live App:** https://accsoft.streamlit.app  
**GitHub:** https://github.com/jewel0606/accsoft  
**Database:** Supabase (accsoft project)

---

## Project Stack

| Layer | Tool | Purpose |
|---|---|---|
| Database | Supabase (PostgreSQL) | Tables, views, all accounting logic |
| Frontend | Streamlit (Python) | Display reports in browser |
| Code Storage | GitHub | Stores Python files |
| Hosting | Streamlit Cloud | Runs app free online

---

## What You Can See in the Live App

Open the live app: **https://accsoft.streamlit.app**

You will see these reports, all loading live from the database:

| Tab | What It Shows |
|---|---|
| Chart of Accounts | All accounts (asset, liability, equity, income, expense) |
| Trial Balance | Total debits, credits, and final balance per account |
| Income Statement | All income and expenses with Net Income total |
| Balance Sheet | Assets, liabilities, equity with Total Balance row |
| Journal Register | Every single journal line posted to the system |

Each report is generated **live at the moment you click the button** — 
not stored as a static file. The data comes directly from Supabase.

---

## How It Works — The Full Picture

You enter data → Supabase (PostgreSQL database)
↓
SQL views calculate reports
↓
Python (Streamlit) fetches the result
↓
Browser shows the live report table


**Data entry** happens directly in Supabase — using the Supabase table 
editor or SQL insert statements. There is no entry form in the frontend 
by design — the frontend is read-only, showing reports only.

**Streamlit** does not do any accounting calculation. It only:
1. Connects to Supabase using a URL and API key
2. Fetches the result of a SQL view when you click a button
3. Displays it as a table on screen

**All the accounting intelligence** — double-entry validation, 
multi-level aggregation, balance sheet equation, net income calculation — 
is written in SQL inside Supabase.

**GitHub** stores only three Python files (db.py, app.py, requirements.txt). 
Streamlit Cloud reads these files from GitHub and runs them as a live website.

---

## Why This Architecture

| Reason | Explanation |
|---|---|
| SQL-heavy | The developer's strength is SQL — so all logic stays in SQL |
| Free | Supabase free tier + Streamlit Cloud free tier + GitHub free = zero cost |
| Online | Accessible from any browser, no installation needed |
| Simple frontend | Python (Streamlit) chosen because it needs almost no HTML or JS |
| Academic demo | Shows real double-entry accounting logic, not just a UI mockup |

---

## What "Double-Entry" Means in This System

Every transaction in the `jnl` table has two lines — one debit and one credit.
The same `transaction_id` links them together.

Example — paying rent:
Dr  Rent Expense     1000   (debit increases expense)
Cr  Cash             1000   (credit decreases asset)

The SQL views then aggregate all these lines to produce:
- Trial Balance (are debits = credits across all accounts?)
- Income Statement (income minus expenses = net profit?)
- Balance Sheet (assets = liabilities + equity?)
- Reconciliation check (does asset - liability - equity - income + expense = 0?)

If the reconciliation shows 0, the books are perfectly balanced.



## Level 1: Set Up All Platforms

### Step 0: Create Supabase Account

1. Go to supabase.com → Sign up → free account
2. Create project:
   - Name: accsoft
   - Password: save this somewhere safe
   - Region: Southeast Asia (nearest to Bangladesh)
   - Plan: Free
   - Click Create → wait 2 minutes
3. Create tables in SQL Editor → New Query → Run in this exact order:
```
   currency → chart_of_accounts → contact → department →
   location → item → budget → user → jnl
```
4. Insert minimum seed data:
```sql
   INSERT INTO public.currency (currency_id) VALUES ('USD');
```
5. Create views (SQL Editor → New Query → paste view code → Run):
   - view_chart_of_accounts
   - view_trial_balance
   - view_income_statement
   - view_balance_sheet
   - view_recon
   - view_journal_register
   - view_cash_flow (requires account_pattern data in chart_of_accounts)

6. Set security on core tables only (not views):
```sql
   ALTER TABLE public.jnl ENABLE ROW LEVEL SECURITY;
   ALTER TABLE public.chart_of_accounts ENABLE ROW LEVEL SECURITY;
   CREATE POLICY "anon_read_only" ON public.jnl FOR SELECT USING (true);
   CREATE POLICY "anon_read_only" ON public.chart_of_accounts FOR SELECT USING (true);
```
   Note: Views do NOT have RLS. Only tables do. Never run ALTER TABLE on a view.

7. Get credentials — Settings → API:
   - SUPABASE_URL = Project URL
   - SUPABASE_KEY = anon public key (never use service_role key)

8. Test before moving on:
```sql
   SELECT * FROM view_trial_balance LIMIT 5;
```
   If no error → Supabase is ready.

---

### Step 1: Create GitHub Account
Go to github.com → Sign up → free account

### Step 2: Create Repository
- Click + → New repository
- Name: accsoft
- Tick: Add a README file
- Visibility: Public
- Click Create repository

### Step 3: Create requirements.txt
```
streamlit
supabase
pandas
```

### Step 4: Create db.py
```python
from supabase import create_client

SUPABASE_URL = "https://phu"
SUPABASE_KEY = "your-anon-key-here"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
```

### Step 5: Create app.py
```python
import streamlit as st
from db import supabase
import pandas as pd

st.set_page_config(page_title="Accounting System", layout="wide")

st.markdown("""
<h1 style='color:#2c3e50;'>Accounting System — MSc Demo</h1>
<p>All reports load live from Supabase PostgreSQL database.</p>
<hr>
""", unsafe_allow_html=True)

def show_report(view_name):
    try:
        result = supabase.table(view_name).select("*").execute()
        if result.data:
            df = pd.DataFrame(result.data)
            st.dataframe(df, use_container_width=True, height=600)
        else:
            st.info("No data found.")
    except Exception as e:
        st.error(f"Error: {e}")

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
```

### Step 6: Create Streamlit Account
Go to share.streamlit.io → Sign in with GitHub

### Step 7: Deploy App
1. Click Create app
2. Repository → jewel0606/accsoft
3. Branch → main
4. Main file path → app.py
5. App URL → accsoft
6. Click Deploy → wait 60 seconds

### Step 8: Files on GitHub
```
accsoft/
├── README.md
├── requirements.txt
├── db.py
└── app.py
```

---

## Level 2: Code Explanation

### GitHub — Why
Streamlit Cloud cannot read files from your laptop. GitHub stores your code in the cloud so Streamlit can read it. Every time you edit and commit on GitHub, Streamlit updates automatically within 10 seconds.

### requirements.txt — Why
Streamlit Cloud server starts empty. This file tells it what to install before running your code: streamlit, supabase, pandas.

### db.py — Line by Line

```python
from supabase import create_client
# Imports the connection tool from the supabase library

SUPABASE_URL = "https://..."
# Address of your Supabase database — like a home address

SUPABASE_KEY = "eyJhbG..."
# Password (anon key) — proves Python has read permission

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
# Opens the actual connection — stored as variable 'supabase'
# Every other file imports this variable
```

### app.py — Line by Line

```python
import streamlit as st          # Streamlit, nicknamed st
from db import supabase         # Borrow the connection from db.py
import pandas as pd             # Table tool, nicknamed pd

st.set_page_config(...)         # Sets browser tab title and wide layout
st.markdown("""...""")          # Draws the heading using HTML colors

def show_report(view_name):     # Reusable function — write once, call many times
    result = supabase.table(view_name).select("*").execute()
    # Fetches all columns from the named Supabase view

    df = pd.DataFrame(result.data)
    # Converts raw data into a table Streamlit can display

    st.dataframe(df, use_container_width=True, height=600)
    # Draws the table — height=600 prevents freeze (never use height=10000)

tab1, tab2... = st.tabs([...])  # Creates navigation tabs automatically

with tab1:
    if st.button("Load"):       # Button — when clicked calls show_report
        show_report("view_name")
```

### How to Add a New Report Tab
1. Add tab name to tabs list
2. Add `with tabN:` block at bottom
3. Commit on GitHub → Streamlit updates automatically

---

## Level 3: SQL Supabase Structure

### Table Creation Order
Must follow this sequence — foreign keys require parent tables first:

```
1. currency          ← jnl needs currency_id
2. chart_of_accounts ← jnl needs account_code
3. contact           ← jnl needs contact_id for invoices/bills
4. department        ← optional
5. location          ← optional
6. item              ← optional
7. budget            ← optional
8. user              ← optional
9. jnl               ← always last
```

### Report Dependency Map

```
jnl + chart_of_accounts
        ↓
   account_summary  — one row per account with debit/credit/balance
        ↓
       fs            — 5 aggregation levels (sort_order 0 to 4)
        ↓
   ┌────┴──────┬────────────────┬───────────────┬─────────────┐
 recon    balance_sheet   income_statement  trail_balance     fs
(verify)  (asset/liab      (income/expense   (all accounts   (all
           /equity)         + net income)     raw detail)     levels)

jnl + contact (account_code = 106 = Accounts Payable)
        ↓
     Bill Master
        ↓
   bills_to_pay / aged_payables / vendor_statement

jnl + contact (account_code = 107 = Accounts Receivable)
        ↓
   Invoice Master
        ↓
   customer_ledger / invoices_summary / aged_receivables / customer_statement

jnl + chart_of_accounts (account_pattern = 'cash' or 'bank')
        ↓
   Cash Flow → Operating / Investing / Financing / Net / Opening / Closing
```

### Table Schemas

**Table 1: jnl** — main transaction table, every entry goes here
```sql
create table public.jnl (
  transaction_id character varying(40) not null,
  transaction_line_id character varying(40) not null,
  transaction_date date not null,
  description character varying(400) not null,
  account_code integer not null,
  amount double precision not null,
  dc character varying(10) not null,
  transaction_type character varying(20) not null,
  memo character varying(80) not null,
  note character varying(400) null,
  contact_id character varying(40) null,
  status character varying(10) not null,
  currency_id character varying(40) not null,
  total_amount double precision not null,
  due_date date null,
  adjustment character varying(400) null,
  tracking character varying(200) null,
  created_date timestamp without time zone null,
  related_transaction_id character varying(40) null,
  payment_transaction_id character varying(40) null,
  posting_period_id date null,
  accounting_period_id date null,
  created_by_id character varying(40) null,
  department_id character varying(40) null,
  location_id character varying(40) null,
  attachment_id character varying(40) null,
  item_id integer null,
  quantity integer null,
  rate double precision null,
  expense_category_id character varying(40) null,
  vat_rate double precision null,
  vat_amount double precision null,
  tax_rate double precision null,
  tax_amount double precision null,
  tracking_name1 character varying(200) null,
  tracking_name2 character varying(200) null,
  tracking_name3 character varying(200) null,
  repet_post_start date null,
  repet_post_frequency integer null,
  repet_post_due integer null,
  repet_post_end date null,
  repet_post_type character varying(10) null,
  repet_post_note character varying(200) null,
  reminder_start date null,
  reminder_frequency integer null,
  reminder_end date null,
  constraint jnl_pkey primary key (transaction_line_id),
  constraint jnl_contact_id_fkey foreign KEY (contact_id) references contact (contact_id),
  constraint jnl_currency_id_fkey foreign KEY (currency_id) references currency (currency_id),
  constraint jnl_account_code_fkey foreign KEY (account_code) references chart_of_accounts (account_code),
  constraint jnl_dc_check check (dc::text = any (array['debit','credit']::text[])),
  constraint jnl_status_check check (status::text = any (array['draft','post','void']::text[])),
  constraint jnl_transaction_type_check check (transaction_type::text = any (array['bill','invoice','journal','dnote','cnote','paid','received']::text[]))
);
```

**Table 2: chart_of_accounts** — must exist before jnl
```sql
create table public.chart_of_accounts (
  account_code bigint not null,
  account_name character varying(300) not null,
  account_sub1 character varying(300) null,
  account_category character varying(100) null,
  account_type character varying(70) not null,
  account_sub2 character varying null,
  account_pattern character varying null,
  account_support character varying null,
  constraint chart_of_accounts_pkey primary key (account_code),
  constraint chart_of_accounts_account_name_key unique (account_name),
  constraint chart_of_accounts_account_type_check check (
    account_type::text = any (array['asset','liability','equity','income','expense']::text[]))
);
```

**Table 3: contact** — needed for invoice/bill reports
```sql
create table public.contact (
  contact_id character varying not null,
  type text null,
  name character varying(40) not null,
  trade_license_name character varying(40) null,
  tacking_name character varying(40) null,
  address character varying(120) null,
  bin character varying(40) null,
  tin character varying(40) null,
  notes character varying(120) null,
  road_and_location character varying(40) null,
  city character varying(40) null,
  state character varying(40) null,
  country character varying(40) null,
  constraint contact_pkey primary key (contact_id),
  constraint contact_type_check check (type = any (array['Customer','Supplier','Other']))
);
```

**Tables 4–10: Supporting tables** (currency, department, location, item, budget, user, expense)
```sql
create table public.currency (currency_id character varying(40) not null, constraint currency_pkey primary key (currency_id));
create table public.department (department_id character varying(40) not null, constraint department_pkey primary key (department_id));
create table public.location (location_id character varying(40) not null, constraint location_pkey primary key (location_id));
create table public.user (user_id character varying(40) not null, constraint user_pkey primary key (user_id));
create table public.item (item_id integer not null, item_name character varying(300) not null, item_sub_category character varying(300) null, item_category character varying(300) null, constraint item_pkey primary key (item_id));
create table public.budget (expense_category_id character varying(200) not null, name character varying(200) not null, category_type character varying(10) not null, sub_category_name character varying(200) null, constraint budget_pkey primary key (expense_category_id));
create table public.expense (id serial not null, date date null, amount numeric(15,2) null, details character varying(300) null, month date null, payment character varying(100) null, main_category character varying(300) null, sub_category character varying(300) null, name character varying(300) null, constraint expense_pkey primary key (id));
```

---

### Report Views — Complete List

**Group A — Master code views (jnl + chart_of_accounts):**

| View | Final SELECT |
|---|---|
| view_chart_of_accounts | SELECT * FROM chart_of_accounts ORDER BY account_code |
| view_trial_balance | Master code + SELECT * FROM trail_balance |
| view_income_statement | Master code + SELECT * FROM income_statement |
| view_balance_sheet | Master code + SELECT * FROM balance_sheet |
| view_recon | Master code + SELECT * FROM recon |

**Group B — Single query views:**

| View | Code |
|---|---|
| view_cash_flow | Code 8 |
| view_journal_register | Code 9 |

**Group C — Contact views (jnl + contact):**

| View | Master + Code |
|---|---|
| view_vendor_ledger | Vendor Master + SELECT * FROM main |
| view_purchase_summary | Vendor Master + SELECT * FROM purchase_summary |
| view_customer_ledger | Invoice Master + SELECT * FROM customer_ledger |
| view_invoices_summary | Invoice Master + SELECT * FROM invoices_summary |
| view_aged_receivables | Invoice Master + SELECT * FROM aged_receivables |
| view_bills_to_pay | Bill Master + SELECT * FROM bills_to_pay |
| view_aged_payables | Bill Master + SELECT * FROM aged_payables |
| view_vendor_statement | Bill Master + SELECT * FROM vendor_statement |

---

### Known Problems and Fixes

**Problem 1: discount not allowed in transaction_type**
Affects: Vendor report, Vendor Ledger, Purchase Summary
Fix:
```sql
ALTER TABLE public.jnl DROP CONSTRAINT jnl_transaction_type_check;
ALTER TABLE public.jnl ADD CONSTRAINT jnl_transaction_type_check
CHECK (transaction_type IN ('bill','invoice','journal','dnote','cnote','paid','received','discount'));
```

**Problem 2: due_date allows NULL**
Affects: All invoice and bill aging reports
Fix: Always enter due_date when posting bill or invoice entries. Or set default:
```sql
ALTER TABLE public.jnl ALTER COLUMN due_date SET DEFAULT CURRENT_DATE;
```

**Problem 3: Cash Flow requires account_pattern**
Affects: view_cash_flow
Fix: Set account_pattern = 'cash' or 'bank' in chart_of_accounts for cash/bank accounts.

---

### SQL Codes

**Code 1: Master Code** (generates all Group A reports by changing last line)

```sql
with
  account_summary as (
    select
      coa.account_code, coa.account_type, coa.account_category,
      case when coa.account_sub1 is null and coa.account_sub2 is null then coa.account_name
           when coa.account_sub1 is null and coa.account_sub2 is not null then coa.account_sub2
           else coa.account_sub1 end as main_ledger,
      case when coa.account_sub2 is null then coa.account_name else coa.account_sub2 end as sub_ledger,
      coa.account_name, coa.account_sub1, coa.account_sub2,
      sum(case when jnl.dc::text = 'debit'::text then jnl.amount else 0 end) as total_debit,
      sum(case when jnl.dc::text = 'credit'::text then jnl.amount else 0 end) as total_credit,
      case when coa.account_type::text = any (array['asset','expense']::text[])
           then sum(case when jnl.dc::text = 'debit'::text then jnl.amount else -jnl.amount end)
           else sum(case when jnl.dc::text = 'credit'::text then jnl.amount else -jnl.amount end)
      end as final_balance
    from jnl join chart_of_accounts coa on jnl.account_code = coa.account_code
    group by coa.account_code, coa.account_type, coa.account_category, coa.account_name, coa.account_sub1,
      case when coa.account_sub1 is null then coa.account_name else coa.account_sub1 end,
      case when coa.account_sub2 is null then coa.account_sub1 else coa.account_sub2 end
  ),
  fs as (
    select account_summary.account_type, null::character varying as account_category,
      null::text as main_ledger, null::text as sub_ledger, null::text as account_name,
      sum(account_summary.total_debit) as total_debit, sum(account_summary.total_credit) as total_credit,
      sum(account_summary.final_balance) as final_balance, 0 as sort_order
    from account_summary group by account_summary.account_type
    union all
    select account_summary.account_type, account_summary.account_category,
      null::text, null::text, null::text,
      sum(account_summary.total_debit), sum(account_summary.total_credit), sum(account_summary.final_balance), 1
    from account_summary group by account_summary.account_type, account_summary.account_category
    union all
    select account_summary.account_type, account_summary.account_category, account_summary.main_ledger,
      null::text, null::text,
      sum(account_summary.total_debit), sum(account_summary.total_credit), sum(account_summary.final_balance), 2
    from account_summary group by account_summary.account_type, account_summary.account_category, account_summary.main_ledger
    union all
    select account_summary.account_type, account_summary.account_category, account_summary.main_ledger, account_summary.sub_ledger,
      null::text,
      sum(account_summary.total_debit), sum(account_summary.total_credit), sum(account_summary.final_balance), 3
    from account_summary group by account_summary.account_type, account_summary.account_category, account_summary.main_ledger, account_summary.sub_ledger
    union all
    select account_summary.account_type, account_summary.account_category, account_summary.main_ledger, account_summary.sub_ledger,
      account_summary.account_name, account_summary.total_debit, account_summary.total_credit, account_summary.final_balance, 4
    from account_summary
    order by 1, 2 desc, 3 desc, 4 desc, 9, 5
  ),
  recon as (
    select fs.account_type, fs.account_category, fs.main_ledger, fs.sub_ledger, fs.account_name,
      fs.total_debit, fs.total_credit, fs.final_balance, fs.sort_order
    from fs where fs.account_category is null
    union all
    select 'income statement = income - expense', null, null, null, null, null, null,
      (select fs.final_balance from fs where fs.account_type = 'income' and fs.account_category is null) -
      (select fs.final_balance from fs where fs.account_type = 'expense' and fs.account_category is null), null
    union all
    select 'balance sheet = asset - liability - equity', null, null, null, null, null, null,
      (select fs.final_balance from fs where fs.account_type = 'asset' and fs.account_category is null) -
      (select fs.final_balance from fs where fs.account_type = 'liability' and fs.account_category is null) -
      (select fs.final_balance from fs where fs.account_type = 'equity' and fs.account_category is null), null
    union all
    select 'asset - liability - equity - income + expense = 0', null, null, null, null, null, null,
      (select fs.final_balance from fs where fs.account_type = 'asset' and fs.account_category is null) -
      (select fs.final_balance from fs where fs.account_type = 'liability' and fs.account_category is null) -
      (select fs.final_balance from fs where fs.account_type = 'equity' and fs.account_category is null) -
      (select fs.final_balance from fs where fs.account_type = 'income' and fs.account_category is null) +
      (select fs.final_balance from fs where fs.account_type = 'expense' and fs.account_category is null), null
  ),
  balance_sheet as (
    select fs.account_type, fs.account_category, fs.main_ledger, fs.sub_ledger, fs.account_name,
      fs.total_debit, fs.total_credit, fs.final_balance
    from fs where fs.account_type = any (array['asset','liability','equity']) and fs.sort_order = 4
    union all
    select 'TOTAL', null, null, null, 'Total Balance', sum(fs.total_debit), sum(fs.total_credit),
      (select fs_1.final_balance from fs fs_1 where fs_1.account_type = 'asset' and fs_1.account_category is null) -
      (select fs_1.final_balance from fs fs_1 where fs_1.account_type = 'liability' and fs_1.account_category is null) -
      (select fs_1.final_balance from fs fs_1 where fs_1.account_type = 'equity' and fs_1.account_category is null)
    from fs where fs.account_type = any (array['asset','liability','equity']) and fs.sort_order = 4
    order by 1, 2 desc nulls last, 3, 4, 5
  ),
  trail_balance as (
    select account_summary.account_code, account_summary.account_type, account_summary.account_category,
      account_summary.main_ledger, account_summary.sub_ledger, account_summary.account_name,
      account_summary.account_sub1, account_summary.account_sub2,
      account_summary.total_debit, account_summary.total_credit, account_summary.final_balance
    from account_summary
  ),
  income_statement as (
    select fs.account_type, fs.account_category, fs.main_ledger, fs.sub_ledger, fs.account_name,
      fs.total_debit, fs.total_credit, fs.final_balance
    from fs where fs.account_type = any (array['income','expense']) and fs.sort_order = 4
    union all
    select 'TOTAL', null, null, null, 'Net Income', sum(fs.total_debit), sum(fs.total_credit),
      (select fs_1.final_balance from fs fs_1 where fs_1.account_type = 'income' and fs_1.account_category is null) -
      (select fs_1.final_balance from fs fs_1 where fs_1.account_type = 'expense' and fs_1.account_category is null)
    from fs where fs.account_type = any (array['income','expense']) and fs.sort_order = 4
    order by 1, 2 desc nulls last, 3, 4, 5
  )
-- Change this last line to switch reports:
-- select * from account_summary;     → Code 2: raw account data
-- select * from trail_balance;       → Code 5: Trial Balance
-- select * from fs;                  → Code 7: Full Financial Statement
-- select * from recon;               → Reconciliation
-- select account_type, account_category, main_ledger, sub_ledger, account_name, total_debit, total_credit, final_balance from balance_sheet; → Code 3: Balance Sheet
-- select account_type, account_category, main_ledger, sub_ledger, account_name, total_debit, total_credit, final_balance from income_statement; → Code 4: Income Statement
select account_type, account_category, main_ledger, sub_ledger, account_name, total_debit, total_credit, final_balance
from income_statement;
```

**Code 8: Cash Flow**
```sql
WITH report_params AS (
    SELECT DATE '2024-07-01' AS period_start_date, DATE '2025-12-31' AS period_end_date
),
cash_accounts AS (
    SELECT account_code, account_name FROM chart_of_accounts WHERE account_pattern IN ('cash', 'bank')
),
opening_cash_balance AS (
    SELECT COALESCE(SUM(CASE WHEN jnl.dc = 'debit' THEN jnl.amount WHEN jnl.dc = 'credit' THEN -jnl.amount ELSE 0 END), 0) AS opening_balance
    FROM jnl WHERE jnl.account_code IN (SELECT account_code FROM cash_accounts) AND jnl.transaction_date < (SELECT period_start_date FROM report_params)
),
cash_flow_entries AS (
    SELECT jnl.transaction_id, jnl.transaction_date, jnl.account_code AS line_account_code, coa.account_type AS line_account_type, coa.account_category AS line_account_category, jnl.dc, jnl.amount, jnl.description,
        CASE WHEN jnl.account_code IN (SELECT account_code FROM cash_accounts) AND jnl.dc = 'debit' THEN jnl.amount WHEN jnl.account_code IN (SELECT account_code FROM cash_accounts) AND jnl.dc = 'credit' THEN -jnl.amount ELSE 0 END AS cash_impact,
        CASE WHEN jnl.account_code IN (SELECT account_code FROM cash_accounts) THEN TRUE ELSE FALSE END AS is_cash_line
    FROM jnl JOIN chart_of_accounts coa ON jnl.account_code = coa.account_code
    WHERE jnl.transaction_date BETWEEN (SELECT period_start_date FROM report_params) AND (SELECT period_end_date FROM report_params)
    AND jnl.transaction_id IN (SELECT DISTINCT transaction_id FROM jnl WHERE account_code IN (SELECT account_code FROM cash_accounts) AND transaction_date BETWEEN (SELECT period_start_date FROM report_params) AND (SELECT period_end_date FROM report_params))
),
classified_transactions AS (
    SELECT cfe.transaction_id, cfe.transaction_date, cfe.description, SUM(cfe.cash_impact) AS net_cash_change_for_txn,
        MAX(CASE WHEN NOT cfe.is_cash_line THEN CASE WHEN cfe.line_account_type IN ('income','expense') THEN 'Operating' WHEN cfe.line_account_category IN ('Current Assets','Current Liabilities') AND cfe.line_account_code NOT IN (SELECT account_code FROM cash_accounts) THEN 'Operating' WHEN cfe.line_account_category = 'Non-Current Assets' THEN 'Investing' WHEN cfe.line_account_category IN ('Non-Current Liabilities','Shareholder Equity') THEN 'Financing' ELSE 'Unclassified' END ELSE NULL END) AS primary_classification_type
    FROM cash_flow_entries cfe GROUP BY cfe.transaction_id, cfe.transaction_date, cfe.description HAVING SUM(cfe.cash_impact) != 0
),
cash_flow_summary AS (
    SELECT primary_classification_type AS cash_flow_category, SUM(net_cash_change_for_txn) AS total_cash_flow
    FROM classified_transactions WHERE primary_classification_type IS NOT NULL AND primary_classification_type != 'Unclassified' GROUP BY primary_classification_type
),
net_cash_flow_period AS (SELECT SUM(total_cash_flow) AS net_increase_decrease_in_cash FROM cash_flow_summary),
closing_cash_balance AS (
    SELECT COALESCE(SUM(CASE WHEN jnl.dc = 'debit' THEN jnl.amount WHEN jnl.dc = 'credit' THEN -jnl.amount ELSE 0 END), 0) AS closing_balance
    FROM jnl WHERE jnl.account_code IN (SELECT account_code FROM cash_accounts) AND jnl.transaction_date <= (SELECT period_end_date FROM report_params)
)
SELECT 'Cash Flow from Operating Activities' AS Category, COALESCE(SUM(CASE WHEN cfs.cash_flow_category='Operating' THEN cfs.total_cash_flow ELSE 0 END),0) AS Amount FROM cash_flow_summary cfs
UNION ALL SELECT 'Cash Flow from Investing Activities', COALESCE(SUM(CASE WHEN cfs.cash_flow_category='Investing' THEN cfs.total_cash_flow ELSE 0 END),0) FROM cash_flow_summary cfs
UNION ALL SELECT 'Cash Flow from Financing Activities', COALESCE(SUM(CASE WHEN cfs.cash_flow_category='Financing' THEN cfs.total_cash_flow ELSE 0 END),0) FROM cash_flow_summary cfs
UNION ALL SELECT 'Net Increase (Decrease) in Cash', (SELECT net_increase_decrease_in_cash FROM net_cash_flow_period)
UNION ALL SELECT 'Cash at Beginning of Period', (SELECT opening_balance FROM opening_cash_balance)
UNION ALL SELECT 'Cash at End of Period', (SELECT closing_balance FROM closing_cash_balance);
```

**Code 9: Journal Register**
```sql
WITH report_params AS (
    SELECT DATE '2024-01-01' AS period_start_date, DATE '2025-12-31' AS period_end_date
),
journal_register AS (
    SELECT jnl.transaction_date, jnl.transaction_id, jnl.transaction_line_id, jnl.account_code, coa.account_name, jnl.description, jnl.memo,
        CASE WHEN jnl.dc = 'debit' THEN jnl.amount ELSE 0 END AS debit,
        CASE WHEN jnl.dc = 'credit' THEN jnl.amount ELSE 0 END AS credit
    FROM jnl JOIN chart_of_accounts coa ON jnl.account_code = coa.account_code JOIN report_params rp ON TRUE
    WHERE jnl.transaction_date BETWEEN rp.period_start_date AND rp.period_end_date
    ORDER BY jnl.transaction_date, jnl.transaction_id, jnl.transaction_line_id
)
SELECT transaction_date, transaction_id, transaction_line_id, account_code, account_name, description, memo, debit, credit
FROM journal_register;
```

**Code 10: Ledger**
```sql
WITH dates AS (SELECT DATE '2024-07-01' AS start, DATE '2025-12-31' AS end),
account AS (SELECT 'Accounts Payable' AS name),
opening_balance AS (
  SELECT COALESCE(SUM(CASE WHEN coa.account_type IN ('asset','expense') THEN CASE WHEN jnl.dc='debit' THEN jnl.amount WHEN jnl.dc='credit' THEN -jnl.amount ELSE 0 END ELSE CASE WHEN jnl.dc='debit' THEN -jnl.amount WHEN jnl.dc='credit' THEN jnl.amount ELSE 0 END END), 0) AS opening_balance
  FROM jnl JOIN chart_of_accounts coa ON jnl.account_code=coa.account_code JOIN dates ON TRUE JOIN account ON TRUE
  WHERE coa.account_name=account.name AND jnl.transaction_date < dates.start
),
ledger AS (
  SELECT jnl.transaction_id, jnl.transaction_date, coa.account_name, coa.account_type,
    CASE WHEN jnl.dc='debit' THEN jnl.amount ELSE 0 END AS debit,
    CASE WHEN jnl.dc='credit' THEN jnl.amount ELSE 0 END AS credit,
    SUM(CASE WHEN coa.account_type IN ('asset','expense') THEN CASE WHEN jnl.dc='debit' THEN jnl.amount WHEN jnl.dc='credit' THEN -jnl.amount ELSE 0 END ELSE CASE WHEN jnl.dc='debit' THEN -jnl.amount WHEN jnl.dc='credit' THEN jnl.amount ELSE 0 END END)
    OVER (ORDER BY jnl.transaction_date, jnl.transaction_id, jnl.transaction_line_id) AS running_delta
  FROM jnl JOIN chart_of_accounts coa ON jnl.account_code=coa.account_code JOIN dates ON TRUE JOIN account ON TRUE
  WHERE coa.account_name=account.name AND jnl.transaction_date BETWEEN dates.start AND dates.end
)
SELECT NULL AS transaction_id, dates.start AS transaction_date, 'Opening Balance' AS account_name, 0 AS debit, 0 AS credit, opening_balance.opening_balance AS balance FROM dates, opening_balance
UNION ALL SELECT transaction_id, transaction_date, account_name, debit, credit, opening_balance.opening_balance + running_delta AS balance FROM ledger, opening_balance
UNION ALL SELECT NULL, NULL, 'Total', SUM(debit), SUM(credit), MAX(opening_balance.opening_balance) + CASE WHEN MAX(account_type) IN ('asset','expense') THEN SUM(debit)-SUM(credit) ELSE SUM(credit)-SUM(debit) END FROM ledger, opening_balance;
```

**Code 11: Vendor Master** (base for Codes 12–13)
```sql
WITH dates AS (SELECT DATE '2025-12-31' AS d),
main AS (
  SELECT jnl.contact_id, contact.name,
    CASE WHEN dc != 'credit' THEN payment_transaction_id ELSE transaction_id END AS txn,
    CASE WHEN dc = 'credit' THEN amount WHEN dc = 'debit' THEN -amount ELSE 0 END AS final,
    SUM(CASE WHEN dc='credit' THEN amount WHEN dc='debit' THEN -amount ELSE 0 END) OVER (PARTITION BY jnl.contact_id ORDER BY transaction_date, transaction_id) AS running,
    ROW_NUMBER() OVER (PARTITION BY jnl.contact_id ORDER BY transaction_date, transaction_id) AS txn_row,
    transaction_id, transaction_line_id, transaction_date, due_date, payment_transaction_id, amount, dc, description, account_code, transaction_type, memo, dates.d AS report_date
  FROM jnl JOIN contact ON jnl.contact_id=contact.contact_id JOIN dates ON TRUE WHERE account_code=106
),
purchase_summary AS (
  SELECT contact_id, name,
    COUNT(DISTINCT CASE WHEN transaction_type='bill' THEN transaction_id ELSE NULL END) AS "Bills",
    SUM(CASE WHEN transaction_type='bill' AND dc='credit' THEN amount ELSE 0 END) AS "Total Purchase",
    SUM(CASE WHEN transaction_type IN ('cnote','discount') AND dc='debit' THEN amount ELSE 0 END) AS "Discounts & Returns",
    SUM(CASE WHEN transaction_type='dnote' AND dc='credit' THEN amount ELSE 0 END) AS "Debit Notes",
    SUM(final) AS "Net Purchases"
  FROM main GROUP BY contact_id, name ORDER BY name
)
-- Code 12: SELECT * FROM main;
-- Code 13: SELECT * FROM purchase_summary;
SELECT * FROM main;
```

**Code 14: Invoice Master** (base for Codes 15–18)
```sql
WITH dates AS (SELECT DATE '2025-12-31' AS d),
txn_base_ar AS (
    SELECT CASE WHEN dc!='debit' THEN payment_transaction_id ELSE transaction_id END AS txn,
        CASE WHEN dc='debit' THEN amount WHEN dc='credit' THEN -amount ELSE 0 END AS final,
        SUM(CASE WHEN dc='debit' THEN amount WHEN dc='credit' THEN -amount ELSE 0 END) OVER (PARTITION BY CASE WHEN dc!='debit' THEN payment_transaction_id ELSE transaction_id END ORDER BY transaction_date, transaction_id) AS running,
        ROW_NUMBER() OVER (PARTITION BY CASE WHEN dc!='debit' THEN payment_transaction_id ELSE transaction_id END ORDER BY transaction_date, transaction_id) AS txn_row,
        transaction_id, transaction_line_id, transaction_date, due_date, payment_transaction_id, amount, dc, description, account_code, transaction_type, memo, contact_id, dates.d AS report_date
    FROM jnl, dates WHERE account_code=107 AND transaction_date<=dates.d ORDER BY transaction_date
),
balance_ar AS (SELECT * FROM txn_base_ar WHERE (txn,txn_row) IN (SELECT txn,MAX(txn_row) FROM txn_base_ar GROUP BY txn)),
info_ar AS (SELECT * FROM txn_base_ar WHERE (txn,txn_row) IN (SELECT txn,MIN(txn_row) FROM txn_base_ar GROUP BY txn)),
summary_ar AS (
    SELECT balance_ar.txn, balance_ar.final, balance_ar.running, balance_ar.txn_row,
        balance_ar.report_date-info_ar.transaction_date AS txn_diff, balance_ar.report_date-info_ar.due_date AS due_diff,
        info_ar.transaction_id, info_ar.transaction_line_id, info_ar.transaction_date, info_ar.due_date, info_ar.payment_transaction_id, info_ar.amount, info_ar.dc, info_ar.description, info_ar.account_code, info_ar.transaction_type, info_ar.memo, info_ar.contact_id
    FROM balance_ar JOIN info_ar ON balance_ar.txn=info_ar.txn
),
invoices_summary AS (
    SELECT txn, running AS outstanding_amount, transaction_id, transaction_date, due_date, contact_id, description,
        CASE WHEN due_diff<=0 THEN running ELSE 0 END AS current_due,
        CASE WHEN due_diff BETWEEN 1 AND 30 THEN running ELSE 0 END AS days_1_30_overdue,
        CASE WHEN due_diff BETWEEN 31 AND 60 THEN running ELSE 0 END AS days_31_60_overdue,
        CASE WHEN due_diff BETWEEN 61 AND 90 THEN running ELSE 0 END AS days_61_90_overdue,
        CASE WHEN due_diff>90 THEN running ELSE 0 END AS days_90_plus_overdue
    FROM summary_ar WHERE running!=0 ORDER BY due_date, transaction_id
),
aged_receivables AS (
    SELECT contact_id, SUM(CASE WHEN due_diff<=0 THEN running ELSE 0 END) AS current_due_total, SUM(CASE WHEN due_diff BETWEEN 1 AND 30 THEN running ELSE 0 END) AS days_1_30, SUM(CASE WHEN due_diff BETWEEN 31 AND 60 THEN running ELSE 0 END) AS days_31_60, SUM(CASE WHEN due_diff BETWEEN 61 AND 90 THEN running ELSE 0 END) AS days_61_90, SUM(CASE WHEN due_diff>90 THEN running ELSE 0 END) AS days_90_plus, SUM(running) AS total_receivable
    FROM summary_ar WHERE running!=0 GROUP BY contact_id ORDER BY contact_id
),
customer_statement AS (
    SELECT contact_id, transaction_id, transaction_date, due_date, description, dc, amount, running AS transaction_balance
    FROM summary_ar WHERE running!=0 ORDER BY contact_id, transaction_date, transaction_id
),
customer_ledger AS (
    SELECT jnl.contact_id, contact.name, CASE WHEN dc!='debit' THEN payment_transaction_id ELSE transaction_id END AS txn,
        CASE WHEN dc='debit' THEN amount WHEN dc='credit' THEN -amount ELSE 0 END AS final,
        SUM(CASE WHEN dc='debit' THEN amount WHEN dc='credit' THEN -amount ELSE 0 END) OVER (PARTITION BY jnl.contact_id ORDER BY transaction_date, transaction_id) AS running,
        ROW_NUMBER() OVER (PARTITION BY jnl.contact_id ORDER BY transaction_date, transaction_id) AS txn_row,
        transaction_id, transaction_line_id, transaction_date, due_date, payment_transaction_id, amount, dc, description, account_code, transaction_type, memo, dates.d AS report_date
    FROM jnl JOIN contact ON jnl.contact_id=contact.contact_id JOIN dates ON TRUE WHERE account_code=107
)
-- Code 15: SELECT * FROM customer_ledger;
-- Code 16: SELECT * FROM invoices_summary;
-- Code 17: SELECT * FROM aged_receivables;
-- Code 18: SELECT * FROM customer_statement;
SELECT * FROM customer_ledger;
```

**Code 19: Bill Master** (base for Codes 20–22)
```sql
WITH dates AS (SELECT DATE '2025-12-31' AS d),
txn_base AS (
  SELECT CASE WHEN dc!='credit' THEN payment_transaction_id ELSE transaction_id END AS txn,
    CASE WHEN dc='credit' THEN amount WHEN dc='debit' THEN -amount ELSE 0 END AS final,
    SUM(CASE WHEN dc='credit' THEN amount WHEN dc='debit' THEN -amount ELSE 0 END) OVER (PARTITION BY CASE WHEN dc!='credit' THEN payment_transaction_id ELSE transaction_id END ORDER BY transaction_date, transaction_id) AS running,
    ROW_NUMBER() OVER (PARTITION BY CASE WHEN dc!='credit' THEN payment_transaction_id ELSE transaction_id END ORDER BY transaction_date, transaction_id) AS txn_row,
    transaction_id, transaction_line_id, transaction_date, due_date, payment_transaction_id, amount, dc, description, account_code, transaction_type, memo, contact_id, dates.d AS report_date
  FROM jnl, dates WHERE account_code=106 AND transaction_date<=dates.d ORDER BY transaction_date
),
balance AS (SELECT * FROM txn_base WHERE (txn,txn_row) IN (SELECT txn,MAX(txn_row) FROM txn_base GROUP BY txn)),
info AS (SELECT * FROM txn_base WHERE (txn,txn_row) IN (SELECT txn,MIN(txn_row) FROM txn_base GROUP BY txn)),
summary AS (
  SELECT balance.txn, balance.final, balance.running, balance.txn_row,
    balance.report_date-info.transaction_date AS txn_diff, balance.report_date-info.due_date AS due_diff,
    info.transaction_id, info.transaction_line_id, info.transaction_date, info.due_date, info.payment_transaction_id, info.amount, info.dc, info.description, info.account_code, info.transaction_type, info.memo, info.contact_id
  FROM balance JOIN info ON balance.txn=info.txn
),
bills_to_pay AS (
  SELECT txn, CASE WHEN due_diff<30 THEN running ELSE 0 END AS month_1_less, CASE WHEN due_diff BETWEEN 31 AND 60 THEN running ELSE 0 END AS month_2, CASE WHEN due_diff BETWEEN 61 AND 90 THEN running ELSE 0 END AS month_3, CASE WHEN due_diff>90 THEN running ELSE 0 END AS more
  FROM summary ORDER BY txn
),
aged_payables AS (SELECT contact_id, SUM(running) AS total_due FROM summary GROUP BY contact_id),
vendor_statement AS (SELECT contact_id, * FROM summary WHERE running!=0)
-- Code 20: SELECT * FROM bills_to_pay;
-- Code 21: SELECT * FROM aged_payables;
-- Code 22: SELECT * FROM vendor_statement;
SELECT * FROM bills_to_pay;
```

---

*Built by Jewel (Yaqin) — MSc Computer Science, Comilla University*
