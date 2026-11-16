# External Credit Bureau Reports

## 1. Purpose

This document contains illustrative external credit bureau information for five corporate customers.

The reports provide credit scores, repayment observations, adverse record indicators, and report statuses for use in the credit risk assessment workflow.

**Data classification:** Synthetic sample data. These are not actual reports issued by Dun & Bradstreet (D&B), CIBIL, or any other credit bureau.

## 2. Credit Bureau Reports

### 2.1 Apex Manufacturing Pvt Ltd

| Field | Value |
|---|---|
| Company Name | Apex Manufacturing Pvt Ltd |
| Registration Number | U29299KA2018PTC112345 |
| GSTIN | 29AABCA1234F1Z5 |
| Industry | Manufacturing |
| Financial Year | 2025 |
| External Credit Bureau | Illustrative D&B-style report |
| Bureau Score | 720 |
| Report Reference | SAMPLE-CB-2025-001 |
| Report Date | 31 December 2025 |
| Credit Bureau Status | Good Standing |
| Payment History | Regular repayments |
| Adverse Records | None reported |
| Outstanding Disputes | None reported |
| Report Availability | Available |
| Assessment Status | Eligible for automated scoring |

**Assessment Observation:** Apex Manufacturing Pvt Ltd has an illustrative bureau score of 720, indicating a relatively strong external credit profile under the configured scoring thresholds. No adverse records are reported in this sample.

### 2.2 Bluewave Technologies Pvt Ltd

| Field | Value |
|---|---|
| Company Name | Bluewave Technologies Pvt Ltd |
| Registration Number | U72900KA2019PTC123456 |
| GSTIN | 29AABCB2345F1Z4 |
| Industry | IT Services |
| Financial Year | 2025 |
| External Credit Bureau | Illustrative D&B-style report |
| Bureau Score | 745 |
| Report Reference | SAMPLE-CB-2025-002 |
| Report Date | 31 December 2025 |
| Credit Bureau Status | Good Standing |
| Payment History | Consistent repayments |
| Adverse Records | None reported |
| Outstanding Disputes | None reported |
| Report Availability | Available |
| Assessment Status | Eligible for automated scoring |

**Assessment Observation:** Bluewave Technologies Pvt Ltd has an illustrative bureau score of 745. Its sample repayment history is consistent, with no reported adverse records.

### 2.3 Greenfield Agro Industries Pvt Ltd

| Field | Value |
|---|---|
| Company Name | Greenfield Agro Industries Pvt Ltd |
| Registration Number | U01100KA2020PTC134567 |
| GSTIN | 29AABCG3456H1Z3 |
| Industry | Agro Processing |
| Financial Year | 2025 |
| External Credit Bureau | Illustrative D&B-style report |
| Bureau Score | 635 |
| Report Reference | SAMPLE-CB-2025-003 |
| Report Date | 31 December 2025 |
| Credit Bureau Status | Moderate Credit Standing |
| Payment History | Limited repayment history |
| Adverse Records | No major adverse records reported |
| Outstanding Disputes | None reported |
| Report Availability | Available |
| Assessment Status | Eligible for partial scoring, industry review pending |

**Assessment Observation:** Greenfield Agro Industries Pvt Ltd has an illustrative bureau score of 635. Its limited repayment history requires consideration during the assessment.

**Manual Review Requirement:** Agro Processing is not included in the configured industry risk matrix. The company must undergo industry risk review before an automated final risk classification can be produced.

### 2.4 Sunrise Infrastructure Ltd

| Field | Value |
|---|---|
| Company Name | Sunrise Infrastructure Ltd |
| Registration Number | U45201KA2017PLC098765 |
| GSTIN | 29AABCS4567J1Z2 |
| Industry | Construction |
| Financial Year | 2025 |
| External Credit Bureau | Illustrative D&B-style report |
| Bureau Score | 580 |
| Report Reference | SAMPLE-CB-2025-004 |
| Report Date | 31 December 2025 |
| Credit Bureau Status | Poor Credit Standing |
| Payment History | Delayed repayments reported |
| Adverse Records | Adverse payment history reported |
| Outstanding Disputes | None reported |
| Report Availability | Available |
| Assessment Status | Eligible for automated scoring with high-risk indicators |

