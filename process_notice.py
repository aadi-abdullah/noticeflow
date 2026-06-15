"""
NoticeFlow Lite – Notice Processing Engine (Groq Edition)
Core logic for OCR extraction and Groq structured parsing of tax notices.

This module handles:
1. File type detection and OCR (Azure Document Intelligence or Groq Vision)
2. Raw text extraction from PDFs and images
3. Structured JSON extraction using Groq (llama-3.3-70b-versatile) with custom system prompt
4. Error handling and fallback mechanisms

Usage:
    from process_notice import process_notice
    result = process_notice(uploaded_file)
"""

import os
import json
import io
import logging
from typing import Dict, Any, Optional, List
import base64

# External dependencies
from groq import Groq, APIError
from PIL import Image
import PyPDF2

# Azure Document Intelligence (optional, preferred for OCR)
try:
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.core.credentials import AzureKeyCredential
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Groq client initialisation
# ---------------------------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
    logger.warning(
        "GROQ_API_KEY is not set. Notice parsing will not work. "
        "Add it to .streamlit/secrets.toml or your environment."
    )
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Groq model names
GROQ_TEXT_MODEL = "llama-3.3-70b-versatile"
GROQ_VISION_MODEL = "llama-3.2-90b-vision-preview"

# Azure Document Intelligence credentials (optional)
AZURE_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

# ---------------------------------------------------------------------------
# System prompt for Groq to extract and parse FBR notices
# ---------------------------------------------------------------------------
FBR_SYSTEM_PROMPT = """You are an expert system for parsing Pakistani FBR (Federal Board of Revenue) and IRIS tax notices.

Your task is to extract and structure information from tax notices with high accuracy and confidence tracking.

IMPORTANT RULES:
1. Extract ONLY information explicitly stated in the notice. Do NOT infer or guess.
2. For any ambiguous or missing information, add it to the "uncertainties" list and explain why you couldn't extract it with confidence.
3. Always cite the exact section number (e.g., 122(5A), 114, 177, 161) as stated in the notice.
4. Identify the tax year (e.g., 2023, 2023-24, FY2024).
5. Extract the deadline date if present. Format as YYYY-MM-DD. If not found, return null.
6. Summarize the allegations/reasons for notice in plain language, 2-3 bullet points.
7. Based on section cited and allegations, generate a specific document checklist (not generic; tailored to the type of notice).
8. Assess risk level (low/medium/high) based on:
   - Section severity: 177, 143, 122(5A) are high risk; 161, 148 are medium.
   - Days to deadline: <7 days = high; 7-14 = medium; >14 = low.
   - Nature of allegation: fraud/evasion = high; procedural/clarification = low.
9. Return a valid JSON object, even if some fields are uncertain.

KNOWN FBR SECTIONS (for reference):
- 114: Best judgment assessment (high severity, medium deadline)
- 122(5A): Best judgment for income (high severity, high deadline)
- 143(2): Demand after assessment (medium severity, medium deadline)
- 148: Reassessment (medium-high severity, medium deadline)
- 161: Verification notice (low-medium severity, longer deadline)
- 177: Penalty notice (high severity, urgent deadline)

Document Checklist Guidelines:
- For section 114/122: Bank statements, sales/purchase ledgers, WHT certs, tax returns.
- For section 161: Specific documents related to the query.
- For section 177: Proof of compliance, audit reports, legal opinions.
- Always include: Balance sheet, Profit & Loss statement, tax return (if applicable).
- Do NOT include generic advice; be specific to the notice type.

Return output as valid JSON with this exact structure:
{
  "section_cited": "e.g., 122(5A)",
  "tax_year": "e.g., 2023",
  "deadline": "YYYY-MM-DD or null",
  "allegations_summary": ["allegation 1", "allegation 2", ...],
  "document_checklist": ["document 1", "document 2", ...],
  "risk_level": "low/medium/high",
  "risk_reason": "one-line explanation",
  "uncertainties": ["field: reason for uncertainty", ...]
}

Never fabricate data. If a field cannot be extracted, mark it as uncertain."""


# =========================================================================
# TEXT EXTRACTION HELPERS
# =========================================================================

