import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import logging

class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename
        
    def predict(self):
        try:
            # Setup logging to debug the prediction process
            logging.basicConfig(level=logging.INFO)
            
            # Load the model
            model_path = os.path.join('artifacts', 'training', 'model.keras')
            logging.info(f"Loading model from: {model_path}")
            model = load_model(model_path)
            
            # Load and process the image
            image_name = self.filename
            logging.info(f"Processing image: {image_name}")
            
            if not os.path.exists(image_name):
                logging.error(f"Image file not found: {image_name}")
                return [{'image': 'Error: Image file not found'}]
            
            test_image = image.load_img(image_name, target_size=(180, 180))
            test_image = image.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis=0)
            test_image = test_image / 255.0
            
            # Make prediction
            raw_prediction = model.predict(test_image)
            logging.info(f"Raw prediction values: {raw_prediction}")
            
            result = np.argmax(raw_prediction, axis=1)
            logging.info(f"Predicted class index: {result[0]}")
            
            class_labels = {0: 'Bacterial leaf blight', 1: 'Brown spot', 2: 'Leaf smut'}
            prediction = class_labels.get(result[0], 'Unknown')
            logging.info(f"Predicted class: {prediction}")
            
            # Return prediction and confidence
            confidence = float(raw_prediction[0][result[0]]) * 100
            return [{'image': prediction, 'confidence': f"{confidence:.2f}%", 'raw_values': raw_prediction.tolist()}]
            
        except Exception as e:
            logging.error(f"Error during prediction: {str(e)}")
            return [{'image': f'Error: {str(e)}'}]