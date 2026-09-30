# Add references
from fastmcp import FastMCP


# Create an MCP server
mcp = FastMCP(name="CreditRisk")


# Add a document verification MCP tool
@mcp.tool()
def verify_documents(
    company_name: str,
    registration_certificate: str,
    gst_certificate: str,
) -> str:
    """Verify whether the required company documents are available and company names match."""

    missing = []

    if (
        not registration_certificate
        or registration_certificate.strip().lower() == "missing"
    ):
        missing.append("company registration certificate")

    if (
        not gst_certificate
        or gst_certificate.strip().lower() == "missing"
    ):
        missing.append("GST certificate")

    if missing:
        return f"Missing required documents: {', '.join(missing)}."

    company_name_lower = company_name.strip().lower()

    if (
        company_name_lower not in registration_certificate.lower()
        or company_name_lower not in gst_certificate.lower()
    ):
        return "Company name mismatch across documents."

    return "Documents available and company names match."


# Add a financial ratio calculation MCP tool
@mcp.tool()
def calculate_financial_ratios(
    current_assets: float,
    current_liabilities: float,
    total_debt: float,
    equity: float,
    net_profit: float,
    revenue: float,
) -> str:
    """Calculate current ratio, debt-to-equity ratio, and net profit margin."""

    current_ratio = (
        current_assets / current_liabilities
        if current_liabilities
        else None
    )

    debt_to_equity = (
        total_debt / equity
        if equity
        else None
    )

    net_profit_margin = (
        (net_profit / revenue) * 100
        if revenue
        else None
    )

    return (
        f"Current Ratio: {current_ratio:.2f}\n"
        f"Debt-to-Equity Ratio: {debt_to_equity:.2f}\n"
        f"Net Profit Margin: {net_profit_margin:.2f}%"
    )


# Add a credit-risk summary MCP tool
@mcp.tool()
def generate_risk_summary(
    company_name: str,
    current_ratio: float,
    debt_to_equity_ratio: float,
    net_profit_margin: float,
) -> str:
    """Generate a credit-risk summary based on the provided financial ratios."""

    if (
        current_ratio >= 1.5
        and debt_to_equity_ratio <= 1.0
        and net_profit_margin >= 5.0
    ):
        risk_level = "Low"
        liquidity = "Strong"
        leverage = "Low"
        profitability = "Healthy"

    elif (
        current_ratio >= 1.0
        and debt_to_equity_ratio <= 2.0
        and net_profit_margin >= 0
    ):
        risk_level = "Medium"
        liquidity = "Adequate"
        leverage = "Moderate"
        profitability = "Acceptable"

    else:
        risk_level = "High"
        liquidity = "Weak"
        leverage = "High"
        profitability = "Weak"

    return (
        f"Credit-risk summary for {company_name}:\n\n"
        f"- Risk level: {risk_level}\n"
        f"- Liquidity: {liquidity}, with a current ratio of {current_ratio}\n"
        f"- Leverage: {leverage}, with a debt-to-equity ratio of "
        f"{debt_to_equity_ratio}\n"
        f"- Profitability: {profitability}, with a net profit margin of "
        f"{net_profit_margin}%\n\n"
        f"Overall assessment: The company appears financially stable "
        f"based on the provided ratios."
    )


# Run the MCP server
mcp.run(show_banner=False)