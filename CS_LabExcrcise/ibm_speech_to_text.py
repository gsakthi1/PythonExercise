from ibm_watson import SpeechToTextV1 
import json
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

url_s2t = "https://stream.watsonplatform.net/speech-to-text/api"

iam_apikey_s2t = "kKBqpOnxZ1GO0DVYFi5gZLvVYmTSnEuh4Cylfs7Wa7C0"

authenticator = IAMAuthenticator(iam_apikey_s2t)
s2t = SpeechToTextV1(authenticator=authenticator)
s2t.set_service_url(url_s2t)
s2t

#filename='PolynomialRegressionandPipelines.mp3'
filename='example_1.mp3'

with open(filename, mode="rb")  as wav:
    response = s2t.recognize(audio=wav, content_type='audio/mp3')

#print(response.result)

from pandas.io.json import json_normalize

json_normalize(response.result['results'],"alternatives")

recognized_text=response.result['results'][0]["alternatives"][0]["transcript"]
type(recognized_text)

from ibm_watson import LanguageTranslatorV3

url_lt='https://gateway.watsonplatform.net/language-translator/api'

apikey_lt='aOrls6NPXJ-ltt_Ub89AWKPiLv3KcFLTkjt9e5yHnXAC'

version_lt='2018-05-01'

authenticator = IAMAuthenticator(apikey_lt)
language_translator = LanguageTranslatorV3(version=version_lt,authenticator=authenticator)
language_translator.set_service_url(url_lt)
language_translator

from pandas.io.json import json_normalize

x = json_normalize(language_translator.list_identifiable_languages().get_result(), "languages")
#print("json - ", x)

translation_response = language_translator.translate(text=recognized_text, model_id='en-es')
translation=translation_response.get_result()
spanish_translation =translation['translations'][0]['translation']
print(spanish_translation)

tamil_trans_rsp = language_translator.translate(text=recognized_text, model_id='en-hi')
tamil_trans=tamil_trans_rsp.get_result()
tamil_trans_rslt = tamil_trans['translations'][0]['translation']
print(tamil_trans_rslt)

tamil_trans_rsp = language_translator.translate(text=recognized_text, model_id='en-de')
tamil_trans=tamil_trans_rsp.get_result()
tamil_trans_rslt = tamil_trans['translations'][0]['translation']
print(tamil_trans_rslt)
