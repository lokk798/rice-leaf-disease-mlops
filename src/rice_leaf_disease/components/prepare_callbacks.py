import os
import time
import tensorflow as tf
from rice_leaf_disease.entity.config_entity import PrepareCallbackConfig

class PrepareCallback:
    def __init__(self, config: PrepareCallbackConfig):
        self.config = config
        
    
    """
    The @property decorator is used to define a method as a getter property.
    It allows to access the method as if it were an attribute, 
    without explicitly calling it like a function.    
    """    
    @property
    def _create_tb_callbacks(self):
        """
        Logs training metrics for visualization in TensorBoard.
        """
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
        
        tb_running_log_dir = os.path.join(
            self.config.tensorboard_root_log_dir,
            f"tb_logs_at_{timestamp}"
        )
        
        return tf.keras.callbacks.TensorBoard(log_dir=tb_running_log_dir)
    
    @property
    def _create_checkpoint_callbacks(self):
        """
        Saves model checkpoints during training, ensuring best performing
        model is retained.
        """
        return tf.keras.callbacks.ModelCheckpoint(
            filepath=self.config.checkpoint_model_filepath,
            save_best_only=True
        )
    
    def get_tb_checkpoint_callback(self):
        return [
            self._create_tb_callbacks,
            self._create_checkpoint_callbacks
        ]