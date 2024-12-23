from rice_leaf_disease.utils.common import read_yaml, create_directories
from rice_leaf_disease.entity.config_entity import DataIngestionConfig
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
        Retrieves and prepares the configuration specific to 
        the data ingestion step.
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