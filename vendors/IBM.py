from ibm_watson import VisualRecognitionV3 # IBM's SDK
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator # IBM's SDK
import config

class WatsonVisualRecognition: # Class of AWS's API
    
    def __init__(self): # Constructor
        self.results = list() # Create a empty list
        
    def image_recognition(self, image_path):
        templist = list()
        with open(image_path, 'rb') as images_file: # Create an image object
            authenticator = IAMAuthenticator(config.IBM['api_key']) # Enter the API_KEY here
            visual_recognition = VisualRecognitionV3(version = config.IBM['version'], authenticator = authenticator) # Create a IBM's VisualRecognition object
            labels = visual_recognition.classify(images_file = images_file, threshold = '0.8').get_result() # Calling its "Label detection" method and filtering the results that score is lower than 0.8
            labels = labels['images'][0]['classifiers'][0]['classes'] # Processing output format
            for each in labels:
                templist.append(each['class']) # Appending the names into the list
            self.results = templist
            self.format_output()
    
    # Get data from the database    
    def get_image_data(self, database, API, imageID):
        self.results = list(set(database.hget(API, imageID).decode('ascii').replace('\'','').replace('[', '').replace(']', '').split(', ')))
        self.format_output()
    
    # Uniforms all results to same format and separate words
    def format_output(self):
        self.results = [ each.lower() for each in self.results]
        templist = list()
        for i in self.results:
            for j in i.split(' '):
                templist.append(j)
        self.results = templist
        
# Testing    
if __name__ == "__main__":  
    ibm = WatsonVisualRecognition()
    results = ibm.image_recognition(r'.\Tested resources\caribou.jpg')
    print(results)