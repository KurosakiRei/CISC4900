import vendors.AWS as AWS
import vendors.Clarifai as Clarifai
import vendors.Google as Google
import vendors.IBM as IBM
import redis

class Main:
    # Constructor
    def __init__(self):
        # Initialize all API's object
        # Create necessay data structure
        self.API_list = ['Amazon', 'Clarifai', 'Google', 'IBM']
        self.table = dict()
        self.aws = AWS.Rekonition()
        self.clarifai = Clarifai.Predict()
        self.google = Google.VisionAI()
        self.ibm = IBM.WatsonVisualRecognition()
        
        # Files Path
        self.ImageFolderPath = r'./images'
        self.AnswerKeyPath = r'Answer.txt'
        
        # Table Control
        self.create_table()
        self.update_table()
        
    #  Initialize the data structure  
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
    
    # Comparison
    def update_table(self):
        with open(self.AnswerKeyPath, 'r') as file:
            for each in file:
                image = each.split(' ')
                image = [each.strip() for each in image]
                image_path = self.ImageFolderPath + '\\' + image [0] + '.jpg'
                
                if image[1] == 'null':
                    #self.recognition_invocation(image_path)
                    self.temp_recognition_invocation(image [0])
                    self.null_comparison()
                    self.update_rate_and_F1(self.API_list)
                #Animal    
                else: 
                    #self.recognition_invocation(image_path)
                    self.temp_recognition_invocation(image [0])
                    self.animal_comparison(image)
                    self.update_rate_and_F1(self.API_list)
                #print(image, self.ibm.results)
                    
    # Compare the result for animal line         
    def animal_comparison(self, answer):
        # Amazon
        if answer[1] in self.aws.results:
            self.table['Amazon']['#TruePositive'] += 1
        else:
            self.table['Amazon']['#FalseNegative'] += 1
            
        # Clarifai
        if answer[1] in self.clarifai.results:
            self.table['Clarifai']['#TruePositive'] += 1
        else:
            self.table['Clarifai']['#FalseNegative'] += 1
            
        # Google
        if answer[1] in self.google.results:
            self.table['Google']['#TruePositive'] += 1   
        else:
            self.table['Google']['#FalseNegative'] += 1
            
        # IBM
        if answer[1] in self.ibm.results:
            self.table['IBM']['#TruePositive'] += 1       
        else:
            self.table['IBM']['#FalseNegative'] += 1
            
             
    # Compare the result for No-results line            
    def null_comparison(self):
        # Amazon
        if ('animal' in self.aws.results) or ('caribou' in self.aws.results):
            self.table['Amazon']['#FalsePositive'] += 1
        else:
            self.table['Amazon']['#TrueNegative'] += 1
        # Clarifai     
        if ('animal' in self.clarifai.results) or ('caribou' in self.clarifai.results):
            self.table['Clarifai']['#FalsePositive'] += 1
        else:
            self.table['Clarifai']['#TrueNegative'] += 1
        # Google    
        if ('animal' in self.google.results) or ('caribou' in self.google.results):
            self.table['Google']['#FalsePositive'] += 1
        else:
            self.table['Google']['#TrueNegative'] += 1
        # IBM    
        if ('animal' in self.ibm.results) or ('caribou' in self.ibm.results):
            self.table['IBM']['#FalsePositive'] += 1
        else:
            self.table['IBM']['#TrueNegative'] += 1    
            
            
    # Invoke each class's recognition method           
    def recognition_invocation(self, image):
        # CLear previous results
        self.aws.image_recognition(image)
        self.clarifai.image_recognition(image)
        self.google.image_recognition(image)
        self.ibm.image_recognition(image)
        
     # Inquiry the image data in temporary database   
    def temp_recognition_invocation(self, imageID):
        # CLear previous results
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
            
    # TP/(TP + FN)        
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

        
if __name__ == '__main__': #testing
    obj = Main()
    for each in obj.table:
        print(each, obj.table[each])