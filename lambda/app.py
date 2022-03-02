import base64
import json
import os
import urllib.parse

import boto3

from models import Event

COLLECTION_NAME = os.environ['COLLECTION_NAME']

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')


def index_faces(event, _context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        result = rekognition.index_faces(
            CollectionId=COLLECTION_NAME,
            Image={
                "S3Object": {
                    "Bucket": bucket,
                    "Name": key
                }
            },
        )
        if result['FaceRecords']:
            image = Event(
                f"imageId#{result['FaceRecords'][0]['Face']['ImageId']}",
                key
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
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
              
def find_faces(event, _context):
    # TODO: #2 Query all images at the same time

    event_name = event['pathParameters']['event_name']

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
    
    images = [image.sk for image_id in matches for image in Event.query(f"imageId#{image_id}", Event.sk.startswith(f"{event_name}/"))]

    print(rk_result)
    return {
        'statusCode': 200,
        'body': json.dumps(images)
    }
