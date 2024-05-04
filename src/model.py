import spacy
import random
import pandas as pd

# Load product names
data= pd.read_csv('../products.csv', delimiter=';')

# Load the SpaCy model
nlp = spacy.blank('en')

# Create a new entity recognizer and add it to the pipeline
ner = nlp.create_pipe('ner')
nlp.add_pipe(ner)

# Add the label 'PRODUCT' to the entity recognizer
ner.add_label('PRODUCT')

# Start the training
nlp.begin_training()

# Train for 10 iterations
for itn in range(10):
    random.shuffle(data)
    losses = {}

    # Batch the examples and iterate over them
    for batch in spacy.util.minibatch(data, size=2):
        texts = [text for text, entities in batch]
        annotations = [entities for text, entities in batch]

        # Update the model
        nlp.update(texts, annotations, losses=losses)

    print(losses)