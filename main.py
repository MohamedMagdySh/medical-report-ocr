#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import json

from ocr_engine import extract_text_from_file, check_image_quality
from text_parser import extract_results_from_text
from report_builder import build_report, format_report_text

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass


def analyze_lab_result(file_path: str, sex: str = None, verbose: bool = True, crop_margins: dict = None) -> dict:
    """Run the full pipeline (quality check -> OCR -> parsing -> evaluation) and return the final report dict."""
    if verbose:
        print(f"📄 جاري قراءة الملف: {file_path}")

    # Image quality check only applies to image files, not PDFs.
    quality_warning = None
    if not file_path.lower().endswith(".pdf"):
        quality = check_image_quality(file_path)
        if quality["is_low_quality"]:
            quality_warning = quality["message"]
            if verbose:
                print(quality_warning + "\n")

    raw_text = extract_text_from_file(file_path, crop_margins=crop_margins)

    if verbose:
        print(f"✅ تم استخراج {len(raw_text)} حرف من الملف")
        print("\n--- النص المستخرج (للمراجعة) ---")
        print(raw_text[:1500] + ("..." if len(raw_text) > 1500 else ""))
        print("---------------------------------\n")

    extracted_results = extract_results_from_text(raw_text)

    if verbose:
        print(f"🔍 تم التعرف على {len(extracted_results)} تحليل من النص")

    if not extracted_results:
        if verbose:
            print(
                "⚠️ لم يتم التعرف على أي تحليل معروف في الملف.\n"
                "   الأسباب المحتملة: جودة الصورة ضعيفة، أو التحليل غير مدرج "
                "في قاعدة البيانات الحالية، أو تنسيق غير متوقع."
            )
        return {
            "raw_text": raw_text,
            "results": [],
            "summary": {"total": 0, "normal": 0, "high": 0, "low": 0, "unknown": 0},
            "quality_warning": quality_warning,
        }

    report = build_report(extracted_results, sex=sex)
    report["raw_text"] = raw_text
    report["quality_warning"] = quality_warning

    if verbose:
        print(format_report_text(report))

    return report


def main():
    """CLI entry point: parse arguments, run the analysis, and print the result."""
    parser = argparse.ArgumentParser(
        description="Lab result analyzer - compares test results against reference values"
    )
    parser.add_argument("file", help="Path to the lab result file (PDF or image)")
    parser.add_argument(
        "--sex", choices=["male", "female"], default=None,
        help="Patient sex (optional) - improves accuracy of sex-specific tests"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output the result as JSON instead of formatted text"
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Print detailed processing steps (useful for debugging)"
    )
    parser.add_argument(
        "--crop-top", type=float, default=0.0,
        help="Fraction to crop from the top of the image (0.0 to 0.9)"
    )
    parser.add_argument(
        "--crop-bottom", type=float, default=0.0,
        help="Fraction to crop from the bottom of the image (0.0 to 0.9)"
    )
    parser.add_argument(
        "--crop-left", type=float, default=0.0,
        help="Fraction to crop from the left of the image (0.0 to 0.9)"
    )
    parser.add_argument(
        "--crop-right", type=float, default=0.0,
        help="Fraction to crop from the right of the image (0.0 to 0.9)"
    )

    args = parser.parse_args()

    crop_margins = None
    if any([args.crop_top, args.crop_bottom, args.crop_left, args.crop_right]):
        crop_margins = {
            "top": args.crop_top,
            "bottom": args.crop_bottom,
            "left": args.crop_left,
            "right": args.crop_right,
        }

    try:
        # Default mode prints only the final report; --verbose shows intermediate steps too.
        report = analyze_lab_result(
            args.file, sex=args.sex,
            verbose=args.verbose and not args.json,
            crop_margins=crop_margins,
        )
    except FileNotFoundError as e:
        print(f"❌ خطأ: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ خطأ: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع أثناء المعالجة: {e}")
        sys.exit(1)

    if args.json:
        output = {"summary": report["summary"], "results": report["results"]}
        print(json.dumps(output, ensure_ascii=False, indent=2))
    elif not args.verbose:
        print(format_report_text(report))
    # If --verbose was used, the report was already printed inside analyze_lab_result().


if __name__ == "__main__":
    main()
