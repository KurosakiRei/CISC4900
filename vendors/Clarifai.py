from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import config

class Predict: # Class of AWS's API
    
    def __init__(self): # Constructor
        self.results = list() # Create a empty list
    
    def image_recognition(self, image_path):
        templist = list()
        app = ClarifaiApp(api_key=config.CLARIFAI['api_key']) # Enter the API key
        model = app.public_models.general_model # Create a Clarifai's Client Object
        model.model_version = config.CLARIFAI['version'] # Set the client's version
        response = model.predict_by_filename(filename=image_path) # Calling the "Recognition" method
        labels = response['outputs'][0]['data']['concepts'] # Processing the output format
        for each in labels:# Filtering the results that score is lower than 0.8
            if each['value'] >= 0.8:
                templist.append(each['name']) # Appending the results to the list
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
    clarifai = Predict()
    results = clarifai.image_recognition(r'.\Tested resources\caribou.jpg')
    print(results)