from ingestion import DataIngestion
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from utils.custom_logger import app_logger as logger
import joblib, os


def train_model(X_train, y_train, X_test, y_test):
    """
    Train a logistic regression model
    """
    logger.info("Training the model : Start")

    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    logger.info("Model trained successfully")

    logger.info(f"Classification report: {classification_report(y_test, y_pred)}")

    return model, classification_report(y_test, y_pred)


def save_model(model, preprocessor, model_path, preprocessor_path):
    """
    Save the model to a file
    """

    # check if model already exists then rename it to model_old.pkl
    if os.path.exists(model_path):
        # take the last part of the path and add _old to it
        logger.info("Saving Model : Model already exists")
        logger.info(f"Saving Model : Old model path: {model_path}")

        base_path = model_path.split("/")[:-1][0]
        logger.info(f"Saving Model : base path is: {base_path}")

        model_old_path = base_path + "/" + "old_model.pkl"
        preprocessor_old_path = base_path + "/" + "old_preprocessor.pkl"

        logger.info(f"Saving Model : Old model path: {model_old_path}")
        logger.info("Saving Model : Old model renamed to *_old.pkl")

        os.rename(model_path, model_old_path)
        os.rename(preprocessor_path, preprocessor_old_path)


    
    # other conditions can be set to make sure no request is recieved while saving and updating the model but for now this can be good enough 

    joblib.dump(model, model_path)
    joblib.dump(preprocessor, preprocessor_path)
    logger.info(f"Saving Model : Model saved to {model_path}")
    logger.info(f"Saving Model : Preprocessor saved to {preprocessor_path}")

    # return the full path of the saved model
    return model_path, preprocessor_path


if __name__ == "__main__":

    logger.info("Train.py script started")

    # Initialize the data ingestion class
    data_ingestion = DataIngestion("data/dataset.csv")
    logger.info("Data ingestion class initialized")

    # Read the data
    data_ingestion.read_data()
    logger.info("Data read successfully")
 
    # Preprocess the data
    X_train, X_test, X_inference, y_train, y_test, y_inference, preprocessor, val_size_number, inference_size_number = data_ingestion.preprocess_train()
    logger.info("Data preprocessed successfully")
    logger.info(f"X_train shape: {X_train.shape}")
    logger.info(f"X_test shape: {X_test.shape}")
    logger.info(f"X_inference shape: {X_inference.shape}")

    # convert numpy ndarrays to pandas dataframes
    X_train = pd.DataFrame(X_train, columns=preprocessor.get_feature_names_out())
    X_test = pd.DataFrame(X_test, columns=preprocessor.get_feature_names_out())
    X_inference = pd.DataFrame(X_inference, columns=preprocessor.get_feature_names_out())

    # save the separated datasets
    # calculate base path from the current file path
    base_path = os.path.dirname(os.path.abspath(__file__)) 

    X_train.to_csv(base_path + "X_train.csv", index=False)
    X_test.to_csv(base_path + "X_test.csv", index=False)
    X_inference.to_csv(base_path + "X_inference.csv", index=False)
    y_train.to_csv(base_path + "y_train.csv", index=False)
    y_test.to_csv(base_path + "y_test.csv", index=False)
    y_inference.to_csv(base_path + "y_inference.csv", index=False)
    

    logger.info("Data splits saved successfully")

    # Train the model
    model, report_ = train_model(X_train, y_train, X_test, y_test)
    logger.info("Model trained successfully")

    # Save the model
    print( save_model(model, preprocessor, "model.pkl", "preprocessor.pkl") ) 

    print("Model trained successfully")
