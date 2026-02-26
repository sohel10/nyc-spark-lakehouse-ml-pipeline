from src.logger import get_logger

logger = get_logger()

def run_pipeline():

    logger.info("Pipeline started")

    print("NYC Spark Lakehouse ML Pipeline")

    logger.info("Pipeline execution completed successfully")

if __name__ == "__main__":
    run_pipeline()