import datetime

import requests
from json_handler import json_handler
from database import db_handler


class Ocr:
    @staticmethod
    def ocr_space_file(filename, overlay=False, api_key='helloworld', language='eng'):
        """ OCR.space API request with local file.
            Python3.5 - not tested on 2.7
        :param filename: Your file path & name.
        :param overlay: Is OCR.space overlay required in your response.
                        Defaults to False.
        :param api_key: OCR.space API key.
                        Defaults to 'helloworld'.
        :param language: Language code to be used in OCR.
                        List of available language codes can be found on https://ocr.space/OCRAPI
                        Defaults to 'en'.
        :return: Result in JSON format.
        """
        # api_key = 'K86313628888957'
        payload = {'isOverlayRequired': overlay,
                   'apikey': api_key,
                   'language': language,
                   }
        with open(filename, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                              files={filename: f},
                              data=payload,
                              )
        return r.content.decode()

    @staticmethod
    def ocr_space_url(url, overlay=False, api_key='helloworld', language='eng'):
        """ OCR.space API request with remote file.
            Python3.5 - not tested on 2.7
        :param url: Image url.
        :param overlay: Is OCR.space overlay required in your response.
                        Defaults to False.
        :param api_key: OCR.space API key.
                        Defaults to 'helloworld'.
        :param language: Language code to be used in OCR.
                        List of available language codes can be found on https://ocr.space/OCRAPI
                        Defaults to 'en'.
        :return: Result in JSON format.
        """
        # api_key = 'K86313628888957'
        payload = {'url': url,
                   'isOverlayRequired': overlay,
                   'apikey': api_key,
                   'language': language,
                   }
        r = requests.post('https://api.ocr.space/parse/image',
                          data=payload,
                          )
        return r.content.decode()

    @staticmethod
    def _extract_lp(json_data):
        """
        extract the license plate number from the json data
        :param json_data: dict
        :return: lp_number: int
        """
        lp_text = json_data['ParsedResults'][0]['ParsedText']
        lp_number = ''.join(x for x in lp_text if x.isdigit())
        return lp_number

    @staticmethod
    def get_decision(lp_number):
        """
        get the decision for specific license plate number to enter/Not enter the parking lot
        :param lp_number:
        :return:
        """
        if lp_number[-2:] == '25' or lp_number[-2:] == '26':
            entered = True
            print("Please enter the parking lot.")
        elif lp_number[-2:] in ['85', '86', '87', '88', '89', '00']:
            entered = False
            print("Vehicle '{}' should not enter the parking lot.".format(lp_number))
        elif len(lp_number) == 7 and lp_number[-1] in ['0', '5']:
            entered = False
            print("vehicle '{}' cannot enter the parking lot.".format(lp_number))
        else:
            entered = True
            print('Please enter the parking lot.')

        return entered

    @staticmethod
    def insert_data_to_parking_lot_table(*values):
        """
        Insert values to parking_lot table
        :param values:
        :return:
        """
        db_handler.insert_into_table('parking_lot', 'lp, entered, timestamp', *values)


    @staticmethod
    def get_vehicle_decision(lp_image_file):
        """
        get vehicle license plate image and return a decision for the vehicle to enter/Not enter the parking lot
        :param lp_image_file:
        :return: license plate number [int], decision: [bool] (True- entered / False- Not entered)
        """
        text_file = Ocr.ocr_space_file(filename=lp_image_file, language='pol')
        text_dict = json_handler.convert_str_to_json(text_file)
        lp = Ocr._extract_lp(text_dict)
        decision = Ocr.get_decision(lp)
        return lp, decision
        # current_time = datetime.datetime.now()
        # Ocr.insert_data_to_parking_lot_table([int(lp), decision, "'{}'".format(current_time)])

