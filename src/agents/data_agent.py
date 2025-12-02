import pandas as pd

class DataAgent:
    REQUIRED_COLUMNS = [
        "campaign_name", "adset_name", "date", "spend", "impressions",
        "clicks", "ctr", "purchases", "revenue", "roas",
        "creative_type", "creative_message", "audience_type", "platform", "country"
    ]

    def __init__(self, config):
        self.config = config

    def validate_schema(self, df):
        missing_cols = [c for c in self.REQUIRED_COLUMNS if c not in df.columns]

        if missing_cols:
            raise ValueError(
                f"❌ Dataset schema validation failed.\nMissing required columns: {missing_cols}\n"
                f"Expected columns: {self.REQUIRED_COLUMNS}\n"
                f"Found columns: {list(df.columns)}"
            )

        return True

    def run(self, df):
        self.validate_schema(df)

        summary = {
            "overall_roas": (df["revenue"].sum() / df["spend"].sum()) if df["spend"].sum() > 0 else 0,
            "total_spend": df["spend"].sum(),
            "total_revenue": df["revenue"].sum(),
        }

        return {"summary": summary, "df": df}
