from google.cloud import language_v1
import os

class Gnsentiment():
    def __init__(self, path=''):
        self._var = 'GOOGLE_APPLICATION_CREDENTIALS'
        self._path_api = path
        self._error = False

        try:
            self._error = self._createVar()
        except:
            self._error = True

    def _createVar(self):
        if self._path_api == '' or self._path_api[-5:] != '.json':
            return True
        
        os.environ[self._var] = self._path_api

        try:
            if os.environ[self._var]:
                return False 
        except:
            return True
        
    def analyze_sentiment(self, text):
        if self._error:
            return {
                'error': True
            }

        try:
            client = language_v1.LanguageServiceClient()
            type_ = language_v1.Document.Type.PLAIN_TEXT

            language = 'es'
            document = {'content': text, 'type_': type_, 'language': language}
            encoding_type = language_v1.EncodingType.UTF8
        
            response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})

            score = response.document_sentiment.score
            magnitude = response.document_sentiment.magnitude
            sentences = response.sentences

            return {
                'error': False,
                'score': round(score, 3),
                'magnitude': round(magnitude, 3),
                'sentences': sentences
            }
        except:
            return {
                'error': True
            }
        
    def sentiment(self, score):
        if score >= -1.0 and score < -0.25:
            return 0
        elif score >= -0.25 and score <= 0.25:
            return 2
        elif score > 0.25 and score <= 1.0:
            return 1
        else:
            return 3
