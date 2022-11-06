from dotenv import load_dotenv
import os, io
import itertools
import requests
import six
from google.cloud import vision_v1
from google.cloud import translate_v2 as translate

from google.cloud.vision_v1 import types
from google.cloud import speech_v1p1beta1 as speech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'
load_dotenv(".env")

def transcribe_file():
    client = speech.SpeechClient()
    AUDIO_FILE = "output/audio.flac"
    with io.open(AUDIO_FILE, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)


    config = speech.RecognitionConfig(
        language_code="en-US",
        alternative_language_codes=["es", "zh", "ko"]
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    print(operation)
    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.

    transcription = response.results[0].alternatives[0].transcript
    # print(transcription)
    client = vision_v1.ImageAnnotatorClient()   

    translate_client = translate.Client()

    if isinstance(transcription, six.binary_type):
        transcription = transcription.decode("utf-8")
    
    result = translate_client.translate(transcription, target_language='en')
    # print(result["translatedText"])
    return result["translatedText"]

    # for result in response.results:
    #     # The first alternative is the most likely one for this portion.
    #     # print('here2')
    #     print(u"Transcript: {}".format(result.alternatives[0].transcript))
    #     print("Confidence: {}".format(result.alternatives[0].confidence))
# transcribe_file()
