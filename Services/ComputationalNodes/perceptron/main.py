import os
import pandas as pd
import shutil
import warnings
from datetime import datetime
from tensorflow.keras.utils import load_img
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
from keras import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense
import numpy as np
from perceptron_exceptions import *
from PIL import Image
import time

warnings.filterwarnings('ignore')

class Bot:
    def __init__(self, image_width=256, image_height=256) -> None:
        self.class_labels = {}
        self.label_list = []
        self.img_width = image_width
        self.img_height = image_height
    
    #returns dict
    #throws FileNotFoundError
    def data_class_label(self, resource_folder="TrainingData"):
        if not os.path.isdir(resource_folder):
            raise FileNotFoundError(f"{resource_folder} does not exist or is invalid!")
        
        self.class_labels = {}
        label = 0
        
        #labeling the names of data_classes with 0 or 1
        for index, data_class in enumerate(os.listdir(resource_folder)):
            if index > 1:
                print(f"The perceptron is limited to only two data classes\nProceeding with {self.class_labels.keys()}")
                break
            self.class_labels[data_class] = str(label)
            self.label_list.append(data_class)
            label += 1
        return self.class_labels
    
    #throws FileNotFoundError
    def trim_dataset(self, resource_folder="TrainingData"):
        if not os.path.isdir(resource_folder):
            raise FileNotFoundError(f"{resource_folder} does not exist or is invalid!")
        
        for data_class in os.listdir(resource_folder):
            #remove files that are not images or are corrupted from the dataset
            for file in os.listdir(os.path.join(resource_folder, data_class)):
                path_to_file = os.path.join(resource_folder, data_class, file)
                try:
                    if not os.path.isfile(path_to_file):
                        print(f"{path_to_file} is not a file!")
                        shutil.rmtree(path_to_file)
                    elif ".jpg" not in file:
                        print(f"{path_to_file} is not an image!")
                        os.remove(path_to_file)
                    else:
                        try:
                            Image.open(path_to_file)
                        except:
                            print(f"{path_to_file} is corrupted!")
                            os.remove(path_to_file)
                except:
                    shutil.rmtree(path_to_file)

    #returns pd.DataFrame
    #throws InvalidDatasetDistribution
    def create_dataframe(self, resource_folder="TrainingData", treshold=0.4):
        if not os.path.isdir(resource_folder):
            raise FileNotFoundError(f"{resource_folder} does not exist or is invalid!")
        data = []
        for data_class in os.listdir(resource_folder):
            for file in os.listdir(os.path.join(resource_folder, data_class)):
                path_to_file = os.path.join(resource_folder, data_class, file)
                # add files to the dataframe
                data.append([path_to_file, data_class, self.class_labels[data_class]])
        
        df = pd.DataFrame(data, columns=['Path', 'Classification', 'Label'])
        zero_amount = df[df['Label']=="0"]['Label'].count()
        total_amount = df['Label'].count()
        print(zero_amount, total_amount)
        if zero_amount/total_amount < treshold or zero_amount/total_amount > 1-treshold:
            raise InvalidDatasetDistribution(f"Datasets are distributed incorrectly.\n \
                                            Was {int((1 - zero_amount/total_amount)*100)} | {int((zero_amount/total_amount)*100)} \n \
                                            but should be (at least) {treshold*100} | {(1-treshold)*100}")
            
        # return shuffled dataframe    
        return df.sample(frac=1).reset_index(drop=True)
    
    def get_model_list(self, source_dir="models"):
        if not os.path.isdir(source_dir):
            raise IOError(f"Source dir {source_dir} does not exist or is invalid!")
        elif os.path.getsize(source_dir) == 0:
            raise IOError(f"Source dir {source_dir} is empty!")
        
        list_ = os.listdir(source_dir)
        return list(map(lambda x: os.path.join(source_dir, x), list_))

    #@throws IncorrectModelType
    def save_model(self, model, name="model", target_dir="models"):
        if not isinstance(model, Sequential):
            raise IncorrectModelType(f"Should be Sequential, but was {type(model)}")
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)
        try:
            model.save(os.path.join(target_dir, name))
        except Exception as e:
            print("Model saving failed!")
            print(e.message)
        else:
            print(f"Model saved successfully at: {os.path.join(target_dir, name)}")

    #@returns model
    #@throws IOError
    def load_model(self, name=None, source_dir="models", path=None):
        if not os.path.isdir(source_dir):
            raise IOError(f"Source dir {source_dir} does not exist or is invalid!")
        elif os.path.getsize(source_dir) == 0:
            raise IOError(f"Source dir {source_dir} is empty!")

        if path is None:
            #loading random model from the source
            if name is None:
                print("Name was not provided. Loading last any model from the source.")
                dir_list = os.listdir(source_dir)
                for dir_ in dir_list:
                    if os.path.isdir(dir_):
                        name = dir_
                        try:
                            model = keras.models.load_model(os.path.join(source_dir, name))
                        except:
                            user_input = input(f"The model {os.path.join(source_dir, name)} is not appropriate and could not be loaded. Should it be deleted? [y/n]")
                            if user_input.lower() in {"yes", "y"}:
                                print("Deleting the model...")
                                shutil.rmtree(os.path.join(source_dir, name))
                        else:
                            print("Model successfully loaded!")
                            return model   
                #if no appropriate model was found
                if name is None:
                    raise IOError(f"Source dir {source_dir} contains no appropriate models!")
            else:
                path = os.path.join(source_dir, name)
        try:
            model = keras.models.load_model(path)
        except:
            user_input = input(f"The model {path} is not appropriate and could not be loaded. Should it be deleted? [y/n]")
            if user_input.lower() in {"yes", "y"}:
                print("Deleting the model...")
                shutil.rmtree(path)
            raise IOError(f"Model could not be loaded!")
        else:
            print("Model successfully loaded!")
            return model
    
    # @params
    # train_dataframe, test_dataframe - panas.Dataframe for training and testing
    # throws invalid dataset distribution
    # training model design and some parameters taken from https://www.geeksforgeeks.org/python-image-classification-using-keras/?ref=lbp
    def train_model(self, train_dataframe, test_dataframe, img_width=256, img_height=256, sample_limit=5000, epochs=10, batch_size=32, name=None, save=True, target_dir="models"):
        if train_dataframe.size < 32 or test_dataframe.size < 32:
            raise InvalidDatasetDistribution("Datasets should contain at least 32 images!")
        
        if train_dataframe.size > sample_limit:
            train_dataframe = train_dataframe.sample(sample_limit)
        if test_dataframe.size > sample_limit:
            test_dataframe = test_dataframe.sample(sample_limit)
        
        train_generator = ImageDataGenerator(
            rescale = 1./255,
            rotation_range = 42,
            shear_range = 0.2,
            zoom_range = 0.2,
            horizontal_flip = True
        )

        train_iterator = train_generator.flow_from_dataframe(
            train_dataframe,
            rescale=1./255,
            x_col='Path',
            y_col='Classification',
            target_size=(img_width,img_height),
            batch_size=batch_size,
            class_mode='binary'
        )
        
        test_iterator = ImageDataGenerator().flow_from_dataframe(
            test_dataframe,
            x_col='Path',
            y_col='Classification',
            target_size=(img_width,img_height),
            batch_size=batch_size,
            class_mode='binary'
        )

        model = Sequential([
                    Conv2D(16, (3,3), activation='relu', input_shape=(img_width,img_height,3)),
                    MaxPool2D((2,2)),
                    Conv2D(32, (3,3), activation='relu'),
                    MaxPool2D((2,2)),
                    Conv2D(64, (3,3), activation='relu'),
                    MaxPool2D((2,2)),
                    Flatten(),
                    Dense(512, activation='relu'),
                    Dense(1, activation='sigmoid')
        ])
        
        if os.path.exists("checkpoints"):
            shutil.rmtree("checkpoints")
        os.mkdir("checkpoints")
        
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        model_checkpoint = keras.callbacks.ModelCheckpoint(os.path.join("checkpoints", "weights{epoch:08d}.h5"), save_weights_only=True)
        best_checkpoint = keras.callbacks.ModelCheckpoint(os.path.join("checkpoints", "best_weights.h5"), save_weights_only=True, save_best_only=True)
        model.fit(train_iterator, epochs=epochs, validation_data=test_iterator, callbacks=[model_checkpoint, best_checkpoint])
        
        if save:
            if name is None:
                timestamp = str(datetime.now().strftime("%d_%m_%y"))
                name = "model_" + timestamp
            try:
                self.save_model(model, name, target_dir)
            except IncorrectModelType as e:
                print(e.message)

    def predict(self, model, path):
        image = load_img(path, target_size=(self.img_width, self.img_height))
        img = np.array(image)
        img = img / 255.0
        img = img.reshape(1, self.img_width, self.img_height,3)
        return model.predict(img)
    
if __name__ == "__main__":
    b = Bot(128, 128)
    b.data_class_label()
    # b.trim_dataset()
    df = b.create_dataframe()
    # b.train_model(df, df, sample_limit=1000, epochs=10)
    model = b.load_model(path="models/150_epochs")
    # prediction = b.label_list[int(b.predict(model,'input/d/n02089867_24.jpg')[0][0])]
    # print(f"Predicted Class: ", prediction)
    input_dir = "input"
    while True:
        try:
            if len(os.listdir(input_dir)) == 1:
                path = os.path.join(input_dir, os.listdir(input_dir)[0])
                prediction = int(b.predict(model, path)[0][0])
                print(f"Predicted Class: ", prediction)
                os.remove(path)
                time.sleep(1)
        except:
            pass