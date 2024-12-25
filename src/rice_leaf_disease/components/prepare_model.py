import tensorflow as tf
from tensorflow.keras import layers, models
from pathlib import Path
from rice_leaf_disease.entity.config_entity import PrepareModelConfig


class PrepareModel:
    def __init__(self, config: PrepareModelConfig):
        self.config = config
        self.model = None  # Initialize model as None, it will be built later.

    def get_model(self):
        # Build the model based on the config parameters
        self.model = self._build_custom_model()

        # Save the model (the path is defined in the config)
        self.save_model(path=self.config.model_path, model=self.model)

    def _build_custom_model(self):
        model = models.Sequential()

        # Add the input layer
        model.add(layers.Input(shape=self.config.input_shape))

        # First convolutional block
        model.add(layers.Conv2D(
            filters=self.config.conv1_filters,
            kernel_size=self.config.conv1_kernel_size,
            activation=self.config.conv1_activation,
            padding='same'
        ))
        model.add(layers.MaxPooling2D())
        model.add(layers.Dropout(self.config.conv1_dropout_rate))

        # Second convolutional block
        model.add(layers.Conv2D(
            filters=self.config.conv2_filters,
            kernel_size=self.config.conv2_kernel_size,
            activation=self.config.conv2_activation,
            padding='same'
        ))
        model.add(layers.MaxPooling2D())
        model.add(layers.Dropout(self.config.conv2_dropout_rate))

        # Third convolutional block
        model.add(layers.Conv2D(
            filters=self.config.conv3_filters,
            kernel_size=self.config.conv3_kernel_size,
            activation=self.config.conv3_activation,
            padding='same'
        ))
        model.add(layers.MaxPooling2D())

        # Flatten the output from convolutional layers
        model.add(layers.Flatten())

        # Fully connected (dense) layers
        model.add(layers.Dense(
            units=self.config.dense1_units,
            activation=self.config.dense1_activation
        ))

        # Output layer
        model.add(layers.Dense(
            units=self.config.num_classes,
            activation=self.config.dense2_activation
        ))

        # Compile the model with the specified optimizer, loss, and metrics
        model.compile(
            optimizer=self.config.optimizer,
            loss=self.config.loss_function,
            metrics=self.config.metrics
        )
        
        model.summary()

        return model



    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        # Save the model to the specified path
        model.save(path)
