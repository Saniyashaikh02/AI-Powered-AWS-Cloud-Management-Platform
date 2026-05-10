import streamlit as st
import pandas as pd
import requests

from agent import run_agent

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AWS AI Dashboard", layout="wide")

# ===== SESSION =====
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ===== LOGIN =====
def login_page():
    st.title("🔐 Login to AWS AI Dashboard")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")


# ===== LOGOUT =====
def logout():
    st.session_state.logged_in = False
    st.rerun()


# ===== FETCH DATA FROM API =====
def get_data(endpoint):
    try:
        return requests.get(f"{API_URL}/{endpoint}").json()
    except:
        return []


# ===== MAIN APP =====
def main_app():

    st.sidebar.title("⚙️ AWS AI Dashboard")

    if st.sidebar.button("🚪 Logout"):
        logout()

    menu = st.sidebar.radio(
        "Navigate",
        ["Dashboard", "AI Assistant", "Raw Data"]
    )

    # ===== FETCH FROM BACKEND =====
    instances = get_data("instances")
    stopped = get_data("instances/stopped")
    running = get_data("instances/running")
    buckets = get_data("s3")

    # ===== DASHBOARD =====
    if menu == "Dashboard":

        st.title("📊 AWS Overview")

        col1, col2, col3, col4 = st.columns(4)

        if col1.button(f"📦 Total\n{len(instances)}"):
            st.session_state["view"] = "all"

        if col2.button(f"🟢 Running\n{len(running)}"):
            st.session_state["view"] = "running"

        if col3.button(f"🔴 Stopped\n{len(stopped)}"):
            st.session_state["view"] = "stopped"

        if col4.button(f"🪣 Buckets\n{len(buckets)}"):
            st.session_state["view"] = "s3"

        st.divider()

        if "view" in st.session_state:

            if st.session_state["view"] == "all":
                st.subheader("📦 All EC2 Instances")
                st.dataframe(pd.DataFrame(instances))

            elif st.session_state["view"] == "running":
                st.subheader("🟢 Running Instances")
                st.dataframe(pd.DataFrame(running))

            elif st.session_state["view"] == "stopped":
                st.subheader("🔴 Stopped Instances")
                st.dataframe(pd.DataFrame(stopped))

            elif st.session_state["view"] == "s3":
                st.subheader("🪣 S3 Buckets")
                st.write(buckets)

        st.divider()

        # ===== REGION BREAKDOWN =====
        st.subheader("🌍 Region-wise EC2 Distribution")

        region_counts = {}
        for inst in instances:
            region = inst["Region"]
            region_counts[region] = region_counts.get(region, 0) + 1

        for region, count in region_counts.items():
            st.write(f"• {region} → {count} instance(s)")

        st.divider()

        # ===== ALERTS =====
        st.subheader("⚠️ Alerts")

        if stopped:
            st.warning(f"{len(stopped)} stopped instance(s) found → possible cost waste")
        else:
            st.success("No unused resources detected")

    # ===== AI ASSISTANT =====
    elif menu == "AI Assistant":

        st.title("🤖 AWS AI Assistant")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        user_input = st.text_input("Ask something about your AWS:")

        if user_input:
            response = run_agent(user_input)

            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("AI", response))

        for sender, msg in st.session_state.chat_history:
            if sender == "You":
                st.markdown(f"**🧑 You:** {msg}")
            else:
                st.markdown(f"**🤖 AI:** {msg}")

    # ===== RAW DATA =====
    elif menu == "Raw Data":

        st.title("📂 AWS Data Explorer")

        with st.expander("EC2 Instances"):
            st.dataframe(pd.DataFrame(instances))

        with st.expander("Running Instances"):
            st.dataframe(pd.DataFrame(running))

        with st.expander("Stopped Instances"):
            st.dataframe(pd.DataFrame(stopped))

        with st.expander("S3 Buckets"):
            st.write(buckets)


# ===== ROUTING =====
if not st.session_state.logged_in:
    login_page()
else:
    main_app()