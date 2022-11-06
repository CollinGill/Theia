from dotenv import load_dotenv
import os, io
import itertools
import requests
from google.cloud import vision_v1

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'
load_dotenv(".env")
EXCHANGE_RATE_API_KEY = os.environ.get("EXCHANGE_RATE_API_KEY")

def textConvert(input):
    dct = {'dollar':        'USD',
           '$':             'USD',
           'dollars':       'USD',
           'usd':           'USD',
           'euro':          'EUR',
           'euros':         'EUR',
           '€':             'EUR',
           'eur':           'EUR',
           'yen':           'JPY',
           '円':            'JPY',
           '¥':             'JPY',
           'jpy':           'JPY',
           'sterling':      'GBP',
           'pound':         'GBP',
           'sterlings':     'GBP',
           'pounds':        'GBP',
           '£':             'GBP',
           'gpb':           'GPB',
           '元':            'CNY',
           'renminbi':      'CNY',
           'cny':           'CNY',
           'austrailian':   'AUD',
           'aud':           'AUD',
           'a$':            'AUD',
           'cad':           'CAD',
           'c$':            'CAD',
           'C$':            'CAD',
           '₹':             'INR',
           'rupee':         'INR',
           'rupees':        'INR',
           '₱':             'PHP',
           'peso':          'MXN',
           'pesos':         'MXN',
           '₽':             'RUB',
           'ruble':         'RUB',
           'rubles':        'RUB'}

    splitInput = ["".join(x) for _, x in itertools.groupby(input, key=str.isdigit)]
    for count, value in enumerate(splitInput):
        if value == '.':
            splitInput[count-1] = splitInput[count-1] + splitInput[count] + splitInput[count+1]
            splitInput.pop(count)
            splitInput.pop(count)
    splitOutput = []
    for segment in splitInput:
        if segment.lower() in dct:
            splitOutput.append(dct[segment.lower().strip()])
        elif segment[0].isnumeric:
            splitOutput.append(segment.strip())
        else: 
            return "There was an error, scanned something it shouldn't have"
    return splitOutput

def currencyConvert(splitInput):
    rates = requests.get("https://v6.exchangerate-api.com/v6/" + EXCHANGE_RATE_API_KEY + "/latest/USD").json()["conversion_rates"]
    num = ""
    currency = ""
    if len(splitInput) != 2:
        return "ERROR"
    for segment in splitInput:
        if segment[0].isdigit():
            num = segment
        else:
            currency = segment
    conversionRate = rates[textConvert(currency)[0]]
    return "$" + str(round(float(num)/conversionRate, 2))

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

    orig = docText
    USD = currencyConvert(textConvert(docText))
    return (orig, USD)