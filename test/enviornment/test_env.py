import sys
print(sys.executable)

from transformers import pipeline
sentiment = pipeline("sentiment-analysis")
print(sentiment("Testing in VS Code!"))
print(sentiment("I love you!"))
print(sentiment("I hate you!"))
print(sentiment("I am happy!"))
print(sentiment("I am sad!"))
print(sentiment("I am angry!"))
print(sentiment("I am excited!"))
print(sentiment("I am bored!"))
print(sentiment("I am scared!"))
print(sentiment("I am tired!"))
print(sentiment("I am hungry!"))
print(sentiment("I am thirsty!"))
print(sentiment("I am sleepy!"))
print(sentiment("I am lonely!"))
