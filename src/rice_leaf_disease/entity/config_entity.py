from pathlib import Path 
from dataclasses import dataclass


"""
- @dataclass decorator is used to automatically generate special 
    methods for the class such as __init__().
- The frozen = True parameter makes the class immutable. 
"""

@dataclass(frozen=True)
class DataIngestionConfig:
    """
    Configuration class for the data ingestion phase of the pipeline
    to store configuration details.
    """
    root_dir: Path
    source_url: str
    local_data_file:Path
    unzip_dir: Path

@dataclass(frozen=True)
class PrepareModelConfig:
    """
    Configuration class for preparing the model.
    
    This class contains all the parameters required to define, build,
    and save the model.
    """
    
    # Model Preparation Paths
    root_dir: Path
    model_path: Path
    
    # Model Architecture Params
    input_shape: tuple
    num_classes: int
    
    # Convolutional Layer Params
    conv1_filters: int
    conv1_kernel_size: int
    conv1_activation: str
    conv1_dropout_rate: float
    
    conv2_filters: int
    conv2_kernel_size: int
    conv2_activation: str
    conv2_dropout_rate: float
    
    conv3_filters: int
    conv3_kernel_size: int
    conv3_activation: str
    conv3_dropout_rate: float
    
    # Dense Layer Params
    dense1_units: int
    dense1_activation: str
    
    dense2_units: int
    dense2_activation: str
    
    # Training Params
    optimizer: str
    loss_function: str
    metrics: list

@dataclass(frozen=True)
class PrepareCallbackConfig:
    """
    Configuration class containing callbacks parameters 
    (paths to save model logs and checkpoints)
    """
    root_dir: Path
    tensorboard_root_log_dir: Path
    checkpoint_model_filepath: Path