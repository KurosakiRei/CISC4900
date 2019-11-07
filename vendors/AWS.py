import boto3 # AWS SDK
import redis
  
class Rekonition: # Class of AWS's API
    
    def __init__(self): # Constructor
        self.results = list() # Create a empty list
        
    def image_recognition(self, image_path):
        self.results.clear()
        image = self.get_file_content(image_path) # Create an image object
        
        client = boto3.client('rekognition') # Create a AWS client object
        response = client.detect_labels(Image={'Bytes': image,}) # Calling its "Label detection" method and assign the results to "response"
        labels = response['Labels'] # Processing output format
        for each in labels:
            if each['Confidence'] >= 80: # Filtering the results that score is lower than 0.8
                self.results.append(each['Name']) # Appending the names into the list
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
            
    def get_file_content(self, filePath): # Method for opening the image file and return an image object
        with open(filePath, 'rb') as fp:
            return fp.read()
    
    
    
if __name__ == "__main__": # Testing 
    aws = Rekonition()
    results = aws.image_recognition(r'C:\Users\KurosakiRei\Desktop\caribou.jpg')
    print(results)
        