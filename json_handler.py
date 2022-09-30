import json


class JsonHandler:

    @staticmethod
    def convert_str_to_json(string):
        """
        :param string:
        :return: dict
        """
        json_obj = json.loads(string)
        return json_obj


json_handler = JsonHandler()
