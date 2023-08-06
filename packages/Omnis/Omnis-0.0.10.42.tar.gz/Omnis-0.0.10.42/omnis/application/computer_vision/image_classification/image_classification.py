from __future__ import division, print_function

from collections import OrderedDict
import csv
import json
import os

import cv2
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import multi_gpu_model
from keras.callbacks import ModelCheckpoint, EarlyStopping
from math import ceil
import numpy as np

from omnis.lib.config_lib import DeepblockLogConfig, ImageClassificationConfig
from omnis.lib.custom_callback import DeepBlockCallback
from omnis.lib.general_lib import (
    get_data_path_type, reverse_dict,
)
from omnis.lib.image_lib import reshape_data
from omnis.lib.saving_lib import (
    load_models_with_class_indices, save_models_with_class_indices,
)

from .model import image_classification_model
from ...application import Application


class ImageClassification(Application):
    def __init__(self, model_path=None, model_type='densenet121'):
        super().__init__()

        self.model = None
        self.model_type = model_type

        if model_path is not None:
            self.load(model_path)

    def train(self,
              data_path=None,
              optimizer='nadam',
              metrics='accuracy',
              epochs=1,
              batch_size=32,
              verbose=0,
              shuffle=False):
        if not isinstance(metrics, list):
            metrics = [metrics]
        get_image_from = get_data_path_type(data_path)

        train_generator = self.make_train_generator(
            get_image_from=get_image_from,
            data_path=data_path,
            batch_size=batch_size)
        class_indices = self.change_dict_value_int_from_string(
            train_generator.class_indices)
        num_dataset = train_generator.n
        steps_per_epoch = ceil(num_dataset / batch_size)

        if self.model is None:
            self.model = self.create_and_compile_model(
                class_indices=class_indices,
                model_type=self.model_type,
                optimizer=optimizer,
                metrics=metrics)
        if self.deepblock_log:
            deepblock_log_json = OrderedDict()
            deepblock_log_json[
                DeepblockLogConfig.LOG_TYPE] = DeepblockLogConfig.TRAIN_START
            print(json.dumps(deepblock_log_json, ensure_ascii=False))

        callbacks = []
        if self.deepblock_log:
            callbacks = [DeepBlockCallback(
                total_step=steps_per_epoch, total_epoch=epochs)]

        self.model.fit_generator(
            train_generator,
            steps_per_epoch=steps_per_epoch,
            epochs=epochs,
            verbose=verbose,
            callbacks=callbacks,
            shuffle=shuffle)

        if self.deepblock_log:
            deepblock_log_json = OrderedDict()
            deepblock_log_json[DeepblockLogConfig.LOG_TYPE] = \
                DeepblockLogConfig.TRAIN_END
            print(json.dumps(deepblock_log_json, ensure_ascii=False))

    def predict(self, data_path, batch_size=16, verbose=0):
        data_path_type = get_data_path_type(data_path)

        pair_dict = OrderedDict()

        if self.deepblock_log:
            deepblock_log_json = OrderedDict()
            deepblock_log_json[
                DeepblockLogConfig.LOG_TYPE] = DeepblockLogConfig.PREDICT_START
            print(json.dumps(deepblock_log_json, ensure_ascii=False))

        if data_path_type == 'directory':

            datagen = OneDirectoryImageGenerator()
            predict_data_generator = datagen.flow_one_directory(
                directory_path=data_path,
                shuffle=False,
                batch_size=batch_size,
                image_shape=self.model.input_shape[1:3]
            )

            num_dataset = len(predict_data_generator.image_filenames)
            probs = self.model.predict_generator(
                predict_data_generator, steps=ceil(num_dataset / batch_size))
            predicted_order_filenames = \
                predict_data_generator.predict_order_filenames
            predicted_class_indices = probs.argmax(axis=-1)

            reversed_dict = reverse_dict(self.model.class_indices)
            for i in range(len(predicted_class_indices)):
                pair_dict[predicted_order_filenames[i]] = reversed_dict[
                    str(probs.argmax(axis=-1)[i])]

            if self.deepblock_log:
                log_dict = OrderedDict()
                log_dict[
                    DeepblockLogConfig.LOG_TYPE] = \
                    DeepblockLogConfig.PREDICT_END
                log_dict[DeepblockLogConfig.RESULT] = pair_dict
                return json.dumps(log_dict, ensure_ascii=False)
            else:
                return json.dumps(pair_dict, ensure_ascii=False)
        elif data_path_type == 'image':
            _, only_file_name = os.path.split(data_path)
            img_to_predict = cv2.imread(data_path)
            img_array = np.expand_dims(img_to_predict, axis=0)
            reshaped_array = reshape_data(data_array=img_array,
                                          input_shape=self.model.input_shape)
            probs = self.model.predict(
                reshaped_array,
                batch_size=batch_size,
                verbose=verbose)

            reversed_dict = reverse_dict(self.model.class_indices)
            pair_dict[only_file_name] = reversed_dict[
                str(probs.argmax(axis=-1)[0])]

            if self.deepblock_log:
                log_dict = OrderedDict()
                log_dict[
                    DeepblockLogConfig.LOG_TYPE] = \
                    DeepblockLogConfig.PREDICT_END
                log_dict[DeepblockLogConfig.RESULT] = pair_dict
                return json.dumps(log_dict, ensure_ascii=False)
            else:
                return json.dumps(pair_dict, ensure_ascii=False)
        else:
            assert False
            return None

    def load(self, model_path=None):
        try:
            self.model = load_models_with_class_indices(model_path)
            if self.gpu_num > 1:
                self.model = multi_gpu_model(self.model, gpus=self.gpu_num)
        except Exception as e:
            raise e

    def save(self, model_path):
        try:
            if isinstance(self.model, type(None)):
                raise TypeError('You should create a model before saving it')

            if self.deepblock_log:
                log_json = OrderedDict()
                log_json[
                    DeepblockLogConfig.LOG_TYPE] = DeepblockLogConfig.SAVE_START
                log_json[DeepblockLogConfig.SUCCESS] = "true"
                print(json.dumps(log_json, ensure_ascii=False))

            save_models_with_class_indices(self.model, model_path)

            if self.deepblock_log:
                log_json = OrderedDict()
                log_json[
                    DeepblockLogConfig.LOG_TYPE] = DeepblockLogConfig.SAVE_END
                log_json[DeepblockLogConfig.SUCCESS] = "true"
                print(json.dumps(log_json, ensure_ascii=False))
        except Exception as e:
            raise e

    def create_and_compile_model(self, class_indices, model_type, optimizer,
                                 metrics):
        model = image_classification_model(num_classes=len(class_indices),
                                           gpu_num=self.gpu_num,
                                           model_type=model_type)
        model.compile(optimizer=optimizer,
                      loss=keras.losses.categorical_crossentropy,
                      metrics=metrics)
        model.class_indices = class_indices
        return model

    def make_train_generator(self, get_image_from, data_path, batch_size):
        if get_image_from == 'directory':
            train_datagen = ImageDataGenerator(rescale=1. / 255.)
            train_generator = train_datagen.flow_from_directory(
                data_path,
                target_size=ImageClassificationConfig.INPUT_SHAPE[0:2],
                class_mode='categorical',
                batch_size=batch_size)
        elif get_image_from == 'csv':
            train_datagen = CsvGenerator()
            train_generator = train_datagen.flow_from_csv(
                csv_file_path=data_path,
                image_directory_path="",
                target_size=ImageClassificationConfig.INPUT_SHAPE[0:2],
                batch_size=batch_size)

        return train_generator

    def evaluate(self, data_path=None, batch_size=1):
        try:
            if isinstance(data_path, type(None)):
                raise TypeError('You should give a proper data path')

            evaluate_datagen = ImageDataGenerator(rescale=1. / 255)
            validation_generator = evaluate_datagen.flow_from_directory(
                data_path,
                target_size=self.model.input_shape[1:3],
                batch_size=batch_size
            )

            scores = self.model.evaluate_generator(
                validation_generator,
                ceil(len(validation_generator) / batch_size))
            print("accuracy : ", scores[1] * 100)
        except Exception as e:
            raise e

    def change_dict_value_int_from_string(self, class_indices):
        string_class_indices = {}
        for key, value in class_indices.items():
            string_class_indices[key] = str(value)

        return string_class_indices


