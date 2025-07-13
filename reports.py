import pandas as pd
import streamlit as st
from datetime import datetime
from openpyxl.workbook import Workbook

def generate_report(purchases):
    df = pd.DataFrame(purchases)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["month"] = df["timestamp"].dt.to_period("M")

    st.write("### 📋 Recent Purchases")
    st.dataframe(df.sort_values(by="timestamp", ascending=False).head(10))

    st.write("### 🔍 Advanced Filters")
    with st.expander("Click to Filter Data"):
        category_filter = st.multiselect("Filter by Category", options=df["category"].unique())
        mood_filter = st.multiselect("Filter by Mood", options=df["mood"].unique())
        need_want_filter = st.multiselect("Need or Want", options=df["need_or_want"].unique())
        date_range = st.date_input("Date Range", [])
        note_keyword = st.text_input("Search in Notes")

    filtered_df = df.copy()
    if category_filter:
        filtered_df = filtered_df[filtered_df["category"].isin(category_filter)]
    if mood_filter:
        filtered_df = filtered_df[filtered_df["mood"].isin(mood_filter)]
    if need_want_filter:
        filtered_df = filtered_df[filtered_df["need_or_want"].isin(need_want_filter)]
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df["timestamp"].dt.date >= date_range[0]) &
            (filtered_df["timestamp"].dt.date <= date_range[1])
        ]
    if note_keyword:
        filtered_df = filtered_df[filtered_df["notes"].str.contains(note_keyword, case=False, na=False)]

    st.write("### 📊 Filtered Results")
    st.dataframe(filtered_df)

    # Export Option
    if not filtered_df.empty:
        excel_file = "filtered_report.xlsx"
        filtered_df.to_excel(excel_file, index=False)
        with open(excel_file, "rb") as f:
            st.download_button("📥 Export to Excel", f, file_name=excel_file)

    st.write("### 📅 Total Spend by Month")
    spend_by_month = filtered_df.groupby(filtered_df["timestamp"].dt.to_period("M"))["price"].sum()
    st.bar_chart(spend_by_month)

    st.write("### 📂 Category-wise Spending")
    category_spending = filtered_df.groupby("category")["price"].sum().sort_values(ascending=False)
    st.bar_chart(category_spending)

    st.write("### 😀 Mood-wise Spending")
    mood_spend = filtered_df.groupby("mood")["price"].sum()
    st.bar_chart(mood_spend)

    st.write("### ⚖️ Needs vs Wants")
    need_want = filtered_df["need_or_want"].value_counts()
    st.bar_chart(need_want)
