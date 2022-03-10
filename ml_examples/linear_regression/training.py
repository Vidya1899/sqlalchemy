import os
import gzip
import random
import pickle
import yaml
import pandas as pd
from base64 import b64encode
from sklearn.linear_model import LinearRegression
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
    blob = Column(LargeBinary)


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


def create_data(config):
    """
    Generates data for linear regression
        *    Configuration dictionary

    :param config: config dict for dataset configurations
    :return: dataset as a pandas dataframe
    """
    m = config["gradient"]
    c = config["y_intercept"]
    data = []
    for x in range(config["x_start"], config["x_end"]):
        # for x from x_start to x_end generate y using y=mx+c with random noise based on range specified in config
        y = m * x + c + random.uniform(config["noise_range_start"], config["noise_range_end"])
        data.append([x, y])
    dataframe = pd.DataFrame(data, columns=['x', 'y'])
    return dataframe


def train_lr(df, config):
    """
    Trains the linear regressor for the given dataset
        *    The dataset for training
        *    The config for training configurations

    :param df: The dataframe
    :param config: Config for train configurations
    :return: The regressor model object
    """
    X = df.iloc[:, :-1].values
    # get a copy of dataset, exclude last column
    y = df.iloc[:, 1].values

    # split to train and test set and start training the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=config["test_size"],
                                                        random_state=config["random_state"])
    regressor = LinearRegression()
    regressor = regressor.fit(X_train, y_train)

    # save the regressor in the model directory
    isExist = os.path.exists(config["model_directory"])

    if not isExist:
        # Create a new directory if it does not exist already
        os.makedirs(config["model_directory"])

    with open(os.path.join(config["model_directory"], config["model_file"]), "wb") as f:
        # Dump pickle into the path specified in configs
        pickle.dump(regressor, f)
    return regressor


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
    dataset = create_data(my_config)
    model_obj = train_lr(dataset, my_config)
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
