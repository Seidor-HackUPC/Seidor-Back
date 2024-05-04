import requests
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


# Load product names
df = pd.read_csv('../products.csv', delimiter=';')

# Transcribe audio to text
def voice_to_text(filename):
    client = speech.SpeechClient()

    with open(filename, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        audio_channel_count=2,
        language_code="en-US",
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

# Extract product names from text
def extract_products(text):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['name'])
    product_names = vectorizer.get_feature_names_out()
    return [word for word in text.split() if word in product_names]

# Add products to shopping list
def add_to_list(products):
    shopping_list = []
    shopping_list.extend(products)
    return shopping_list

# Main function
def main():
    # Replace 'your-audio-file' with the path to your audio file
    text = voice_to_text('../audio2.wav')
    text_to_voice(text)
    products = extract_products(text)
    shopping_list = add_to_list(products)
    print(shopping_list)

main()