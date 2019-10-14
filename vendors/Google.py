import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
  
class Google: # Class of AWS's API
    
    def __init__(self): # Constructor
        self.results = list() # Create a empty list
        
    def image_recognition(self, image_path):
        image = self.get_file_content(image_path) # Create an image object
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'
        # Instantiates a client
        client = vision.ImageAnnotatorClient()
        
        response = client.label_detection(image=image)
        labels = response.label_annotations
        for each in labels:
            if float(each.score) >= 0.8:        
                self.results.append(each.description)
        return self.results 
        
        # Method for Loads the image file
    def get_file_content(self, filePath): 
        # The name of the image file to annotate
        file_name = os.path.abspath(filePath)
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
            return types.Image(content=content)
    
    # Testing 
if __name__ == "__main__": 
    google = Google()
    results = google.image_recognition('husky.jpg')
    print(results)
