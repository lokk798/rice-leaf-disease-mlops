import json
from pathlib import Path
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image

from rice_leaf_disease.entity.config_entity import EvaluationConfig


class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config
    
    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        if not path.exists():
            raise FileNotFoundError(f"Model file not found at {path}")
        return tf.keras.models.load_model(path)
    
    @staticmethod
    def preprocess_data(data_path: Path, image_size: tuple) -> tuple:
        """
        Load and preprocess the dataset for evaluation.
        """
        bacteria = list(data_path.glob("Bacterial leaf blight/*"))
        brown = list(data_path.glob("Brown spot/*"))
        smut = list(data_path.glob("Leaf smut/*"))
        data = {"bacteria": bacteria, "brown": brown, "smut": smut}
        
        labels_dict = {
            'bacteria': 0,
            'brown': 1,
            'smut': 2
        }
        X, y = [], []

        for class_name, images in data.items():
            for image in images:
                img = cv2.imread(str(image))
                if img is None:
                    print(f"Failed to load image: {image}")
                    continue
                resized_img = cv2.resize(img, image_size[:2])
                X.append(resized_img)
                y.append(labels_dict[class_name])
        
        X = np.array(X) / 255.0  # Normalize images
        y = np.array(y)  # Labels
        return X, y
    
    def evaluation(self) -> dict:
        """
        Evaluate the model's performance on the dataset.
        """
        model = self.load_model(self.config.model_path)
        
        image_size = tuple(self.config.params_image_size)
        X, y = self.preprocess_data(self.config.training_data, image_size)

        print("Evaluating the model...")
        scores = model.evaluate(X, y, verbose=1)
        
        # Create a dictionary with metric names and values
        metrics = dict(zip(model.metrics_names, scores))
        print(f"Evaluation Metrics: {metrics}")
        return metrics
    
    def save_score(self, scores: dict, output_path: Path = Path('artifacts/evaluation/score.json')):
        """
        Save the evaluation metrics to a JSON file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(scores, f, indent=4)
        print(f"Scores saved to {output_path}")