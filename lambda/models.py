import os

from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model

DYNAMODB_TABLE_NAME = os.environ['DYNAMODB_TABLE_NAME']


class ImageModel(Model):
    class Meta:
        table_name = DYNAMODB_TABLE_NAME
    
    event_id = UnicodeAttribute(hash_key=True)
    image_id = UnicodeAttribute(range_key=True)

    s3_object = UnicodeAttribute()
