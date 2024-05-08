# Imports the Google Cloud client library
from google.cloud import language_v1

# Instantiates a client
client = language_v1.LanguageServiceClient()

# The text to analyze
def analise_texto_toxico(text):
    document = language_v1.types.Document(
        content=text, type_=language_v1.types.Document.Type.PLAIN_TEXT
    )

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment
    
    if sentiment.magnitude <= 0.50:
        print(f'{text}:{sentiment.magnitude}')
        return False
    elif sentiment.magnitude >=0.51:
        print(f'{text}:{sentiment.magnitude}')
        return True
    
a = analise_texto_toxico('caralho de gata filha da puta')
if a:
    print('toxx')
if not a:
    print('np')
