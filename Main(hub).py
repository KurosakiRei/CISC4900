import vendors.AWS as AWS
import vendors.Clarifai as Clarifai
import vendors.Google as Google
import vendors.IBM as IBM

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
        
        #Files Path
        self.ImageFolderPath = r'D:\github-repos\CISC4900\images'
        self.AnswerKeyPath = r'D:\github-repos\CISC4900\Answer.txt'
        
        #----------------------------------------------------------
        self.create_table()
        self.update_table()
    
    #  Initialize the data structure  
    def create_table(self):
        for each in self.API_list:
            self.table.setdefault(each, {})
            self.table[each].setdefault('#Correct', 0)
            self.table[each].setdefault('#Wrong', 0)
            self.table[each].setdefault('#NoResult', 0)
            self.table[each].setdefault('Precision', 0)
            self.table[each].setdefault('Recall', 0)
            self.table[each].setdefault('F1-Score', 0)
    
    # Comparison
    def update_table(self):
        with open(self.AnswerKeyPath, 'r') as file:
            for each in file:
                image = each.split(' ')
                image = [ each.strip() for each in image]
                image_path = self.ImageFolderPath + '\\' + image [0] + '.jpg'
                print(image, image_path)
                if image[1] == 'null':
                    self.recognition_invocation(image_path)
                    self.noresult_comparison()
                    self.update_rate_and_F1(self.API_list)
                #Animal    
                else: 
                    self.recognition_invocation(image_path)
                    self.animal_comparison(image)
                    self.update_rate_and_F1(self.API_list)
                    
    # Compare the result for animal line         
    def animal_comparison(self, answer):
        # Amazon
        if answer[1] in self.aws.results:
            self.table['Amazon']['#Correct'] += 1
            
            """ if answer[2] in self.aws.results:
                self.table['Amazon']['#Correct'] += 1
            else:
                self.table['Amazon']['#Wrong'] += 1 """
                
        else:
            self.table['Amazon']['#Wrong'] += 1
        # Clarifai
        if answer[1] in self.clarifai.results:
            self.table['Clarifai']['#Correct'] += 1
            
            """ if answer[2] in self.clarifai.results:
                self.table['Clarifai']['#Correct'] += 1
            else:
                self.table['Clarifai']['#Wrong'] += 1 """
                
        else:
            self.table['Clarifai']['#Wrong'] += 1
        # Google
        if answer[1] in self.google.results:
            self.table['Google']['#Correct'] += 1
            
            """ if answer[2] in self.google.results:
                self.table['Google']['#Correct'] += 1
            else:
                self.table['Google']['#Wrong'] += 1 """
                
        else:
            self.table['Google']['#Wrong'] += 1
        # IBM
        if answer[1] in self.ibm.results:
            self.table['IBM']['#Correct'] += 1
            
            """ if answer[2] in self.ibm.results:
                self.table['IBM']['#Correct'] += 1
            else:
                self.table['IBM']['#Wrong'] += 1 """
                
        else:
            self.table['IBM']['#Wrong'] += 1
             
    # Compare the result for No-results line            
    def noresult_comparison(self):
        # Amazon
        if ('animal' in self.aws.results) or ('caribou' in self.aws.results):
            self.table['Amazon']['#Wrong'] += 1
        else:
            self.table['Amazon']['#NoResult'] += 1
        # Clarifai     
        if ('animal' in self.clarifai.results) or ('caribou' in self.clarifai.results):
            self.table['Clarifai']['#Wrong'] += 1
        else:
            self.table['Clarifai']['#NoResult'] += 1
        # Google    
        if ('animal' in self.google.results)or ('caribou' in self.google.results):
            self.table['Google']['#Wrong'] += 1
        else:
            self.table['Google']['#NoResult'] += 1
        # IBM    
        if ('animal' in self.ibm.results)or ('caribou' in self.ibm.results):
            self.table['IBM']['#Wrong'] += 1
        else:
            self.table['IBM']['#NoResult'] += 1    
            
            
    # Invoke each class's recognition method           
    def recognition_invocation(self, image):
        # CLear previous results
        self.aws.results.clear()
        self.clarifai.results.clear()
        self.google.results.clear()
        self.ibm.results.clear() 
        
        self.aws.image_recognition(image)
        self.format_output(self.aws)
        self.clarifai.image_recognition(image)
        self.format_output(self.clarifai)
        self.google.image_recognition(image)
        self.format_output(self.google)
        self.ibm.image_recognition(image)
        self.format_output(self.ibm)
    
    # Uniforms all results to same format and separate words
    def format_output(self, API): 
        API.results = [ each.lower() for each in API.results]
        templist = list()
        for i in API.results:
            for j in i.split(' '):
                templist.append(j)
        API.results = templist
    
    # Update Precision, Recall, F1-Score
    def update_rate_and_F1(self, API_list): 
        for each in API_list:
            self.table[each]['Precision'] = self.get_precision_rate(each)
            self.table[each]['Recall'] = self.get_recall_rate(each)
            self.table[each]['F1-Score'] = self.get_F1score(each)
            
    # (C/(C+W))        
    def get_precision_rate(self, API):
        return (self.table[API]['#Correct'] / (self.table[API]['#Correct'] + self.table[API]['#Wrong'])) * 100
    
    # ((C+W)/total)
    def get_recall_rate(self, API):
        return ((self.table[API]['#Correct'] + self.table[API]['#Wrong'])/(self.table[API]['#Correct'] + self.table[API]['#Wrong'] + self.table[API]['#NoResult'])) * 100
    
    # 2 * ((precision * recall) / (precision + recall))
    def get_F1score(self, API):
        return 2.0 * ((self.table[API]['Precision'] * self.table[API]['Recall'])/(self.table[API]['Precision'] + self.table[API]['Recall']))
        
if __name__ == '__main__': #testing
    obj = Main()
    for each in obj.table:
        print(each, obj.table[each])