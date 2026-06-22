import streamlit as st
import pandas as pd
import psycopg2


# DB Connections

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="Sales_Management-Project1",
    user="postgres",
    password="1234"
)

cur = conn.cursor()


# Title & Logout Column


col1, col2, col3 = st.columns([8, 2, 2])

with col1:
    st.title("📘 Advanced SQL Queries")

with col2:
    if st.button("Back"):
        st.switch_page("pages/Management.py")

with col3:
    if st.button("Logout"):
        st.session_state.clear()
        st.success("Logged out")
        st.switch_page("login.py")


# Selection List

option = st.selectbox(
    "Choose an SQL query to run",
    [
        "1. Retrieve all records from the customer_sales table",
        "2. Retrieve all records from the branches table",
        "3. Retrieve all records from the payment_splits table",
        "4. Display all sales with status = 'Open'",
        "5. Retrieve all sales belonging to the Chennai branch",
        "6. Calculate total gross sales across all branches",
        "7. Calculate the total received amount across all sales",
        "8. Calculate the total pending amount across all sales",
        "9. Count the total number of sales per branch",
        "10. Retrieve sales details along with the branch name",
        "11. Retrieve sales with payment details",
        "12. Show branch-wise total gross sales",
        "13. Display sales along with payment method used",
        "14. Find sales where pending amount > 5000",
        "15. Retrieve top 3 highest gross sales",
        "16. Find branch with highest total gross sales"
    ]
)


# SQL Query Mapping

queries = {
    "1. Retrieve all records from the customer_sales table": "SELECT * FROM customer_sales",

    "2. Retrieve all records from the branches table": "SELECT * FROM branches",

    "3. Retrieve all records from the payment_splits table": "SELECT * FROM payment_splits",

    "4. Display all sales with status = 'Open'": "SELECT * FROM customer_sales WHERE status = 'Open'",

    "5. Retrieve all sales belonging to the Chennai branch": "SELECT * FROM customer_sales WHERE branch_id= 1",

    "6. Calculate total gross sales across all branches":
        "SELECT SUM(gross_sales) AS total_gross_sales FROM customer_sales",

    "7. Calculate the total received amount across all sales":
        "SELECT SUM(received_amount) AS total_received_amount FROM customer_sales",

    "8. Calculate the total pending amount across all sales":
        "SELECT SUM(pending_amount) AS total_pending_amount FROM customer_sales",

    "9. Count the total number of sales per branch":
        "select b.branch_name, count(c.name) as total_sales from customer_sales as c join branches b on b.branch_id = c.branch_id group by branch_name order by count(c.name) Desc",

    "10. Retrieve sales details along with the branch name":
        "SELECT cs.*, b.branch_name FROM customer_sales cs JOIN branches b ON cs.branch_id = b.branch_id",

    "11. Retrieve sales with payment details":
        "SELECT cs.*, ps.amount_paid, ps.payment_method FROM customer_sales cs JOIN payment_splits ps ON cs.sale_id = ps.sale_id",

    "12. Show branch-wise total gross sales":
        "select b.branch_name, sum(c.gross_sales) as Total_Gross_Sale_amount from customer_sales as c join branches as b on b.branch_id = c.branch_id group by b.branch_name order by sum(c.gross_sales) desc",

    "13. Display sales along with payment method used":
        "SELECT cs.sale_id, cs.name, ps.payment_method, ps.amount_paid FROM customer_sales cs JOIN payment_splits ps ON cs.sale_id = ps.sale_id",

    "14. Find sales where pending amount > 5000":
        "SELECT * FROM customer_sales WHERE pending_amount > 5000",

    "15. Retrieve top 3 highest gross sales":
        "SELECT * FROM customer_sales ORDER BY gross_sales DESC LIMIT 3",

    "16. Find branch with highest total gross sales":
        "SELECT branch_id, SUM(gross_sales) AS total_sales FROM customer_sales GROUP BY branch_id ORDER BY total_sales DESC LIMIT 1"
}


# Run Query Automatically

sql_query = queries[option]

st.subheader("🧾 SQL Query")
st.code(sql_query, language="sql")

try:
    cur.execute(sql_query)

    # If query returns data
    if cur.description:
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

        df = pd.DataFrame(rows, columns=columns)

        st.subheader("📊 Result")
        st.dataframe(df, use_container_width=True)

    else:
        conn.commit()
        st.success("Query executed successfully!")

except Exception as e:
    st.error(f"Error: {e}")