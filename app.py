#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tempfile
import traceback
from typing import Optional

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from main import analyze_lab_result
from predictor import predict_cbc, is_cbc_report

app = FastAPI(
    title="Lab Result Analyzer API",
    description="Analyzes medical lab result images and returns structured JSON reports with optional ML-based CBC diagnosis.",
    version="1.0.0",
)

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}


def _is_allowed(filename: str) -> bool:
    """Check whether the uploaded file extension is supported."""
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


@app.get("/health")
def health_check():
    """Liveness check used by Railway and the .NET backend."""
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(..., description="Lab result image or PDF"),
    sex: Optional[str] = Form(None, description="Patient sex: 'male' or 'female'"),
):
    """
    Main endpoint: receive a lab result file and return a full analysis report as JSON.

    Response fields:
    - success         : whether processing succeeded
    - summary         : counts of normal / high / low / abnormal results
    - results         : per-test breakdown (value, reference range, status)
    - ml_prediction   : CBC ML diagnosis if enough features were extracted, else null
    - quality_warning : present if image resolution is too low
    """
    if not _is_allowed(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Supported: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    if sex not in (None, "", "male", "female"):
        sex = None

    ext = os.path.splitext(file.filename)[1].lower()

    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        # Step 1: OCR + rule-based analysis
        report = analyze_lab_result(tmp_path, sex=sex, verbose=False)

        # Step 2: CBC ML prediction (only if enough features extracted)
        ml_prediction = None
        if report["results"] and is_cbc_report(report["results"]):
            numeric_values = {
                r["test_name"]: r["value"]
                for r in report["results"]
                if r.get("value_type", "numeric") == "numeric"
                and isinstance(r.get("value"), (int, float))
            }
            if numeric_values:
                ml_prediction = predict_cbc(numeric_values)
                # predict_cbc returns None if confidence or features are insufficient

        return JSONResponse(content={
            "success":         True,
            "summary":         report["summary"],
            "results":         report["results"],
            "ml_prediction":   ml_prediction,
            "quality_warning": report.get("quality_warning"),
        })

    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error processing the file.")

    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass

# ==========================================================================
# Local development:
#   uvicorn app:app --host 0.0.0.0 --port 5000 --reload
#
# Production (Dockerfile CMD):
#   gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:${PORT:-5000} app:app
#
# Auto-generated docs after running:
#   http://localhost:5000/docs   → Swagger UI
#   http://localhost:5000/redoc → ReDoc
# ==========================================================================
