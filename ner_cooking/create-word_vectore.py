import spacy
import json
from tqdm import tqdm
from gensim.models.word2vec import Word2Vec

nlp = spacy.load('it_core_news_lg')

f = open('../data/all_data.json')
data = json.load(f)

all_token_list = list()
for recipe in tqdm(data[:50]):
    for step in recipe['steps'].values():
        doc = nlp(step)
        token_list = [token.text for token in doc if not token.is_stop and not token.is_punct and not token.text == ' ']
        all_token_list.append(token_list)

num_features = 300
min_word_count = 3
num_workers = 2
window_size = 6
subsampling = 1e-3


model = Word2Vec(
    all_token_list,
    vector_size=500,
    workers=num_workers,
    min_count=min_word_count,
    window=window_size,
    sample=subsampling
)

model.build_vocab(all_token_list)
model.train(all_token_list, total_examples=model.corpus_count, epochs=30)
model_name = "my_domain_specific_word2vec_model"
model.save(f"{model_name}.model")
