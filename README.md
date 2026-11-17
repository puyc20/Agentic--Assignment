# Resume Agent Automation Framework

This project implements a modular, data-driven automation framework for validating a Resume Updating Agent using Python, Playwright, Pytest, Ollama, and DeepEval.

## Objective

The framework follows the assignment flow:

Excel manual test cases -> test case reader -> validation -> Ollama-based input generation -> Playwright UI automation -> transcript capture -> DeepEval LLM-as-a-Judge -> reporting.

## Project Structure

```text
resume_agent_automation/
  config/settings.py
  integrations/ollama_client.py
  integrations/deepeval_judge.py
  pages/base_page.py
  pages/resume_agent_page.py
  tests/conftest.py
  tests/test_resume_agent.py
  tests/test_deepeval.py
  evaluations/metrics.py
  evaluations/evaluation_runner.py
  utils/excel_reader.py
  utils/transcript_manager.py
  utils/test_data_manager.py
  utils/logger.py
  prompts/prompt_templates.py
  main.py
  test_data/manual_test_cases.xlsx
  transcripts/
  reports/
  screenshots/
  logs/
```

## Prerequisites

- Python 3.11+
- Playwright Python
- Pytest
- Ollama installed and running locally
- DeepEval installed
- Browser dependencies for Playwright (`playwright install`)

## Setup

1. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
playwright install chromium
```

3. Configure environment variables:

```bash
cp .env.example .env
```

Update the values in `.env` with the real application credentials and local service settings. Do not commit `.env`.

## Ollama Setup

1. Install Ollama from https://ollama.com/download
2. Start the service:

```bash
ollama serve
```

3. Download the judge/generation model:

```bash
ollama pull gemma2:2b
ollama list
```

4. Verify the service is reachable:

```bash
curl http://localhost:11434/api/tags
```

## Running Tests

### Run just the smoke login test

```bash
pytest resume_agent_automation/tests/test_resume_agent.py -k login_smoke -q
```

### Run the DeepEval checks

```bash
pytest resume_agent_automation/tests/test_deepeval.py -q
```

### Run the full suite

```bash
pytest -q
```

## Running the evaluation independently

```bash
python -m resume_agent_automation.main --pytest resume_agent_automation/tests/test_deepeval.py
```

## Manual test case source

The framework reads the workbook in `resume_agent_automation/test_data/manual_test_cases.xlsx` and tracks the source manual scenarios in the automated tests.

## Transcript and report location

- JSON transcripts: `resume_agent_automation/transcripts/`
- Screenshots: `resume_agent_automation/screenshots/`
- HTML/CSV reports: `resume_agent_automation/reports/`
- Logs: `resume_agent_automation/logs/`

## Important note about the target Resume Updating Agent

This workspace contains the assignment materials and the required framework skeleton, but the actual Resume Updating Agent provided in the assignment does not currently expose the requested resume-editing workflow in this environment. The automation layer is therefore designed to:

- log in to the provided authenticated app,
- read the manual scenario workbook,
- skip the resume-agent workflow when the feature is not available,
- keep the framework ready for real execution when the target feature is enabled.

To execute the full resume-agent workflow, set:

```bash
RESUME_AGENT_ENABLED=true
```

and ensure the Resume Updating Agent is reachable in the app after login.

## Troubleshooting

- `playwright install` failed: install the Chromium dependencies for your OS.
- `Ollama model not found`: run `ollama pull gemma2:2b` and restart the service.
- `401` or login failure: check `.env` credentials and the application URL.
- `No resume workflow found`: verify the feature is enabled in the application and the selectors match the live UI.
