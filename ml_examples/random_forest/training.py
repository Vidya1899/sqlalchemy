import os
import gzip
import pickle
import yaml
import pandas as pd
import numpy as np
from base64 import b64encode
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary

Base = declarative_base()
CONFIG_PATH = ""


# Create a table for the models
class Models(Base):
    __tablename__ = 'models'
    model_id = Column(Integer, primary_key=True)
    model_name = Column(String(30))
    blob = Column(LargeBinary(length=(3773838)))


def load_config(config_name):
    """
    Loads the base configurations for the model
        *    Configuration for model from config.yml

    :param: config_name
    :return: loaded config dictionary
    """
    with open(os.path.join(CONFIG_PATH, config_name)) as file:
        config = yaml.safe_load(file)
    return config


def train_rf(df, config):
    """
    Preprocess and train the random forest model

    :param df: Dataset
    :param config: Training configurations
    :return: model object
    """
    # One-hot encode the data using pandas get_dummies
    features = pd.get_dummies(df)
    # Display the first 5 rows of the last 12 columns
    # features.iloc[:, 5:].head(5)
    # Labels are the values we want to predict
    labels = np.array(features['actual'])
    # Remove the labels from the features
    # axis 1 refers to the columns
    features = features.drop('actual', axis=1)
    # Saving feature names for later use
    feature_list = list(features.columns)
    # Convert to numpy array
    features = np.array(features)
    # Split the data into training and testing sets
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels,
                                                                                test_size=config["test_size"],
                                                                                random_state=config["random_state"])
    # Instantiate model with 1000 decision trees
    rf = RandomForestRegressor(n_estimators=config["n_estimators"], random_state=config["random_state"])
    # Train the model on training data
    rf = rf.fit(train_features, train_labels)

    isExist = os.path.exists(config["model_directory"])

    if not isExist:
        # Create a new directory if it does not exist already
        os.makedirs(config["model_directory"])

    with open(os.path.join(config["model_directory"], config["model_file"]), "wb") as f:
        # Dump pickle into the path specified in configs
        pickle.dump(rf, f)

    return rf


def compress(model):
    """
    Pickles, compresses and base64 encodes the model

    :param model: model object
    :return: Compressed and encoded model
    """
    pickled_data = pickle.dumps(model)
    compressed = gzip.compress(pickled_data, compresslevel=9)
    encoded_data = b64encode(compressed)
    return encoded_data


if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://vidya:Vidya1899@localhost/models', echo=True)

    # load model config
    my_config = load_config("config.yml")

    # Create and train dataset
    dataset = pd.read_csv(my_config["data_directory"])
    model_obj = train_rf(dataset, my_config)
    compressed_model = compress(model_obj)

    # Create the Models table
    Base.metadata.create_all(engine, checkfirst=True)

    # use sessionmaker to provide a factory for Session objects against the engine
    Session = sessionmaker(bind=engine)

    # add the model record to the table and commit
    model_record = Models(model_id=my_config["model_id"], model_name=my_config["model_name"], blob=compressed_model)
    session1 = Session()
    session1.add(model_record)
    session1.commit()