def extract_text_from_pdf_with_azure(pdf_bytes: bytes) -> Optional[str]:
    """
    Extract text from PDF using Azure Document Intelligence.
    Preferred method for scanned PDFs and mixed-format documents.

    Args:
        pdf_bytes (bytes): PDF file content.

    Returns:
        Optional[str]: Extracted text, or None if extraction fails.
    """
    if not AZURE_AVAILABLE or not AZURE_ENDPOINT or not AZURE_KEY:
        logger.warning("Azure Document Intelligence not configured. Skipping.")
        return None

    try:
        logger.info("Attempting OCR with Azure Document Intelligence...")
        client_azure = DocumentIntelligenceClient(
            endpoint=AZURE_ENDPOINT,
            credential=AzureKeyCredential(AZURE_KEY),
        )

        poller = client_azure.begin_analyze_document(
            "prebuilt-document",
            pdf_bytes,
            content_type="application/pdf",
        )
        result = poller.result()

        extracted_text = result.content
        logger.info(f"Azure OCR successful. Extracted {len(extracted_text)} characters.")
        return extracted_text

    except Exception as e:
        logger.warning(f"Azure OCR failed: {str(e)}")
        return None


def extract_text_from_pdf_with_pypdf2(pdf_bytes: bytes) -> Optional[str]:
    """
    Extract text from text-based PDFs using PyPDF2.
    Fallback for simple PDFs (not scanned).

    Args:
        pdf_bytes (bytes): PDF file content.

    Returns:
        Optional[str]: Extracted text, or None if extraction fails or PDF is scanned.
    """
    try:
        logger.info("Attempting text extraction with PyPDF2...")
        pdf_file = io.BytesIO(pdf_bytes)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""

        # Extract from first 5 pages (limit for performance)
        for page_num in range(min(5, len(reader.pages))):
            page = reader.pages[page_num]
            text += page.extract_text()

        if text.strip():
            logger.info(f"PyPDF2 extraction successful. Extracted {len(text)} characters.")
            return text
        else:
            logger.info("PyPDF2 extraction returned empty text. Likely a scanned PDF.")
            return None

    except Exception as e:
        logger.warning(f"PyPDF2 extraction failed: {str(e)}")
        return None


def encode_image_to_base64(image_bytes: bytes) -> str:
    """
    Encode image bytes to base64 string for Groq Vision API.

    Args:
        image_bytes (bytes): Image file content.

    Returns:
        str: Base64 encoded image.
    """
    return base64.b64encode(image_bytes).decode("utf-8")


def pdf_first_page_to_image(pdf_bytes: bytes) -> Optional[bytes]:
    """
    Convert the first page of a PDF to a PNG image byte buffer.
    Used so that Groq Vision can "see" scanned PDFs.

    Args:
        pdf_bytes (bytes): PDF file content.

    Returns:
        Optional[bytes]: PNG image bytes of the first page, or None on failure.
    """
    try:
        from pdf2image import convert_from_bytes  # optional dependency
        images = convert_from_bytes(pdf_bytes, first_page=1, last_page=1, dpi=200)
        if images:
            buf = io.BytesIO()
            images[0].save(buf, format="PNG")
            buf.seek(0)
            return buf.read()
    except ImportError:
        logger.warning(
            "pdf2image not installed. Cannot convert PDF page to image for Groq Vision. "
            "Install with: pip install pdf2image  (also requires poppler on your system)"
        )
    except Exception as e:
        logger.warning(f"PDF-to-image conversion failed: {str(e)}")
    return None


