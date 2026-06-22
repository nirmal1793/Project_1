import streamlit as st
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


# Checking for login 

if not st.session_state.get("logged_in"):
    st.switch_page("login.py")

username = st.session_state.get("username")
role = st.session_state.get("role")
user_branch_id = st.session_state.get("branch_id")


# Get Branch Name details

if role != "Super Admin":
    cur.execute(
        "SELECT branch_name FROM branches WHERE branch_id=%s",
        (user_branch_id,)
    )
    row = cur.fetchone()
    branch_name = row[0] if row else "Unknown"
else:
    branch_name = "All Branches"


# Title & Logout Column

col1, col2, col3 = st.columns([8, 2, 2])

with col1:
    st.title("Enrolment Form")

with col2:
    if st.button("Back"):
        st.switch_page("pages/Management.py")

with col3:
    if st.button("Logout"):
        st.session_state.clear()
        st.switch_page("login.py")

st.info(
    f"User: {username} | 👤 Role: {role} | 🏢 Branch: {branch_name}"
)


# Tabs for the enrolments

tab1, tab2 = st.tabs(["Course Entries", "Payment Updates"])


# Course details submission

with tab1:

    st.subheader("Student Sales Entry Form")

    with st.form("sales_form"):

        # Branch Selection
        if role == "Super Admin":

            cur.execute("""
                SELECT branch_id, branch_name
                FROM branches
                ORDER BY branch_name
            """)

            branches = cur.fetchall()

            branch_options = {
                bname: bid
                for bid, bname in branches
            }

            selected_branch = st.selectbox(
                "Branch",
                list(branch_options.keys())
            )

            branch_id = branch_options[selected_branch]

        else:

            st.text_input(
                "Branch",
                value=branch_name,
                disabled=True
            )

            branch_id = user_branch_id

        date = st.date_input("Date")
        name = st.text_input("Name")
        mobile_number = st.text_input("Mobile Number")

        product_data = {
            "DS": 40000,
            "BA": 30000,
            "DA": 35000,
            "FSD": 45000,
            "ML": 42000,
            "AI": 48000,
            "BI": 28000,
            "SQL": 25000
        }

        product_name = st.selectbox(
            "Product Name",
            list(product_data.keys())
        )

        gross_sales = st.number_input(
            "Gross Sale",
            value=float(product_data[product_name]),
            disabled=True
        )

        received_amount = st.number_input(
            "Received Amount",
            min_value=0.0
        )

        status = st.selectbox(
            "Status",
            ["Open", "Close"]
        )

        submit = st.form_submit_button("Submit Enrollment")

        if submit:

            cur.execute("""
                INSERT INTO customer_sales
                (
                    branch_id,
                    date,
                    name,
                    mobile_number,
                    product_name,
                    gross_sales,
                    received_amount,
                    status
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                RETURNING sale_id
            """,
            (
                branch_id,
                date,
                name,
                mobile_number,
                product_name,
                gross_sales,
                received_amount,
                status
            ))

            sale_id = cur.fetchone()[0]

            conn.commit()

            st.success(
                f"Enrollment completed successfully. Sale ID: {sale_id}"
            )


# Payment Update Tab

with tab2:

    st.subheader("Payment Updates")

    with st.form("payment_form"):

        sale_id = st.text_input("Sale ID")

        payment_date = st.date_input("Payment Date")

        amount_paid = st.number_input(
            "Amount Paid",
            min_value=0.0
        )

        payment_method = st.selectbox(
            "Payment Method",
            ["Cash", "Card", "UPI"]
        )

        submit_payment = st.form_submit_button(
            "Update Payment"
        )

        if submit_payment:

            cur.execute("""
                INSERT INTO payment_splits
                (
                    sale_id,
                    payment_date,
                    amount_paid,
                    payment_method
                )
                VALUES (%s,%s,%s,%s)
            """,
            (
                sale_id,
                payment_date,
                amount_paid,
                payment_method
            ))

            conn.commit()

            st.success("Payment updated successfully")