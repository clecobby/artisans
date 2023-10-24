import boto3
from decouple import config

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
REGION_NAME = config('REGION_NAME')

client=boto3.client('dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
    )
resource=boto3.resource('dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
    )

def CreatATableBook():
        
    client.create_table(
        AttributeDefinitions = [ # Name and type of the attributes 
            {
                'AttributeName': 'id', # Name of the attribute
                'AttributeType': 'N'   # N -> Number (S -> String, B-> Binary)
            }
        ],
        TableName = 'Book', # Name of the table 
        KeySchema = [       # Partition key/sort key attribute 
            {
                'AttributeName': 'id',
                'KeyType'      : 'HASH' 
                # 'HASH' -> partition key, 'RANGE' -> sort key
            }
        ],
        BillingMode = 'PAY_PER_REQUEST',
        Tags = [ # OPTIONAL 
            {
                'Key' : 'test-resource',
                'Value': 'dynamodb-test'
            }
        ]
    )
BookTable = resource.Table('Book')

def addItemToBook(id, title, author):
    response = BookTable.put_item(
        Item = {
            'id'     : id,
            'title'  : title,
            'author' : author,
            'likes'  : 0
        }
    )
    return response

def GetItemFromBook(id):
    response = BookTable.get_item(
        Key = {
            'id'     : id
        },
        AttributesToGet=[
            'title', 'author'
        ]
    )
    return response

def UpdateItemInBook(id,dict):
    response = BookTable.update_item(
        Key = {
            'id': id
        },
        AttributeUpdates={
            'title': {
                'Value'  : data['title'],
                'Action' : 'PUT' # available options -> DELETE(delete), PUT(set), ADD(increment)
            },
            'author': {
                'Value'  : data['author'],
                'Action' : 'PUT'
            }
        },
        ReturnValues = "UPDATED_NEW" # returns the new updated values
    )
    return response

def LikeABook(id):
    response = BookTable.update_item(
        Key = {
            'id': id
        },
        AttributeUpdates = {
            'likes': {
                'Value'  : 1,   # Add '1' to the existing value
                'Action' : 'ADD'
            }
        },
        ReturnValues = "UPDATED_NEW"
    )
    # The 'likes' value will be of type Decimal, which should be  converted to python int type, to pass the response in json format.
    response['Attributes']['likes'] = int(response['Attributes']['likes'])
    return response


def DeleteAnItemFromBook(id):
    response = BookTable.delete_item(
        Key = {
            'id': id
        }
    )
    return response

