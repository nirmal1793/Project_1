import streamlit as st
import psycopg2

def authenticate(username, password):

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="Sales_Management-Project1",
        user="postgres",
        password="1234"
    )

    cur = conn.cursor()

    cur.execute("""
        SELECT
            user_id,
            username,
            branch_id,
            role
        FROM users
        WHERE username = %s
        AND password = %s
    """, (username, password))

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user

# Session initiation


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# Login process

st.title("Sales Management Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    user = authenticate(username, password)

    if user:

        st.session_state.logged_in = True
        st.session_state.user_id = user[0]
        st.session_state.username = user[1]
        st.session_state.branch_id = user[2]
        st.session_state.role = user[3]

        st.success("Login Successful")

        st.switch_page("pages/Management.py")

    else:
        st.error("Invalid Username or Password")