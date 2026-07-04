# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
from PIL import Image
import pytesseract
import pdfplumber
from pdf2image import convert_from_path

# Windows-only paths: on Linux/macOS, Tesseract and Poppler are normally
# available on PATH already. On Windows these must be set explicitly.
TESSERACT_PATH_WINDOWS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH_WINDOWS = r"C:\Users\dell\Desktop\Poppler\poppler-26.02.0\Library\bin"

if os.name == "nt":
    if os.path.exists(TESSERACT_PATH_WINDOWS):
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH_WINDOWS
    POPPLER_PATH = POPPLER_PATH_WINDOWS if os.path.exists(POPPLER_PATH_WINDOWS) else None
else:
    POPPLER_PATH = None


def check_image_quality(file_path: str) -> dict:
    """Check image resolution and flag it as low quality if below a usable threshold for OCR."""
    img = Image.open(file_path)
    w, h = img.size
    max_dim = max(w, h)

    LOW_RES_THRESHOLD = 800
    is_low_quality = max_dim < LOW_RES_THRESHOLD

    message = ""
    if is_low_quality:
        message = (
            f"⚠️ دقة الصورة منخفضة ({w}x{h} بكسل). هذا قد يقلل من دقة "
            "قراءة التحليل بشكل كبير. للحصول على أفضل نتيجة، يُفضّل:\n"
            "   - تصوير الورقة بكاميرا الموبايل مباشرة (وليس تصغير/ضغط صورة قديمة)\n"
            "   - التأكد من إضاءة جيدة ومتساوية وعدم وجود انعكاس ضوء\n"
            "   - تصوير الورقة وهي مفرودة على سطح مستوٍ، والكاميرا موازية لها تمامًا\n"
            "   - التأكد إن الورقة تملأ معظم الكادر بدون خلفية كبيرة حولها"
        )

    return {
        "is_low_quality": is_low_quality,
        "width": w,
        "height": h,
        "message": message,
    }


def manual_crop_margins(pil_image: Image.Image, top=0.0, bottom=0.0, left=0.0, right=0.0) -> Image.Image:
    """Crop a percentage of each margin from an image (used to remove background clutter around the document)."""
    w, h = pil_image.size
    left_px = int(w * left)
    right_px = int(w * (1 - right))
    top_px = int(h * top)
    bottom_px = int(h * (1 - bottom))
    return pil_image.crop((left_px, top_px, right_px, bottom_px))


def preprocess_image_for_ocr(pil_image: Image.Image, variant: str = "otsu") -> Image.Image:
    """Upscale, denoise, and threshold an image for OCR. Supports two thresholding strategies."""
    img = np.array(pil_image.convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    h, w = gray.shape
    target_size = 2400 if max(h, w) < 1000 else 1800
    if max(h, w) < target_size:
        scale = target_size / max(h, w)
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_LANCZOS4)

    if variant == "otsu":
        # Best for noisy/unevenly lit mobile photos (the most common real-world case).
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)
        _, processed = cv2.threshold(
            denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
    else:  # adaptive
        denoised = cv2.fastNlMeansDenoising(gray, h=15)
        processed = cv2.adaptiveThreshold(
            denoised, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31, 11
        )

    return Image.fromarray(processed)


def _ocr_score(text: str) -> int:
    """Score OCR output quality: reward digits/letters, penalize noise characters."""
    if not text:
        return 0
    digits = sum(c.isdigit() for c in text)
    letters = sum(c.isalpha() for c in text)
    noise = sum(c in "~`^|\\{}_<>" for c in text)
    return digits * 3 + letters - noise * 2


def ocr_image(pil_image: Image.Image, lang: str = "eng+ara", crop_margins: dict = None) -> str:
    """Run OCR on an image, trying multiple preprocessing variants and keeping the best-scoring result."""
    config = "--oem 3 --psm 6"

    if crop_margins:
        pil_image = manual_crop_margins(
            pil_image,
            top=crop_margins.get("top", 0.0),
            bottom=crop_margins.get("bottom", 0.0),
            left=crop_margins.get("left", 0.0),
            right=crop_margins.get("right", 0.0),
        )

    best_text = ""
    best_score = -10**9

    for variant in ("otsu", "adaptive"):
        processed = preprocess_image_for_ocr(pil_image, variant=variant)
        try:
            text = pytesseract.image_to_string(processed, lang=lang, config=config)
        except pytesseract.TesseractError:
            text = pytesseract.image_to_string(processed, lang="eng", config=config)

        score = _ocr_score(text)
        if score > best_score:
            best_score = score
            best_text = text

    return best_text


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text directly from a PDF, falling back to OCR if the PDF turns out to be a scanned image."""
    extracted_text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages_text = []
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                pages_text.append(page_text)
            extracted_text = "\n".join(pages_text).strip()
    except Exception:
        extracted_text = ""

    if len(extracted_text) < 30:
        try:
            if POPPLER_PATH:
                images = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
            else:
                images = convert_from_path(pdf_path, dpi=300)
            ocr_texts = [ocr_image(img) for img in images]
            extracted_text = "\n".join(ocr_texts)
        except Exception as e:
            raise RuntimeError(f"Failed to convert PDF to images for OCR: {e}")

    return extracted_text


def extract_text_from_file(file_path: str, crop_margins: dict = None) -> str:
    """Unified entry point: extract text from either a PDF or an image file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"):
        img = Image.open(file_path)
        return ocr_image(img, crop_margins=crop_margins)
    else:
        raise ValueError(f"Unsupported file type: {ext} (supported: PDF, PNG, JPG, JPEG, BMP, TIFF)")
