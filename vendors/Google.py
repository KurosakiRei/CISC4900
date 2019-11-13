import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
  
class VisionAI: # Class of AWS's API
    
    def __init__(self): # Constructor
        self.results = list() # Create a empty list
        
    def image_recognition(self, image_path):
        self.results.clear()
        image = self.get_file_content(image_path) # Create an image object
        
<<<<<<< HEAD
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'D:\github-repos\CISC4900 - Copy\ServiceAccountToken.json'
=======
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'..\CISC4900 - Copy\ServiceAccountToken.json'
>>>>>>> 7532f240e7eabf27204912d966c2ebe391d82aab
        # Instantiates a client
        client = vision.ImageAnnotatorClient()
        
        response = client.label_detection(image=image)
        labels = response.label_annotations
        for each in labels:
            if float(each.score) >= 0.8:        
                self.results.append(each.description)
        self.format_output()
        return self.results 
        
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
<<<<<<< HEAD
    results = google.image_recognition(r'C:\Users\KurosakiRei\Desktop\caribou.jpg')
=======
    results = google.image_recognition(r'.\Tested resources\caribou.jpg')
>>>>>>> 7532f240e7eabf27204912d966c2ebe391d82aab
    print(results)