def extract_text_with_groq_vision(
    file_bytes: bytes, file_type: str, file_name: str
) -> Optional[str]:
    """
    Extract text from an image using Groq Vision (llama-3.2-90b-vision-preview).
    Fallback method for scanned PDFs and images when Azure is unavailable.

    Args:
        file_bytes (bytes): File content.
        file_type (str): MIME type (e.g., "image/png", "image/jpeg").
        file_name (str): Original file name.

    Returns:
        Optional[str]: Extracted text, or None if extraction fails.
    """
    if not client:
        logger.error("Groq client not initialised. Cannot use Vision API.")
        return None

    try:
        logger.info(f"Attempting OCR with Groq Vision for {file_name}...")

        # If the file is a PDF we need to convert it to an image first
        if file_type == "application/pdf":
            image_bytes = pdf_first_page_to_image(file_bytes)
            if image_bytes is None:
                logger.warning(
                    "Could not convert PDF to image for Groq Vision. "
                    "Skipping vision extraction for this PDF."
                )
                return None
            file_type = "image/png"
            file_bytes = image_bytes

        base64_image = encode_image_to_base64(file_bytes)

        response = client.chat.completions.create(
            model=GROQ_VISION_MODEL,
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{file_type};base64,{base64_image}"
                            },
                        },
                        {
                            "type": "text",
                            "text": (
                                "Extract all text from this tax notice. "
                                "Preserve structure and formatting. "
                                "Return only the extracted text."
                            ),
                        },
                    ],
                }
            ],
        )

        extracted_text = response.choices[0].message.content
        logger.info(
            f"Groq Vision extraction successful. Extracted {len(extracted_text)} characters."
        )
        return extracted_text

    except APIError as e:
        logger.warning(f"Groq Vision API error: {str(e)}")
        return None
    except Exception as e:
        logger.warning(f"Groq Vision extraction failed: {str(e)}")
        return None


def extract_raw_text(uploaded_file) -> Optional[str]:
    """
    Extract raw text from uploaded file (PDF or image).
    Uses multiple fallback strategies: Azure → PyPDF2 → Groq Vision.

    Args:
        uploaded_file: Streamlit UploadedFile object.

    Returns:
        Optional[str]: Raw extracted text, or None if all methods fail.
    """
    file_bytes = uploaded_file.read()
    file_name = uploaded_file.name
    file_type = uploaded_file.type

    logger.info(
        f"Starting text extraction for {file_name} ({file_type}, {len(file_bytes)} bytes)"
    )

    # ------- PDF -------
    if file_type == "application/pdf":
        # Try Azure first (best for scanned PDFs)
        if AZURE_AVAILABLE and AZURE_ENDPOINT and AZURE_KEY:
            text = extract_text_from_pdf_with_azure(file_bytes)
            if text and text.strip():
                return text

        # Try PyPDF2 for text-based PDFs
        text = extract_text_from_pdf_with_pypdf2(file_bytes)
        if text and text.strip():
            return text

        # Fall back to Groq Vision
        text = extract_text_with_groq_vision(file_bytes, file_type, file_name)
        if text and text.strip():
            return text

    # ------- Image -------
    elif file_type in ["image/png", "image/jpeg", "image/jpg", "image/webp"]:
        # For images, try Azure first (if available), then Groq Vision
        if AZURE_AVAILABLE and AZURE_ENDPOINT and AZURE_KEY:
            text = extract_text_from_pdf_with_azure(file_bytes)
            if text and text.strip():
                return text

        text = extract_text_with_groq_vision(file_bytes, file_type, file_name)
        if text and text.strip():
            return text

    logger.error(f"All text extraction methods failed for {file_name}")
    return None


# =========================================================================
# STRUCTURED PARSING
# =========================================================================

