import sys
from src.utils.logging_utils import RunLogger
from src.orchestrator.runner import main

if __name__ == "__main__":
    user_query = sys.argv[1] if len(sys.argv) > 1 else "Analyze ROAS performance"

    logger = RunLogger(logs_dir="logs")
    try:
        main(user_query, logger)
    except Exception as e:
        logger.log_event("CRASH", {"error": str(e)})
        raise e
