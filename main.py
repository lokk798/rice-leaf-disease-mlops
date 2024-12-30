from rice_leaf_disease import logger
from rice_leaf_disease.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from rice_leaf_disease.pipeline.stage_03_training import ModelTrainingPipeline
from rice_leaf_disease.pipeline.stage_04_evaluation import EvaluationPipeline
from rice_leaf_disease.pipeline.stage_02_prepare_model import PrepareModelTrainingPipeline
from colorama import Fore, Style

STAGE_NAME = "Data Ingestion stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} {Fore.BLUE}STARTED ...{Style.RESET_ALL} <<<<<<")
   data_ingestion = DataIngestionTrainingPipeline()
   data_ingestion.main()
   logger.info(f">>>>>> stage {STAGE_NAME} {Fore.GREEN}DONE!{Style.RESET_ALL} <<<<<<")
except Exception as e:
        logger.exception(e)
        raise e
     

STAGE_NAME = "Prepare model"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} {Fore.BLUE}STARTED ...{Style.RESET_ALL} <<<<<<")
   prepare_model = PrepareModelTrainingPipeline()
   prepare_model.main()
   logger.info(f">>>>>> stage {STAGE_NAME} {Fore.GREEN}DONE!{Style.RESET_ALL} <<<<<<")
except Exception as e:
        logger.exception(e)
        raise e


STAGE_NAME = "Training"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} {Fore.BLUE}STARTED ...{Style.RESET_ALL} <<<<<<")
   prepare_model = ModelTrainingPipeline()
   prepare_model.main()
   logger.info(f">>>>>> stage {STAGE_NAME} {Fore.GREEN}DONE!{Style.RESET_ALL} <<<<<<")
except Exception as e:
        logger.exception(e)
        raise e
     

STAGE_NAME = "Evaluation"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} {Fore.BLUE}STARTED ...{Style.RESET_ALL} <<<<<<")
   prepare_model = EvaluationPipeline()
   prepare_model.main()
   logger.info(f">>>>>> stage {STAGE_NAME} {Fore.GREEN}DONE!{Style.RESET_ALL} <<<<<<")
except Exception as e:
        logger.exception(e)
        raise e