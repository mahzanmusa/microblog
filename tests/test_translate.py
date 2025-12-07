import boto3
import json

# Configure the AWS region (change to your desired region, e.g., 'us-east-1')
region = 'us-east-1' 
service_name = 'translate'

# Initialize the Translate client. Boto3 handles the SigV4 signing automatically
try:
    translate = boto3.client(service_name, region_name=region)
except Exception as e:
    print(f"Error creating boto3 client: {e}")
    print("Please ensure your AWS credentials are configured correctly.")
    exit()

# Text to translate
text_to_translate = "Hello, world! How are you today?"

# Source and target languages
# 'auto' lets Amazon Translate automatically detect the source language
# 'es' is the code for Spanish
source_lang = 'auto' 
target_lang = 'es' 

print(f"Translating: '{text_to_translate}'")

try:
    # Call the translate_text API operation
    response = translate.translate_text(
        Text=text_to_translate,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang
    )
    
    # Print the translated text and detected source language
    print(f"Source language detected: {response['SourceLanguageCode']}")
    print(f"Translated text: {response['TranslatedText']}")
    #print(type(response))
    print(json.dumps(response['TranslatedText']))

except Exception as e:
    print(f"An error occurred during translation: {e}")

