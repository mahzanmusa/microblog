import requests
from flask import current_app
from flask_babel import _
import boto3
import json

'''
def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in current_app.config or not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    auth = {
        'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY'],
        'Ocp-Apim-Subscription-Region': current_app.config['MS_TRANSLATOR_REGION']
    }
    r = requests.post(
        'https://api.cognitive.microsofttranslator.com'
        '/translate?api-version=3.0&from={}&to={}'.format(
            source_language, dest_language), headers=auth, json=[
                {'Text': text}])
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    
    print(r.json()[0]['translations'][0]['text'])
    return r.json()[0]['translations'][0]['text']
'''

def translate(text, source_language, dest_language):
    # Configure the AWS region (change to your desired region, e.g., 'us-east-1')
    region = current_app.config['AWS_DEFAULT_REGION'] 
    service_name = 'translate'

    # Initialize the Translate client. Boto3 handles the SigV4 signing automatically
    try:
        translate = boto3.client(service_name, region_name=region)
    except Exception as e:
        print(f"Error creating boto3 client: {e}")
        print("Please ensure your AWS credentials are configured correctly.")
        exit()

    # Text to translate
    text_to_translate = text

    # Source and target languages
    # 'auto' lets Amazon Translate automatically detect the source language
    # 'es' is the code for Spanish
    source_lang = source_language 
    target_lang = dest_language 

    try:
        # Call the translate_text API operation
        response = translate.translate_text(
            Text=text_to_translate,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang
        )
        
        # Print the translated text and detected source language
        return response['TranslatedText']

    except Exception as e:
        print(f"An error occurred during translation: {e}")
