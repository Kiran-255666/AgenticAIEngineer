import json


def _load_requirements(
    file_path: str = "data/document_requirements.txt"
) -> dict:
    requirements = {}

    with open(file_path) as f:
        for line in f:
            parts = line.strip().split("|")

            if len(parts) == 2:
                requirements[parts[0]] = parts[1]

    return requirements


def _load_thresholds(
    file_path: str = "data/risk_thresholds.txt"
) -> dict:
    thresholds = {}

    with open(file_path) as f:
        for line in f:
            parts = line.strip().split("|")

            if len(parts) == 2:
                thresholds[parts[0]] = float(parts[1])

    return thresholds


DOCUMENT_REQUIREMENTS = _load_requirements()
RISK_THRESHOLDS = _load_thresholds()


# Verify the required company documents
def verify_documents(
    company_registration: bool,
    gst_certificate: bool
) -> str:
    """Check whether the required company documents are available."""

    documents_complete = (
        company_registration and gst_certificate
    )

    return json.dumps({
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


# Calculate basic financial ratios
def calculate_financial_ratios(
    current_assets: float,
    current_liabilities: float,
    total_debt: float,
    equity: float,
    net_profit: float,
    revenue: float
) -> str:
    """Calculate basic financial ratios for credit-risk assessment."""

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
        "current_ratio": round(current_ratio, 2),
        "debt_to_equity": round(debt_to_equity, 2),
        "net_profit_margin": round(net_profit_margin, 2),
        "thresholds": {
            "current_ratio_good": RISK_THRESHOLDS[
                "current_ratio_good"
            ],
            "current_ratio_medium": RISK_THRESHOLDS[
                "current_ratio_medium"
            ],
            "debt_to_equity_good": RISK_THRESHOLDS[
                "debt_to_equity_good"
            ],
            "debt_to_equity_medium": RISK_THRESHOLDS[
                "debt_to_equity_medium"
            ],
            "net_profit_margin_good": RISK_THRESHOLDS[
                "net_profit_margin_good"
            ],
            "net_profit_margin_medium": RISK_THRESHOLDS[
                "net_profit_margin_medium"
            ]
        }
    })


# Generate a simple credit-risk summary
def generate_risk_summary(
    company_name: str,
    current_ratio: float,
    debt_to_equity: float,
    net_profit_margin: float
) -> str:
    """Generate a summary of the calculated credit-risk indicators."""

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
        "current_ratio": current_ratio,
        "debt_to_equity": debt_to_equity,
        "net_profit_margin": net_profit_margin,
        "risk_level": risk_level,
        "status": "Risk summary generated successfully"
    })