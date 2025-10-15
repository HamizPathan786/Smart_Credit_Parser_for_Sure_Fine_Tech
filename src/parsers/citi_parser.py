import re
from src.parsers.base_parser import BaseParser

class CitiParser(BaseParser):
    def __init__(self, pdf_path=None):
        super().__init__(pdf_path)
        self.bank_name = "Citi Bank"

    def parse(self):
        text = self.text
        data = {
            "bank": self.bank_name,
            "cardholder_name": None,
            "card_last_4": None,
            "total_due": None,
            "due_date": None,
            "total_spent": None,
            "transactions": []
        }

        # --- Extract main fields ---
        # Cardholder name
        name_match = re.search(r"Cardholder[:\-]?\s*([A-Za-z\s\.]+)", text)
        if name_match:
            data["cardholder_name"] = name_match.group(1).strip()

        # Card number (last 4 digits)
        card_match = re.search(r"Card\s*(?:Ending|Number)[:\-]?\s*(?:\*{4}\s*){3}(\d{4})", text)
        if card_match:
            data["card_last_4"] = card_match.group(1)

        # Total due
        total_due_match = re.search(r"Total\s+Due[:\-]?\s*[₹Rs]*\s*([\d,]+\.\d{2})", text)
        if total_due_match:
            data["total_due"] = float(total_due_match.group(1).replace(",", ""))

        # Due date
        due_date_match = re.search(r"Due\s*Date[:\-]?\s*(\d{1,2}-[A-Za-z]{3}-\d{4})", text)
        if due_date_match:
            data["due_date"] = due_date_match.group(1)

        # Total spent
        spent_match = re.search(r"Total\s+Spent[:\-]?\s*[₹Rs]*\s*([\d,]+\.\d{2})", text)
        if spent_match:
            data["total_spent"] = float(spent_match.group(1).replace(",", ""))

        # --- Transactions ---
        txn_pattern = re.findall(
            r"(\d{2}-[A-Za-z]{3}-\d{4})\s+(.+?)\s+([\d,]+\.\d{2})",
            text
        )
        for t in txn_pattern:
            data["transactions"].append({
                "date": t[0],
                "description": t[1].strip(),
                "amount": float(t[2].replace(",", ""))
            })

        # --- Confidence ---
        found_values = [v for k, v in data.items() if v and k != "transactions"]
        data["_confidence"] = round(len(found_values) / (len(data) - 1), 2)

        return data
