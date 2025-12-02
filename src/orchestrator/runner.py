import json
import time
import pandas as pd
from datetime import datetime

from src.utils.config_loader import load_config
from src.utils.data_loader import load_dataset
from src.utils.logging_utils import RunLogger

from src.agents.planner_agent import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent


# ---------- Retry wrapper ----------
def retry(operation, logger, label: str, max_attempts=3, backoff=1):
    for attempt in range(1, max_attempts + 1):
        try:
            return operation()
        except Exception as e:
            logger.log_event("RETRY_FAILED", {
                "operation": label,
                "attempt": attempt,
                "error": str(e)
            })
            if attempt == max_attempts:
                logger.log_event("HARD_FAIL", {"operation": label})
                raise e
            time.sleep(backoff)


# ---------- Main Pipeline Controller ----------
def main(user_query: str, logger: RunLogger):

    start_time = time.time()
    logger.log_event("RUN_START", {"query": user_query})

    # Load config
    config = load_config()
    logger.log_event("CONFIG_LOADED", {"config_path": "config/config.yaml"})

    # Load dataset (retry protected)
    df = retry(lambda: load_dataset(config["data"]["path"], config["data"]["date_column"]),
               logger, "DATA_LOAD")
    logger.log_event("DATA_LOADED", {"rows": len(df)})

    # Initialize agents
    planner = PlannerAgent()
    data_agent = DataAgent(config)
    insight_agent = InsightAgent()
    evaluator_agent = EvaluatorAgent(config)
    creative_agent = CreativeAgent()

    # Validate schema
    try:
        logger.log_event("SCHEMA_VALIDATION_START", {})
        data_agent.validate_schema(df)
        logger.log_event("SCHEMA_VALIDATION_PASS", {"columns": list(df.columns)})
    except Exception as e:
        logger.log_event("SCHEMA_VALIDATION_FAIL", {"error": str(e)})
        raise e

    # Task plan
    plan = planner.plan(user_query)
    logger.log_event("PLAN_CREATED", {"steps": [t.__dict__ for t in plan]})

    # Execute workflow
    data_summary = retry(lambda: data_agent.run(df), logger, "DATA_SUMMARY")
    logger.log_event("DATA_SUMMARY", {"summary": data_summary["summary"]})

    hypotheses = retry(lambda: insight_agent.generate_hypotheses(data_summary),
                       logger, "INSIGHT_GENERATION")
    logger.log_event("HYPOTHESES_CREATED", {"count": len(hypotheses)})

    evaluated = retry(lambda: evaluator_agent.evaluate(df, hypotheses),
                      logger, "EVALUATION")
    logger.log_event("HYPOTHESES_EVALUATED", {"count": len(evaluated)})

    creatives = retry(lambda: creative_agent.generate(df, config["analysis"]["low_ctr_threshold"]),
                      logger, "CREATIVE_GENERATION")
    logger.log_event("CREATIVES_GENERATED", {"count": len(creatives)})

    # Save JSON outputs
    with open(config["output"]["insights_file"], "w") as f:
        json.dump(evaluated, f, indent=2, default=lambda x: x.item() if hasattr(x, "item") else str(x))

    with open(config["output"]["creatives_file"], "w") as f:
        json.dump(creatives, f, indent=2, default=lambda x: x.item() if hasattr(x, "item") else str(x))

    # Generate report
    report_lines = []
    report_lines.append("# ROAS Performance Analysis Report\n")
    report_lines.append(f"Run timestamp: {datetime.now().isoformat()}\n")
    report_lines.append("## Summary\n")
    report_lines.append(f"- **Overall ROAS:** {data_summary['summary']['overall_roas']:.2f}")
    report_lines.append(f"- **Total Spend:** {data_summary['summary']['total_spend']:.2f}")
    report_lines.append(f"- **Total Revenue:** {data_summary['summary']['total_revenue']:.2f}\n")

    report_lines.append("## Top Drivers\n")

    if len(evaluated) == 0:
        report_lines.append("- No significant performance drivers detected.\n")
    else:
        for h in evaluated[:2]:
            report_lines.append(f"- **{h['id']}** — {h['description']}")
            report_lines.append(f"  - Supported: {h['is_supported']}")
            report_lines.append(f"  - Confidence: {h['confidence']}")
            report_lines.append(f"  - Evidence: {h['evidence']}\n")

    report_lines.append("## Recommended Next Actions\n")
    if any(h["is_supported"] for h in evaluated):
        report_lines.append("- Refresh creatives for underperforming low-CTR segments.")
        report_lines.append("- Reallocate spend away from weak adsets with declining ROAS.")
        report_lines.append("- Run A/B test on new messaging themes.\n")
    else:
        report_lines.append("- No severe performance drops detected; monitor trends and retest in 7 days.\n")

    with open(config["output"]["report_file"], "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    # Finish run
    run_time = round(time.time() - start_time, 2)
    logger.log_event("RUN_COMPLETE", {"execution_time_sec": run_time})

    print("\n🎉 Analysis completed successfully!")
    print(f"Report saved at: {config['output']['report_file']}")
