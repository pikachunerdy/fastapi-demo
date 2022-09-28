'''Encodings for messages send from the device service to the sensors'''

from libs.byte_encoder.encoder import TemplateBase, TemplateInt, TemplateVarList

class MeasurementEncoding(TemplateBase):
    '''Encoding for a sensor measurement'''
    time : int = TemplateInt(4)
    distance : int = TemplateInt(2)

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
    # device_id = (int,4)
    class Config(TemplateBase.Config):
        '''Encoding Config'''
        USE_ID = True
        ID_LENGTH = 4
        USE_ENCRYPTION = True
        USE_IV = True
    device_secret = TemplateInt(4)
    measurements = TemplateVarList(MeasurementEncoding)

class ServerDeviceEncoding(TemplateBase):
    '''Encoding for settings sent from device to sensor'''
    class Config(TemplateBase.Config):
        '''Encoding Config'''
        USE_ID = False
        USE_ENCRYPTION = True
    message_wait_time_s = TemplateInt(3)
    measurement_sleep_time_s = TemplateInt(3)
    warning_distance_mm = TemplateInt(3)
    warning_message_wait_time_s = TemplateInt(3)
    warning_measurement_sleep_time_s = TemplateInt(3)
    code_version = TemplateInt(3)
