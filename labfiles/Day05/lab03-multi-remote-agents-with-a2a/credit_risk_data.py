from __future__ import annotations

from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent / "data"


def load_all_data() -> dict[str, str]:
    files: dict[str, str] = {}
    for path in sorted(DATA_DIR.glob("*.txt")):
        files[path.name] = path.read_text(encoding="utf-8").strip()
    return files


def _parse_key_values(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        cleaned_key = key.strip()
        cleaned_value = value.strip()
        if cleaned_key:
            values[cleaned_key] = cleaned_value
    return values


def get_company_document_data() -> dict[str, str]:
    content = load_all_data().get("company_documents.txt", "")
    return _parse_key_values(content)


def get_financial_data() -> dict[str, Any]:
    values: dict[str, Any] = {}
    content = load_all_data().get("financial_data.txt", "")
    for line in content.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        clean_key = key.strip()
        clean_value = value.strip()
        if not clean_key:
            continue
        if clean_value.isdigit() or (clean_value.replace(".", "", 1).isdigit() and clean_value.count(".") <= 1):
            try:
                values[clean_key] = float(clean_value)
            except ValueError:
                values[clean_key] = clean_value
        else:
            values[clean_key] = clean_value
    return values


def get_credit_bureau_data() -> dict[str, str]:
    content = load_all_data().get("credit_bureau_report.txt", "")
    return _parse_key_values(content)


def get_document_verification_rules() -> str:
    return load_all_data().get("document_verification_instructions.txt", "")


def get_financial_analysis_rules() -> str:
    return load_all_data().get("financial_analysis_instructions.txt", "")


def get_credit_risk_rules() -> str:
    return load_all_data().get("credit_risk_instructions.txt", "")


def get_all_relevant_context() -> str:
    data = load_all_data()
    sections = []
    for file_name in sorted(data):
        sections.append(f"--- {file_name} ---\n{data[file_name]}")
    return "\n\n".join(sections)


def get_context_for_question(question: str) -> str:
    text = question.lower()
    relevant_files = []

    if any(word in text for word in ["document", "registration", "gst", "certificate", "company documents"]):
        relevant_files.extend(["company_documents.txt", "document_verification_instructions.txt"])

    if any(word in text for word in ["ratio", "financial", "revenue", "profit", "debt", "liability", "equity", "asset"]):
        relevant_files.extend(["financial_data.txt", "financial_analysis_instructions.txt"])

    if any(word in text for word in ["bureau", "credit", "risk", "industry", "assessment"]):
        relevant_files.extend(["credit_bureau_report.txt", "credit_risk_instructions.txt"])

    if not relevant_files:
        relevant_files = sorted(load_all_data().keys())

    unique_files = []
    for name in relevant_files:
        if name not in unique_files:
            unique_files.append(name)

    data = load_all_data()
    sections = []
    for file_name in unique_files:
        if file_name in data:
            sections.append(f"--- {file_name} ---\n{data[file_name]}")
    return "\n\n".join(sections)


def compute_financial_ratios() -> dict[str, float | str]:
    financial = get_financial_data()
    current_assets = float(financial.get("Current Assets", 0) or 0)
    current_liabilities = float(financial.get("Current Liabilities", 0) or 0)
    total_debt = float(financial.get("Total Debt", 0) or 0)
    shareholders_equity = float(financial.get("Shareholders' Equity", 0) or 0)
    revenue = float(financial.get("Revenue", 0) or 0)
    net_profit = float(financial.get("Net Profit", 0) or 0)

    ratios: dict[str, float | str] = {}

    if current_liabilities != 0:
        ratios["Current Ratio"] = round(current_assets / current_liabilities, 2)
    else:
        ratios["Current Ratio"] = "Not available in the provided documents."

    if shareholders_equity != 0:
        ratios["Debt-to-Equity Ratio"] = round(total_debt / shareholders_equity, 2)
    else:
        ratios["Debt-to-Equity Ratio"] = "Not available in the provided documents."

    if revenue != 0:
        ratios["Net Profit Margin"] = round((net_profit / revenue) * 100, 2)
    else:
        ratios["Net Profit Margin"] = "Not available in the provided documents."

    return ratios
