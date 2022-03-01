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
                f"imageId#{result['FaceRecords'][0]['Face']['FaceId']}",
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
              