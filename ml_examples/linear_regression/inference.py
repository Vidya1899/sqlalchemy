import gzip
import pickle
from base64 import b64decode
from sqlalchemy import create_engine
from training import Models
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('mysql+pymysql://vidya:Vidya1899@localhost/models', echo=True)
Base = declarative_base()


def decode(blob):
    # decode base64, uncompress and load for inference
    decoded = b64decode(blob)
    uncompressed_data = gzip.decompress(decoded)
    regressor = pickle.loads(uncompressed_data)
    return regressor


if __name__ == '__main__':

    Session = sessionmaker(bind=engine)
    session1 = Session()

    model = session1.query(Models).filter_by(model_name='linear_regression').first()

    # Get regressor for inference
    inf_model = decode(model.blob)

    # Inference
    result = inf_model.predict([[5000]])
    print(result)