def parse_notice_with_groq(raw_text: str, max_retries: int = 1) -> Dict[str, Any]:
    """
    Send extracted text to Groq (llama-3.3-70b-versatile) for structured
    parsing and JSON extraction. Includes retry logic for transient API
    errors or invalid JSON.

    Args:
        raw_text (str): Extracted raw text from notice.
        max_retries (int): Number of retry attempts for invalid JSON.

    Returns:
        Dict[str, Any]: Parsed notice data with structure defined in FBR_SYSTEM_PROMPT.
    """
    if not client:
        return _get_fallback_response(
            "Groq client not initialised. Check GROQ_API_KEY."
        )

    retries = 0

    while retries <= max_retries:
        try:
            logger.info(
                f"Sending notice text to Groq for parsing (attempt {retries + 1})..."
            )

            response = client.chat.completions.create(
                model=GROQ_TEXT_MODEL,
                max_tokens=1500,
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": FBR_SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": (
                            "Parse this tax notice and extract information:\n\n"
                            f"{raw_text[:4000]}"  # Limit context to stay within token budget
                        ),
                    },
                ],
            )

            response_text = response.choices[0].message.content
            result = json.loads(response_text)

            logger.info(
                f"Groq parsing successful. Extracted: {result.get('section_cited', 'Unknown')}"
            )
            return result

        except json.JSONDecodeError as e:
            logger.warning(
                f"Invalid JSON response from Groq (attempt {retries + 1}): {str(e)}"
            )
            retries += 1
            if retries > max_retries:
                logger.error("Max retries exceeded. Returning fallback response.")
                return _get_fallback_response(
                    "JSON parsing error from Groq. Unable to extract structured data."
                )

        except APIError as e:
            logger.warning(f"Groq API error (attempt {retries + 1}): {str(e)}")
            retries += 1
            if retries > max_retries:
                logger.error("Max retries exceeded. Returning fallback response.")
                return _get_fallback_response(f"Groq API error: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error during Groq parsing: {str(e)}")
            return _get_fallback_response(f"Unexpected error: {str(e)}")

    return _get_fallback_response("Unknown error during parsing.")


# =========================================================================
# VALIDATION & FALLBACK
# =========================================================================

def _get_fallback_response(error_message: str) -> Dict[str, Any]:
    """
    Return a fallback response when parsing fails.
    Ensures the app doesn't crash with invalid data.

    Args:
        error_message (str): User-facing error message.

    Returns:
        Dict[str, Any]: Fallback response with error flag.
    """
    return {
        "error": f"{error_message} Please upload a clearer scan or try again.",
        "section_cited": None,
        "tax_year": None,
        "deadline": None,
        "allegations_summary": [],
        "document_checklist": [],
        "risk_level": "unknown",
        "risk_reason": "Unable to assess",
        "uncertainties": ["All fields: Unable to process document"],
    }


def validate_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and clean the parsed result.
    Ensures all expected fields are present and properly formatted.

    Args:
        result (Dict[str, Any]): Parsed result from Groq.

    Returns:
        Dict[str, Any]: Validated result with safe defaults.
    """
    expected_fields = {
        "section_cited": "Unknown",
        "tax_year": "Unknown",
        "deadline": None,
        "allegations_summary": [],
        "document_checklist": [],
        "risk_level": "unknown",
        "risk_reason": "Unable to assess",
        "uncertainties": [],
    }

    for key, default in expected_fields.items():
        if key not in result:
            result[key] = default

        # Validate list fields
        if key in ["allegations_summary", "document_checklist", "uncertainties"]:
            if not isinstance(result[key], list):
                result[key] = default if isinstance(default, list) else [str(result[key])]

    # Validate deadline format
    if result.get("deadline") and not isinstance(result["deadline"], str):
        result["deadline"] = None

    # Validate risk level
    if result.get("risk_level") not in ["low", "medium", "high", "unknown"]:
        result["risk_level"] = "unknown"

    logger.info("Result validation complete.")
    return result


# =========================================================================
# MAIN ENTRY POINT
# =========================================================================

def process_notice(uploaded_file) -> Dict[str, Any]:
    """
    Main orchestration function for processing a tax notice.

    Pipeline:
    1. Extract raw text from file (PDF or image)
    2. Send to Groq for structured parsing
    3. Validate and return result

    Args:
        uploaded_file: Streamlit UploadedFile object.

    Returns:
        Dict[str, Any]: Structured notice data or error response.

    Example:
        result = process_notice(uploaded_file)
        if "error" not in result:
            print(result["section_cited"])
            print(result["deadline"])
    """
    try:
        # Step 1: Extract raw text
        raw_text = extract_raw_text(uploaded_file)
        if not raw_text:
            logger.error("Text extraction failed for all methods.")
            return _get_fallback_response(
                "The document could not be read. Please try a clearer scan or photo."
            )

        # Step 2: Parse with Groq
        result = parse_notice_with_groq(raw_text)

        # Step 3: Validate
        result = validate_result(result)

        logger.info("Notice processing complete.")
        return result

    except Exception as e:
        logger.error(f"Unexpected error in process_notice: {str(e)}")
        return _get_fallback_response(f"Unexpected error: {str(e)}")