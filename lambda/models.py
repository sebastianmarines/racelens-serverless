import os

from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model

DYNAMODB_TABLE_NAME = os.environ['DYNAMODB_TABLE_NAME']


class Event(Model):
    class Meta:
        table_name = DYNAMODB_TABLE_NAME
    
    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
