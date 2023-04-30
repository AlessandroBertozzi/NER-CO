from tqdm import tqdm
import json
import srsly


f = open('..\\data\\training_data.json')
training_data = json.load(f)
all_text = list()
for training_example in tqdm(training_data):
    text = training_example['text']
    all_text.append({'text': text})

srsly.write_jsonl("../data/text.jsonl", all_text)
