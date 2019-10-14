import vendors.AWS as AWS
import vendors.Clarifai as Clarifai
import vendors.Google as Google
import vendors.IBM as IBM

if __name__ == '__main__':
    aws = AWS.Rekonition()
    clarifai = Clarifai.Predict()
    google = Google.VisionAI()
    ibm = IBM.WatsonVisualRecognition()