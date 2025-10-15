# src/main.py
import sys
import os
import json
from src.utils.pdf_utils import extract_text_from_pdf
from src.parsers import PARSERS
from src.parsers import HDFCParser, SBIParser, ICICIParser, AxisParser, CitiParser
# ✅ Correct (matches your actual parser class names)
from src.parsers.axis_parser import AxisParser
from src.parsers.sbi_parser import SBIParser
from src.parsers.hdfc_parser import HDFCParser
from src.parsers.citi_parser import CitiParser
from src.parsers.icici_parser import ICICIParser



# -----------------------------
# Parser map
# -----------------------------
parsers = {
    "hdfc": HDFCParser,
    "sbi": SBIParser,
    "icici": ICICIParser,
    "axis": AxisParser,
    "citi": CitiParser
}


# -----------------------------
# Smart Bank detection logic
# -----------------------------
def detect_bank(text: str, pdf_path: str = ""):
    """Detect bank from text content and filename fallback."""
    t = text.lower()

    # weighted keyword scoring
    scores = {
        "hdfc": 0,
        "sbi": 0,
        "icici": 0,
        "axis": 0,
        "citi": 0
    }

    # Primary text-based detection
    if "hdfc bank credit card" in t or "hdfc credit card statement" in t:
        scores["hdfc"] += 3
    elif "hdfc bank" in t:
        scores["hdfc"] += 1

    if "state bank of india" in t or "sbi card" in t or "sbi credit card" in t:
        scores["sbi"] += 3
    elif "sbi" in t:
        scores["sbi"] += 1

    if "icici bank credit card" in t or "icici credit card" in t:
        scores["icici"] += 3
    elif "icici bank" in t:
        scores["icici"] += 1

    if "axis bank credit card" in t or "axis credit card" in t:
        scores["axis"] += 3
    elif "axis bank" in t:
        scores["axis"] += 1

    if "citibank credit card" in t or "citi credit card" in t:
        scores["citi"] += 3
    elif "citibank" in t or "citi bank" in t:
        scores["citi"] += 1

    # Pick the highest score
    best = max(scores, key=scores.get)
    if scores[best] > 0:
        return best

    # 🔁 Fallback to filename hint if no keywords detected
    fname = os.path.basename(pdf_path).lower()
    if "icici" in fname:
        return "icici"
    elif "axis" in fname:
        return "axis"
    elif "sbi" in fname:
        return "sbi"
    elif "citi" in fname:
        return "citi"
    elif "hdfc" in fname:
        return "hdfc"
    else:
        return None


def get_parser_for(bank_key: str):
    cls = PARSERS.get(bank_key)
    return cls


def detect_bank_with_logo(text: str, pdf_path: str = ""):
    first_page = text[:300].lower()
    bank = detect_bank(first_page, pdf_path)
    return bank


# -----------------------------
# Main parsing function
# -----------------------------
def parse_file(path: str, output_dir: str = "output"):
    # Extract text from PDF
    text = extract_text_from_pdf(path)

    # Detect bank using text + filename
    bank_key = detect_bank(text, path)
    print(f"[INFO] detected bank: {bank_key}")

    # Choose parser class
    if not bank_key:
        print("[WARN] Bank not detected automatically. Using HDFC parser as default.")
        parser_cls = HDFCParser
    else:
        parser_cls = get_parser_for(bank_key)
        if parser_cls is None:
            print(f"[WARN] Parser class for {bank_key} not found. Using HDFC parser as fallback.")
            parser_cls = HDFCParser

    # Instantiate parser
    parser = parser_cls(path)

    # Parse PDF
    try:
        result = parser.parse()
    except NotImplementedError as e:
        print("[ERROR]", e)
        return None

    # Save JSON output
    os.makedirs(output_dir, exist_ok=True)
    base = os.path.basename(path)
    json_name = os.path.splitext(base)[0] + ".json"
    out_path = os.path.join(output_dir, json_name)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"[OK] Parsed output saved to {out_path}")
    return out_path


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m src.main <path-to-pdf> [output-dir]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else "output"
    parse_file(pdf_path, outdir)
