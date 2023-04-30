from bs4 import BeautifulSoup
import requests
import json
import argparse
import os


def normalize_text(text: str):
    normalize_list_token = list()
    for token in text.split(' '):
        if token != '':
            normalize_list_token.append(token)

    return " ".join(normalize_list_token)


def run():
    parser = argparse.ArgumentParser()

    parser.add_argument("--output", default="./data")

    args = parser.parse_args()

    output = args.output

    list_terms = dict()
    categories = [
        'altri-ingredienti',
        'antipasti',
        '157-2',
        'burri-e-salse',
        'carni',
        'dolci',
        'erbe-spezie-aromi',
        'formaggi',
        'frutta',
        'pesci',
        'primi-piatti',
        'salumi',
        'uova',
        'verdure'
    ]
    for category in categories:
        try:
            list_term_one_category = list()
            response = requests.get(f'https://online.scuola.zanichelli.it/enogastronomiacucina/{category}/')

            soup = BeautifulSoup(response.content, 'lxml')

            table = soup.find_all("table", {"class": "MsoNormalTable"})[1]
            for i, subtag in enumerate(table.tbody):
                if subtag == '\n' or i in [1, 2, 3]:
                    continue
                list_term_one_category.append(normalize_text(subtag.find_all('td')[0].text.strip().lower()))
            list_terms[category] = list_term_one_category
            if category == '157-2':
                list_terms['bevande'] = list_term_one_category
        except IndexError:
            pass

    output = os.path.join(output, 'list_terms.json')
    with open(output, 'w') as handle:
        json.dump(list_terms, handle)
