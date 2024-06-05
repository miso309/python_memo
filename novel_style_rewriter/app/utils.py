# utils.py
import nltk
from nltk.tokenize import word_tokenize

def preprocess_text(text):
    """
    テキストの前処理を行う関数。小文字化、トークン化を行う。
    """
    text = text.lower()
    tokens = word_tokenize(text)
    return tokens

# データの前処理のテスト
sample_text = "This is an example sentence. Let's see how it's tokenized!"
print(preprocess_text(sample_text))
