import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from data_store import load_purchases

load_dotenv()

llm = ChatGoogleGenerativeAI(
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    model="models/gemini-1.5-pro-latest",  # ✅ Correct full model name
    temperature=0.6
)

def ask_advisor(user_input):
    purchases = load_purchases()
    recent_spending = sum(p["price"] for p in purchases[-5:])
    need_want_ratio = calculate_need_want_ratio(purchases)

    context = f"Recent spending: ₹{recent_spending:.2f}. Need/Want ratio: {need_want_ratio:.2f}."
    full_prompt = f"{context}\nUser is considering: {user_input}\nGive clear, practical advice on whether they should buy it or wait."

    response = llm.invoke([HumanMessage(content=full_prompt)])
    return response.content

def calculate_need_want_ratio(purchases):
    if not purchases:
        return 1.0
    needs = sum(1 for p in purchases if p["need_or_want"] == "Need")
    wants = sum(1 for p in purchases if p["need_or_want"] == "Want")
    return needs / wants if wants else needs
