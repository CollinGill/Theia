from dotenv import load_dotenv
import os, io
import itertools
import requests
from google.cloud import vision_v1
from google.cloud.vision_v1 import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'
load_dotenv(".env")
EXCHANGE_RATE_API_KEY = os.environ.get("EXCHANGE_RATE_API_KEY")

def get_output():
    orig = ""
    USD = ""
    client = vision_v1.ImageAnnotatorClient()   
    IMAGE_FILE = "output/currency.jpg"
    with io.open(IMAGE_FILE, 'rb') as image_file:
        content = image_file.read()

    image = vision_v1.types.Image(content=content)
    response = client.document_text_detection(image=image)
    docText = response.full_text_annotation.text

    def textConvert(input):
        dct = {'dollar': 'USD',
            '$': 'USD',
            'dollars': 'USD',
            'usd': 'USD',
            'euro': 'EUR',
            'euros': 'EUR',
            '€': 'EUR',
            'eur': 'EUR',
            'yen': 'JPY',
            '円': 'JPY',
            '¥': 'JPY',
            'JPY': 'JPY',
            'sterling': 'GBP',
            'pound': 'GBP',
            'sterlings': 'GBP',
            'pounds': 'GBP',
            '£': 'GBP',
            'gpb': 'GPB',
            '元': 'CNY',
            'renminbi': 'CNY',
            'CNY': 'CNY',
            'austrailian': 'AUD',
            'aud': 'AUD',
            'a$': 'AUD',
            'cad': 'CAD',
            'c$': 'CAD'}
        spltInput = ["".join(x) for _, x in itertools.groupby(input, key=str.isdigit)]
        for count, value in enumerate(spltInput):
            if value == '.':
                spltInput[count-1] = spltInput[count-1] + spltInput[count] + spltInput[count+1]
                spltInput.pop(count)
                spltInput.pop(count)
        spltOutput = []
        for segment in spltInput:
            if segment.lower() in dct:
                spltOutput.append(dct[segment.lower()])
            elif segment[0].isnumeric:
                spltOutput.append(segment)
            else: 
                return "There was an error, scanned something it shouldn't have"
        return spltOutput

    def currencyConvert(spltInput):
        rates = requests.get("https://v6.exchangerate-api.com/v6/" + EXCHANGE_RATE_API_KEY + "/latest/USD").json()["conversion_rates"]
        num = ""
        currency = ""
        if len(spltInput) != 2:
            return "ERROR"
        for segment in spltInput:
            if segment[0].isdigit():
                num = segment
            else:
                currency = segment
        conversionRate = rates[currency]
        return "$" + str(round(float(num)/conversionRate, 2))

    orig = docText
    USD = currencyConvert(textConvert(docText))
    return (orig, USD)
