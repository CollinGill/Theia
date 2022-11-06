from dotenv import load_dotenv
import os, io
import six
from google.cloud import vision_v1
from google.cloud import translate_v2 as translate

from google.cloud import speech_v1p1beta1 as speech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'
load_dotenv(".env")

def transcribe_file():
    client = speech.SpeechClient()
    AUDIO_FILE = "output/Penn_State_6.flac"
    with io.open(AUDIO_FILE, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        language_code="en-US",
        alternative_language_codes=["es", "zh", "ko"],
        enable_automatic_punctuation = True
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    print(operation)
    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)
    transcription = response.results[0].alternatives[0].transcript
    client = vision_v1.ImageAnnotatorClient()   

    translate_client = translate.Client()

    if isinstance(transcription, six.binary_type):
        transcription = transcription.decode("utf-8")
    
    result = translate_client.translate(transcription, target_language='en')
    return (transcription, result["translatedText"])
