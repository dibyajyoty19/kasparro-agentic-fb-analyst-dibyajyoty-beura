import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from src.agents.evaluator_agent import EvaluatorAgent


def test_roas_drop_evaluation():
    df = pd.DataFrame({
        "spend": [100, 100],
        "revenue": [400, 200],     # ROAS drop from 4 → 2 (50% drop)
        "ctr": [0.03, 0.02]
    })

    config = {"analysis": {"roas_drop_threshold_pct": 0.20, "low_ctr_threshold": 0.015}}
    evaluator = EvaluatorAgent(config)
    hypotheses = [{"id": "H1", "description": "ROAS Drop Hypothesis"}]

    result = evaluator.evaluate(df, hypotheses)[0]

    assert result["is_supported"] == True
    assert result["confidence"] > 0.5
    assert round(result["evidence"]["before_roas"], 2) == 4.00
    assert round(result["evidence"]["after_roas"], 2) == 2.00


def test_low_ctr_logic():
    df = pd.DataFrame({
        "campaign_name": ["A", "A", "B"],
        "adset_name": ["1", "1", "2"],
        "ctr": [0.01, 0.03, 0.02],
        "spend": [50, 50, 50],
        "revenue": [60, 80, 75]
    })

    config = {"analysis": {"low_ctr_threshold": 0.015, "roas_drop_threshold_pct": 0.20}}
    evaluator = EvaluatorAgent(config)

    hypotheses = [{"id": "H2", "description": "Low CTR Hypothesis"}]
    result = evaluator.evaluate(df, hypotheses)[0]

    assert result["is_supported"] == True
    assert result["confidence"] >= 0.50
    assert result["evidence"]["low_ctr_rows"] >= 1
