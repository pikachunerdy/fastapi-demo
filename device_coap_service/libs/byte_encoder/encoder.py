# TODO add custom exceptions
# TODO add compilation option
# TODO add bytes for list length
# TODO add custom type hinting

# TODO string length
from base64 import encodebytes
from typing import Optional, Tuple, Type
from Crypto.Cipher import AES
from Crypto import Random
# Template values are either (type, length) or (list, (type,length)) or (list, TemplateBase)


class TemplateBase:
    '''Base Class for an encoding template'''

    class Config:
        '''Config for encoding and decoding'''
        # HEADER SUM ID IV MESSAGE
        USE_HEADER_BYTE: bool = True
        HEADER_BYTE_VALUE: int = 0
        USE_SUM: bool = True
        USE_ID: bool = False
        ID_LENGTH: int = 4
        USE_ENCRYPTION: bool = False
        # USE_IV: bool = False
        IV_SIZE_BYTES: int = 16
        ENDIAN = 'little'
        STR_ENCODING = 'utf-8'


class Encoder:
    '''Class used to encode and decode bytes objects'''

    def __init__(self, template: Type[TemplateBase]) -> None:
        self.template = template
        self.members = [(attr, self.template.__dict__[attr])
                        for attr in self.template.__dict__.keys()
                        if not callable(getattr(self.template, attr)) and not attr.startswith("__")]
        #  TODO maybe compile encoding and decoding function chain at this stage

    def _encode_bytes(self, obj: TemplateBase):

        def encode_class(klass: Type, sub_obj, num_bytes: int) -> bytearray:
            if klass is int:
                sub_obj: int = sub_obj
                return sub_obj.to_bytes(num_bytes, self.template.Config.ENDIAN)
            if klass is str:
                sub_obj: str = sub_obj
                return sub_obj.encode(self.template.Config.STR_ENCODING)
            if klass is bool:
                return int(1).to_bytes(1, self.template.Config.ENDIAN) if sub_obj else int(0).to_bytes(1, self.template.Config.ENDIAN)
            return bytearray()

        encoded_bytes = bytearray()

        for member_name, member_value in self.members:
            klass = member_value[0]
            is_list = klass is list
            # case (list,TemplateBase) or (list, (int,4))
            if is_list:
                obj_list = obj.__dict__[member_name]
                list_length = len(obj_list)
                # add the list length to the bytes
                encoded_bytes.extend(list_length.to_bytes(
                    2, self.template.Config.ENDIAN))
                list_klass = member_value[1]
                # case (list, (int,4)
                if isinstance(list_klass, tuple):
                    list_klass, length = list_klass
                    # add each item in the list to the bytes
                    for sub_obj in obj_list:
                        encoded_bytes.extend(encode_class(
                            list_klass, sub_obj, length))
                # case (list,TemplateBase)
                elif issubclass(list_klass, TemplateBase):
                    encoder = Encoder(list_klass)
                    for sub_obj in obj_list:
                        encoded_bytes.extend(encoder._encode_bytes(sub_obj))
            # case (int,4)
            else:
                length = member_value[1]
                encoded_bytes.extend(encode_class(
                    klass, obj.__dict__[member_name], length))

        return encoded_bytes

    def encode_bytes(
            self, obj: TemplateBase,
            obj_id: Optional[int] = None, key: Optional[bytes] = None) -> bytes:
        '''Encoded an object as bytes'''
        encoded_bytes = self._encode_bytes(obj)
        if self.template.Config.USE_ENCRYPTION:
            aes_iv = Random.new().read(self.template.Config.IV_SIZE_BYTES)
            cipher = AES.new(key, AES.MODE_CFB, IV=aes_iv)
            encoded_bytes = cipher.encrypt(encoded_bytes)
            encoded_bytes = aes_iv + encoded_bytes
        if self.template.Config.USE_SUM:
            encoded_bytes = bytearray(
                [sum([int(x) for x in encoded_bytes]) & 255]) + encoded_bytes
        if self.template.Config.USE_ID:
            encoded_bytes = obj_id.to_bytes(
                self.template.Config.ID_LENGTH, self.template.Config.ENDIAN) + encoded_bytes
        if self.template.Config.USE_HEADER_BYTE:
            encoded_bytes[0:0] = self.template.Config.HEADER_BYTE_VALUE.to_bytes(
                1, self.template.Config.ENDIAN)
        return bytes(encoded_bytes)

    def _decode_bytes(self,
                      byte_array: bytes,
                      use_header: bool,
                      start_index: int) -> Tuple[TemplateBase, int]:
        '''Convert a byte array into the TemplateBase object,
        starting at the byte index given'''

        def decode_class(klass, byte_array):
            '''Convert a byte array into a specific object type'''
            if klass is int:
                return int.from_bytes(byte_array, self.template.Config.ENDIAN, signed=False)
            if klass is str:
                return byte_array.decode(self.template.Config.STR_ENCODING)
            if klass is bool:
                return int.from_bytes(byte_array, self.template.Config.ENDIAN, signed=False) > 0

        count = start_index
        if use_header:
            if self.template.Config.USE_HEADER_BYTE:
                count += 1
            if self.template.Config.USE_SUM:
                count += 1
            if self.template.Config.USE_ID:
                count += self.template.Config.ID_LENGTH

        response = self.template()
        for member_name, member_value in self.members:
            klass = member_value[0]
            is_list = klass is list
            # case (list,TemplateBase) or (list, (int,4))
            if is_list:
                decoded_list = []
                list_klass = member_value[1]
                # case (list, (int,4)
                if isinstance(list_klass, tuple):
                    list_klass, length = list_klass
                    list_length = int.from_bytes(
                        byte_array[count:count+2],
                        self.template.Config.ENDIAN,
                        signed=False,
                    )
                    count += 2
                    for _ in range(list_length):
                        decoded_value = decode_class(
                            list_klass, byte_array[count:count+length])
                        decoded_list.append(decoded_value)
                        count = count + length
                # case (list,TemplateBase)
                elif issubclass(list_klass, TemplateBase):
                    encoder = Encoder(list_klass)
                    list_length = int.from_bytes(
                        byte_array[count:count+2], self.template.Config.ENDIAN, signed=False)
                    count += 2
                    for _ in range(list_length):
                        decoded_value, count_addition = encoder._decode_bytes(
                            byte_array, False, count)
                        count += count_addition
                        decoded_list.append(decoded_value)
                response.__dict__[member_name] = decoded_list
            # case (int,4)
            else:
                length = member_value[1]
                decoded_value = decode_class(
                    klass, byte_array[count:count+length])
                count = count + length
                response.__dict__[member_name] = decoded_value

        return response, count - start_index

    def get_id(self, byte_array: bytes) -> int:
        '''Get the object ID from the encoding'''
        index = 0 if not self.template.Config.USE_HEADER_BYTE else 1
        index = index if not self.template.Config.USE_SUM else (index + 1)
        return int.from_bytes(
            byte_array[index:index + self.template.Config.ID_LENGTH],
            self.template.Config.ENDIAN, signed=False)

    def validate_header(self, byte_array: bytes) -> bool:
        '''Ensure the the checks in the header are met such as the sum'''
        count = 0
        ints = [int(x) for x in byte_array]
        if self.template.Config.USE_HEADER_BYTE:
            if byte_array[count] != self.template.Config.HEADER_BYTE_VALUE:
                return False
            count += 1
        if self.template.Config.USE_SUM:
            message_sum = ints[1]
            actual_sum = sum(ints[2:]) & 255
            if actual_sum != message_sum:
                return False
        return True

    def decrypt(self, byte_array: bytes, key: bytes) -> bytes:
        '''Decrypt the message body given an aes key'''
        index = 0 if not self.template.Config.USE_HEADER_BYTE else 1
        index = index if not self.template.Config.USE_SUM else (index + 1)
        index = index if not self.template.Config.USE_ID else (
            index + self.template.Config.ID_LENGTH)
        header = byte_array[:index]
        iv = byte_array[index:index + self.template.Config.IV_SIZE_BYTES]
        index += self.template.Config.IV_SIZE_BYTES
        cipher = AES.new(key, AES.MODE_CFB, IV=iv)
        message = cipher.decrypt(byte_array[index:])
        return header + message

    def decode_bytes(self, byte_array: bytes, key: Optional[bytes] = None) -> TemplateBase:
        '''Convert a decrypted byte array into '''
        if key is not None:
            byte_array = self.decrypt(byte_array, key)
        obj, _ = (self._decode_bytes(byte_array, True, 0))
        return obj


if __name__ == '__main__':
    class Test(TemplateBase):

        x = (int, 2)
        y = (bool, 1)

    test = Test()
    test.x = 253
    test.y = True

    encoder = Encoder(Test)
    out = encoder.encode_bytes(test)
    response = encoder.decode_bytes(out)
    assert response.x == test.x
    assert response.y == test.y

    class Test2(TemplateBase):
        class Config(TemplateBase.Config):
            USE_ENCRYPTION: bool = True
        x = (list, (int, 5))
        y = int, 4

    key = b'\x12!\xfbLT\xf6\xd1YY}\xc9\xd4i\xdb\xb9\x92'

    test2 = Test2()
    test2.x = [2345, 234, 4363, 32]
    test2.y = 234

    encoder = Encoder(Test2)
    out = encoder.encode_bytes(test2, key=key)
    response = encoder.decode_bytes(out, key=key)
    assert len(test2.x) == len(response.x)
    for x, y in zip(test2.x, response.x):
        assert x == y
    assert response.y == test2.y
