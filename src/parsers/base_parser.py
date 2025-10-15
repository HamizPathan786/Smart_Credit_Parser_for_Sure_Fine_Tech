
from typing import Dict, Any
from src.utils.pdf_utils import extract_text_from_pdf
from src.utils import regex_patterns as patterns

class BaseParser:
   
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text = extract_text_from_pdf(pdf_path)

    def parse(self) -> Dict[str, Any]:
        raise NotImplementedError

    def find_first(self, regex_list, default=None):
        for r in regex_list:
            m = r.search(self.text)
            if m:
                return m.group(1).strip()
        return default

