# limits.py
from datetime import datetime
from collections import defaultdict
import streamlit as st
from data_store import load_purchases, get_monthly_limits

def check_spending_limits():
    limits = get_monthly_limits()
    purchases = load_purchases()
    warnings = []

    # Filter by current month
    current_month = datetime.now().strftime("%Y-%m")
    monthly_spend = defaultdict(float)
    for p in purchases:
        ts_month = p["timestamp"][:7]
        if ts_month == current_month:
            monthly_spend[p["category"]] += p["price"]

    for category, spent in monthly_spend.items():
        if category in limits and spent > limits[category]:
            warnings.append(f"⚠ Over budget for {category}: ₹{spent:.2f} / ₹{limits[category]:.2f}")

    return warnings

def get_upcoming_bills():
    purchases = load_purchases()
    reminders = []
    today = datetime.now().date()

    for p in purchases:
        if p["is_recurring"]:
            ts = datetime.fromisoformat(p["timestamp"]).date()
            days_since = (today - ts).days
            if days_since >= 25:  # Approx 1-month due logic
                reminders.append(f"💡 You have a recurring bill for **{p['item']} (₹{p['price']})** from {p['category']} due this week.")
    return reminders

def get_price_watch_alerts():
    purchases = load_purchases()
    alerts = []
    for p in purchases:
        if p["price_watch"] and p["price"] > p["price_watch"]:
            alerts.append(f"📉 {p['item']} may have dropped below ₹{p['price_watch']} — current logged: ₹{p['price']}")
    return alerts
