import logging
import json
import boto3
import base64
import io
from botocore.client import Config
from customEncoder import CustomEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3 = boto3.client('s3')


getMethod = "GET"
healthPath = "/rekognition/health"
rekognition = boto3.client('rekognition')



#main handler
def lambda_handler(event, context):

    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    image_base64 = event['imageBase64']

    if httpMethod == getMethod and path == healthPath:

        #decode
        image_data = base64.b64decode(image_base64)

        #convert
        image = Image.open(io.BytesIO(image_data))

        #run rekognition detect_faces API
        response = rekognition.detect_labels(Image={'Bytes': image_data})
    
        labels = get_labels(response)
        result = {'labels': labels}

        labels_json = json.dumps()
        
        return buildResponse(200, labels)
    
    else:
        return buildResponse(404, 'Not Found')
    

# Response builder.
def buildResponse(statusCode, body = None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls = CustomEncoder)
    return response