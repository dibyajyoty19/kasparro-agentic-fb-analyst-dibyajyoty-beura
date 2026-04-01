import numpy as np

def compute_adaptive_ctr_threshold(df):
    return float(df['ctr'].quantile(0.25))

def compute_adaptive_roas_drop_threshold(df):
    window = max(5, int(len(df) * 0.3))  
    baseline = df['roas'][:-window].mean()
    current = df['roas'][-window:].mean()
    std = df['roas'][:-window].std()

    threshold_pct = std / baseline if baseline > 0 else 0
    return baseline, current, threshold_pct
import numpy as np

def compute_adaptive_ctr_threshold(df):
    return float(df['ctr'].quantile(0.25))

def compute_adaptive_roas_drop_threshold(df):
    window = max(5, int(len(df) * 0.3))  
    baseline = df['roas'][:-window].mean()
    current = df['roas'][-window:].mean()
    std = df['roas'][:-window].std()

    threshold_pct = std / baseline if baseline > 0 else 0
    return baseline, current, threshold_pct
