import streamlit as st
import psycopg2
import pandas as pd


# Checking for login

if not st.session_state.get("logged_in"):
    st.switch_page("login.py")


# DB Connections

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="Sales_Management-Project1",
    user="postgres",
    password="1234"
)

cur = conn.cursor()


# Session Data

username = st.session_state.get("username")
role = st.session_state.get("role")
user_branch_id = st.session_state.get("branch_id")


# Get Branch Name Details

if role != "Super Admin":

    cur.execute("""
        SELECT branch_name
        FROM branches
        WHERE branch_id = %s
    """, (user_branch_id,))

    row = cur.fetchone()

    branch_name = row[0] if row else "Unknown"

else:
    branch_name = "All Branches"


# Title & Logout Column

col1, col2, col3 = st.columns([8, 2, 2])

with col1:
    st.title("📊 Students Enrollment Dashboard")

with col2:
    if st.button("Back"):
        st.switch_page("pages/Management.py")

with col3:
    if st.button("Logout"):
        st.session_state.clear()
        st.switch_page("login.py")


# User information

st.info(
    f" User: {username} | 👤 Role: {role} | 🏢 Branch: {branch_name}"
)


# Branches Details Loaded

cur.execute("""
SELECT branch_id, branch_name
FROM branches
ORDER BY branch_name
""")

branch_rows = cur.fetchall()

branch_dict = {"All": None}

for bid, bname in branch_rows:
    branch_dict[bname] = bid


# Filter options 

st.subheader("Filter Controls")

col1, col2, col3, col4 = st.columns(4)


# Branch wise filter

with col1:

    if role == "Super Admin":

        branch_filter = st.selectbox(
            "Branch Name",
            list(branch_dict.keys())
        )

    else:

        branch_filter = branch_name

        st.text_input(
            "Branch Name",
            value=branch_name,
            disabled=True
        )


# Product wise filter

with col2:

    product_filter = st.selectbox(
        "Product Name",
        ["All", "DS", "BA", "DA", "FSD", "ML", "AI", "BI", "SQL"]
    )


# Date wise filters

with col3:
    start_date = st.date_input("Start Date")

with col4:
    end_date = st.date_input("End Date")


# Financial Summary 

query = """
SELECT
    gross_sales,
    received_amount
FROM customer_sales
WHERE 1=1
"""

params = []


# Role wise details

if role != "Super Admin":

    query += " AND branch_id = %s"
    params.append(user_branch_id)

elif branch_filter != "All":

    query += " AND branch_id = %s"
    params.append(branch_dict[branch_filter])


# Product wise filter

if product_filter != "All":

    query += " AND product_name = %s"
    params.append(product_filter)


# Date wise filter

if start_date and end_date:

    query += " AND date BETWEEN %s AND %s"
    params.extend([start_date, end_date])

# Execute
cur.execute(query, params)
rows = cur.fetchall()


# Calculations

total_revenue = 0
total_received = 0

for gross_sales, received_amount in rows:

    total_revenue += gross_sales or 0
    total_received += received_amount or 0

total_pending = total_revenue - total_received


# Summary Column

st.subheader("💰 Financial Summary")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Total Revenue",
        f"₹ {total_revenue:,.2f}"
    )

with c2:
    st.metric(
        "Total Received",
        f"₹ {total_received:,.2f}"
    )

with c3:
    st.metric(
        "Total Pending",
        f"₹ {total_pending:,.2f}"
    )


# Detailed Record Column

st.subheader("📄 Detailed Records")

data_query = """
SELECT
    cs.sale_id,
    cs.branch_id,
    b.branch_name,
    cs.date,
    cs.name,
    cs.mobile_number,
    cs.product_name,
    cs.gross_sales,
    cs.received_amount,
    cs.pending_amount,
    cs.status
FROM customer_sales cs
JOIN branches b
    ON cs.branch_id = b.branch_id
WHERE 1=1
"""

params = []


# Role wise filters

if role != "Super Admin":

    data_query += " AND cs.branch_id = %s"
    params.append(user_branch_id)

elif branch_filter != "All":

    data_query += " AND cs.branch_id = %s"
    params.append(branch_dict[branch_filter])


# Product Wise filters

if product_filter != "All":

    data_query += " AND cs.product_name = %s"
    params.append(product_filter)


# Date wise filters

if start_date and end_date:

    data_query += " AND cs.date BETWEEN %s AND %s"
    params.extend([start_date, end_date])

data_query += """
ORDER BY cs.sale_id DESC
"""

# Execute
cur.execute(data_query, params)

data = cur.fetchall()

columns = [desc[0] for desc in cur.description]

df = pd.DataFrame(
    data,
    columns=columns
)

# Display
st.dataframe(
    df,
    use_container_width=True
)


# Record count information

st.info(
    f"Total Records Found: {len(df)}"
)


# Close connections

cur.close()
conn.close()