# Lookup table of reference (normal) values for common lab tests, grouped by category.
REFERENCE_VALUES = {

    "Hemoglobin": {
        "aliases": ["hemoglobin", "hgb", "hb", "هيموجلوبين"],
        "unit": "g/dL",
        "arabic_name": "الهيموجلوبين",
        "category": "CBC",
        "sex_specific": {
            "male": {"low": 13.5, "high": 17.5},
            "female": {"low": 12.0, "high": 15.5},
        },
    },
    "RBC": {
        "aliases": ["rbc", "red blood cells", "red cells count", "red cell count", "كرات الدم الحمراء"],
        "unit": "million/uL",
        "arabic_name": "كرات الدم الحمراء",
        "category": "CBC",
        "sex_specific": {
            "male": {"low": 4.7, "high": 6.1},
            "female": {"low": 4.2, "high": 5.4},
        },
    },
    "WBC": {
        "aliases": ["wbc", "white blood cells", "white cells count", "white cell count", "كرات الدم البيضاء"],
        "unit": "x10^3/uL",
        "arabic_name": "كرات الدم البيضاء",
        "category": "CBC",
        "low": 4.0, "high": 11.0,
    },
    "Platelets": {
        "aliases": ["platelets", "plt", "الصفائح الدموية"],
        "unit": "x10^3/uL",
        "arabic_name": "الصفائح الدموية",
        "category": "CBC",
        "low": 150, "high": 450,
    },
    "Hematocrit": {
        "aliases": ["hematocrit", "hct", "هيماتوكريت"],
        "unit": "%",
        "arabic_name": "نسبة الهيماتوكريت (تركيز الدم)",
        "category": "CBC",
        "sex_specific": {
            "male": {"low": 41, "high": 53},
            "female": {"low": 36, "high": 46},
        },
    },
    "MCV": {
        "aliases": ["mcv"],
        "unit": "fL",
        "arabic_name": "متوسط حجم الكرة الحمراء",
        "category": "CBC",
        "low": 80, "high": 100,
    },
    "MCH": {
        "aliases": ["mch"],
        "unit": "pg",
        "arabic_name": "متوسط هيموجلوبين الكرة الحمراء",
        "category": "CBC",
        "low": 27, "high": 33,
    },
    "MCHC": {
        "aliases": ["mchc"],
        "unit": "g/dL",
        "arabic_name": "متوسط تركيز هيموجلوبين الكرة الحمراء",
        "category": "CBC",
        "low": 32, "high": 36,
    },
    "Neutrophils": {
        "aliases": ["neutrophils", "العدلات"],
        "unit": "%",
        "arabic_name": "العدلات",
        "category": "CBC",
        "low": 40, "high": 75,
    },
    "Lymphocytes": {
        "aliases": ["lymphocytes", "الخلايا الليمفاوية"],
        "unit": "%",
        "arabic_name": "الخلايا الليمفاوية",
        "category": "CBC",
        "low": 20, "high": 45,
    },
    "Monocytes": {
        "aliases": ["monocytes", "الوحيدات"],
        "unit": "%",
        "arabic_name": "الوحيدات",
        "category": "CBC",
        "low": 2, "high": 10,
    },

    "Fasting Blood Sugar": {
        "aliases": ["fbs", "fasting blood sugar", "fasting glucose", "سكر صائم", "جلوكوز صائم"],
        "unit": "mg/dL",
        "arabic_name": "السكر الصائم",
        "category": "Glucose",
        "low": 70, "high": 100,
    },
    "Random Blood Sugar": {
        "aliases": ["rbs", "random blood sugar", "glucose", "blood glucose", "سكر عشوائي"],
        "unit": "mg/dL",
        "arabic_name": "السكر العشوائي",
        "category": "Glucose",
        "low": 70, "high": 140,
    },
    "HbA1c": {
        "aliases": ["hba1c", "a1c", "السكر التراكمي"],
        "unit": "%",
        "arabic_name": "السكر التراكمي",
        "category": "Glucose",
        "low": 4.0, "high": 5.6,
    },

    "ALT": {
        "aliases": ["alt", "sgpt", "انزيم الكبد alt"],
        "unit": "U/L",
        "arabic_name": "إنزيم الكبد ALT",
        "category": "Liver",
        "low": 7, "high": 56,
    },
    "AST": {
        "aliases": ["ast", "sgot", "انزيم الكبد ast"],
        "unit": "U/L",
        "arabic_name": "إنزيم الكبد AST",
        "category": "Liver",
        "low": 10, "high": 40,
    },
    "ALP": {
        "aliases": ["alp", "alkaline phosphatase", "الفوسفاتيز القلوي"],
        "unit": "U/L",
        "arabic_name": "إنزيم الفوسفاتيز القلوي",
        "category": "Liver",
        "low": 44, "high": 147,
    },
    "Total Bilirubin": {
        "aliases": ["total bilirubin", "bilirubin total", "البيليروبين الكلي"],
        "unit": "mg/dL",
        "arabic_name": "البيليروبين الكلي",
        "category": "Liver",
        "low": 0.1, "high": 1.2,
    },
    "Direct Bilirubin": {
        "aliases": ["direct bilirubin", "البيليروبين المباشر"],
        "unit": "mg/dL",
        "arabic_name": "البيليروبين المباشر",
        "category": "Liver",
        "low": 0.0, "high": 0.3,
    },
    "Albumin": {
        "aliases": ["albumin", "الألبيومين"],
        "unit": "g/dL",
        "arabic_name": "الألبيومين",
        "category": "Liver",
        "low": 3.5, "high": 5.0,
    },
    "Total Protein": {
        "aliases": ["total protein", "البروتين الكلي"],
        "unit": "g/dL",
        "arabic_name": "البروتين الكلي",
        "category": "Liver",
        "low": 6.0, "high": 8.3,
    },

    "Urea": {
        "aliases": ["urea", "blood urea", "اليوريا"],
        "unit": "mg/dL",
        "arabic_name": "اليوريا",
        "category": "Kidney",
        "low": 15, "high": 45,
    },
    "Creatinine": {
        "aliases": ["creatinine", "الكرياتينين"],
        "unit": "mg/dL",
        "arabic_name": "الكرياتينين",
        "category": "Kidney",
        "sex_specific": {
            "male": {"low": 0.7, "high": 1.3},
            "female": {"low": 0.6, "high": 1.1},
        },
    },
    "Uric Acid": {
        "aliases": ["uric acid", "حمض اليوريك"],
        "unit": "mg/dL",
        "arabic_name": "حمض اليوريك",
        "category": "Kidney",
        "sex_specific": {
            "male": {"low": 3.4, "high": 7.0},
            "female": {"low": 2.4, "high": 6.0},
        },
    },
    "Sodium": {
        "aliases": ["sodium", "na", "الصوديوم"],
        "unit": "mmol/L",
        "arabic_name": "الصوديوم",
        "category": "Kidney",
        "low": 135, "high": 145,
    },
    "Potassium": {
        "aliases": ["potassium", "k", "البوتاسيوم"],
        "unit": "mmol/L",
        "arabic_name": "البوتاسيوم",
        "category": "Kidney",
        "low": 3.5, "high": 5.1,
    },

    "Total Cholesterol": {
        "aliases": ["total cholesterol", "cholesterol", "الكوليسترول الكلي"],
        "unit": "mg/dL",
        "arabic_name": "الكوليسترول الكلي",
        "category": "Lipid",
        "low": 0, "high": 200,
    },
    "Triglycerides": {
        "aliases": ["triglycerides", "tg", "الدهون الثلاثية"],
        "unit": "mg/dL",
        "arabic_name": "الدهون الثلاثية",
        "category": "Lipid",
        "low": 0, "high": 150,
    },
    "HDL": {
        "aliases": ["hdl", "hdl cholesterol", "الكوليسترول الجيد"],
        "unit": "mg/dL",
        "arabic_name": "الكوليسترول الجيد (HDL)",
        "category": "Lipid",
        "low": 40, "high": 60,
    },
    "LDL": {
        "aliases": ["ldl", "ldl cholesterol", "الكوليسترول الضار"],
        "unit": "mg/dL",
        "arabic_name": "الكوليسترول الضار (LDL)",
        "category": "Lipid",
        "low": 0, "high": 100,
    },

    "TSH": {
        "aliases": ["tsh", "الهرمون المنبه للغدة الدرقية"],
        "unit": "mIU/L",
        "arabic_name": "الهرمون المنبه للغدة الدرقية",
        "category": "Thyroid",
        "low": 0.4, "high": 4.0,
    },
    "T3": {
        "aliases": ["t3", "triiodothyronine"],
        "unit": "ng/dL",
        "arabic_name": "هرمون T3",
        "category": "Thyroid",
        "low": 80, "high": 200,
    },
    "T4": {
        "aliases": ["t4", "thyroxine"],
        "unit": "µg/dL",
        "arabic_name": "هرمون T4",
        "category": "Thyroid",
        "low": 5.0, "high": 12.0,
    },

    "HBsAg": {
        "aliases": ["hbsag", "hepatitis b surface antigen", "انتجين سطحي لالتهاب الكبد ب"],
        "unit": "",
        "arabic_name": "مستضد التهاب الكبد B",
        "category": "Hepatitis",
        "value_type": "qualitative",
        "normal_values": ["negative", "non reactive", "non-reactive"],
    },
    "HCV Ab": {
        "aliases": ["hcv ab", "hcv antibody", "anti hcv", "أجسام مضادة لالتهاب الكبد سي"],
        "unit": "",
        "arabic_name": "أجسام مضادة لالتهاب الكبد C",
        "category": "Hepatitis",
        "value_type": "qualitative",
        "normal_values": ["negative", "non reactive", "non-reactive"],
    },

    "Urine Color": {
        "aliases": ["colour", "color"],
        "unit": "",
        "arabic_name": "لون البول",
        "category": "Urine",
        "value_type": "qualitative",
        "normal_values": ["yellow", "pale yellow", "straw", "amber"],
    },
    "Urine Appearance": {
        "aliases": ["appearance", "turbidity"],
        "unit": "",
        "arabic_name": "مظهر البول",
        "category": "Urine",
        "value_type": "qualitative",
        "normal_values": ["clear", "transparent"],
    },
    "Urine pH": {
        "aliases": ["urine ph", "ph"],
        "unit": "",
        "arabic_name": "درجة حموضة البول",
        "category": "Urine",
        "low": 4.5, "high": 8.0,
    },
    "Urine Protein": {
        "aliases": ["protein in urine", "urine protein", "albumin (urine)"],
        "unit": "",
        "arabic_name": "بروتين في البول",
        "category": "Urine",
        "value_type": "qualitative",
        "normal_values": ["negative", "nil", "absent"],
    },
    "Urine Glucose": {
        "aliases": ["glucose in urine", "sugar in urine", "urine glucose", "urine sugar"],
        "unit": "",
        "arabic_name": "سكر في البول",
        "category": "Urine",
        "value_type": "qualitative",
        "normal_values": ["negative", "nil", "absent"],
    },
    "Urine RBCs": {
        "aliases": ["rbcs", "red blood cells"],
        "unit": "/HPF",
        "arabic_name": "كرات دم حمراء في البول",
        "category": "Urine",
        "low": 0, "high": 3,
    },
    "Urine WBCs": {
        "aliases": ["wbcs", "pus cells"],
        "unit": "/HPF",
        "arabic_name": "خلايا صديد في البول",
        "category": "Urine",
        "low": 0, "high": 5,
    },
    "Urine Bacteria": {
        "aliases": ["bacteria (urine)"],
        "unit": "",
        "arabic_name": "بكتيريا في البول",
        "category": "Urine",
        "value_type": "qualitative",
        "normal_values": ["negative", "nil", "absent", "few", "rare"],
    },

    "Stool Color": {
        "aliases": ["stool colour", "stool color", "colour", "color"],
        "unit": "",
        "arabic_name": "لون البراز",
        "category": "Stool",
        "value_type": "qualitative",
        "normal_values": ["brown", "yellowish brown"],
    },
    "Stool Consistency": {
        "aliases": ["consistency"],
        "unit": "",
        "arabic_name": "قوام البراز",
        "category": "Stool",
        "value_type": "qualitative",
        "normal_values": ["formed", "semi-formed"],
    },
    "Stool Reaction": {
        "aliases": ["reaction"],
        "unit": "",
        "arabic_name": "تفاعل البراز (حموضة)",
        "category": "Stool",
        "value_type": "qualitative",
        "normal_values": ["acidic", "neutral", "alkaline"],
    },
    "Occult Blood": {
        "aliases": ["occult blood", "blood (stool)", "دم خفي في البراز"],
        "unit": "",
        "arabic_name": "دم خفي في البراز",
        "category": "Stool",
        "value_type": "qualitative",
        "normal_values": ["negative", "nil", "absent"],
    },
    "Stool Parasites": {
        "aliases": ["ova", "ova and parasites", "طفيليات"],
        "unit": "",
        "arabic_name": "بويضات الطفيليات (Ova) في البراز",
        "category": "Stool",
        "value_type": "qualitative",
        "normal_values": ["negative", "nil", "absent", "not seen"],
    },
    "Stool Cysts": {
        "aliases": ["cysts"],
        "unit": "",
        "arabic_name": "أكياس طفيلية (Cysts) في البراز",
        "category": "Stool",
        "value_type": "qualitative",
        "normal_values": ["negative", "nil", "absent", "not seen"],
    },
    "Stool Trophozoite": {
        "aliases": ["trophozoite", "trophozoites"],
        "unit": "",
        "arabic_name": "الطور المتحرك للطفيليات (Trophozoite) في البراز",
        "category": "Stool",
        "value_type": "qualitative",
        "normal_values": ["negative", "nil", "absent", "not seen"],
    },
    "Stool Mucus": {
        "aliases": ["mucus"],
        "unit": "",
        "arabic_name": "مخاط في البراز",
        "category": "Stool",
        "value_type": "qualitative",
        "normal_values": ["negative", "nil", "absent"],
    },
    "Stool RBCs": {
        "aliases": ["rbcs", "red blood cells"],
        "unit": "/HPF",
        "arabic_name": "كرات دم حمراء في البراز",
        "category": "Stool",
        "low": 0, "high": 4,
    },
    "Stool Pus Cells": {
        "aliases": ["pus", "pus cells", "wbcs"],
        "unit": "/HPF",
        "arabic_name": "خلايا صديد في البراز",
        "category": "Stool",
        "low": 0, "high": 10,
    },
    "Stool Odour": {
        "aliases": ["odour", "odor"],
        "unit": "",
        "arabic_name": "رائحة البراز",
        "category": "Stool",
        "value_type": "qualitative",
        "normal_values": ["offensive", "normal", "characteristic"],
    },
    "Stool Worms": {
        "aliases": ["worms"],
        "unit": "",
        "arabic_name": "ديدان في البراز",
        "category": "Stool",
        "value_type": "qualitative",
        "normal_values": ["negative", "nil", "absent", "not seen"],
    },
    "Stool Food Particles": {
        "aliases": ["food particles"],
        "unit": "",
        "arabic_name": "بقايا طعام غير مهضوم في البراز",
        "category": "Stool",
        "value_type": "qualitative",
        "normal_values": ["negative", "nil", "absent"],
    },
    "Stool Fat": {
        "aliases": ["fat"],
        "unit": "",
        "arabic_name": "دهون غير مهضومة في البراز",
        "category": "Stool",
        "value_type": "qualitative",
        "normal_values": ["negative", "nil", "absent", "+"],
    },
    "Stool Starch": {
        "aliases": ["starch"],
        "unit": "",
        "arabic_name": "نشا غير مهضوم في البراز",
        "category": "Stool",
        "value_type": "qualitative",
        "normal_values": ["negative", "nil", "absent", "+"],
    },
    "Stool Vegetable Fibers": {
        "aliases": ["vegetable", "vegetable fibers"],
        "unit": "",
        "arabic_name": "ألياف نباتية في البراز",
        "category": "Stool",
        "value_type": "qualitative",
        "normal_values": ["negative", "nil", "absent", "+", "++"],
    },
    "Stool Muscle Fibers": {
        "aliases": ["muscle fibers", "muscle fibres"],
        "unit": "",
        "arabic_name": "ألياف عضلية غير مهضومة في البراز",
        "category": "Stool",
        "value_type": "qualitative",
        "normal_values": ["negative", "nil", "absent", "+"],
    },
}


