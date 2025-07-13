
# 🧠💸 SpendMind - Your AI Spending Advisor

SpendMind is a smart, personal finance assistant powered by AI. Track your expenses, get personalized buying advice, set budgets, upload receipts, and more — all in a clean, Streamlit-powered web interface.

---

## ✨ Features

### 🔍 Smart Expense Logging
- Log purchases with category, mood, and need/want flags
- Tag purchases with notes (e.g., #food, #gadget)
- Recurring expense and price-watch support

### 📊 Monthly Reports
- Visual analytics (bar charts, filters, summaries)
- Category-wise breakdown
- Mood-wise spending behavior
- Export filtered data to Excel

### 🧠 Ask the AI
- Describe what you want to buy and get smart advice
- AI uses past spending patterns + mood to help you decide

### 🔔 Warnings & Reminders
- Spending limit alerts (per category)
- Upcoming recurring bill reminders
- Price drop alerts for tracked items

### 🧾 Receipt OCR
- Upload a receipt image
- Automatically extract text using Tesseract OCR

### 📅 Calendar View
- Timeline of spending activity per day

---

## 📦 Technologies Used

- [Streamlit](https://streamlit.io/)
- [LangChain + Gemini](https://ai.google.dev/)
- [SQLite](https://www.sqlite.org/)
- [Pandas](https://pandas.pydata.org/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- Python 3.8+

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/deepalisachan04/spendmind.git
cd spendmind
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR

#### On Ubuntu/Debian
```bash
sudo apt update && sudo apt install tesseract-ocr
```

#### On macOS
```bash
brew install tesseract
```

#### On Windows
- Download from: https://github.com/tesseract-ocr/tesseract

---

### 4. Set Up API Key

1. Copy the `.env.example` file to `.env`
2. Add your Google Gemini API Key:

```
GOOGLE_API_KEY=your_api_key_here
```

---

### 5. Run the App

```bash
streamlit run app.py
```

---


## 🛡 Security Note

- Do NOT commit your `.env` file or API keys.
- Use `.gitignore` to exclude `*.env` and `*.db`

---

## 🙋‍♀️ Author

Made with 💙 by [Deepali Sachan](https://github.com/deepalisachan04)

---

## 📃 License

MIT License
