# Завдання 2

# Напишіть Python-скрипт, який завантажує текст із заданої URL-адреси, аналізує частоту 
# використання слів у тексті за допомогою парадигми MapReduce і візуалізує топ-слова 
# з найвищою частотою використання у тексті.

# Покрокова інструкція

# Імпортуйте необхідні модулі (matplotlib та інші).
# Візьміть код реалізації MapReduce з конспекту.
# Створіть функцію visualize_top_words для візуалізації результатів.
# У головному блоці коду отримайте текст за URL, застосуйте MapReduce та візуалізуйте результати.

import string
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from collections import Counter
from multiprocessing import Pool

import requests

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        return None

# Функція для видалення знаків пунктуації
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    return word, 1

def reduce_function(word_counts):
    counter = Counter()
    for word, count in word_counts:
        counter[word] += count
    return counter

# Виконання MapReduce
def map_reduce(text):
    words = text.split()
    with Pool() as pool:
        word_counts = pool.map(map_function, words)
    return reduce_function(word_counts)

def visualize_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)
    plt.barh(words, counts)
    plt.ylabel('Words')
    plt.xlabel('Frequency')
    plt.title('Top Words by Frequency')
    plt.gca().invert_yaxis()
    plt.show()

if __name__ == '__main__':
    # Вхідний текст для обробки
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    if text:
        # Виконання MapReduce на вхідному тексті
        search_words = ['war', 'peace', 'love'] # specify words to search
        word_counts = map_reduce(text) # add second argument search_words for specific words
        visualize_top_words(word_counts)
        print("Результат підрахунку слів:", word_counts)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")
