
import json
from pathlib import Path


# Load data files relative to this Python file
DATA_DIR = Path(__file__).resolve().parent / "data"


def _load_requirements(
    file_path=DATA_DIR / "document_requirements.txt"
) -> dict:
    requirements = {}

    with open(file_path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|", 1)

            if len(parts) == 2:
                requirements[parts[0]] = parts[1]

    return requirements


def _load_thresholds(
    file_path=DATA_DIR / "risk_thresholds.txt"
) -> dict:
    thresholds = {}

    with open(file_path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|", 1)

            if len(parts) == 2:
                thresholds[parts[0]] = float(parts[1])

    return thresholds


# Load multiple company records from one file
def _load_companies(
    file_path=DATA_DIR / "sample_company_data.txt"
) -> dict:
    companies = {}
    current_company = None

    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith("[") and line.endswith("]"):
                current_company = line[1:-1]
                companies[current_company] = {}
                continue

            parts = line.split("|", 1)

            if current_company and len(parts) == 2:
                key, value = parts
                companies[current_company][key] = value

    return companies


DOCUMENT_REQUIREMENTS = _load_requirements()
RISK_THRESHOLDS = _load_thresholds()
COMPANIES = _load_companies()


# Retrieve company information by name
def _get_company(company_name: str) -> dict:
    for company in COMPANIES.values():
        if company.get("company_name", "").lower() == company_name.lower():
            return company

    raise ValueError(
        f"Company '{company_name}' was not found in sample_company_data.txt."
    )


# Convert company document values to boolean
def _get_boolean(value: str) -> bool:
    return value.strip().lower() == "true"


# Verify the required company documents
def verify_documents(company_name: str) -> str:
    """Check whether the required company documents are available."""

    try:
        company = _get_company(company_name)

        company_registration = _get_boolean(
            company["company_registration"]
        )

        gst_certificate = _get_boolean(
            company["gst_certificate"]
        )

        documents_complete = (
            company_registration and gst_certificate
        )

        return json.dumps({
            "company_name": company_name,
            "required_documents": list(
                DOCUMENT_REQUIREMENTS.values()
            ),
            "company_registration": company_registration,
            "gst_certificate": gst_certificate,
            "documents_complete": documents_complete,
            "status": (
                "Documents verified"
                if documents_complete
                else "Required documents are missing"
            )
        })

    except (ValueError, KeyError) as error:
        return json.dumps({"error": str(error)})


# Calculate basic financial ratios
def calculate_financial_ratios(company_name: str) -> str:
    """Calculate financial ratios using the company's stored data."""

    try:
        company = _get_company(company_name)

        current_assets = float(company["current_assets"])
        current_liabilities = float(company["current_liabilities"])
        total_debt = float(company["total_debt"])
        equity = float(company["equity"])
        net_profit = float(company["net_profit"])
        revenue = float(company["revenue"])

        if current_liabilities <= 0:
            return json.dumps({
                "error": "Current liabilities must be greater than zero."
            })

        if equity <= 0:
            return json.dumps({
                "error": "Equity must be greater than zero."
            })

        if revenue <= 0:
            return json.dumps({
                "error": "Revenue must be greater than zero."
            })

        current_ratio = current_assets / current_liabilities
        debt_to_equity = total_debt / equity
        net_profit_margin = (net_profit / revenue) * 100

        return json.dumps({
            "company_name": company_name,
            "current_ratio": round(current_ratio, 2),
            "debt_to_equity": round(debt_to_equity, 2),
            "net_profit_margin": round(net_profit_margin, 2),
            "thresholds": RISK_THRESHOLDS
        })

    except (ValueError, KeyError) as error:
        return json.dumps({"error": str(error)})


# Generate a simple credit-risk summary
def generate_risk_summary(company_name: str) -> str:
    """Generate a credit-risk summary using stored company information."""

    try:
        company = _get_company(company_name)

        current_assets = float(company["current_assets"])
        current_liabilities = float(company["current_liabilities"])
        total_debt = float(company["total_debt"])
        equity = float(company["equity"])
        net_profit = float(company["net_profit"])
        revenue = float(company["revenue"])

        if current_liabilities <= 0 or equity <= 0 or revenue <= 0:
            return json.dumps({
                "error": "Invalid financial data for risk assessment."
            })

        current_ratio = current_assets / current_liabilities
        debt_to_equity = total_debt / equity
        net_profit_margin = (net_profit / revenue) * 100

        if (
            current_ratio >= RISK_THRESHOLDS["current_ratio_good"]
            and debt_to_equity <= RISK_THRESHOLDS["debt_to_equity_good"]
            and net_profit_margin >= RISK_THRESHOLDS["net_profit_margin_good"]
        ):
            risk_level = "Low"

        elif (
            current_ratio >= RISK_THRESHOLDS["current_ratio_medium"]
            and debt_to_equity <= RISK_THRESHOLDS["debt_to_equity_medium"]
            and net_profit_margin >= RISK_THRESHOLDS["net_profit_margin_medium"]
        ):
            risk_level = "Medium"

        else:
            risk_level = "High"

        return json.dumps({
            "company_name": company_name,
            "current_ratio": round(current_ratio, 2),
            "debt_to_equity": round(debt_to_equity, 2),
            "net_profit_margin": round(net_profit_margin, 2),
            "risk_level": risk_level,
            "status": "Risk summary generated successfully"
        })

    except (ValueError, KeyError) as error:
        return json.dumps({"error": str(error)})
