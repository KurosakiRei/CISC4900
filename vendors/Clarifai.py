from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

class Predict: # Class of AWS's API
    
    def __init__(self): # Constructor
        self.results = list() # Create a empty list
        
    def image_recognition(self, image_path):
        self.results.clear()
        app = ClarifaiApp(api_key='4e651845c45345a783e8d3a42e167174') # Enter the API key
        model = app.public_models.general_model # Create a Clarifai's Client Object
        model.model_version = 'aa7f35c01e0642fda5cf400f543e7c40' # Set the client's version
        response = model.predict_by_filename(filename=image_path) # Calling the "Recognition" method
        
     
        labels = response['outputs'][0]['data']['concepts'] # Processing the output format
        for each in labels:# Filtering the results that score is lower than 0.8
            if each['value'] >= 0.8:
                self.results.append(each['name']) # Appending the results to the list
        self.format_output()
        return self.results
    
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
    results = clarifai.image_recognition(r'C:\Users\KurosakiRei\Desktop\caribou.jpg')
    print(results)