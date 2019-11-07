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
        self.database = redis.Redis(host = '127.0.0.1', port = '6379')
        self.aws = AWS.Rekonition()
        self.clarifai = Clarifai.Predict()
        self.google = Google.VisionAI()
        self.ibm = IBM.WatsonVisualRecognition()
        self.image_name_list = [ r'images/' + each for each in os.listdir(r'./images')]
        self.error_image = list()
        
    def get_images_data(self):
        count = 0
        for each in self.image_name_list:
            image_id = each.split('/')[-1].split('.')[0]
            count += 1
            print(image_id, count)
            # Amazon
            if self.database.hsetnx(self.API_list[0], image_id, str(self.aws.image_recognition(each))) != 1:
                self.error_image.append([self.API_list[0], image_id])
                
            # Clarifai    
            if self.database.hsetnx(self.API_list[1], image_id, str(self.clarifai.image_recognition(each))) != 1:
                self.error_image.append([self.API_list[1], image_id])
                
            # Google    
            if self.database.hsetnx(self.API_list[2], image_id, str(self.google.image_recognition(each))) != 1:
                self.error_image.append([self.API_list[2], image_id])
                
            # IBM    
            if self.database.hsetnx(self.API_list[3], image_id, str(self.ibm.image_recognition(each))) != 1:
                self.error_image.append([self.API_list[3], image_id])
        # No any errors
        if len(self.error_image) == 0:
            return True
        else:
            return False
if __name__ == "__main__":
    redis = Redis()
    if redis.get_images_data():
        print('Imported Successfully!')