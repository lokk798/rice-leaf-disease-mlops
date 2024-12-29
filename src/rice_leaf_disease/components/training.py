from pathlib import Path
from rice_leaf_disease.entity.config_entity import TrainingConfig
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, Sequential
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image

class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.model = None  # Model will be loaded in the get_model method

    def get_model(self):
        """
        Load the model structure from the specified path and compile it.
        """
        model_path = Path('artifacts/prepare_model/model.keras')
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        self.model = tf.keras.models.load_model(model_path)
        
        # Compile the model only if it's not compiled already
        if not self.model.optimizer:
            self.model.compile(
                optimizer=self.config.params_optimizer,
                loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                metrics=self.config.params_metrics
            )   
    
    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)
    
    def get_and_prepare_data(self):
        data_path = Path('artifacts/data_ingestion/rice_leaf_diseases')
        bacteria = list(data_path.glob("Bacterial leaf blight/*"))
        brown = list(data_path.glob("Brown spot/*"))
        smut = list(data_path.glob("Leaf smut/*"))
        
        print(f"Bacteria samples: {len(bacteria)}")
        print(f"Brown spot samples: {len(brown)}")
        print(f"Smut samples: {len(smut)}")

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
                resized_img = cv2.resize(img, (180, 180))
                X.append(resized_img)
                y.append(labels_dict[class_name])
        
        print(f"Loaded {len(X)} images.")
        
        X = np.array(X)
        y = np.array(y)
        
        # Ensure that the arrays are not empty
        if X.size == 0 or y.size == 0:
            raise ValueError("No data found to train the model.")

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
        X_train_scaled = X_train / 255.0
        X_test_scaled = X_test / 255.0
        return X_train_scaled, X_test_scaled, y_train, y_test

        
    def train(self, callback_list: list):
        """
        Train the model using the specified callbacks and configuration.
        """
        # Ensure the model is loaded before training
        self.model = Sequential([
        layers.Input(shape=(180, 180, 3)),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.25),  # Dropout after first Conv2D layer

        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.25),  # Dropout after second Conv2D layer

        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),

        layers.Flatten(),
        layers.Dense(128, activation='relu'),

        layers.Dense(3, activation='softmax')
     ])

        
        # Compile the model if it hasn't been compiled yet
        self.model.compile(
            optimizer='adam', 
            loss=tf.keras.losses.SparseCategoricalCrossentropy(),
            metrics=['accuracy']
        )
        
        # Get the data
        X_train_scaled, X_test_scaled, y_train, y_test = self.get_and_prepare_data()

        # Train the model using fit
        self.model.fit(
            X_train_scaled, y_train,
            validation_data=(X_test_scaled, y_test),
            epochs=self.config.params_epochs,
            callbacks=callback_list
        )

        # Save the trained model
        self.save_model(self.config.trained_model_path, self.model)