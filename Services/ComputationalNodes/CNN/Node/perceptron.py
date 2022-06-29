import os
import pandas as pd
import shutil
import warnings
from datetime import datetime
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
from keras import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense
import numpy as np
from perceptron_exceptions import *
from PIL import Image

warnings.filterwarnings('ignore')
dir_path = os.path.dirname(__file__)


class Bot:   
    #returns dict, list
    #throws FileNotFoundError
    def data_class_label(self, resource_folder="TrainingData"):
        resource_path = os.path.join(dir_path, resource_folder)
        if not os.path.isdir(resource_path):
            raise FileNotFoundError(f"{resource_folder} does not exist or is invalid!")
        
        class_labels = {}
        label_list = []
        label = 0
        
        #labeling the names of data_classes with 0 or 1
        for index, data_class in enumerate(os.listdir(resource_path)):
            if index > 1:
                print(f"The perceptron is limited to only two data classes\nProceeding with {class_labels.keys()}")
                break
            # add data_class to dictionary and assign it label
            class_labels[data_class] = str(label)
            label_list.append(data_class)
            label += 1
        return class_labels, label_list
    
    #throws FileNotFoundError
    def trim_dataset(self, resource_folder="TrainingData"):
        resource_path = os.path.join(dir_path, resource_folder)
        if not os.path.isdir(resource_path):
            raise FileNotFoundError(f"{resource_folder} does not exist or is invalid!")
        
        for data_class in os.listdir(resource_path):
            print("Trimming: ", data_class)
            #remove files that are not images or are corrupted from the dataset
            for file in os.listdir(os.path.join(resource_path, data_class)):
                path_to_file = os.path.join(resource_path, data_class, file)
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
        resource_path = os.path.join(dir_path, resource_folder)
        if not os.path.isdir(resource_path):
            raise FileNotFoundError(f"{resource_path} does not exist or is invalid!")
        data = []
        for data_class in os.listdir(resource_path):
            for file in os.listdir(os.path.join(resource_path, data_class)):
                path_to_file = os.path.join(resource_path, data_class, file)
                # add files to the dataframe
                data.append([path_to_file, data_class, self.class_labels[data_class]])
        
        df = pd.DataFrame(data, columns=['Path', 'Classification', 'Label'])
        zero_amount = df[df['Label']=="0"]['Label'].count()
        total_amount = df['Label'].count()
        print(zero_amount, total_amount)
        # check for correct distribution
        if zero_amount/total_amount < treshold or zero_amount/total_amount > 1-treshold:
            raise InvalidDatasetDistribution(f"Datasets are distributed incorrectly.\n \
                                            Was {int((1 - zero_amount/total_amount)*100)} | {int((zero_amount/total_amount)*100)} \n \
                                            but should be (at least) {treshold*100} | {(1-treshold)*100}")
            
        # return shuffled dataframe    
        return df.sample(frac=1).reset_index(drop=True)
    
    
    def __init__(self, image_width=256, image_height=256, resource_folder="TrainingData") -> None:
        # create data class labels and label list for easier access to results
        self.class_labels, self.label_list = self.data_class_label(resource_folder)
        
        #prepare dataset for further instructions and create dataframe
        self.trim_dataset(resource_folder)
        self.df = self.create_dataframe(resource_folder)
        self.img_width = image_width
        self.img_height = image_height
        self.model = None

    #@throws IncorrectModelType
    def save_model(self, model, name="model", target_dir="models"):
        if not isinstance(model, Sequential):
            raise IncorrectModelType(f"Should be Sequential, but was {type(model)}")
        if not os.path.isdir(os.path.join(dir_path, target_dir)):
            os.makedirs(os.path.join(dir_path, target_dir))
        
        #TODO uncomment
        #to save only last model
        # if os.path.exists(os.path.join(dir_path, target_dir)):
        #     shutil.rmtree(os.path.join(dir_path, target_dir))
        # os.mkdir(os.path.join(dir_path, target_dir))    
            
        try:
            model.save(os.path.join(os.path.join(dir_path, target_dir), name))
            model.save_weights(os.path.join(os.path.join(dir_path, target_dir), "model_weights.h5"))
        except Exception as e:
            print("Model saving failed!")
            print(e.message)
        else:
            print(f"Model saved successfully at: {os.path.join(os.path.join(dir_path, target_dir), name)}")

    def has_models(self, source_dir="models"):
        return len(os.listdir(source_dir)) != 0
    
    #@returns model
    #@throws IOError
    def load_model(self, source_dir="models", name=""):
        model_dir = os.path.join(dir_path, source_dir)
        print(model_dir)
        if self.has_models(model_dir) != 0:
            models = os.listdir(model_dir)
            path_to_model = os.path.join(model_dir, name)
            # if name is provided, load the model with that name
            if name in models:
                try:
                    print("Loading", path_to_model)
                    model = keras.models.load_model(path_to_model)
                except Exception as e:
                    print(e)
                    user_input = input(f"The model {path_to_model} is not appropriate and could not be loaded. Should it be deleted? [y/n]")
                    if user_input.lower() in {"yes", "y"}:
                        print("Deleting the model...")
                        shutil.rmtree(path_to_model)
                else:
                    print("Model successfully loaded!")
                    return model
            #otherwise, finde first fitting model
            for name in models:
                path_to_model = os.path.join(model_dir, name)
                try:
                    print("Loading", path_to_model)
                    model = keras.models.load_model(path_to_model)
                except Exception as e:
                    print(e)
                    user_input = input(f"The model {path_to_model} is not appropriate and could not be loaded. Should it be deleted? [y/n]")
                    if user_input.lower() in {"yes", "y"}:
                        print("Deleting the model...")
                        shutil.rmtree(path_to_model)
                else:
                    print("Model successfully loaded!")
                    return model   
        return None
    
    # @params
    # train_dataframe, test_dataframe - panas.Dataframe for training and testing
    # throws invalid dataset distribution
    # training model design and some parameters taken from https://www.geeksforgeeks.org/python-image-classification-using-keras/?ref=lbp
    def train_model(self, train_dataframe, test_dataframe=None, img_width=128, img_height=128, sample_limit=5000, epochs=10, batch_size=32, name=None, save=True, target_dir="models"):
        if test_dataframe is None:
            test_dataframe = train_dataframe.copy(deep=True)
        
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
        
        if os.path.exists(os.path.join(dir_path, "checkpoints")):
            shutil.rmtree(os.path.join(dir_path, "checkpoints"))
        os.mkdir(os.path.join(dir_path, "checkpoints"))
        
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        model_checkpoint = keras.callbacks.ModelCheckpoint(os.path.join(os.path.join(dir_path, "checkpoints"), "weights{epoch:08d}.h5"), save_weights_only=True)
        best_checkpoint = keras.callbacks.ModelCheckpoint(os.path.join(os.path.join(dir_path, "checkpoints"), "best_weights.h5"), save_weights_only=True, save_best_only=True)
        model.fit(train_iterator, epochs=epochs, validation_data=test_iterator, callbacks=[model_checkpoint, best_checkpoint])
        
        if save:
            if name is None:
                timestamp = str(datetime.now().strftime("%d_%m_%y"))
                name = "model_" + timestamp
            try:
                self.save_model(model, name, target_dir)
            except IncorrectModelType as e:
                print(e.message)
        
        self.model = model
        return model

    # params model - keras.Model
    # params img_add - np.arr(shape=(1,img_width,img_height,3), dtype=float32)
    # returns np.array [[prediction : float]]
    def predict_img(self, model, img_arr):
        return model.predict(img_arr)
    
if __name__ == "__main__":
    # b = Bot(128, 128)
    # b.data_class_label()
    # b.trim_dataset()
    # df = b.create_dataframe()
    # # b.train_model(df, df, sample_limit=1000, epochs=10)
    # model = b.load_model(path="models/150_epochs")
    # # prediction = b.label_list[int(b.predict(model,'input/d/n02089867_24.jpg')[0][0])]
    # # print(f"Predicted Class: ", prediction)
    # input_dir = "input"
    # while True:
    #     try:
    #         if len(os.listdir(input_dir)) == 1:
    #             path = os.path.join(input_dir, os.listdir(input_dir)[0])
    #             prediction = int(b.predict(model, path)[0][0])
    #             print(f"Predicted Class: ", prediction)
    #             os.remove(path)
    #             time.sleep(1)
    #     except:
    #         pass
    # import base64
    # import sys
    # sys.path.insert(1, "../../../StorageNode")
    # import storage_service
    
    b = Bot(128, 128)
    # b.data_class_label()
    # b.trim_dataset()
    # df = b.create_dataframe()
    # model = b.train_model(df, df, sample_limit=100000, batch_size=100, epochs=150, name="150_epochs")
    model = b.load_model()