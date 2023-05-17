import math
import re
from collections import Counter
import pandas as pd

data = pd.read_csv('./data/catalog.csv', encoding='utf-8', sep=';')
df = data['product_name']
df.fillna('', inplace=True)

WORD = re.compile(r"\w+")


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)

def get_link(string):
    list_cos = []
    text1 = string
    vector1 = text_to_vector(text1)
    for i in range(df.shape[0]):
        text2 = df.iloc[i]
        vector2 = text_to_vector(text2)
        list_cos.append(get_cosine(vector1, vector2))
    result = list_cos.index(max(list_cos))
    # print("Cosine:", result)
    # print(df.iloc[result])
    return [data.iloc[result]['product_name'], data.iloc[result]['Link']]
    # return  data.iloc[result]['Link']


def parse_output(text):
    # Ищем все сочетания, начинающиеся с числа и точки
    pattern = re.compile(r"\d+\.")
    # Разбиваем исходную строку на элементы, используя найденные числа и точки в качестве разделителей
    elements = pattern.split(text)
    # Выводим найденные элементы на экран
    return [elem.strip() for elem in elements[1:]]
    
# Приходит строка, её обрабатывает parse_output, потом для каждого элемента формируется
def output_for_user(msg):
    result = ''
    dishes = parse_output(msg)
    for dish in dishes:
        temp = get_link(dish)
        # result += dish + ' - '
        # result += get_link(dish) + '\n'
        result += f'{temp[0]} - {temp[1]}\n'
    return result

