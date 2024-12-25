"""
This script is responsible for orchestrating the Data Ingestion Stage.
It initializes the configuration, invokes the DataIngestion component,
and handles the process of preparing raw data for further steps in
the pipeline.
"""

from rice_leaf_disease.components.data_ingestion import DataIngestion
from rice_leaf_disease.config.configuration import ConfigurationManager
from rice_leaf_disease import logger


STAGE_NAME = 'Data Ingestion Stage'

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        try:
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            # Have already downloaded the data
            # data_ingestion.download_file()
            data_ingestion.extract_zip_file()
        except Exception as e:
            raise e
        
if __name__ == '__main__':
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} done <<<<<")
    except Exception as e:
        logger.exception(e)
        raise e

        