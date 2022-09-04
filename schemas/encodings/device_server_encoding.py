from libs.byte_encoder.encoder import TemplateBase


class MeasurementEncoding(TemplateBase):
    time = (int, 4)
    distance = (int, 2)


class DeviceServerEncoding(TemplateBase):
    '''
    The received messages should be of the form
    0-1: 1 byte: Start of message = 0
    1-2: 1 byte: sum of all the bytes
    2-6: 4 byte: Device ID
    6-8: 2 byte: Num reading
    8-8+6*num_readings
    For each reading
        4 bytes time, 2 bytes distance
    '''
    device_id = (int,4)
    measurements = (list,MeasurementEncoding)

class ServerDeviceEncoding(TemplateBase):
    message_wait_time = (int,2)
    measurement_sleep_time = (int,2)
    warning_distance = (int,2)
    warning_message_wait_time = (int,2)
    warning_measurement_sleep_time = (int,2)
    code_version = (int,2)
