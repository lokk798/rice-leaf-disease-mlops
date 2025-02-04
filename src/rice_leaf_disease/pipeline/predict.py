import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename
        
    def predict(self):
        
        model = load_model(os.path.join('artifacts', 'training', 'model.keras'))
        
        # Load and process the image
        image_name = self.filename
        test_image = image.load_img(image_name, target_size=(180, 180))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        test_image = test_image / 255.0
        
        
        # Make prediction
        result = np.argmax(model.predict(test_image), axis=1)
        
        class_labels = {0: 'Bacterial leaf blight', 1: 'Brown spot', 2: 'Leaf smut'}
        prediction = class_labels.get(result[0], 'Unknown') # If result[0] is not found, it defaults to "Unknown"
        
        return [{'image': prediction}]