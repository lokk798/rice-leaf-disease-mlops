from pathlib import Path 
from dataclasses import dataclass

@dataclass(frozen=True)
class DataIngestionConfig:
    """
    Configuration class for the data ingestion phase of the pipeline
    to store configuration details.
    - @dataclass decorator is used to automatically generate special 
    methods for the class such as __init__()
    - The frozen = True parameter makes the class immutable. 
    """
    root_dir: Path
    source_url: str
    local_data_file:Path
    unzip_dir: Path
    