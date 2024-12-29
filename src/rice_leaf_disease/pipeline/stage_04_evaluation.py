from rice_leaf_disease.components.evaluation import Evaluation
from rice_leaf_disease.config.configuration import ConfigurationManager  
from rice_leaf_disease import logger


STAGE_NAME = 'Training'

class EvaluationPipeline:
    def __init__(self):
        pass
    
    def main(self):
        try:
            config_manager = ConfigurationManager()
            eval_config = config_manager.get_evaluation_config()
            evaluation = Evaluation(config=eval_config)
            
            scores = evaluation.evaluation()
            
            evaluation.save_score(scores)

        except Exception as e:
            print(f"Error during evaluation: {e}")
            raise e
    
if __name__ == '__main__':
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = EvaluationPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} done <<<<<")
    except Exception as e:
        logger.exception(e)
        raise e