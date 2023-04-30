import json
import spacy
from spacy.matcher import Matcher
from tqdm import tqdm
import argparse


def update_matcher(file, type, matcher):
    data = file
    for item in data:
        single_pattern = list()
        for i, word in enumerate(item.split(' ')):
            if i == 0:
                single_pattern.append({'LOWER': word.lower(), 'OP': '+'})
            else:
                single_pattern.append({'LOWER': word.lower(), 'OP': '*'})
        else:
            matcher.add(type, [single_pattern])


def run():
    parser = argparse.ArgumentParser()

    parser.add_argument("--ner_category_input", default="data\\all_ingredients.json")
    parser.add_argument("--all_data_input", default=f'data\\all_data.json')
    parser.add_argument("--output_directory", default=f'data')
    parser.add_argument("--ner_category_name", default='INGREDIENTS')
    parser.add_argument("--spacy_model_name", default='it_core_news_lg')

    args = parser.parse_args()

    all_data_input = args.all_data_input
    input_ner_category = args.ner_category_input
    output_directory = args.output_directory
    ner_category_name = args.ner_category_name
    spacy_model_name = args.spacy_model_name

    f = open(input_ner_category)
    ingredients = json.load(f)['recipe']
    nlp = spacy.load(spacy_model_name)
    matcher = Matcher(nlp.vocab)
    update_matcher(ingredients, ner_category_name, matcher)

    f = open(all_data_input)
    all_data = json.load(f)
    training_data = list()
    for recipe in tqdm(all_data):
        for step in recipe['steps'].values():
            all_matches = list()
            doc = nlp(step)
            matches = matcher(doc)
            for match_id, start, end in matches:
                span = doc[start:end]
                all_matches.append((span.start_char, span.end_char, nlp.vocab.strings[match_id]))

            training_data.append({
                'entities': all_matches,
                'text': step
            })

    training_size = int(len(training_data) * 0.8)
    print(f"Size total data: {len(training_data)}")
    print(f"Size training data: {training_size}")
    print(f"Size test data: {len(training_data) - training_size}")

    with open(f'{output_directory}/training_data.json', 'w') as f:
        json.dump(training_data[:training_size], f)

    with open(f'{output_directory}/test_data.json', 'w') as f:
        json.dump(training_data[training_size:], f)
