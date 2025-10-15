import re
from src.parsers.base_parser import BaseParser

class AxisParser(BaseParser):
    def __init__(self, pdf_path=None):
        super().__init__(pdf_path)
        self.bank_name = "Axis Bank"

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

        # --- Extract key fields ---
        # Match "Cardholder:" instead of "Cardholder Name:"
        name_match = re.search(r"Cardholder:\s*(.+)", text)
        if name_match:
            data["cardholder_name"] = name_match.group(1).strip()

        # Match "Card Ending: **** **** **** 4567"
        card_match = re.search(r"Card Ending:\s*\*+\s*\*+\s*\*+\s*(\d{4})", text)
        if card_match:
            data["card_last_4"] = card_match.group(1)

        # Match total due and total spent (₹ or n prefixed)
        total_due_match = re.search(r"Total Due:\s*[₹nRs]*\s*([\d,]+\.\d{2})", text)
        if total_due_match:
            data["total_due"] = float(total_due_match.group(1).replace(",", ""))

        spent_match = re.search(r"Total Spent:\s*[₹nRs]*\s*([\d,]+\.\d{2})", text)
        if spent_match:
            data["total_spent"] = float(spent_match.group(1).replace(",", ""))

        # Match due date like 10-Oct-2025
        due_date_match = re.search(r"Due Date:\s*(\d{1,2}-[A-Za-z]{3}-\d{4})", text)
        if due_date_match:
            data["due_date"] = due_date_match.group(1)

        # --- Extract transactions ---
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

        # --- Confidence score ---
        found_values = [v for k, v in data.items() if v and k != "transactions"]
        data["_confidence"] = round(len(found_values) / (len(data) - 1), 2)

        return data