def get_all_aliases():
    """Build a lookup dict mapping every known alias string to its standard test name."""
    alias_map = {}
    for test_name, info in REFERENCE_VALUES.items():
        for alias in info["aliases"]:
            alias_map[alias.lower().strip()] = test_name
    return alias_map


def get_reference_range(test_name: str, sex: str = None):
    """Return the (low, high) normal range for a test, accounting for sex-specific ranges if defined."""
    info = REFERENCE_VALUES.get(test_name)
    if not info:
        return None, None

    if "sex_specific" in info:
        if sex in ("male", "female"):
            rng = info["sex_specific"][sex]
            return rng["low"], rng["high"]
        else:
            # No sex provided: fall back to the widest combined range across sexes
            lows = [v["low"] for v in info["sex_specific"].values()]
            highs = [v["high"] for v in info["sex_specific"].values()]
            return min(lows), max(highs)

    return info.get("low"), info.get("high")


def resolve_numeric_reference(test_name: str, printed_range, sex: str = None):
    """Decide whether to trust the printed reference range from the report or fall back to the stored one."""
    stored_low, stored_high = get_reference_range(test_name, sex)

    if not printed_range or stored_low is None or stored_high is None:
        return stored_low, stored_high, "stored"

    printed_low, printed_high = printed_range

    stored_mid = (stored_low + stored_high) / 2
    printed_mid = (printed_low + printed_high) / 2

    if stored_mid == 0:
        return stored_low, stored_high, "stored"

    # Likely OCR digit loss (e.g. "40-75" misread as "0-75"): reject and fall back
    if printed_low == 0 and stored_low > 0.15 * stored_high:
        return stored_low, stored_high, "stored"

    # Accept the printed range only if its midpoint is reasonably close to the stored one
    ratio = printed_mid / stored_mid
    if 0.55 <= ratio <= 1.8:
        return printed_low, printed_high, "printed"

    return stored_low, stored_high, "stored"
