import json
import subprocess
import os
import boto3


def lambda_handler(event, context):
    filename = event['filename']

    s3 = boto3.resource('s3')
    s3.Bucket('masteraula-documents').download_file('html/{}.html'.format(filename), '/tmp/{}.html'.format(filename))
    
    subprocess.getoutput('/opt/pandoc -o /tmp/{}.docx /tmp/{}.html'.format(filename, filename))
    
    s3.Bucket('masteraula-documents').upload_file('/tmp/{}.docx'.format(filename), 'docx/{}.docx'.format(filename))
    stdoutdata = subprocess.getoutput('/opt/pandoc -v')
    
    return {
        'statusCode': 200,
        'body': filename
    }

