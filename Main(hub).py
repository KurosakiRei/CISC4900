import vendors.AWS as AWS
import vendors.Clarifal as Clarifal
import vendors.Google as Google
import vendors.IBM as IBM

if __name__ == '__main__':
    aws = AWS.AWS()
    print(aws.image_recognition('hashiqi.jpg'))