import re
import requests
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
import pandas as pd
import spacy
from sklearn.feature_extraction.text import CountVectorizer


# Load product names
df = pd.read_csv('../products.csv', delimiter=';')

# Transcribe audio to text
def voice_to_text(filename, hints):
    client = speech.SpeechClient()

    with open(filename, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        speech_contexts=[{"phrases": hints}],
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        audio_channel_count=2,
        language_code="es-ES",
        enable_automatic_punctuation=True,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    print(transcript)
    return transcript

def text_to_voice(text):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)

# Load product names from products.csv
def load_products():
    data = pd.read_csv('../products.csv', delimiter=';')
    return data['name'].tolist()

def load_hints():
    data = pd.read_csv('../products.csv', delimiter=';')
    product_names = data['name'].tolist()
    words = []
    for name in product_names:
        words.extend(name.split())
    return words

# Add products to shopping list
def add_to_list(text, products):
    shopping_list = []
    text = text.lower()
    for product in products:
        if product.lower() in text:
            shopping_list.append(product)
    return shopping_list

def main():
    # Load SpaCy model
    nlp = spacy.load('en_core_web_sm')

    # Replace 'your-audio-file' with the path to your audio file
    text = voice_to_text('../javi2.wav', load_hints())
    # text_to_voice(text)

    # Remove spaces between numbers and "ml"
    text = re.sub(r'(\d+)\s+ml', r'\1ml', text, flags=re.IGNORECASE)
    text = re.sub(r'(\d+)\s+cm', r'\1cm', text, flags=re.IGNORECASE)
    text = re.sub(r'(\d+)\s+cp', r'\1cp', text, flags=re.IGNORECASE)
    text = text.replace('Excalibur', 'scalibor')
    text = re.sub(r'\boti\w*', 'otinet', text, flags=re.IGNORECASE)
    text = re.sub(r'\bothy\w*', 'otinet', text, flags=re.IGNORECASE)
    text = text.replace(' dash ', '-')
    text = text.replace(' slash ', '/')
    text = text.replace(' mililiters', 'ml')
    
    print(text)

    # Analyze the text with the NER model
    products = load_products()

    shopping_list = add_to_list(text, products)
    
    print(shopping_list)

main()