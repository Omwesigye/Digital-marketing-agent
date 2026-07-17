from pipelines.data_pipeline import DataPipeline
from utils.logger import get_logger

logger = get_logger("listening_pipeline")

def run_listening_pipeline() -> list:
    """
    Runs the multi-channel ETL pipeline.
    """
    logger.info("Starting listening ETL process...")
    etl_pipeline = DataPipeline()
    inserted_ids = etl_pipeline.run()
    logger.info("Listening ETL process completed.")
    return inserted_ids