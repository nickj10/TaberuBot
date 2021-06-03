# Imports the Google Cloud client library
from google.cloud import language_v1

# Instantiates a client
client = language_v1.LanguageServiceClient()

class GoogleLPHandler:

    def __init__(self):
        self

    def analyzeText(self,update, context):
        # The text to analyze
        document = language_v1.Document(content=update.message.text, type_=language_v1.Document.Type.PLAIN_TEXT)

        # Detects the sentiment of the text
        # sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        entities = client.analyze_entities(request={'document': document}).entities
        print("Text: {}".format(update.message.text))
        # print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))
        print("Entities: {}".format(entities))
