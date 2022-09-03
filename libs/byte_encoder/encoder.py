# TODO add custom exceptions
from email import message
from typing import Tuple, Type
from typing import get_type_hints
import inspect

# Template values are either (type, length) or (list, (type,length))

class TemplateBase:

    class Config:
        HEADER_VALUE : int = 0
        USE_SUM : bool = True
        ENDIAN = 'little'
        STR_ENCODING = 'utf-8'



class Child(TemplateBase):

    class Config(TemplateBase.Config):
        HEADER_VALUE = 1


class Encoder:

    def __init__(self, template : Type[TemplateBase]) -> None:
        self.template = template
        self.members = [(attr,self.template.__dict__[attr]) for attr in self.template.__dict__.keys() if not callable(getattr(self.template, attr)) and not attr.startswith("__")]

        # print('hello')

    def encode_bytes(self, object) -> bytes:
        pass

    def _decode_bytes(self, byte_array : bytes, use_header: bool, start_index : int) -> Tuple[TemplateBase, int]:
        def decode_class(klass, byte_array):
            if klass is int:
                # print(int.from_bytes(byte_array,self.template.Config.ENDIAN, signed=False))
                # print([int(x) for x in byte_array])
                return int.from_bytes(byte_array,self.template.Config.ENDIAN, signed=False)
            if klass is str:
                return byte_array.decode(self.template.Config.STR_ENCODING)
            if klass is bool:
                return int.from_bytes(byte_array,self.template.Config.ENDIAN, signed=False) > 0
        # print(byte_array)
        count = start_index
        if use_header:
            ints = [int(x) for x in byte_array]
            if byte_array[count] != self.template.Config.HEADER_VALUE:
                raise Exception
            count += 1
            if self.template.Config.USE_SUM:
                message_sum = ints[1]
                actual_sum = sum(ints[2:]) & 255
                # print(actual_sum)
                # print(message_sum)
                if actual_sum != message_sum:
                    raise Exception
                count += 1
        response = self.template()
        for name,value in self.members:
            klass = value[0]
            is_list = klass is list
            # print(klass)
            if is_list:
                encoder = Encoder(value[1])
                # print('bits',[int(x) for x in byte_array[count:count+2]])
                list_length = int.from_bytes(byte_array[count:count+2],self.template.Config.ENDIAN, signed=False)
                # print(count)
                # print(list_length)
                count += 2
                decoded_list = []
                # print('length',list_length)
                for i in range(list_length):
                    decoded_value, count_addition = encoder._decode_bytes(byte_array, False, count)
                    count += count_addition
                    decoded_list.append(decoded_value)
                    # print(decoded_value)
                response.__dict__[name] = decoded_list
            else:
                length = value[1]
                # print('bit length',length)
                decoded_value = decode_class(klass, byte_array[count:count+length])
                count = count + length
                response.__dict__[name] = decoded_value

        return response, count - start_index


    def decode_bytes(self, byte_array : bytes) -> TemplateBase:
        x = (self._decode_bytes(byte_array, True, 0))
        print([int(x) for x in byte_array])
        # print(x)
        return x[0]




class Template(TemplateBase):

    time = (list,(int,2))
    measurements = (list,(int,2))
