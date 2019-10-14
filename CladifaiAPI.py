from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

app = ClarifaiApp(api_key='4e651845c45345a783e8d3a42e167174')
model = app.public_models.general_model
model.model_version = 'aa7f35c01e0642fda5cf400f543e7c40'
response = model.predict_by_filename(filename='husky.jpg')

concepts = response['outputs'][0]['data']['concepts']
for concept in concepts:
    print(concept['name'], concept['value'])