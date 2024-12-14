"""
This module provides utilities that are going to be used throughout the project.
"""
import os
import yaml
import json
import joblib
import base64
from pathlib import Path
from typing import Any
from box.exceptions import BoxValueError
from rice_leaf_disease import logger
from ensure import ensure_annotations
from box import ConfigBox


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox: 
    """
    Reads a yaml file and returns its content
    
    Args: 
        - path_to_yaml (Path): path like input
    
    Raises:
        - ValueError: if the yaml file is empty
        - e: empty file
        
    Returns:
        - ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(path_to_yaml)
            logger.info(f"YAML file: {path_to_yaml}  loaded successfully!")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("Empty YAML file")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Create a list of directories

    Args:
        - path_to_directories (list): list of path of directories
        - verbose (bool) : logs the creation of directory default True
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Saves json data

    Args:
        - path (Path): path to the json file
        - data (dict): data to be saved in the json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")




@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Loads json files data and returns its content

    Args:
        - path (Path): path to json file

    Returns:
        - ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded successfully from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """
    Saves binary file

    Args:
        - data (Any): data to be saved as binary
        - path (Path): path to the binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Loads binary data

    Args:
        - path (Path): path to the binary file

    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """
    Gets size in KB 

    Args:
        - path (Path): path of the file

    Returns:
        - str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"

@ensure_annotations
def decodeImage(imgstring: str, fileName: str):
    """
    Decodes a base64 encoded image string and writes it to a file.
    
    Args:
        - imgstring (str): the base64 encoded string representing the image.
        - fileName (str): the file where the decoded image will be saved.
    """
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


@ensure_annotations
def encodeImageIntoBase64(croppedImagePath: str) -> bytes:
    """
    Encodes the content of an image file into a base64 encoded string

    Args:
        - croppedImagePath (str): path to the image to be encoded
    Returns: 
        - bytes: a base 64 encoded string representing the image file.
    """
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())
