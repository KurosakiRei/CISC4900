import vendors.AWS as AWS
import vendors.Clarifai as Clarifai
import vendors.Google as Google
import vendors.IBM as IBM
import Render 
import redis

class Main:
    # Constructor
    def __init__(self):
        # Initialize all API's object
        # Create necessay data structure
        self.answers = ['animal', 'deer', 'caribou']
        self.API_list = ['Amazon', 'Clarifai', 'Google', 'IBM']
        self.table = dict()
        self.aws = AWS.Rekonition()
        self.clarifai = Clarifai.Predict()
        self.google = Google.VisionAI()
        self.ibm = IBM.WatsonVisualRecognition()
        self.render = Render.Processing()
        
        # Files Path
        self.ImageFolderPath = r'.\images'
        self.AnswerKeyPath = r'.\anwsers.txt'
        
        # Table Control
        self.create_table()
        self.update_table()
        
    # Initialize the data structure  
    def create_table(self):
        for each in self.API_list:
            self.table.setdefault(each, {})
            self.table[each].setdefault('#TruePositive', 0)
            self.table[each].setdefault('#TrueNegative', 0)
            self.table[each].setdefault('#FalsePositive', 0)
            self.table[each].setdefault('#FalseNegative', 0)
            self.table[each].setdefault('Precision', 0)
            self.table[each].setdefault('Recall', 0)
            self.table[each].setdefault('F1-Score', 0)
    
    # Start comparison
    def update_table(self):
        with open(self.AnswerKeyPath, 'r') as file:
            for each in file:
                image = each.split('\t')
                image = [each.strip() for each in image]
                imageID, answer = image[0], image[1]
                image_path = self.ImageFolderPath + '\\' + imageID + '.jpg'
                #self.recognition(image_path)
                self.temp_recognition(imageID)
                self.comparison(imageID, answer)
            self.update_rate_and_F1(self.API_list)
            self.render.HTMLGenerator()
    # Comparison         
    def comparison(self, imageID, answer):
        # Compare the result for Null line 
        if answer == 'null':
            imageID = imageID + " - Null"
            self.render.setImageID(imageID)
            # Amazon
            if len(set(self.answers).intersection(self.aws.results)):
                self.table['Amazon']['#FalsePositive'] += 1
                self.render.setImageResults(imageID, 'Amazon', self.aws.results, 'FalsePositive +1')
                
            else:
                self.table['Amazon']['#TrueNegative'] += 1
                self.render.setImageResults(imageID, 'Amazon', self.aws.results, 'TrueNegative +1')
                
            # Clarifai     
            if len(set(self.answers).intersection(self.clarifai.results)):
                self.table['Clarifai']['#FalsePositive'] += 1
                self.render.setImageResults(imageID, 'Clarifai', self.clarifai.results, 'FalsePositive +1')
            else:
                self.table['Clarifai']['#TrueNegative'] += 1
                self.render.setImageResults(imageID, 'Clarifai', self.clarifai.results, 'TrueNegative +1')
                
            # Google    
            if len(set(self.answers).intersection(self.google.results)):
                self.table['Google']['#FalsePositive'] += 1
                self.render.setImageResults(imageID, 'Google', self.google.results, 'FalsePositive +1')
            else:
                self.table['Google']['#TrueNegative'] += 1
                self.render.setImageResults(imageID, 'Google', self.google.results, 'TrueNegative +1')
                
            # IBM    
            if len(set(self.answers).intersection(self.ibm.results)):
                self.table['IBM']['#FalsePositive'] += 1
                self.render.setImageResults(imageID, 'IBM', self.ibm.results, 'FalsePositive +1')
            else:
                self.table['IBM']['#TrueNegative'] += 1
                self.render.setImageResults(imageID, 'IBM', self.ibm.results, 'TrueNegative +1')
            
        # Compare the result for animal line               
        else:
            imageID = imageID + " - Animal"
            self.render.setImageID(imageID)
            # Amazon
            if len(set(self.answers).intersection(self.aws.results)):
                self.table['Amazon']['#TruePositive'] += 1
                self.render.setImageResults(imageID, 'Amazon', self.aws.results, 'TruePositive +1')
            else:
                self.table['Amazon']['#FalseNegative'] += 1
                self.render.setImageResults(imageID, 'Amazon', self.aws.results, 'FalseNegative +1')
                
            # Clarifai
            if len(set(self.answers).intersection(self.clarifai.results)):
                self.table['Clarifai']['#TruePositive'] += 1
                self.render.setImageResults(imageID, 'Clarifai', self.clarifai.results, 'TruePositive +1')
            else:
                self.table['Clarifai']['#FalseNegative'] += 1
                self.render.setImageResults(imageID, 'Clarifai', self.clarifai.results, 'FalseNegative +1')
                
            # Google
            if len(set(self.answers).intersection(self.google.results)):
                self.table['Google']['#TruePositive'] += 1
                self.render.setImageResults(imageID, 'Google', self.google.results, 'TruePositive +1')   
            else:
                self.table['Google']['#FalseNegative'] += 1
                self.render.setImageResults(imageID, 'Google', self.google.results, 'FalseNegative +1')  
                
            # IBM
            if len(set(self.answers).intersection(self.ibm.results)):
                self.table['IBM']['#TruePositive'] += 1
                self.render.setImageResults(imageID, 'IBM', self.ibm.results, 'TruePositive +1')        
            else:
                self.table['IBM']['#FalseNegative'] += 1
                self.render.setImageResults(imageID, 'IBM', self.ibm.results, 'FalseNegative +1')     
            
            
    # Invoke each class's recognition method           
    def recognition(self, image):
        self.aws.image_recognition(image)
        self.clarifai.image_recognition(image)
        self.google.image_recognition(image)
        self.ibm.image_recognition(image)
        
    # Inquiry the image data in temporary database   
    def temp_recognition(self, imageID):
        database = redis.Redis(host = '127.0.0.1', port = '6379')
        self.aws.get_image_data(database, 'Amazon', imageID)
        self.clarifai.get_image_data(database, 'Clarifai', imageID)
        self.google.get_image_data(database, 'Google', imageID)
        self.ibm.get_image_data(database, 'IBM', imageID)
    
    # Update Precision, Recall, F1-Score
    def update_rate_and_F1(self, API_list):
        for each in API_list:
            self.table[each]['Precision'] = self.get_precision_rate(each)
            self.table[each]['Recall'] = self.get_recall_rate(each)
            self.table[each]['F1-Score'] = self.get_F1score(each)
            
    # TP/(TP + FP)        
    def get_precision_rate(self, API):
        TP = self.table[API]['#TruePositive']
        FP = self.table[API]['#FalsePositive']
        if TP + FP != 0:
            return TP/(TP + FP) * 100
        else:
            return 0
        
    # TP/(TP + FN)
    def get_recall_rate(self, API):
        TP = self.table[API]['#TruePositive']
        FN = self.table[API]['#FalseNegative']
        if TP + FN != 0:
            return TP/(TP + FN) * 100
        else:
            return 0
    
    # 2 * ((precision * recall) / (precision + recall))
    def get_F1score(self, API):
        precision = self.table[API]['Precision']
        recall = self.table[API]['Recall']
        if precision + recall != 0:
            return 2.0 * ((precision * recall)/(precision + recall))
        else:
            return 0.0

# Testing        
if __name__ == '__main__':
    obj = Main()
    for i in obj.render.images_results:
        print(i)
        for j in obj.render.images_results[i]:
            print(j, obj.render.images_results[i][j])
        print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    for each in obj.table:
        print(each, obj.table[each])