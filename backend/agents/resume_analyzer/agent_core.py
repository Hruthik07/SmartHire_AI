"""
ResumeAnalyzerAgent Core
------------------------
Responsible for reading and extracting text from resumes.
Supports PDF, DOCX, and TXT with optional OCR fallback.
"""

import os
import logging
import fitz  # PyMuPDF
from docx import Document
from typing import Optional

# Configure logging
logger = logging.getLogger(__name__)

# Optional OCR imports
try:
    from pdf2image import convert_from_path
    import pytesseract
    OCR_ENABLED = True
except ImportError:
    OCR_ENABLED = False
    logger.warning("OCR libraries not available. Install pdf2image and pytesseract for OCR support.")


class ResumeAnalyzerAgent:
    """Extract clean text from resume files with support for multiple formats."""

    def extract_text(self, file_path: str) -> str:
        """
        Extract text from PDF, DOCX, or TXT files.
        
        Args:
            file_path: Path to the resume file
            
        Returns:
            Extracted text as string
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        ext = os.path.splitext(file_path)[1].lower()
        text = ""

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Resume file not found: {file_path}")

        try:
            if ext == ".pdf":
                text = self._extract_pdf_text(file_path)
                if len(text.strip()) < 50 and OCR_ENABLED:
                    logger.info(f"Using OCR for {os.path.basename(file_path)}...")
                    text = self._extract_pdf_with_ocr(file_path)

            elif ext in [".docx", ".doc"]:
                text = self._extract_docx_text(file_path)

            elif ext == ".txt":
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

            else:
                logger.warning(f"Unsupported file format: {ext}")

            return text.strip()

        except Exception as e:
            logger.error(f"Failed to extract text from {file_path}: {e}", exc_info=True)
            return ""

    def _extract_pdf_text(self, file_path: str) -> str:
        """
        Extract text from text-based PDFs.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        try:
            text = ""
            with fitz.open(file_path) as pdf_doc:
                for page in pdf_doc:
                    text += page.get_text("text")
            return text
        except Exception as e:
            logger.error(f"PDF text extraction failed for {file_path}: {e}")
            return ""

    def _extract_docx_text(self, file_path: str) -> str:
        """
        Extract text from DOCX/DOC files.
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            Extracted text
        """
        try:
            doc = Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            logger.error(f"DOCX text extraction failed for {file_path}: {e}")
            return ""

    def _extract_pdf_with_ocr(self, file_path: str) -> str:
        """
        OCR fallback for scanned PDFs.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text via OCR
        """
        if not OCR_ENABLED:
            logger.info("OCR not available (install pdf2image + pytesseract).")
            return ""
        try:
            pages = convert_from_path(file_path)
            text = "".join(pytesseract.image_to_string(p) for p in pages)
            return text
        except Exception as e:
            logger.error(f"OCR extraction failed for {file_path}: {e}")
            return ""
