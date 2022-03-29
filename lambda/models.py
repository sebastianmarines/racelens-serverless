import os

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

IMAGES_DYNAMODB_TABLE_NAME = os.environ['IMAGES_DYNAMODB_TABLE_NAME']
EVENTS_DYNAMODB_TABLE_NAME = os.environ['EVENTS_DYNAMODB_TABLE_NAME']


class ImageModel(Model):
    class Meta:
        table_name = IMAGES_DYNAMODB_TABLE_NAME
    
    event_id = UnicodeAttribute(hash_key=True)
    image_id = UnicodeAttribute(range_key=True)

    s3_object = UnicodeAttribute()


class EventModel(Model):
    class Meta:
        table_name = EVENTS_DYNAMODB_TABLE_NAME

    # TODO: Use event_id as range key and event_date as hash key 
    event_id = UnicodeAttribute(hash_key=True)
    event_date = UTCDateTimeAttribute(range_key=True)
