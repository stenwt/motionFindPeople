from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib
import urllib2
import os

print('Loading function')

rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')

# --------------- Helper Functions to call Rekognition APIs ------------------


#def detect_faces(bucket, key):
#    response = rekognition.detect_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}})
#    return response


def detect_labels(bucket, key):
    response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})

    # Sample code to write response to DynamoDB table 'MyTable' with 'PK' as Primary Key.
    # Note: role used for executing this Lambda function should have write access to the table.
    #table = boto3.resource('dynamodb').Table('MyTable')
    #labels = [{'Confidence': Decimal(str(label_prediction['Confidence'])), 'Name': label_prediction['Name']} for label_prediction in response['Labels']]
    #table.put_item(Item={'PK': key, 'Labels': labels})
    return response


#def index_faces(bucket, key):
    # Note: Collection has to be created upfront. Use CreateCollection API to create a collecion.
    #rekognition.create_collection(CollectionId='BLUEPRINT_COLLECTION')
#    response = rekognition.index_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}}, CollectionId="BLUEPRINT_COLLECTION")
#    return response

def is_person(response):
    person = False
    if 'Labels' in response:
        for l, label in enumerate(response['Labels']):
            if label['Name'] in "People Person Human":
                person = True
    return person

def get_temp_link(bucket, key):
    link = s3.generate_presigned_url('get_object', 
        Params={'Bucket': bucket, 'Key': key})
    return link 

def send_telegram(bucket, key, response):
    link = get_temp_link(bucket, key)
    token = os.getenv('TELEGRAM_API_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    text = "[.]({})".format(urllib.quote_plus(link)) 
    if os.getenv('DEBUG'):
        text += str(response)
    url = "https://api.telegram.org/bot" + token + \
        "/sendMessage?chat_id=" + chat_id + \
        "&parse_mode=markdown" + \
        "&text=" + text

    request = urllib2.Request(url)
    return urllib2.urlopen(request)


# --------------- Main handler ------------------


def lambda_handler(event, context):
    '''Demonstrates S3 trigger that uses
    Rekognition APIs to detect faces, labels and index faces in S3 Object.
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        # Calls rekognition DetectFaces API to detect faces in S3 object
        #response = detect_faces(bucket, key)

        # Calls rekognition DetectLabels API to detect labels in S3 object
        response = detect_labels(bucket, key)

        # Calls rekognition IndexFaces API to detect faces in S3 object and index faces into specified collection
        #response = index_faces(bucket, key)

        # Print response to console.
        print(response)
        
        if is_person(response):
            send_telegram(bucket, key, response)
        
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e
