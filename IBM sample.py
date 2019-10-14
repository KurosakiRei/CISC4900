import json
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('si21GLXqCMSdhw15pibaI9Dl98v-n_IrO1-_NNfSk95B')
visual_recognition = VisualRecognitionV3(
    version='2019-09-11',
    authenticator=authenticator
)

with open('hashiqi.jpg', 'rb') as images_file:
    classes = visual_recognition.classify(
        images_file=images_file,
        threshold='0.6').get_result()
    print(json.dumps(classes, indent=2))