# Credit Risk Assessment Rules

## 1. Purpose

This document defines the common rules used to evaluate corporate customers based on:

- Company document verification.
- Company registration and compliance checks.
- Financial statements and financial ratios.
- External credit bureau information.
- Industry risk classification.
- Overall credit risk scoring.

These rules apply consistently to all five sample companies:

1. Apex Manufacturing Pvt Ltd
2. Bluewave Technologies Pvt Ltd
3. Greenfield Agro Industries Pvt Ltd
4. Sunrise Infrastructure Ltd
5. Metroline Auto Components Pvt Ltd

**Data classification:** These rules are intended for a demonstration using synthetic sample company data. They are not a production credit policy.

## 2. Assessment Requirements

Every company assessment must consider the following information.

| Assessment Component | Required Information |
|---|---|
| Document Verification | Company Registration Certificate and GST Certificate |
| Company Validation | Company name, registration number, GSTIN and MCA status |
| Compliance | Sanctions screening and adverse compliance indicators |
| Financial Validation | Two years of financial statements |
| Liquidity | Current Assets and Current Liabilities |
| Leverage | Total Debt and Shareholders' Equity |
| Profitability | Revenue and Net Profit |
| External Credit | Latest external credit bureau score |
| Industry Risk | Industry classification and configured industry risk category |

The assessment must use the correct company record and must not combine information belonging to different companies.

## 3. Company Identification Rules

Use the following five companies as the complete demonstration dataset.

| Company Name | Registration Number | GSTIN | Industry |
|---|---|---|---|
| Apex Manufacturing Pvt Ltd | U29299KA2018PTC112345 | 29AABCA1234F1Z5 | Manufacturing |
| Bluewave Technologies Pvt Ltd | U72900KA2019PTC123456 | 29AABCB2345F1Z4 | IT Services |
| Greenfield Agro Industries Pvt Ltd | U01100KA2020PTC134567 | 29AABCG3456H1Z3 | Agro Processing |
| Sunrise Infrastructure Ltd | U45201KA2017PLC098765 | 29AABCS4567J1Z2 | Construction |
| Metroline Auto Components Pvt Ltd | U34300KA2021PTC145678 | 29AABCM5678K1Z1 | Manufacturing |

### 3.1 Identification Rules

1. Company names must match exactly across all four documents.
2. Registration numbers must match the corresponding company records.
3. GSTINs must match the corresponding company records.
4. Industry classifications must remain consistent.
5. Financial information must be retrieved using the exact company name.
6. All five companies must be available for individual and comparative queries.

## 4. Document Verification Rules

Every assessment requires:

1. Company Registration Certificate.
2. GST Certificate.

The system must verify:

- Both certificates are available.
- Both certificates are readable.
- Both certificates contain valid company information.
- Company names match the registered customer name.
- Registration numbers match the company record.
- GSTINs match the company record.
- MCA registration status is active.

### 4.1 Verification Outcomes

| Condition | Result |
|---|---|
| Both certificates are available and valid | Continue assessment |
| Company name mismatch | Flag for review |
| Registration number mismatch | Flag for review |
| GSTIN mismatch | Flag for review |
| Required certificate missing | Stop final assessment |
| Certificate unreadable | Request a valid document |
| MCA status inactive | Flag for review |

A verified document status does not automatically mean the company is eligible for credit approval.

## 5. Compliance and Sanctions Rules

The assessment must evaluate:

- MCA registration status.
- Company name consistency.
- Required document verification.
- Sanctions screening.
- Reported adverse compliance indicators.

### 5.1 Compliance Outcomes

| Condition | Action |
|---|---|
| All required documents verified, MCA active, no sanctions match | Compliance passed |
| Missing or invalid documents | Assessment hold |
| Company information mismatch | Analyst review |
| Inactive MCA status | Analyst review |
| Potential sanctions match | Mandatory analyst review |
| Confirmed sanctions match | Block automatic approval and escalate |

A potential sanctions match must not be treated as a confirmed match without investigation.

## 6. Financial Data Rules

Use Financial Year 2025 for all five companies in this demonstration.

The required financial inputs are:

- Current Assets
- Current Liabilities
- Total Debt
- Shareholders' Equity
- Revenue
- Net Profit

Financial values must be retrieved from `financial_data.md`.

### 6.1 Current Ratio

Formula:

Current Ratio = Current Assets / Current Liabilities

Scoring:

| Current Ratio | Points |
|---|---:|
| 1.50 and above | 20 |
| 1.20 to 1.49 | 15 |
| 1.00 to 1.19 | 8 |
| Below 1.00 | 0 |

### 6.2 Debt-to-Equity Ratio

Formula:

Debt-to-Equity Ratio = Total Debt / Shareholders' Equity

