# -*- coding: utf-8 -*-

from reference_values import REFERENCE_VALUES, get_reference_range, resolve_numeric_reference

STATUS_NORMAL = "طبيعي ✅"
STATUS_HIGH = "مرتفع ⬆️"
STATUS_LOW = "منخفض ⬇️"
STATUS_ABNORMAL = "غير طبيعي ⚠️"
STATUS_UNKNOWN = "غير معروف القيمة المرجعية ❓"


def _normalize_qualitative(text: str) -> str:
    """Normalize a qualitative value (lowercase, unify dashes/underscores to spaces) for comparison."""
    return text.lower().replace("-", " ").replace("_", " ").strip()


def evaluate_qualitative_result(test_name: str, value: str, printed_reference: str = None) -> dict:
    """Compare a qualitative value (e.g. Negative/Positive) against the stored list of normal values."""
    info = REFERENCE_VALUES.get(test_name, {})
    normal_values = [_normalize_qualitative(v) for v in info.get("normal_values", [])]

    if _normalize_qualitative(value) in normal_values:
        status = STATUS_NORMAL
    else:
        status = STATUS_ABNORMAL

    return {
        "test_name": test_name,
        "arabic_name": info.get("arabic_name", test_name),
        "value": value.capitalize(),
        "unit": "",
        "reference_range": " / ".join(v.capitalize() for v in info.get("normal_values", [])) or "غير متاح",
        "category": info.get("category", ""),
        "status": status,
    }


def evaluate_result(test_name: str, value, sex: str = None, value_type: str = "numeric",
                     printed_reference=None) -> dict:
    """Evaluate a single test result (numeric or qualitative) against its reference range/values."""
    info = REFERENCE_VALUES.get(test_name)
    if not info:
        return {
            "test_name": test_name,
            "arabic_name": test_name,
            "value": value,
            "unit": "",
            "reference_range": None,
            "status": STATUS_UNKNOWN,
        }

    if value_type == "qualitative":
        return evaluate_qualitative_result(test_name, value, printed_reference)

    low, high, ref_source = resolve_numeric_reference(test_name, printed_reference, sex)

    if low is None or high is None:
        status = STATUS_UNKNOWN
    elif value < low:
        status = STATUS_LOW
    elif value > high:
        status = STATUS_HIGH
    else:
        status = STATUS_NORMAL

    return {
        "test_name": test_name,
        "arabic_name": info.get("arabic_name", test_name),
        "value": value,
        "unit": info.get("unit", ""),
        "reference_range": f"{low} - {high}" if low is not None else "غير متاح",
        "reference_source": ref_source,  # "printed" or "stored", for transparency only
        "category": info.get("category", ""),
        "status": status,
    }


def build_report(extracted_results: list, sex: str = None) -> dict:
    """Build the final report (evaluated results + summary counts) from extracted test results."""
    evaluated = []
    for item in extracted_results:
        result = evaluate_result(
            item["test_name"], item["value"], sex,
            value_type=item.get("value_type", "numeric"),
            printed_reference=item.get("printed_reference"),
        )
        result["raw_line"] = item.get("raw_line", "")
        evaluated.append(result)

    summary = {
        "total": len(evaluated),
        "normal": sum(1 for r in evaluated if r["status"] == STATUS_NORMAL),
        "high": sum(1 for r in evaluated if r["status"] == STATUS_HIGH),
        "low": sum(1 for r in evaluated if r["status"] == STATUS_LOW),
        "abnormal": sum(1 for r in evaluated if r["status"] == STATUS_ABNORMAL),
        "unknown": sum(1 for r in evaluated if r["status"] == STATUS_UNKNOWN),
    }

    return {
        "results": evaluated,
        "summary": summary,
    }


def format_report_text(report: dict) -> str:
    """Format the final report as plain Arabic text for direct display to the user (CLI mode)."""
    lines = []

    if report.get("quality_warning"):
        lines.append(report["quality_warning"])
        lines.append("")

    lines.append("=" * 60)
    lines.append("تقرير تحليل نتيجة المعمل")
    lines.append("=" * 60)

    by_category = {}
    for r in report["results"]:
        cat = r.get("category", "أخرى") or "أخرى"
        by_category.setdefault(cat, []).append(r)

    category_names_ar = {
        "CBC": "صورة الدم الكاملة",
        "Glucose": "السكر",
        "Liver": "وظائف الكبد",
        "Kidney": "وظائف الكلى",
        "Lipid": "تحليل الدهون",
        "Thyroid": "الغدة الدرقية",
        "Hepatitis": "فيروسات الكبد",
        "Urine": "تحليل البول",
        "Stool": "تحليل البراز",
        "أخرى": "أخرى",
    }

    for cat, items in by_category.items():
        lines.append(f"\n--- {category_names_ar.get(cat, cat)} ---")
        for r in items:
            ar_name = r.get("arabic_name", "")
            name_display = f"{r['test_name']} ({ar_name})" if ar_name else r['test_name']
            unit_display = f" {r['unit']}" if r['unit'] else ""
            lines.append(
                f"  • {name_display}: {r['value']}{unit_display} "
                f"(الطبيعي: {r['reference_range']})  →  {r['status']}"
            )

    lines.append("")
    lines.append("-" * 60)
    s = report["summary"]
    lines.append(
        f"الملخص: {s['total']} تحليل تم رصده | "
        f"طبيعي: {s['normal']} | مرتفع: {s['high']} | منخفض: {s['low']}"
        + (f" | غير طبيعي: {s['abnormal']}" if s.get("abnormal") else "")
        + (f" | غير معروف: {s['unknown']}" if s["unknown"] else "")
    )
    lines.append("-" * 60)
    lines.append(
        "\n⚠️ تنبيه هام: هذا التقرير استرشادي تم توليده آليًا ولا يُغني عن "
        "استشارة الطبيب المختص لتفسير النتائج واتخاذ القرار الطبي المناسب."
    )

    return "\n".join(lines)
