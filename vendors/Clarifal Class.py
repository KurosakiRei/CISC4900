from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

class Clarifai: # Class of AWS's API
    
    def __init__(self): # Constructor
        self.results = list() # Create a empty list
        
    def image_recognition(self, image_path):
    
        app = ClarifaiApp(api_key='4e651845c45345a783e8d3a42e167174') # Enter the API key
        model = app.public_models.general_model # Create a Clarifai's Client Object
        model.model_version = 'aa7f35c01e0642fda5cf400f543e7c40' # Set the client's version
        response = model.predict_by_filename(filename=image_path) # Calling the "Recognition" method
        
     
        labels = response['outputs'][0]['data']['concepts'] # Processing the output format
        for each in labels:# Filtering the results that score is lower than 0.8
            if each['value'] >= 0.8:
                self.results.append(each['name']) # Appending the results to the list
        return self.results
    
    # Testing 
if __name__ == "__main__": 
    clarifai = Clarifai()
    results = clarifai.image_recognition('husky.jpg')
    print(results)