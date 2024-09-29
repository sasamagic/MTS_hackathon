import requests  # Импортируем библиотеку для работы с HTTP-запросами
import json  # Импортируем библиотеку для работы с JSON-данными

def get_synonyms_yandex(word, api_key):  # Определяем функцию для получения синонимов
    url = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup"  # URL для API Яндекс. Словаря
    params = {  # Параметры для запроса к API
        "key": api_key,  # Ключ API для аутентификации
        "lang": "ru-ru",  # Язык (русский)
        "text": word  # Слово, для которого ищем синонимы
    }
    response = requests.get(url, params=params)  # Выполняем GET-запрос к API
    if response.status_code == 200:  # Проверяем, успешен ли запрос (статус 200)
        data = response.json()  # Парсим JSON-ответ
        synonyms = []  # Список для хранения найденных синонимов
        for item in data.get('def', []):  # Проходим по определениям слова
            for translation in item.get('tr', []):  # Проходим по переводам
                for synonym in translation.get('syn', []):  # Проходим по синонимам
                    synonyms.append(synonym['text'])  # Добавляем текст синонима в список
        return synonyms  # Возвращаем список синонимов
    return []  # Если запрос не успешен, возвращаем пустой список

# Пример использования
api_key = "dict.1.1.20240927T213247Z.358755a9a879a509.7af5a0e71fcc38f9e828dae96ba34915865f959b"  # Вставьте ваш ключ API

while True:  # Начинаем бесконечный цикл для ввода слов
    words_input = input("Введите слова-ключи через пробел (или нажмите Enter для завершения): ")  # Запрашиваем ввод слов
    if not words_input:  # Проверка на пустую строку (если пользователь нажал Enter)
        print("Завершение работы.")  # Сообщение о завершении работы
        break  # Выходим из цикла

    words = words_input.split()  # Разделяем строку на отдельные слова по пробелам
    synonyms_dict = {}  # Словарь для хранения синонимов

    for word in words:  # Проходим по каждому слову
        synonyms = get_synonyms_yandex(word, api_key)  # Получаем синонимы для слова

        # Сохранение синонимов в словарь
        if synonyms:  # Если синонимы найдены
            synonyms_dict[word] = synonyms  # Добавляем их в словарь
        else:
            synonyms_dict[word] = []  # Если синонимы не найдены, добавляем пустой список

    # Вывод в заданном формате
    print("\nsynonyms = {")  # Начинаем вывод словаря синонимов
    for key, value in synonyms_dict.items():  # Проходим по всем парам "слово:синонимы"
        print(f'    "{key}": {value},')  # Форматируем и выводим каждую пару
    print("}")  # Заканчиваем вывод словаря

    # Сохранение в формате JSON
    with open('synonyms.json', 'w', encoding='utf-8') as json_file:  # Открываем файл для записи
        json.dump(synonyms_dict, json_file, ensure_ascii=False, indent=4)  # Записываем словарь в JSON-формате

    print("\nsynonyms сохранены в 'synonyms.json'.")  # Сообщение об успешном сохранении
