# --------- MAKEFILE FOR KASPARR0 AGENTIC ANALYST ----------

PYTHON=python

setup:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) run.py "Analyze ROAS drop"

test:
	$(PYTHON) -m pytest -q

clean:
	del /Q logs\*.json
	del /Q reports\*.md
