from nltk import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords


def test():
    text = "Я хочу купить большой красивый дом"

    words = word_tokenize(text)

    print(pos_tag(words))
    """
    text = "Text to tokenize. And an other"
    text_2 = word_tokenize("Sir, I protest. I am not a marry man!")
    english_stop_words = set(stopwords.words("english"))
    filtered_list = []
    for word in text_2:
        if word.casefold() not in english_stop_words:
            filtered_list.append(word)
    print(filtered_list)
    """
