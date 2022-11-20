import tensorflow as tf

from tensorflow import keras
from keras import layers
import keras.layers 
from keras.models import Sequential 

class Trainer():

    def __init__(self):
        self.model = ''

    def trainer(self):
        image_size = (180, 180)
        batch_size = 20 

        # loading datasets that are stored in the local directory on the disk into the current workspace to load into the neural network
        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            'HackWestern2022\machine\SteakCookingLevels',  # directory of the images 
            validation_split= 0.2, # hold out a subset of the data for validation
            subset = "training",
            seed = 2, # ensures that we are working with the same set of randomized data every time 
            image_size = image_size,
            batch_size = batch_size,
        )
        validation_ds = tf.keras.preprocessing.image_dataset_from_directory(
            'HackWestern2022\machine\SteakCookingLevels',
            validation_split= 0.2,
            subset = "validation", 
            seed = 1, 
            image_size = image_size,
            batch_size = batch_size,
        )


        num_classes = 3

        model = Sequential([
            # Standardizing the data - as part of the model 
            #  the images have already been resized to be identical (180, 180)
            #  the RGB channel however are in range [0, 255] which is not ideal for neural networks
            #  need to stanndardized them by rescaling 
            tf.keras.layers.experimental.preprocessing.Rescaling(1./255, input_shape=(180, 180, 3)),
            tf.keras.layers.experimental.preprocessing.RandomFlip("vertical"),
            tf.keras.layers.experimental.preprocessing.RandomRotation(0.1), 

            # first layer of a neural network takes in all the pixels within a given image and applies a filter to it. This forms representations of different parts of the image. 
            # the result after feature extraction is called feature maps 
            # convolution = forming a representation of part of an image 
            # feature maps are passed through an activation layer where their non-linearity increases as images are non-linear 
            # most commonly, the Relu activation function is used for this purpose 
            layers.Conv2D(16, 3, strides = 2, padding='same', activation='relu'),
            layers.BatchNormalization(),


            # Pooling Layer downsamples an image --> takes the information of the image and compresses it 
            # makes the network more flexible when it comes to recognizing objects    
            # abstracts away the unnecessary parts of the image, only keeping parts that ara relevant 
            # prevents overfitting --> which is when the network learn too many details and fails to recognize new, more generalized data 
            layers.MaxPooling2D(),

            #repeat with different filter sizes 
            layers.Conv2D(32, 3, strides = 2, padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(),
            
            layers.Conv2D(64, 3, strides = 2, padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(),

            # flattens the mult-dimensional layer to a single dimention
            layers.Flatten(),

            layers.Dense(batch_size, activation='relu'),
            layers.Dense(num_classes,activation='softmax')
        ])

        opt = keras.optimizers.Adam(learning_rate=0.01)

        epochs = 25 
        model.compile(
            optimizer=opt,
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        model.fit(
            train_ds,
            validation_data=validation_ds,
            batch_size=batch_size,
            epochs=epochs,
        )

        self.model = model

        return

    def predict(self, file_path):
        image_size = (180, 180)
        img = tf.keras.preprocessing.image.load_img(
        file_path, target_size=image_size
        )
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create batch axis

        predictions = self.model.predict(img_array)
    
        return predictions
