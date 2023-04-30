@echo off

call venv\Scripts\activate

echo extract information from recipes html...
poetry run ex-rep_info
echo create training data and test data...
poetry run create-training_data
echo generate docBin object for Spacy training
poetry run create-docBin
echo start training new model
spacy train config.cfg --output ./output --paths.train ./data/training_data.spacy --paths.dev ./data/test_data.spacy --gpu-id 0

call venv\Scripts\deactivate
