from spacy.util import filter_spans
import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import json
import argparse


def create_doc(training_data, language_spacy_model):
    nlp = spacy.blank(language_spacy_model)  # load a new spacy model
    doc_bin = DocBin()  # create a DocBin object

    for training_example in tqdm(training_data):
        text = training_example['text']
        labels = training_example['entities']
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in labels:
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                print("Skipping entity")
            else:
                ents.append(span)
        filtered_ents = filter_spans(ents)
        doc.ents = filtered_ents
        doc_bin.add(doc)

    return doc_bin


def run():
    parser = argparse.ArgumentParser()

    parser.add_argument("--language_spacy_model", default='it')
    parser.add_argument("--input_training_data", default='data\\training_data.json')
    parser.add_argument("--input_test_data", default='data\\test_data.json')
    parser.add_argument("--output_doc_bin", default='data')

    args = parser.parse_args()

    language_spacy_model = args.language_spacy_model
    input_training_data = args.input_training_data
    input_test_data = args.input_test_data
    output_doc_bin = args.output_doc_bin

    f = open(input_training_data)
    training_data = json.load(f)

    f = open(input_test_data)
    test_data = json.load(f)

    doc_training = create_doc(training_data, language_spacy_model)
    doc_test = create_doc(test_data, language_spacy_model)

    doc_training.to_disk(f"{output_doc_bin}\\training_data.spacy")  # save the docbin object
    doc_test.to_disk(f"{output_doc_bin}\\test_data.spacy")  # save the docbin object
