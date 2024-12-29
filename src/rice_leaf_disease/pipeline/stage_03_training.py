from rice_leaf_disease.components.prepare_callbacks import PrepareCallback
from rice_leaf_disease.components.training import Training
from rice_leaf_disease.config.configuration import ConfigurationManager  
from rice_leaf_disease import logger


STAGE_NAME = 'Training'

class ModelTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        try:
            config = ConfigurationManager()
            prepare_callbacks_config = config.get_prepare_callback_config()
            prepare_callbacks = PrepareCallback(config=prepare_callbacks_config)
            callback_list = prepare_callbacks.get_tb_checkpoint_callback()

            training_config = config.get_training_config()
            training = Training(config=training_config)
            
            training.train(callback_list)

        except Exception as e:
            print(f"Error during training: {e}")
            raise e
    
if __name__ == '__main__':
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = ModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} done <<<<<")
    except Exception as e:
        logger.exception(e)
        raise e