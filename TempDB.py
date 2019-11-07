import redis
import os
import vendors.AWS as AWS
import vendors.Clarifai as Clarifai
import vendors.Google as Google
import vendors.IBM as IBM


class Redis:
    # Constructor
    def __init__(self):
        # Initialize all API's object
        # Create necessay data structure
        self.API_list = ['Amazon', 'Clarifai', 'Google', 'IBM']
        self.database = redis.Connection(host = '127.0.0.1')
        self.aws = AWS.Rekonition()
        self.clarifai = Clarifai.Predict()
        self.google = Google.VisionAI()
        self.ibm = IBM.WatsonVisualRecognition()
        self.image_name_list = os.listdir(r"./images")
    
    def tester(self):
        print(self.image_name_list)
        print(len(self.image_name_list))
    def initial_database(self):
        pass
    def get_image_data(self):
        pass

if __name__ == "__main__":
    redis = Redis()
    redis.tester()