**Assessment Observation:** Sunrise Infrastructure Ltd has an illustrative bureau score of 580, placing it in the lowest bureau scoring band. Its delayed repayment history and adverse payment indicators require attention during credit assessment.

### 2.5 Metroline Auto Components Pvt Ltd

| Field | Value |
|---|---|
| Company Name | Metroline Auto Components Pvt Ltd |
| Registration Number | U34300KA2021PTC145678 |
| GSTIN | 29AABCM5678K1Z1 |
| Industry | Manufacturing |
| Financial Year | 2025 |
| External Credit Bureau | Illustrative D&B-style report |
| Bureau Score | 690 |
| Report Reference | SAMPLE-CB-2025-005 |
| Report Date | 31 December 2025 |
| Credit Bureau Status | Satisfactory Credit Standing |
| Payment History | Generally regular with minor delays |
| Adverse Records | Minor payment delays reported |
| Outstanding Disputes | None reported |
| Report Availability | Available |
| Assessment Status | Eligible for automated scoring |

**Assessment Observation:** Metroline Auto Components Pvt Ltd has an illustrative bureau score of 690. Its repayment history is generally satisfactory, although minor payment delays are reported.

## 3. Consolidated Credit Bureau Comparison

| Company | Industry | Bureau Score | Credit Bureau Status | Adverse Records |
|---|---|---:|---|---|
| Apex Manufacturing Pvt Ltd | Manufacturing | 720 | Good Standing | None reported |
| Bluewave Technologies Pvt Ltd | IT Services | 745 | Good Standing | None reported |
| Greenfield Agro Industries Pvt Ltd | Agro Processing | 635 | Moderate Credit Standing | No major adverse records |
| Sunrise Infrastructure Ltd | Construction | 580 | Poor Credit Standing | Adverse payment history |
| Metroline Auto Components Pvt Ltd | Manufacturing | 690 | Satisfactory Credit Standing | Minor payment delays |

## 4. External Credit Bureau Scoring Rules

The credit risk assessment uses the following bureau score thresholds.

| Bureau Score | Awarded Points | Scoring Interpretation |
|---|---:|---|
| 700 and above | 15 | Strong |
| 650–699 | 10 | Satisfactory |
| 600–649 | 5 | Moderate |
| Below 600 | 0 | Weak |

### 4.1 Sample Bureau Score Calculation

| Company | Bureau Score | Awarded Points |
|---|---:|---:|
| Apex Manufacturing Pvt Ltd | 720 | 15 |
| Bluewave Technologies Pvt Ltd | 745 | 15 |
| Greenfield Agro Industries Pvt Ltd | 635 | 5 |
| Sunrise Infrastructure Ltd | 580 | 0 |
| Metroline Auto Components Pvt Ltd | 690 | 10 |

## 5. Credit Bureau Interpretation Rules

1. Use the exact company name to retrieve the corresponding bureau report.
2. Do not assign a bureau score based on another company's report.
3. Use the score recorded in the corresponding company report.
4. Apply the scoring thresholds consistently across all five companies.
5. Consider repayment history and adverse records separately from the numerical bureau score.
6. A high bureau score does not automatically approve a credit application.
7. A low bureau score must be reflected in the external credit bureau component of the scorecard.
8. An unavailable bureau report must be reported as missing information. Do not invent a replacement score.
9. Distinguish between a bureau score, bureau status, and final credit risk category.

## 6. Data Consistency

The company names, registration numbers, GSTINs, industries, and FY2025 bureau scores in this document must match the corresponding records in:

- `company_documents.md`
- `financial_data.md`
- `credit_risk_assessment_rules.md`

All bureau scores, report references, dates, and observations are illustrative sample data created for demonstration purposes.