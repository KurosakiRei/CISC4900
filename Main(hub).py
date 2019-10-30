import vendors.AWS as AWS
import vendors.Clarifai as Clarifai
import vendors.Google as Google
import vendors.IBM as IBM
import os

class Main:
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
        self.ImagesPath = r'C:\Users\KurosakiRei\Dropbox\HITS'
        self.AnswerKeyPath = r'D:\github-repos\CISC4900\Answer.txt'
        self.AnswerFile = open(AnswerKeyPath, 'r')
        
        #----------------------------------------------------------
        self.create_table()
        
    def create_table(self):
        for each in self.API_list:
            self.table.setdefault(each, {})
            self.table[each].setdefault('#Correct', 0)
            self.table[each].setdefault('#Wrong', 0)
            self.table[each].setdefault('#NoResult', 0)
            self.table[each].setdefault('Precision', 0)
            self.table[each].setdefault('Recall', 0)
            self.table[each].setdefault('F1-Score', 0)
        for each in self.table:
            print(each, self.table[each])
    
if __name__ == '__main__': #testing
    obj = Main()