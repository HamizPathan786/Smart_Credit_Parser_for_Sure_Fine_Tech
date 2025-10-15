# 💳 SmartCreditParser  
**AI-Powered Credit Card Statement Analyzer**

SmartCreditParser is an intelligent **PDF statement parsing system** built with **Python and Streamlit**, designed to automatically detect and extract key financial details from **credit card statements** across multiple banks — including **HDFC, SBI, ICICI, Axis, and Citi**.

This system performs **bank detection, data extraction, transaction parsing**, and **JSON report generation**, helping automate financial data digitization and analysis with precision.

---
![image alt](https://github.com/HamizPathan786/Smart_Credit_Parser_for_Sure_Fine_Tech/blob/c2d96bac29a5b16177095386e4fcfcc08b1efc34/Screenshot%202025-10-15%20225824.png)
## 🚀 Features

- 🔍 **Automatic Bank Detection** — Identifies the issuing bank using keyword scoring and parsing logic.  
- 🧾 **PDF Parsing Engine** — Extracts and cleans raw text from credit card statements.  
- 💰 **Financial Insights** — Extracts fields such as:
  - Bank Name  
  - Cardholder Name  
  - Last 4 Digits  
  - Total Due  
  - Total Spent  
  - Due Date  
  - Full Transaction History  
- ⚡ **Multi-Bank Support** — Prebuilt parsers for:
  - HDFC Bank  
  - SBI Card  
  - ICICI Bank  
  - Axis Bank  
  - Citi Bank  
- 📊 **Visualization Dashboard** — Built with **Streamlit**, includes spending graphs and JSON data preview.  
- 🧠 **Confidence Scoring** — Measures extraction accuracy based on matched data points.  
- 📦 **JSON Output** — Automatically saves structured parsed data for further analytics or integration.

---

## 🏗️ Tech Stack

| Layer | Technology Used |
|-------|------------------|
| **Frontend (UI)** | Streamlit |
| **Backend Logic** | Python |
| **Parsing & Extraction** | Regex, PDFMiner |
| **Data Visualization** | Matplotlib, Streamlit Components |
| **Output Format** | JSON |

---

## 📁 Folder Structure

SmartCreditParser/
│
├── app.py # Streamlit web app entry
├── src/
│ ├── main.py # Core execution & parser manager
│ ├── utils/
│ │ └── pdf_utils.py # PDF text extraction helper
│ ├── parsers/
│ │ ├── base_parser.py # Abstract base parser class
│ │ ├── hdfc_parser.py
│ │ ├── sbi_parser.py
│ │ ├── icici_parser.py
│ │ ├── axis_parser.py
│ │ ├── citi_parser.py
│ │ └── init.py
│ └── ...
│
├── samples/ # Sample credit card statements
├── output/ # JSON outputs
├── requirements.txt
└── README.md


🧩 Future Enhancements

🤖 Integrate OCR (Optical Character Recognition) for scanned statement images.

📈 Add category-based spending analytics.

☁️ Enable cloud storage & dashboard integration for financial tracking.

🔐 Incorporate data validation & privacy encryption layers.


🧑‍💻 Developed By

👤 Hamiz Abdul Rehman Pathan
🎓 B.Tech in Artificial Intelligence and Data Science
📍 Shah & Anchor Kuttchi Engineering College
💼 Skilled in Python, Flask, React Native, C++, DSA, and AI Systems
📫 Email: hamizp123@gmail.com

🌟 Acknowledgement

This project was developed as part of an initiative to automate financial data extraction and AI-powered document intelligence, focusing on accuracy, scalability, and usability in fintech applications.






