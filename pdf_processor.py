import PyPDF2
import pdfplumber
from typing import List, Tuple


class PDFProcessor:
    @staticmethod
    def extract_text_from_pdf(pdf_bytes) -> Tuple[str, int]:
        try:
            with pdfplumber.open(pdf_bytes) as pdf:
                text = ""
                page_count = len(pdf.pages)
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                return text, page_count
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    @staticmethod
    def extract_text_by_pages(pdf_bytes) -> List[Tuple[int, str]]:
        try:
            pages_text = []
            with pdfplumber.open(pdf_bytes) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text.strip():
                        pages_text.append((page_num, text))
            return pages_text
        except Exception as e:
            raise Exception(f"Error processing PDF by pages: {str(e)}")
