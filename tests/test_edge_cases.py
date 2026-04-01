import pandas as pd
import pytest
from src.agents.data_agent import DataAgent
from src.agents.evaluator_agent import EvaluatorAgent

config = {
    "analysis": {"low_ctr_threshold": 0.015, "roas_drop_threshold_pct": 0.20}
}

def test_missing_columns():
    df = pd.DataFrame({
        "spend": [100, 200],
        "revenue": [400, 500]
        # missing ctr, clicks, impressions, purchases, etc.
    })

    data_agent = DataAgent(config)

    with pytest.raises(Exception):
        data_agent.validate_schema(df)


def test_empty_dataset():
    df = pd.DataFrame(columns=["spend", "revenue", "ctr", "clicks", "impressions", "purchases", "roas"])

    evaluator = EvaluatorAgent(config)

    hypotheses = [{"id": "H1", "description": "Test hypothesis"}]

    with pytest.raises(Exception):
        evaluator.evaluate(df, hypotheses)
