class InsightAgent:
    def generate_hypotheses(self, data_summary):
        overall_roas = data_summary["summary"]["overall_roas"]
        trend = data_summary.get("trend", None)

        hypotheses = [
            {
                "id": "H1",
                "description": "ROAS may have declined due to changes in performance metrics over time.",
                "expected_pattern": "ROAS down and CTR or purchases also down",
            },
            {
                "id": "H2",
                "description": "Low CTR adsets may be negatively impacting ROAS. Possible messaging mismatch or creative fatigue.",
                "expected_pattern": "Low CTR campaigns correlate with ROAS drops",
            }
        ]

        return hypotheses
