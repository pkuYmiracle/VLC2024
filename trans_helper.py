import rsa_helper
import rsa
import transFileBits
import transStrBits
import random
PADDING_LEN = 2 ** 8


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
        if i != 0 and i % 14 == 0:
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
class Server :
    def __init__(self):
        self.users = []

    def add_user(self, key_file : str, random_len : int, user_name : str, password : str):
        self.users.append((key_file, random_len, user_name, password))

    def receive_file(self, file_name : str, all_bits : str):
        
        flag = False
        for i in range(PADDING_LEN - 1):
            padding_start = ""
            for j in range(i, PADDING_LEN):
                padding_start += "0" * 24 + "{:08b}".format(j)
            find_index = all_bits.find(padding_start)
            if find_index != -1:
                all_bits = all_bits[find_index + len(padding_start):]
                flag = True
                break
        if flag == False:
            print("No padding start")
            return 
        padding_end = ""
        for i in range(PADDING_LEN - 1, -1, -1):
            padding_end += "0" * 24 + "{:08b}".format(i)
        index = all_bits.find(padding_end)
        if index == -1:
            print("No padding end")
            return
        all_bits = all_bits[:index]
        
        all_bits,flag = remove_one_and_check(all_bits)
        if flag == False:
            print("Error in format!")
            return
        bits_len = int(all_bits[:32], 2)
        all_bits = all_bits[32:]
        user_name = transStrBits.trans_bits_to_str(all_bits[:bits_len])
        all_bits = all_bits[bits_len:]
        print("user_name :{}, len : {}".format(user_name[:10], bits_len))
        user = ()
        for i in self.users:
            if i[2] == user_name:
                user = i
                break
        
        with open(user[0] + 'publicKey.pem', 'rb') as p:
            publicKey = rsa.PublicKey.load_pkcs1(p.read())
        with open(user[0] + 'privateKey.pem', 'rb') as p:
            privateKey = rsa.PrivateKey.load_pkcs1(p.read())
        
        if user == ():
            print("No such user!")
            return
        password_len = int(all_bits[:32], 2)
        all_bits = all_bits[32:]
        password = transStrBits.binary_to_bytes(all_bits[:password_len])
        all_bits = all_bits[password_len:]
        print("password :{}, len : {}".format(password[:10], password_len))
        password = rsa_helper.decrypt(password, privateKey) 
        if password != user[3]:
            print("Wrong password!")
            return
        file_len = int(all_bits[:32], 2)
        all_bits = all_bits[32:]
        print("file len : {}".format(file_len))
        all_bits = all_bits[user[1]:]
        file_bits = all_bits[:file_len]
        transFileBits.trans_bits_to_file(file_bits, file_name)  
        print("Receive file successfully!")

class Client :
    def __init__(self, key_file : str, random_len : int, user_name : str, password : str):
        
        with open(key_file + 'publicKey.pem', 'rb') as p:
            self.publicKey = rsa.PublicKey.load_pkcs1(p.read()) 
        self.random_len = random_len
        self.user_name = user_name
        self.password = rsa_helper.encrypt(password, self.publicKey)

    def send_file(self, file_name : str):
        # transfer file to  
        # padding start + user_name + encrypt(user_name)  + file_len + [ randombits(len = len(user_name)) + file + randombits(len = len(user_name))] + padding end
        # before transfer, both client and server know the len and keys
        
        all_bits = ""
        
        padding_start = ""
        for i in range(PADDING_LEN):
            padding_start += "0" * 24 + "{:08b}".format(i)
        
        print("padding start len: ", len(padding_start))
         

        bits = transStrBits.trans_str_to_bits(self.user_name)
        bits_len = len(bits)
        print("user_name :{}, len : {}".format(self.user_name[:10], bits_len))
        all_bits += "{:032b}".format(bits_len)
        all_bits += bits
 
        bits = transStrBits.bytes_to_binary(self.password)
        bits_len = len(bits)
        print("password :{}, len : {}".format(self.password[:10], bits_len))
        all_bits += "{:032b}".format(bits_len)
        all_bits += bits



        file_bits = transFileBits.trans_file_to_bits(file_name)  
        bits_len = len(file_bits)
        print("file len : {}".format(bits_len))
        all_bits += "{:032b}".format(bits_len)
        all_bits += generate_random_binary_string(self.random_len)
        all_bits += file_bits
        all_bits += generate_random_binary_string(self.random_len)
 

        
        padding_end = ""
        for i in range(PADDING_LEN - 1, -1, -1):
            padding_end += "0" * 24 + "{:08b}".format(i)


        all_bits = padding_start + add_one_and_check(all_bits) + padding_end
        print("all bits len : {}".format(len(all_bits)))

        return all_bits 

