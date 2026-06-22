import streamlit as st
import psycopg2
import datetime

# CHecking for Login session

if not st.session_state.get("logged_in"):
    st.switch_page("login.py")

# DB Connection

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="Sales_Management-Project1",
    user="postgres",
    password="1234"
)

cur = conn.cursor()


# Session process

username = st.session_state.get("username")
role = st.session_state.get("role")
branch_id = st.session_state.get("branch_id")


# Get Branch Name

if role == "Super Admin":
    branch_name = "All Branches"
else:

    cur.execute("""
        SELECT branch_name
        FROM branches
        WHERE branch_id = %s
    """, (branch_id,))

    row = cur.fetchone()

    branch_name = row[0] if row else "Unknown"


# Title & Logout column

col1, col2 = st.columns([8, 1])

with col1:
    st.title("Sales Management System")

with col2:
    if st.button("Logout"):
        st.session_state.clear()
        st.switch_page("login.py")


# User information

st.info(
    f" User: {username} | 👤 Role: {role} | 🏢 Branch: {branch_name}"
)

# Date & Time (IST)
st.caption(f"📅 {datetime.datetime.now().strftime('%A, %B %d, %Y — %I:%M %p')}")

# Captions
if role == "Super Admin":
    st.caption("Full control across all branches — manage users, sales, and reports.")
else:
    st.caption(f"Welcome back! Here's what's happening at {branch_name}.")

# Menu Options

col1, col2, col3 = st.columns(3)

with col1:
    if st.button(
        "Students Enrollment",
        use_container_width=True
    ):
        st.switch_page("pages/DataEntry.py")

with col2:
    if st.button(
        "Dashboard & Reports",
        use_container_width=True
    ):
        st.switch_page("pages/Dash.py")

with col3:
    if st.button(
        "Advanced SQL Queries",
        use_container_width=True
    ):
        st.switch_page("pages/AdvancedSQL.py")

# Bottom Details

st.divider()
st.caption("Sales Management System v1.0 | Developed by Nirmal | © 2026")

# Close connection

cur.close()
conn.close()