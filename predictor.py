# -*- coding: utf-8 -*-

import os
import json
import pickle
import numpy as np
import pandas as pd

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_MODEL_PATH    = os.path.join(_BASE_DIR, "cbc_model.pkl")
_ENCODER_PATH  = os.path.join(_BASE_DIR, "cbc_label_encoder.pkl")
_METADATA_PATH = os.path.join(_BASE_DIR, "cbc_model_metadata.json")

_model    = None
_encoder  = None
_metadata = None

# Arabic translations for all possible predictions shown to the patient.
DIAGNOSIS_TRANSLATIONS = {
    "Healthy":                          "طبيعي - لا توجد مشكلة",
    "Iron deficiency anemia":           "فقر الدم بنقص الحديد",
    "Leukemia":                         "ابيضاض الدم (اللوكيميا)",
    "Leukemia with thrombocytopenia":   "ابيضاض الدم مع نقص الصفائح الدموية",
    "Macrocytic anemia":                "فقر الدم الضخم الخلايا",
    "Normocytic hypochromic anemia":    "فقر الدم ناقص الصبغة طبيعي الحجم",
    "Normocytic normochromic anemia":   "فقر الدم طبيعي الحجم والصبغة",
    "Other microcytic anemia":          "فقر الدم صغير الخلايا (أنواع أخرى)",
    "Thrombocytopenia":                 "نقص الصفائح الدموية",
}

# Minimum confidence to return a prediction.
# Below this threshold we return None instead of a low-confidence guess.
MIN_CONFIDENCE = 0.50

# Minimum number of the 10 reliably-extractable features that must be present
# before we attempt a prediction.
MIN_FEATURES_REQUIRED = 5

# Map every name the OCR/parser may produce → the model's feature name.
# The model was trained on short codes; the parser produces full English names.
OCR_TO_MODEL = {
    # WBC
    "WBC":                  "WBC",
    "WHITE BLOOD CELLS":    "WBC",
    "WHITE CELLS COUNT":    "WBC",
    "WHITE CELL COUNT":     "WBC",
    "LEUKOCYTES":           "WBC",

    # RBC
    "RBC":                  "RBC",
    "RED BLOOD CELLS":      "RBC",
    "RED CELLS COUNT":      "RBC",
    "RED CELL COUNT":       "RBC",
    "ERYTHROCYTES":         "RBC",

    # HGB
    "HEMOGLOBIN":           "HGB",
    "HAEMOGLOBIN":          "HGB",
    "HGB":                  "HGB",
    "HB":                   "HGB",

    # HCT
    "HEMATOCRIT":           "HCT",
    "HAEMATOCRIT":          "HCT",
    "HCT":                  "HCT",
    "PCV":                  "HCT",

    # MCV
    "MCV":                  "MCV",

    # MCH
    "MCH":                  "MCH",

    # MCHC
    "MCHC":                 "MCHC",

    # PLT
    "PLATELETS":            "PLT",
    "PLT":                  "PLT",
    "PLATELET COUNT":       "PLT",
    "THROMBOCYTES":         "PLT",

    # NEUTp  (percentage - what reports usually show)
    "NEUTROPHILS":          "NEUTp",
    "NEUTP":                "NEUTp",
    "NEUT":                 "NEUTp",

    # LYMp  (percentage)
    "LYMPHOCYTES":          "LYMp",
    "LYMP":                 "LYMp",
    "LYMPHS":               "LYMp",

    # NEUTn  (absolute count - rare in reports, ignored if missing)
    "NEUTN":                "NEUTn",
    "ABSOLUTE NEUTROPHILS": "NEUTn",

    # LYMn  (absolute count - rare)
    "LYMN":                 "LYMn",
    "ABSOLUTE LYMPHOCYTES": "LYMn",

    # PDW  (rare)
    "PDW":                  "PDW",
    "PLATELET DISTRIBUTION WIDTH": "PDW",

    # PCT  (very rare)
    "PCT":                  "PCT",
    "PLATELETCRIT":         "PCT",
}

# The 10 features the OCR can reliably extract — used for the min-feature gate.
RELIABLE_FEATURES = {"WBC","RBC","HGB","HCT","MCV","MCH","MCHC","PLT","NEUTp","LYMp"}


def _load():
    """Load model, encoder, and metadata from disk once at startup."""
    global _model, _encoder, _metadata
    if _model is not None:
        return
    if not os.path.exists(_MODEL_PATH):
        raise FileNotFoundError(f"CBC model not found: {_MODEL_PATH}")
    with open(_MODEL_PATH,    "rb") as f: _model   = pickle.load(f)
    with open(_ENCODER_PATH,  "rb") as f: _encoder = pickle.load(f)
    with open(_METADATA_PATH, "r")  as f: _metadata = json.load(f)


def is_cbc_report(results: list) -> bool:
    """
    Return True if the extracted results contain enough CBC features
    to attempt an ML prediction (at least MIN_FEATURES_REQUIRED reliable ones).
    """
    _load()
    found = set()
    for r in results:
        key = OCR_TO_MODEL.get(r.get("test_name", "").upper())
        if key and key in RELIABLE_FEATURES:
            found.add(key)
    return len(found) >= MIN_FEATURES_REQUIRED


def predict_cbc(test_values: dict) -> dict | None:
    """
    Run the CBC classifier and return a prediction dict, or None if:
    - fewer than MIN_FEATURES_REQUIRED reliable features are present, or
    - the model's confidence is below MIN_CONFIDENCE.

    Args:
        test_values: {test_name: numeric_value} as produced by the OCR parser.

    Returns:
        {
          "prediction":    "Iron deficiency anemia",
          "prediction_ar": "فقر الدم بنقص الحديد",
          "confidence":    0.91,
          "all_probabilities": {"Healthy": 0.02, ...},
          "features_used":    [...],
          "features_missing": [...],
        }
        or None if prediction is not reliable enough.
    """
    _load()

    required = _metadata["features"]   # exact order the model expects
    classes  = _metadata["classes"]

    # Build a canonical lookup: MODEL_FEATURE_NAME → value
    canonical = {}
    for raw_name, value in test_values.items():
        model_key = OCR_TO_MODEL.get(raw_name.upper())
        if model_key:
            canonical[model_key] = float(value)

    # Gate: enough reliable features?
    reliable_found = {k for k in canonical if k in RELIABLE_FEATURES}
    if len(reliable_found) < MIN_FEATURES_REQUIRED:
        return None

    # Build feature vector (0.0 for any feature the report didn't include)
    vector        = []
    features_used = []
    features_miss = []

    for feat in required:
        if feat in canonical:
            vector.append(canonical[feat])
            features_used.append(feat)
        else:
            vector.append(0.0)
            features_miss.append(feat)

    X = pd.DataFrame([vector], columns=required)

    pred_idx  = _model.predict(X)[0]
    proba     = _model.predict_proba(X)[0]
    confidence = float(proba[pred_idx])

    # Gate: confidence high enough?
    if confidence < MIN_CONFIDENCE:
        return None

    prediction = _encoder.inverse_transform([pred_idx])[0]

    all_proba = {
        cls: round(float(p), 4)
        for cls, p in zip(classes, proba)
    }

    return {
        "prediction":        prediction,
        "prediction_ar":     DIAGNOSIS_TRANSLATIONS.get(prediction, prediction),
        "confidence":        round(confidence, 4),
        "all_probabilities": all_proba,
        "features_used":     features_used,
        "features_missing":  features_miss,
    }
