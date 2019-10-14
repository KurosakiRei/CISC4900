import boto3

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content('hashiqi.jpg')

client = boto3.client('rekognition')
response = client.detect_labels(
    Image={
        'Bytes': image,
        }
    
)
results = response['Labels']
for each in results:
    print(each['Name'])