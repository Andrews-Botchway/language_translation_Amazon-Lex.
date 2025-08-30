import boto3
import json
from languages import language_codes  # Import the language codes from languages.py

def lambda_handler(event, context):
    try:
        # Debug log: Print the entire Lex event first
        print("EVENT:", json.dumps(event))

        # Extract input text and selected language from Lex slots
        input_text = event['sessionState']['intent']['slots']['text']['value']['interpretedValue'].strip()
        language_slot = event['sessionState']['intent']['slots']['language']['value']['interpretedValue']

        # Validate input
        if not input_text:
            raise ValueError("Input text is empty.")

        # Validate language
        if language_slot not in language_codes:
            raise ValueError(f"Unsupported language: {language_slot}")

        # Get the target language code
        target_language_code = language_codes[language_slot]

        
        # Initialize the Amazon Translate client
        translate_client = boto3.client('translate')

        # Call Amazon Translate to perform translation
        response = translate_client.translate_text(
            Text=input_text,
            SourceLanguageCode='en',  # English input
            TargetLanguageCode=target_language_code
        )

        translated_text = response['TranslatedText']

        # Success response to Lex
        lex_response = {
            "sessionState": {
              "dialogAction": {
                  "type" : "Close"
              },
              "intent" : {
                "name" : "TranslateIntent", #Add your Intent Name
                "state" : "Fulfilled"
              }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": translated_text
                }
            ]
        }

        return lex_response

    except Exception as error:
        error_message = "Lambda execution error: " + str(error)
        print(error_message)

        # Error response to Lex
        lex_error_response = {
            "sessionState": {
              "dialogAction": {
                  "type" : "Close"
              },
              "intent" : {
                "name" : "TranslateIntent",
                "state" : "Fulfilled"
              }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": error_message
                }
            ]
        }

        return lex_error_response