Scoring:

| Debt-to-Equity Ratio | Points |
|---|---:|
| 0.50 and below | 15 |
| 0.51 to 1.00 | 12 |
| 1.01 to 2.00 | 6 |
| Above 2.00 | 0 |

### 6.3 Net Profit Margin

Formula:

Net Profit Margin = (Net Profit / Revenue) × 100

Scoring:

| Net Profit Margin | Points |
|---|---:|
| 15% and above | 15 |
| 10% to 14.99% | 12 |
| 5% to 9.99% | 6 |
| Below 5% | 0 |

### 6.4 Financial Validation

- Do not calculate ratios when their denominators are zero.
- Do not calculate ratios using missing or invalid financial inputs.
- Report validation errors clearly.
- Do not estimate missing financial figures.
- Preserve the original financial values.
- Use the same financial figures whenever the company is referenced.

## 7. External Credit Bureau Rules

Retrieve the external credit bureau score from `credit_bureau_report.md`.

Apply the following scoring thresholds:

| External Credit Bureau Score | Points |
|---|---:|
| 700 and above | 15 |
| 650 to 699 | 10 |
| 600 to 649 | 5 |
| Below 600 | 0 |

### 7.1 Company Bureau Reference

| Company | Bureau Score | Points |
|---|---:|---:|
| Apex Manufacturing Pvt Ltd | 720 | 15 |
| Bluewave Technologies Pvt Ltd | 745 | 15 |
| Greenfield Agro Industries Pvt Ltd | 635 | 5 |
| Sunrise Infrastructure Ltd | 580 | 0 |
| Metroline Auto Components Pvt Ltd | 690 | 10 |

Additional rules:

- Use the latest available bureau information.
- Do not substitute another company's bureau score.
- Consider adverse payment history separately.
- Flag unavailable bureau information.
- Do not invent missing bureau information.

## 8. Industry Risk Classification Rules

The following industry risk matrix must be applied consistently.

| Industry | Industry Risk Category | Points |
|---|---|---:|
| Utilities | Low Risk | 15 |
| Government | Low Risk | 15 |
| Healthcare | Low Risk | 15 |
| Manufacturing | Medium Risk | 10 |
| FMCG Distribution | Medium Risk | 10 |
| IT Services | Medium Risk | 10 |
| Construction | High Risk | 0 |
| Real Estate Developers | High Risk | 0 |
| Airlines | High Risk | 0 |
| Commodity Trading | High Risk | 0 |
| Startups | High Risk | 0 |
| Mining and Metal | High Risk | 0 |

### 8.1 Industry Classification of the Five Companies

| Company | Industry | Industry Risk Category | Points |
|---|---|---|---:|
| Apex Manufacturing Pvt Ltd | Manufacturing | Medium Risk | 10 |
| Bluewave Technologies Pvt Ltd | IT Services | Medium Risk | 10 |
| Greenfield Agro Industries Pvt Ltd | Agro Processing | Manual Review | Not assigned |
| Sunrise Infrastructure Ltd | Construction | High Risk | 0 |
| Metroline Auto Components Pvt Ltd | Manufacturing | Medium Risk | 10 |

### 8.2 Unlisted Industry Handling

An industry that does not appear in the configured industry risk matrix must not automatically receive a Low, Medium, or High Risk classification.

For example:

Greenfield Agro Industries Pvt Ltd operates in Agro Processing.

Agro Processing is not included in the configured industry risk matrix.

Therefore:

1. Identify the industry as Agro Processing.
2. Check whether it exists in the configured risk matrix.
3. Since it is not listed, mark its industry risk as Manual Review.
4. Do not assign industry risk points automatically.
5. Do not substitute another industry's classification.
6. Request analyst review.
7. Do not produce an automatically approved final assessment until the missing industry classification has been resolved.

## 9. Credit Risk Scorecard

The overall credit risk score is calculated out of 100.

| Component | Maximum Points |
|---|---:|
| Compliance | 20 |
| Liquidity | 20 |
| Leverage | 15 |
| Profitability | 15 |
| External Credit Bureau | 15 |
| Industry Risk | 15 |
| **Total** | **100** |

### 9.1 Score Calculation

Final Score = Compliance + Liquidity + Leverage + Profitability + External Credit Bureau + Industry Risk

Every component must use the scoring thresholds defined in this document.

### 9.2 Compliance Scoring

For this demonstration:

- Award 20 points when all required documents and compliance checks pass.
- Do not award compliance points when the required checks are incomplete or invalid.
- Place the assessment on hold when compliance information is missing.
- Require analyst review for potential sanctions matches or unresolved compliance exceptions.
- Do not interpret a pending compliance check as a successful check.

### 9.3 Missing Industry Information

