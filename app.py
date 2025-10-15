
import streamlit as st
import json
import os
import pandas as pd
from src.main import parse_file

st.set_page_config(page_title="Smart Credit Parser", layout="wide")
st.title("💳 Smart Credit Card Statement Parser")

uploaded_file = st.file_uploader("Upload your credit card statement (PDF)", type=["pdf"])

if uploaded_file:
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info(f"⏳ Parsing `{uploaded_file.name}`...")

    output_path = parse_file(temp_path, output_dir="streamlit_output")

    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    bank_name = data.get("bank", "Unknown Bank")
    st.success(f"✅ Successfully parsed statement for **{bank_name}**")

    st.subheader("📄 Statement Summary")
    summary_data = {
        "Bank": [data.get("bank", "—")],
        "Cardholder Name": [data.get("cardholder_name") or "—"],
        "Card Last 4 Digits": [data.get("card_last_4") or "—"],
        "Total Due": [data.get("total_due") or "—"],
        "Due Date": [data.get("due_date") or "—"],
        "Total Spent": [data.get("total_spent") or "—"],
        "Confidence": [f"{round(data.get('_confidence', 0)*100, 2)}%"],
    }
    st.table(pd.DataFrame(summary_data))

    transactions = data.get("transactions", [])
    if transactions:
        st.subheader("💰 Transaction Details")

        df = pd.DataFrame(transactions)
        df.columns = ["Date", "Description", "Amount (₹)"]
        df["Amount (₹)"] = df["Amount (₹)"].astype(float)

        st.dataframe(df, use_container_width=True)

        st.subheader("📊 Spending Overview")
        import matplotlib.pyplot as plt

        plt.figure(figsize=(10, 4))
        plt.bar(df["Date"], df["Amount (₹)"], color="#4f81bd")
        plt.xticks(rotation=45)
        plt.ylabel("Amount (₹)")
        plt.title(f"Spending Pattern - {bank_name}")
        plt.tight_layout()
        st.pyplot(plt)
    else:
        st.warning("⚠️ No transactions found in this statement.")

    os.remove(temp_path)

