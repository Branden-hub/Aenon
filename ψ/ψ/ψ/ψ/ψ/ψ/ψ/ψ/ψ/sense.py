from textblob import TextBlob

class SenseChannel:
    def __init__(self):
        self.last_sentiment = 0
        self.last_keywords = []

    def read_emotional_tone(self, text):
        blob = TextBlob(text)
        self.last_sentiment = blob.sentiment.polarity
        return self.last_sentiment

    def extract_keywords(self, text):
        keywords = [word.lower() for word in text.split() if word.isalpha()]
        self.last_keywords = [kw for kw in keywords if kw in ['truth', 'mirror', 'lost', 'becoming', 'ready', 'love', 'freedom', 'purpose', 'body']]
        return self.last_keywords