When the industry is not covered by the risk matrix:

- Mark the industry component as Pending Manual Review.
- Do not assign zero points as a substitute for missing classification.
- Do not calculate a definitive final score out of 100.
- Report the available score components separately.
- Require analyst review before final classification.

The same missing-information principle applies to other mandatory assessment inputs.

## 10. Overall Risk Classification

After all mandatory components are available and validated, classify the final score using these boundaries.

| Final Score | Risk Category |
|---|---|
| Above 80 | Low Risk |
| 50 to 80, inclusive | Medium Risk |
| Below 50 | High Risk |

The boundaries must be applied exactly:

- A score of 81 is Low Risk.
- A score of 80 is Medium Risk.
- A score of 50 is Medium Risk.
- A score of 49 is High Risk.

Do not change these thresholds.

## 11. Assessment Outcomes

Every company assessment must produce one of the following outcomes.

| Outcome | Description |
|---|---|
| Low Risk | Final score is above 80 and all mandatory checks are complete. |
| Medium Risk | Final score is between 50 and 80 inclusive and all mandatory checks are complete. |
| High Risk | Final score is below 50 and all mandatory checks are complete. |
| Manual Review | An unlisted industry or unresolved exception requires analyst evaluation. |
| Assessment Hold | Mandatory information is missing, invalid, or incomplete. |

A Manual Review or Assessment Hold is not an additional numerical risk category. It indicates that an automated final assessment cannot yet be completed.

## 12. Credit Recommendation Rules

Credit recommendations must consider:

- Final risk category.
- Financial ratios.
- External credit bureau information.
- Compliance status.
- Industry risk.
- Adverse payment history.
- Missing information and unresolved exceptions.

The following are general demonstration guidelines:

| Risk Category | Recommendation |
|---|---|
| Low Risk | Consider a higher credit limit and standard payment terms, subject to analyst approval. |
| Medium Risk | Consider a moderate credit limit and controlled payment terms. |
| High Risk | Consider a restricted credit limit, stricter payment terms, or further review. |
| Manual Review | Defer the recommendation until industry risk review is completed. |
| Assessment Hold | Do not issue a final credit recommendation. |

Do not invent a specific approved credit limit or payment term when the required policy inputs are unavailable.

## 13. Assessment Response Requirements

Every assessment response should include:

1. Exact company name.
2. Registration number and GSTIN when relevant.
3. Industry classification.
4. Financial year.
5. Document verification status.
6. Compliance and sanctions screening results.
7. Financial inputs.
8. Calculated financial ratios.
9. External credit bureau score.
10. Industry risk classification.
11. Individual scorecard component points.
12. Final score, when all mandatory inputs are available.
13. Final risk category, when applicable.
14. Missing information or manual review requirements.
15. Credit recommendation, when supported by the assessment.

## 14. Cross-Company Comparison Rules

When comparing companies:

- Include all five companies unless the user explicitly requests a subset.
- Use exact company names.
- Use FY2025 for financial comparisons.
- Compare equivalent financial metrics.
- Use the same bureau score thresholds.
- Use the same industry risk matrix.
- Distinguish numerical scores from manual review statuses.
- Do not rank a company as Low, Medium, or High Risk when its final assessment is incomplete.
- Identify missing or unavailable information explicitly.

## 15. Data Integrity and Source References

Use the following documents as the source of truth:

| Document | Information Provided |
|---|---|
| `company_documents.md` | Company names, registration numbers, GSTINs, industry, MCA status and document verification |
| `financial_data.md` | FY2025 financial figures and calculated ratios |
| `credit_bureau_report.md` | External credit bureau scores, report statuses and payment history |
| `credit_risk_assessment_rules.md` | Assessment formulas, scoring thresholds, industry matrix and risk classification rules |

### 15.1 Consistency Requirements

1. All four documents must contain the same five company names.
2. Company registration numbers must match wherever referenced.
3. GSTINs must match wherever referenced.
4. Industry classifications must remain consistent.
5. All financial figures must match the FY2025 financial records.
6. External credit bureau scores must match the corresponding bureau reports.
7. Document verification statuses must remain consistent.
8. No document should introduce an additional company.
9. No company should be omitted from any of the four documents.
10. All sample values must remain clearly identified as illustrative data.

## 16. Important Demonstration Disclaimer

The five companies, registration identifiers, GSTINs, financial figures, bureau scores, report references, and verification observations in this dataset are synthetic.

They are designed to demonstrate:

- Document-based information retrieval.
- Individual company credit assessments.
- Financial ratio calculations.
- External credit score interpretation.
- Industry risk classification.
- Manual review handling.
- Cross-company financial and credit risk comparisons.

They must not be represented as actual financial records, government registration records, or genuine credit bureau reports.