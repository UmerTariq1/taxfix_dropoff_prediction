import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from src.utils.custom_logger import app_logger as logger

class DataIngestion:
    def __init__(self, file_path=None):
        '''
        Data Ingestion and Preprocessing:
        ■ Read and prepare the provided clean dataset (CSV with 5,000 rows).
        ■ Perform necessary preprocessing, including feature encoding, scaling etc.
        ■ Split the dataset into proper training, testing, and inference datasets to simulate real-world conditions.


        Columns:
        ● age: Age of the user.
        ● income: Annual income in Euros.
        ● employment_type: Type of employment (e.g., full_time, part_time, unemployed).
        ● marital_status: User's marital status (e.g., single, married, divorced).
        ● time_spent_on_platform: Total time spent on the platform (in minutes).
        ● number_of_sessions: Total number of sessions.
        ● fields_filled_percentage: Percentage of tax fields filled by the user.
        ● previous_year_filing: Whether the user filed taxes in the previous year (binary: 0/1).
        ● device_type: Device type used by the user (e.g., mobile, desktop, tablet).
        ● referral_source: Source of referral (e.g., friend_referral, organic_search,
        social_media_ad).
        ● completed_filing (Target Variable): Whether the user completed the tax filing process
        (binary: 0/1).
        
        '''
        if file_path!=None: # file_path is none when doing for inference. so no need to set these variables
            self.file_path = file_path
            self.numerical_features = ['age', 'income', 'time_spent_on_platform', 'number_of_sessions', 'fields_filled_percentage']
            self.categorical_features = ['employment_type', 'marital_status', 'previous_year_filing', 'device_type', 'referral_source']
            self.target_column = 'completed_filing'

    def read_data(self):
        """
        Read data from a file and return a pandas DataFrame
        """
        self.df = pd.read_csv(self.file_path)

    def split(self, x_features, y_features, test_size=0.2):
        """
        split data into training and testing sets
        """
        x_train, x_test, y_train, y_test = train_test_split(x_features, y_features, test_size=test_size, random_state=42)
        return x_train, x_test, y_train, y_test
    
    async def preprocess_test(self, df: pd.DataFrame, preprocessor):
        """
        Preprocess the data for inference
        """
        return preprocessor.transform(df)

    def preprocess_train(self, val_size=0.2, inference_size=0.05):
        """
        Preprocess the data by encoding categorical features
        """

        # Define the preprocessing pipeline
        num_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])
        # One-hot encode the categorical features
        cat_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        # Combine the preprocessing steps
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', num_transformer, self.numerical_features),
                ('cat', cat_transformer, self.categorical_features)
            ])
        
        logger.info("Retraining: Ingestion : Preprocessor initialized")

        X = self.df.drop(self.target_column, axis=1)
        y = self.df[self.target_column]

        val_size_number = int(val_size * len(X))
        inference_size_number = int(inference_size * len(X))

        logger.info(f"Retraining: Ingestion : Validation size: {val_size_number}")
        logger.info(f"Retraining: Ingestion : Inference size: {inference_size_number}")

        x_train, x_temp, y_train, y_temp = self.split(X, y, test_size=val_size)
        x_test, x_inference, y_test, y_inference = self.split(x_temp, y_temp, test_size=inference_size)

        x_train = preprocessor.fit_transform(x_train)
        x_test = preprocessor.transform(x_test)
        x_inference = preprocessor.transform(x_inference)

        logger.info("Retraining: Ingestion : Data preprocessed successfully")

        return x_train, x_test, x_inference, y_train, y_test, y_inference, preprocessor, val_size_number, inference_size_number


            
        


