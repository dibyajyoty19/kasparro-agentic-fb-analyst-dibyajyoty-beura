import numpy as np

class EvaluatorAgent:
    def __init__(self, config):
        self.config = config

    def adaptive_ctr_threshold(self, df):
        return np.percentile(df["ctr"].dropna(), 20)  # bottom 20% CTR bucket

    def evaluate(self, df, hypotheses):
        results = []
        if not hypotheses:
            return results

    # Compute ROAS drop
        df = df.sort_values("date")
        baseline = df["roas"].iloc[:len(df)//2].mean()
        recent = df["roas"].iloc[len(df)//2:].mean()
        drop_pct = (recent - baseline) / baseline

        for h in hypotheses:
            if h["id"] == "H1":
                supported = drop_pct < -0.05  # >5% drop
                results.append({
                    "id": h["id"],
                    "description": h["description"],
                    "is_supported": supported,
                    "confidence": abs(drop_pct),
                    "evidence": {
                        "baseline_roas": baseline,
                        "recent_roas": recent,
                        "drop_pct": drop_pct
                    }
                })

            if h["id"] == "H2":
                low_ctr_df = df[df["ctr"] < self.config["analysis"]["low_ctr_threshold"]]
                supported = len(low_ctr_df) > 0
                results.append({
                    "id": h["id"],
                    "description": h["description"],
                    "is_supported": supported,
                    "confidence": 0.85 if supported else 0.25,
                    "evidence": {
                        "low_ctr_rows": len(low_ctr_df)
                    }
                })

        return results

