import streamlit as st
from aws_utils import list_ec2_instances, find_stopped_instances
from ai_utils import generate_ai_response

st.set_page_config(page_title="AWS AI Assistant", layout="centered")

# Header
st.title("🤖 AWS AI Cloud Assistant")
st.markdown("Analyze your AWS infrastructure using AI")

# Divider
st.divider()

# Input box
user_input = st.text_input("💬 Ask your question:")

if user_input:
    with st.spinner("🔍 Analyzing AWS resources..."):

        instances = list_ec2_instances()
        stopped = find_stopped_instances()

        response = generate_ai_response(user_input, instances, stopped)

        # Response box
        st.subheader("🤖 AI Response")
        st.success(response)

        st.divider()

        # Extra info (PRO FEATURE 🔥)
        st.subheader("📊 AWS Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Instances", len(instances))

        with col2:
            st.metric("Stopped Instances", len(stopped))