class CsvGenerator(keras.utils.Sequence):
    def __init__(self, image_filenames=None, image_shape=None, shuffle=False):
        self.image_filenames = image_filenames
        self.image_classes = []
        self.class_indices = []
        self.image_shape = image_shape
        self.shuffle = shuffle
        self.batch_size = 1
        self.n = 0

    def __len__(self):
        return int(np.ceil(len(self.image_filenames) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_x = self.image_filenames[
                  idx * self.batch_size
                  :(idx + 1) * self.batch_size
                  ]
        class_x = self.image_classes[
                  idx * self.batch_size
                  :(idx + 1) * self.batch_size
                  ]

        cnt = 0
        x = []
        index_list = []
        for filename in batch_x:
            try:
                img = cv2.imread(filename)
                resized_img = cv2.resize(img, self.image_shape)
                x.append(resized_img)
                index_list.append(cnt)
                cnt += 1
            except BaseException:
                pass

        batch_y = np.zeros((cnt, len(self.class_indices)), dtype='float')

        i = 0
        for index in index_list:
            find_index = self.class_indices.index(class_x[index])
            batch_y[i, find_index] = 1
            i += 1

        x_array = np.array(x)
        return x_array, batch_y

    def flow_from_csv(self, csv_file_path, image_directory_path,
                      shuffle=False, target_size=None, batch_size=1):
        f = open(csv_file_path, 'r', encoding='utf-8')
        csv_reader = csv.reader(f)
        self.image_classes = list()
        self.image_filenames = list()

        for line in csv_reader:
            atoms = line
            file_full_path = os.path.join(
                image_directory_path, atoms[0] + '.jpg')
            if os.path.isfile(file_full_path):
                self.image_classes.append(atoms[2])
                self.image_filenames.append(file_full_path)
        f.close()
        self.class_indices = list(set(self.image_classes))
        self.shuffle = shuffle
        self.image_shape = target_size
        self.batch_size = batch_size
        self.n = len(self.image_filenames)
        return self


class OneDirectoryImageGenerator(keras.utils.Sequence):
    def __init__(self, image_filenames=None, image_classes=None,
                 batch_size=None, image_shape=None, shuffle=False):
        self.image_filenames = image_filenames
        self.image_classes = image_classes
        self.batch_size = batch_size
        self.image_shape = image_shape
        self.shuffle = shuffle
        self.predict_order_filenames = []

    def __len__(self):
        return int(np.ceil(len(self.image_filenames) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_x = self.image_filenames[
                  idx * self.batch_size
                  :(idx + 1) * self.batch_size
                  ]

        x = []
        for filename in batch_x:
            _, only_file_name = os.path.split(filename)
            self.predict_order_filenames.append(only_file_name)
            img = cv2.imread(filename)
            test_data = np.expand_dims(img, axis=0)
            resized_img = cv2.resize(test_data[0], self.image_shape)
            x.append(resized_img)

        data_array = np.asarray(x)
        data_array = data_array.astype('float32')
        data_array /= 255
        return data_array

    def flow_one_directory(self, directory_path,
                           shuffle=False, batch_size=1, image_shape=None):
        file_list = os.listdir(directory_path)
        self.image_filenames = [
            f'{directory_path}/{file_name}' for file_name in file_list
        ]
        self.batch_size = batch_size
        self.image_shape = image_shape
        self.shuffle = shuffle

        return self
