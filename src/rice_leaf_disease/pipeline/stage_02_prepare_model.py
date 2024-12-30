from rice_leaf_disease.components.prepare_model import PrepareModel
from rice_leaf_disease.config.configuration import ConfigurationManager
from rice_leaf_disease import logger

STAGE_NAME = "Prepare model"

class PrepareModelTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        try:
            config = ConfigurationManager()
            prepare_model_config = config.get_prepare_model_config()
            prepare_model = PrepareModel(config=prepare_model_config)
            prepare_model.get_model()

        except Exception as e:
            raise e
    
if __name__ == '__main__':
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = PrepareModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} done <<<<<")
    except Exception as e:
        logger.exception(e)
        raise e

