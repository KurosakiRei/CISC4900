import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
import config
  
class VisionAI: # Class of AWS's API
    
    def __init__(self): # Constructor
        self.results = list() # Create a empty list
        
    def image_recognition_label_detection(self, image_path):
        templist = list()
        image = self.get_file_content(image_path) # Create an image object
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.GOOGLE
        # Instantiates a client
        client = vision.ImageAnnotatorClient()
        
        response = client.label_detection(image=image)
        labels = response.label_annotations
        for each in labels:
            if float(each.score) >= 0.8:        
                templist.append(each.description)
        self.results = templist
        self.format_output()
    
    def image_recognition_object_localization(self, image_path):
        templist = list()
        image = self.get_file_content(image_path) # Create an image object
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.GOOGLE
        # Instantiates a client
        client = vision.ImageAnnotatorClient()
        
        response = client.object_localization(image=image)
        labels = response.localized_object_annotations
        for each in labels:       
            templist.append(each.name)
        self.results = templist
        self.format_output()
        
    def image_recognition_web_detection(self, image_path):
        templist = list()
        image = self.get_file_content(image_path) # Create an image object
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.GOOGLE
        # Instantiates a client
        client = vision.ImageAnnotatorClient()
        
        response = client.web_detection(image=image)
        labels = response.web_detection.best_guess_labels
        for each in labels:       
            templist.append(each.label)
        self.results = templist
        self.format_output()
        
    # Method for Loads the image file
    def get_file_content(self, filePath): 
        # The name of the image file to annotate
        file_name = os.path.abspath(filePath)
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
            return types.Image(content=content)
    
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
    google = VisionAI()
    google.image_recognition3(os.getcwd() + os.sep + 'Tested resources\caribou.jpg')
    print(google.results)

