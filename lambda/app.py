import base64
import json
import os
import urllib.parse
from uuid import uuid4

import boto3

from models import ImageModel

COLLECTION_NAME = os.environ['COLLECTION_NAME']

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
cognito = boto3.client('cognito-idp')


def index_faces(event, _context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    s3_image_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    event_id, _ = s3_image_key.split('/', 1)

    try:
        result = rekognition.index_faces(
            CollectionId=COLLECTION_NAME,
            Image={
                "S3Object": {
                    "Bucket": bucket,
                    "Name": s3_image_key
                }
            },
        )
        if result['FaceRecords']:
            image_id = result['FaceRecords'][0]['Face']['ImageId']
            image = ImageModel(
                event_id=event_id,
                image_id=image_id,
                s3_object=s3_image_key
            )
            image.save()
            return {
                'statusCode': "OK",
            }

        return {
            'statusCode': "ERROR",
            'body': "No faces found"
        }
    except Exception as e:
        print(e)
        print(f"Error getting object {s3_image_key} from bucket {bucket}. Make sure they exist and your bucket is in the same region as this function.")
        raise e
              
def find_faces(event, _context):
    event_id = event['pathParameters']['event_name']

    try:
        rk_result = rekognition.search_faces_by_image(
            CollectionId=COLLECTION_NAME,
            Image={
                "Bytes": base64.b64decode(event['body'])
            }
        )
    except rekognition.exceptions.InvalidParameterException as e:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid image')
        }
    
    matches = [face['Face']['ImageId'] for face in rk_result['FaceMatches']]

    if not matches:
        return {
            'statusCode': 404,
            'body': json.dumps('No matches found')
        }
    
    images = [ImageModel.get(event_id, image_id).s3_object for image_id in matches]

    print(rk_result)
    return {
        'statusCode': 200,
        'body': json.dumps(images)
    }

def generate_upload_url(event, _context):
    SUPPORTED_EXTENSIONS = ["jpg", "jpeg", "png"]

    event_name = event['pathParameters']['event_name']
    access_token = event['headers'].get('Authorization', None)

    try:
        file_type = event['queryStringParameters']['file_type']
    except TypeError:
        return {
            'statusCode': 422,
            'body': json.dumps('Missing file_type query parameter')
        }


    if file_type not in SUPPORTED_EXTENSIONS:
        return {
            'statusCode': 415,
            'body': json.dumps('Invalid file type')
        }

    if not access_token:
        return {
            'statusCode': 401,
            'body': json.dumps('Missing access token')
        }

    try:
        user = cognito.get_user(AccessToken=access_token)
    except cognito.exceptions.NotAuthorizedException as e:
        return {
            'statusCode': 401,
            'body': json.dumps('Not authorized')
        }
    
    presigned_url = s3.generate_presigned_post(
        Bucket=os.environ['BUCKET_NAME'],
        Key=f"{event_name}/{uuid4()}.{file_type}",
        ExpiresIn=3600
    )
    

    return {
        'statusCode': 200,
        'body': json.dumps(presigned_url)
    }
