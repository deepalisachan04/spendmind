import streamlit as st
from advisor import ask_advisor
from data_store import save_purchase, load_purchases, init_db
from reports import generate_report
from limits import check_spending_limits, get_upcoming_bills, get_price_watch_alerts
from PIL import Image
import pytesseract
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="SpendMind - Your AI Spending Advisor", layout="wide")
st.title("🧠💸 SpendMind")

# Initialize DB
init_db()

# Display alerts
for warn in check_spending_limits():
    st.warning(warn)
for bill in get_upcoming_bills():
    st.info(bill)
for alert in get_price_watch_alerts():
    st.success(alert)

menu = st.sidebar.radio("Choose a section", ["Log Purchase", "Ask Advisor", "Monthly Report", "Calendar View", "Upload Receipt"])

if menu == "Log Purchase":
    st.subheader("📝 Log a Purchase")
    item = st.text_input("Item Name")
    price = st.number_input("Price", min_value=0.0, format="%.2f")
    category = st.text_input("Category")
    mood = st.selectbox("Your Mood", ["😊 Happy", "😟 Stressed", "😐 Neutral", "😔 Sad", "😠 Angry"])
    need_or_want = st.radio("Is this a...", ["Need", "Want"])
    notes = st.text_area("Notes (optional, tags like #food #emotional)")
    is_recurring = st.checkbox("Is this a recurring expense?")
    track_price = st.checkbox("Track this item's price?")
    price_watch = st.number_input("Target price to watch (optional)", min_value=0.0, format="%.2f") if track_price else None

    if st.button("💾 Save Purchase"):
        if item and price > 0:
            save_purchase(item, price, category, mood, need_or_want, notes, int(is_recurring), price_watch)
            st.success("Purchase saved successfully!")
        else:
            st.warning("Item name and price must be provided.")

elif menu == "Ask Advisor":
    st.subheader("🤖 Should I Buy This?")
    user_input = st.text_area("Describe what you want to buy and why")
    if st.button("🧠 Ask SpendMind"):
        if user_input:
            with st.spinner("Thinking..."):
                reply = ask_advisor(user_input)
            st.markdown("### SpendMind says:")
            st.success(reply)
        else:
            st.warning("Please describe the item and your reason for buying it.")

elif menu == "Monthly Report":
    st.subheader("📊 Monthly Spending Report")
    purchases = load_purchases()
    if purchases:
        generate_report(purchases)
    else:
        st.info("No purchases to show yet.")

elif menu == "Calendar View":
    st.subheader("📅 Purchase Calendar")
    df = pd.DataFrame(load_purchases())
    if df.empty:
        st.info("No data to show.")
    else:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["date"] = df["timestamp"].dt.date
        calendar_df = df.groupby("date")["price"].sum().reset_index()
        st.line_chart(calendar_df.set_index("date"))

elif menu == "Upload Receipt":
    st.subheader("🧾 Upload Receipt Image")
    uploaded = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    if uploaded:
        img = Image.open(uploaded)
        st.image(img, caption="Uploaded Receipt", use_column_width=True)
        with st.spinner("Reading text..."):
            text = pytesseract.image_to_string(img)
        st.text_area("🧾 Extracted Text", value=text, height=200)
