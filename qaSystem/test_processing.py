import re

from nltk.tokenize import word_tokenize
from pymorphy3 import MorphAnalyzer

from qaSystem.request import Request
from qaSystem.tag_dictionary import TagDictionary


def creates_request(text: str) -> Request:
    morph = MorphAnalyzer()
    request = Request()
    request.tags = TagDictionary()
    flags = re.IGNORECASE
    is_request_about_moto = False

    linguistic_variable_pattern = r"(не очень большой|очень не большой|маленький|средний|большой)"
    match = re.findall(linguistic_variable_pattern, text, flags)
    if len(match) > 0:
        text = re.sub(linguistic_variable_pattern, '', text, flags)
        match match[0]:
            case "маленький":
                request.max_weight = 100
            case "не очень большой":
                request.min_weight = 100
                request.max_weight = 150
            case "средний":
                request.min_weight = 150
                request.max_weight = 215
            case "очень не большой":
                request.min_weight = 215
                request.max_weight = 320
            case _:
                request.min_weight = 320

    words_tokenized = word_tokenize(text)
    # print(morph.parse('синий')[0])
    for word in words_tokenized:
        match morph.parse(word)[0].normal_form:
            case "показать" | "какой" | "дать" | "вывести":
                request.show = True
            case "мотоцикл":
                request.show = True
                is_request_about_moto = True
                if "plur" in morph.parse(word)[0].tag:
                    request.num_ = "Many"
            case _:
                match str(morph.parse(word)[0].tag).split(",")[0]:
                    case "PREP":
                        match word.lower():
                            case "с":
                                request.exist = True
                            case "без":
                                request.exist = False
                            case "до":
                                request.extr = "Max"
                            case "от":
                                request.extr = "Min"
                    case "CONJ":
                        match word.lower():
                            case "и":
                                request.and_log = True
                            case "или":
                                request.or_log = True
                    case "PRED":
                        match word.lower():
                            case "нет":
                                request.exist = False
                    case "ADJF":
                        match morph.parse(word)[0].normal_form:
                            case "дорожный":
                                request.type = "road"
                            case "внедорожный":
                                request.type = "off-road"
                            case "двоичной":
                                request.type = "dual-sport"
                            case "красный":
                                request.color = "Red"
                            case "чёрный":
                                request.color = "Black"
                            case "белый":
                                request.color = "White"
                            case "синий":
                                request.color = "Bleu"
                            case "зелёный":
                                request.color = "Green"
                            case "жёлтый":
                                request.color = "Yellow"
                            case "серый":
                                request.color = "Grey"
                            case "темно-синый":
                                request.color = "Dark-bleu"
                            case "минимальный":
                                request.extr = "Min"
                            case "максимальный":
                                request.extr = "Max"
                    case "NOUN":
                        index = text.find(word)
                        target_texts = text[index:].split()
                        match morph.parse(word)[0].normal_form:
                            case "трансмиссия" | "вариатор":
                                founded_str = False
                                for target_text in target_texts:
                                    if morph.parse(target_text)[0].normal_form == 'вариатор':
                                        request.tags.add('transmission', 'Variator')
                                        founded_str = True
                                        break
                                    elif morph.parse(target_text)[0].normal_form == 'автоматический':
                                        request.tags.add('transmission', 'Automatic')
                                        founded_str = True
                                        break
                                if not founded_str:
                                    target_texts = text[:index].split()
                                    for target_text in target_texts:
                                        if morph.parse(target_text)[0].normal_form == 'вариатор':
                                            request.tags.add('transmission', 'Variator')
                                            break
                                        elif morph.parse(target_text)[0].normal_form == 'автоматический':
                                            request.tags.add('transmission', 'Automatic')
                                            break
                            case "высота":
                                founded_number = False
                                for target_text in target_texts:
                                    if target_text.isnumeric():
                                        founded_number = True
                                        request.tags.add('height', float(target_text))
                                        break
                                if not founded_number:
                                    target_texts = text[:index].split()
                                    for target_text in target_texts:
                                        if target_text.isnumeric():
                                            request.tags.add('height', float(target_text))
                                            break
                            case "объём":
                                founded_number = False
                                for target_text in target_texts:
                                    if target_text.isnumeric():
                                        founded_number = True
                                        request.tags.add('engine_capacity', float(target_text))
                                        break
                                if not founded_number:
                                    target_texts = text[:index].split()
                                    for target_text in target_texts:
                                        if target_text.isnumeric():
                                            request.tags.add('engine_capacity', float(target_text))
                                            break
                            case "поворотник":
                                request.tags.add('exist_turn_signal', request.exist)

    # print(request.to_str())
    if not is_request_about_moto:
        print("Я не знаю, как ответить на Ваш вопрос т.к. я разбираюсь только по теме мотоцикл")
        request.show = False

    return request
