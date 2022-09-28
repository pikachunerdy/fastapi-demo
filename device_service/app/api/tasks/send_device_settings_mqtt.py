'''Send a devices settings to MQTT server'''

from app.api.main import celery
# from libs.byte_encoder.encoder import Encoder
# from schemas.encodings.device_server_encoding import ServerDeviceEncoding
# from schemas.mongo_models.device_models import MongoDevice


@celery.task(name="send_device_settings_mqtt")
async def send_device_settings_mqtt_task(device_id : int):
    '''Send the device settings information to the mqtt server'''
    # Request the device settings information
    # Encode the device information
    # Send the information to MQTT server
    # mongo_device = await MongoDevice.find(MongoDevice.device_id == device_id).first_or_none()
    # settings = ServerDeviceEncoding()
    # settings.message_wait_time_s = mongo_device.device_settings.message_wait_time_s
    # settings.measurement_sleep_time_s = mongo_device.device_settings.measurement_sleep_time_s
    # settings.warning_distance_mm = mongo_device.device_settings.warning_distance_mm
    # settings.warning_message_wait_time_s = mongo_device.device_settings.warning_message_wait_time_s
    # settings.warning_measurement_sleep_time_s = mongo_device.device_settings.warning_measurement_sleep_time_s
    # settings.code_version = mongo_device.device_settings.code_version

    # encoder = Encoder(ServerDeviceEncoding)
    # mqtt_client.publish('device_settings_' + str(device_id), encoder.encode_bytes(settings))
