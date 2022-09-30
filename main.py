import datetime

from license_plates import Ocr

if __name__ == '__main__':
    lp, decision = Ocr.get_vehicle_decision('123-45-678.jpg')
    current_time = datetime.datetime.now()
    Ocr.insert_data_to_parking_lot_table(int(lp), decision, "'{}'".format(current_time))


