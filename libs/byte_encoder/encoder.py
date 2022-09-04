# TODO add custom exceptions
# TODO add compilation option
# TODO add bytes for list length
# TODO add custom type hinting
from email import message
from typing import Tuple, Type
from typing import get_type_hints
import inspect
from Crypto.Cipher import AES

# Template values are either (type, length) or (list, (type,length))

class TemplateBase:

    class Config:
        USE_HEADER_BYTE : bool = True
        HEADER_BYTE_VALUE : int = 0
        USE_SUM : bool = True
        USE_ID : bool
        ID_LENGTH : int = 4
        USE_ENCRYPTION : bool = False
        USE_PADDING : bool = False
        BLOCK_SIZE_BYTES : int = 16
        USE_IV : bool = False
        IV_SIZE_BYTES : int = 16
        ENDIAN = 'little'
        STR_ENCODING = 'utf-8'



class Child(TemplateBase):

    class Config(TemplateBase.Config):
        HEADER_VALUE = 1


class Encoder:

    def __init__(self, template : Type[TemplateBase]) -> None:
        self.template = template
        self.members = [(attr,self.template.__dict__[attr]) for attr in self.template.__dict__.keys() if not callable(getattr(self.template, attr)) and not attr.startswith("__")]

        #  TODO maybe compile encoding and decoding function chain at this stage

    def encode_bytes(self, object : TemplateBase) -> bytes:
        ...

    def _decode_bytes(self, byte_array : bytes, use_header: bool, start_index : int) -> Tuple[TemplateBase, int]:

        def decode_class(klass, byte_array):
            if klass is int:
                return int.from_bytes(byte_array,self.template.Config.ENDIAN, signed=False)
            if klass is str:
                return byte_array.decode(self.template.Config.STR_ENCODING)
            if klass is bool:
                return int.from_bytes(byte_array,self.template.Config.ENDIAN, signed=False) > 0

        count = start_index
        if use_header:
            ints = [int(x) for x in byte_array]
            if self.template.Config.USE_HEADER_BYTE:
                if byte_array[count] != self.template.Config.HEADER_VALUE:
                    raise Exception
                count += 1
            if self.template.Config.USE_SUM:
                message_sum = ints[1]
                actual_sum = sum(ints[2:]) & 255
                if actual_sum != message_sum:
                    raise Exception
                count += 1
        response = self.template()
        for name,value in self.members:
            klass = value[0]
            is_list = klass is list
            # case (list,TemplateBase) or (list, (int,4))
            if is_list:
                decoded_list = []
                list_klass = value[1]
                # case (list, (int,4)
                if type(list_klass) is tuple:
                    list_klass, length = list_klass
                    list_length = int.from_bytes(byte_array[count:count+2],self.template.Config.ENDIAN, signed=False)
                    for i in range(list_length):
                        decoded_value = decode_class(list_klass, byte_array[count:count+length])
                        count = count + length
                # case (list,TemplateBase)
                elif issubclass(list_klass, TemplateBase):
                    encoder = Encoder(list_klass)
                    list_length = int.from_bytes(byte_array[count:count+2],self.template.Config.ENDIAN, signed=False)
                    count += 2
                    for i in range(list_length):
                        decoded_value, count_addition = encoder._decode_bytes(byte_array, False, count)
                        count += count_addition
                        decoded_list.append(decoded_value)
                response.__dict__[name] = decoded_list
            # case (int,4)
            else:
                length = value[1]
                decoded_value = decode_class(klass, byte_array[count:count+length])
                count = count + length
                response.__dict__[name] = decoded_value

        return response, count - start_index

    def get_id(self, byte_array : bytes) -> bytes:
        index = 0 if not self.template.Config.USE_HEADER_BYTE else 1
        index = index if not self.template.Config.USE_SUM else (index + 1)
        return byte_array[index:index + self.template.Config.ID_LENGTH]


    def decrypt(self, byte_array : bytes, key) -> bytes:
        index = 0 if not self.template.Config.USE_HEADER_BYTE else 1
        index = index if not self.template.Config.USE_SUM else (index + 1)
        index = index if not self.template.Config.USE_ID else (index + self.template.Config.ID_LENGTH )
        nonce = byte_array[index:index + 12]
        index += 12
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)


    def decode_bytes(self, byte_array : bytes) -> TemplateBase:
        x = (self._decode_bytes(byte_array, True, 0))
        return x[0]




class Template(TemplateBase):

    time = (list,(int,2))
    measurements = (list,(int,2))
