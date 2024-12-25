import os
from rice_leaf_disease.utils.common import read_yaml, create_directories
from rice_leaf_disease.entity.config_entity import DataIngestionConfig, PrepareCallbackConfig, PrepareModelConfig
from rice_leaf_disease.constants import *

class ConfigurationManager:
    """
    This class handles reading configurations, creating necessary directories,
    and providing step-specific configuration objects.
    """
    
    def __init__(self,config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):
        
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        
        create_directories([self.config.artifacts_root])
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Retrieves and prepares the configuration specific 
        to the data ingestion step.
        """
        
        config = self.config.data_ingestion
        
        create_directories([config.root_dir])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir = config.root_dir,
            source_url = config.source_url,
            local_data_file = config.local_data_file,
            unzip_dir = config.unzip_dir
        )
        
        return data_ingestion_config
    
    def get_prepare_model_config(self) -> PrepareModelConfig:      
        """
        Returns model configuration paths and model parameters.
        """
        
        config = self.config.prepare_model  # Access prepare_model section in config
        create_directories([config.root_dir])  # Create root directory if it doesn't exist
        
        # Extracting parameters from params.yaml
        model_params = self.params.model_params
        
        prepare_model_config = PrepareModelConfig(
            # Paths from config
            root_dir=Path(config.root_dir),
            model_path=Path(config.model_path),

            # Model architecture parameters from params.yaml
            input_shape=tuple(model_params.input_shape),
            num_classes=model_params.num_classes,
            
            # Convolutional layer parameters
            conv1_filters=model_params.layers.conv1.filters,
            conv1_kernel_size=model_params.layers.conv1.kernel_size,
            conv1_activation=model_params.layers.conv1.activation,
            conv1_dropout_rate=model_params.layers.conv1.dropout_rate,
            
            conv2_filters=model_params.layers.conv2.filters,
            conv2_kernel_size=model_params.layers.conv2.kernel_size,
            conv2_activation=model_params.layers.conv2.activation,
            conv2_dropout_rate=model_params.layers.conv2.dropout_rate,
            
            conv3_filters=model_params.layers.conv3.filters,
            conv3_kernel_size=model_params.layers.conv3.kernel_size,
            conv3_activation=model_params.layers.conv3.activation,
            conv3_dropout_rate=model_params.layers.conv3.dropout_rate,
            
            # Dense layer parameters
            dense1_units=model_params.layers.dense1.units,
            dense1_activation=model_params.layers.dense1.activation,
            
            dense2_units=model_params.layers.dense2.units,
            dense2_activation=model_params.layers.dense2.activation,
            
            # Training parameters
            optimizer=model_params.optimizer,
            loss_function=model_params.loss_function,
            metrics=model_params.metrics
        )
        
        return prepare_model_config

    def get_prepare_callback_config(self) -> PrepareCallbackConfig:
        config = self.config.prepare_callbacks
        model_checkpoint_dir = os.path.dirname(config.checkpoint_model_filepath)
        
        create_directories([Path(model_checkpoint_dir),
                            Path(config.tensorboard_root_log_dir)])
        
        prepare_callback_config = PrepareCallbackConfig(
            root_dir=Path(config.root_dir),
            tensorboard_root_log_dir=Path(config.tensorboard_root_log_dir),
            checkpoint_model_filepath=Path(config.checkpoint_model_filepath)    
        )
        
        return prepare_callback_config