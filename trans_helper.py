import rsa_helper
import rsa
import transFileBits
import transStrBits
import random

def generate_random_binary_string(length):
    return ''.join(random.choices(['0', '1'], k=length)) 
def add_one_and_check(input_str : str) -> str: 
    output_str = ""
    ones = 0
    if len(input_str) % 14:
        input_str += '0' * (14 - len(input_str) % 14)
    input_len = len(input_str)
    for i in range(len(input_str)):
        assert(input_str[i] == '0' or input_str[i] == '1')
        if i % 14 == 0:
            output_str += '1'
            if ones % 2 :
                output_str += '1'
            else :
                output_str += '0'
            ones = 0
        output_str += input_str[i]
        ones += input_str[i] == '1'
    output_str += '1'
    if ones % 2 :
        output_str += '1'
    else :
        output_str += '0' 
    output_len = len(output_str)
    assert(output_len * 14 == input_len * 16)

    return output_str
def remove_one_and_check(input_str: str) -> (str, bool):
    output_str = ""
    ones = 0
    flag = True
    assert(len(input_str) % 16 == 0)

    for i in range(len(input_str)):
        assert(input_str[i] == '0' or input_str[i] == '1')
        if i % 16 == 14:
            flag = flag and (input_str[i] == '1')
        elif i % 16 == 15:
            
            if ones % 2 :
                flag = flag and  (input_str[i] =='1')
            else :
                flag = flag and (input_str[i] == '0')
            ones = 0
        else:
            ones += input_str[i] == '1'
            output_str += input_str[i]

    return output_str, flag


class Client :
    def __init__(self, key_file : str, random_len : int, user_name : str):
        
        with open(key_file + 'publicKey.pem', 'rb') as p:
            self.publicKey = rsa.PublicKey.load_pkcs1(p.read())
        self.padding_len = 2 ** 8
        self.random_len = random_len
        self.user_name = user_name
        self.password = rsa_helper.encrypt(self.user_name.encode('utf-8'), self.publicKey)

    def send_file(self, file_name : str):
        # transfer file to  
        # padding start + user_name + pubkey(user_name)  + [ file_len + randombits(len = len(user_name)) + file + randombits(len = len(user_name))] + padding end
        # before transfer, both client and server know the len and keys
        
        all_bits = ""
        
        padding_start = ""
        for i in range(self.padding_len):
            padding_start += "0" * (self.padding_len) + "{:08b}".format(i)
        
        print("padding start :", padding_start)
         

        bits = transStrBits.trans_str_to_bits(self.user_name)
        bits_len = len(bits)
        print("user_name :{}, len : {}".format(self.user_name[:10], bits_len))
        all_bits += "{:032b}".format(bits_len)
        all_bits += bits

        
        bits = transStrBits.trans_str_to_bits(self.password)
        bits_len = len(bits)
        print("password :{}, len : {}".format(self.password[:10], bits_len))
        all_bits += "{:032b}".format(bits_len)
        all_bits += bits



        file_bits = rsa_helper.encrypt_file(file_name, self.publicKey)
        file_bits = transStrBits.trans_str_to_bits(file_bits) 
        bits_len = len(file_bits)
        print("file len : {}".format(bits_len))
        all_bits += transStrBits.trans_str_to_bits(rsa_helper.encrypt("{:032b}".format(bits_len),self.publicKey))
        all_bits += generate_random_binary_string(self.random_len)
        all_bits += add_one_and_check(file_bits)
        all_bits += generate_random_binary_string(self.random_len)

        return padding_start + add_one_and_check(all_bits)

