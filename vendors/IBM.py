from ibm_watson import VisualRecognitionV3 # IBM's SDK
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator # IBM's SDK

class WatsonVisualRecognition: # Class of AWS's API
    
    def __init__(self): # Constructor
        self.results = list() # Create a empty list
        
    def image_recognition(self, image_path):
        with open(image_path, 'rb') as images_file: # Create an image object
            authenticator = IAMAuthenticator('si21GLXqCMSdhw15pibaI9Dl98v-n_IrO1-_NNfSk95B') # Enter the API_KEY here
            visual_recognition = VisualRecognitionV3(version = '2019-09-11', authenticator = authenticator) # Create a IBM's VisualRecognition object
            labels = visual_recognition.classify(images_file = images_file, threshold = '0.8').get_result() # Calling its "Label detection" method and filtering the results that score is lower than 0.8
            labels = labels['images'][0]['classifiers'][0]['classes'] # Processing output format
            for each in labels:
                self.results.append(each['class']) # Appending the names into the list
            return self.results
    
    
if __name__ == "__main__": # Testing 
    ibm = WatsonVisualRecognition()
    results = ibm.image_recognition(r'C:\Users\KurosakiRei\Desktop\caribou.jpg')
    print(results)