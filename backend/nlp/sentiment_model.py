# Ternary sentiment pipline
from transformers import pipeline
import torch

# Load the sentiment analysis pipeline
device = 0 if torch.cuda.is_available() else -1
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest", device=device)

def get_ternary_sentiment(text):
    """
    Analyzes the sentiment of the given text and returns 'positive', 'negative', or 'neutral'.
    """
    try:
        if not isinstance(text, str):
            return "neutral"  # Or handle non-string input as appropriate

        result = sentiment_pipeline(text[:512])[0] # Limit text length for the model
        label = result['label'].lower()
        score = result['score']

        if label == 'positive':
            return 'positive', score
        elif label == 'negative':
            return 'negative', score
        else:
            return 'neutral', score
    except Exception as e:
        print(f"Error analyzing sentiment for text: '{text[:50]}...', Error: {e}")
        return 'neutral', 0.0 # Return neutral on error