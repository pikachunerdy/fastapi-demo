'''Coap-Device_Service Models for setting up a device'''

from pydantic import  BaseModel

class SetupRequest(BaseModel):
    '''Request from coap service to device service to setup a device'''
    device_id : int
    coordinates : tuple[float,float]
    company_id : str
    account_id : str
