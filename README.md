[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/N3kLi3ZO)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23640731&assignment_repo_type=AssignmentRepo)
# Blockchain Dashboard Project

Use this repository to build your blockchain dashboard project.
Update this README every week.

## Student Information

| Field | Value |
|---|---|
| Student Name |Enrique|
| GitHub Username |esantrui|
| Project Title |CryptoChain Analyzer|
| Chosen AI Approach |Predictor|

## Module Tracking

Use one of these values: `Not started`, `In progress`, `Done`

| Module | What it should include | Status |
|---|---|---|
| M1 | Proof of Work Monitor | Done |
| M2 | Block Header Analyzer | Done |
| M3 | Difficulty History | Done |
| M4 | AI Component | Done |

## Current Progress

Write 3 to 5 short lines about what you have already done.

- Implemented M1 (PoW Monitor) with live block metrics: height, nonce, bits, transactions, and block age calculation.
- Implemented M2 (Block Header Analyzer) with block lookup, UTC timestamp formatting, and raw JSON inspection.
- Implemented M3 (Difficulty History) with moving average, logarithmic scale options, and period-change KPIs.
- Implemented M4 (AI Component) with ARIMA(1,2,1), SARIMA with fallback, and Holt-Winters exponential smoothing for forecasting.
- Fixed blockchain.info API endpoint (switched from /charts to /api.blockchain.info), added statsmodels dependency, and deployed all code to production repo.

## Next Step

Write the next small step you will do before the next class.

- Add screenshots and interpretation notes for each module's output; refine UI/UX for better readability and document model performance metrics.

## Main Problem or Blocker

Write here if you are stuck with something.

- None. All 4 milestones completed and deployed successfully. SARIMA convergence issues resolved with automatic fallback to stable parameters.

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

```text
template-blockchain-dashboard/
|-- README.md
|-- requirements.txt
|-- .gitignore
|-- app.py
|-- api/
|   `-- blockchain_client.py
`-- modules/
    |-- m1_pow_monitor.py
    |-- m2_block_header.py
    |-- m3_difficulty_history.py
    `-- m4_ai_component.py
```

<!-- student-repo-auditor:teacher-feedback:start -->
## Teacher Feedback

### Kick-off Review

Review time: 2026-04-29 20:31 CEST
Status: Amber

Strength:
- I can see the dashboard structure integrating the checkpoint modules.

Improve now:
- M2 still needs clearer block-header verification with hashlib and target logic.

Next step:
- Add local block-header verification with hashlib and show the Proof of Work check clearly.
<!-- student-repo-auditor:teacher-feedback:end -->
