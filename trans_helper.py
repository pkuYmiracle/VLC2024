import rsa_helper
import rsa
import transFileBits
import transStrBits
import random
PADDING_LEN = 2 ** 8
REAL_INFO = 10


def generate_random_binary_string(length):
    return ''.join(random.choices(['0', '1'], k=length)) 
# assume 1/16 error
# 10 / 16
# 8     0 1 2 3 4 5 6 7 8 9 
# 10 0 - 9
# 11 1 3 5 7 9
# 12 2 3 6 7 
# 13 4 5 6 7 
# 14 8 9  
# 15 10 ^ 11 ^ 12 ^ 13 ^ 14
def calc_each_ten(input_str : str) -> str:
    output_str = ''
    all_flag = False
    cur_flag = sum([input_str[j] == '1' for j in [0,1,2,3,4,5,6,7,8,9]]) % 2 == 1
    output_str += '1' if cur_flag else '0'
    all_flag ^= cur_flag
    cur_flag = sum([input_str[j] == '1' for j in [1,3,5,7,9]]) % 2 == 1
    output_str += '1' if cur_flag else '0'
    all_flag ^= cur_flag
    cur_flag = sum([input_str[j] == '1' for j in [2,3,6,7]]) % 2 == 1
    output_str += '1' if cur_flag else '0'
    all_flag ^= cur_flag
    cur_flag = sum([input_str[j] == '1' for j in [4,5,6,7]]) % 2 == 1
    output_str += '1' if cur_flag else '0'
    all_flag ^= cur_flag
    cur_flag = sum([input_str[j] == '1' for j in [8,9]]) % 2 == 1
    output_str += '1' if cur_flag else '0'
    all_flag ^= cur_flag 
    output_str += '1' if all_flag else '0'
    return output_str
def add_one_and_check(input_str : str) -> str: 
    output_str = ""
    if len(input_str) % REAL_INFO:
        input_str += '0' * (REAL_INFO - len(input_str) % REAL_INFO)
    input_len = len(input_str)
    for i in range(input_len):
        assert(input_str[i] == '0' or input_str[i] == '1')
    for i in range(0, input_len, REAL_INFO):
        output_str  += input_str[i : i + REAL_INFO]
        output_str += calc_each_ten(input_str[i : i + REAL_INFO])

    output_len = len(output_str) 
    assert(output_len * REAL_INFO == input_len * 16)
    assert(output_len % 16 == 0)
    return output_str
# assume 1/16 error
# 10 / 16
# 8     0 1 2 3 4 5 6 7 8 9 
# 10 0 - 9
# 11 1 3 5 7 9
# 12 2 3 6 7 
# 13 4 5 6 7 
# 14 8 9  
# 15 10 ^ 11 ^ 12 ^ 13 ^ 14
def remove_one_and_check(input_str: str) -> (str, bool):
    output_str = ""
    
    assert(len(input_str) % 16 == 0)

    for i in range(len(input_str)):
        assert(input_str[i] == '0' or input_str[i] == '1')

    ret_flag = True    
    for i in range(0, len(input_str), 16):
        all_flag = input_str[i + 10] == '1'
        flag1 = input_str[i + 11] == '1'
        flag2 = input_str[i + 12] == '1'
        flag4 = input_str[i + 13] == '1'
        flag8 = input_str[i + 14] == '1'
        flag = input_str[i + 15] == '1'
        if (flag1 ^ flag2 ^ flag4 ^ flag8 ^ all_flag) != flag:
            # error in ecc
            output_str += input_str[i : i + 10]
            continue

        if (sum([input_str[j] == '1' for j in range(i, i + 10)]) % 2 == 1 ) == all_flag:
            # no error
            output_str += input_str[i : i + 10]
            continue
            
        for j in range(i, i + 10):
            cur_str = input_str[i:j] + '1' + input_str[j+1 : i + 10]
            if calc_each_ten(cur_str) == input_str[i + 10 : i + 16]:
                output_str += cur_str
                break
            cur_str = input_str[i:j] + '0' + input_str[j+1 : i + 10]
            if calc_each_ten(cur_str) == input_str[i + 10 : i + 16]:
                output_str += cur_str
                break
            if j == i + 9:
                ret_flag = False 

    assert(ret_flag == False or len(input_str) * REAL_INFO == len(output_str) * 16)
    return output_str,ret_flag
class Server :
    def __init__(self):
        self.users = []

    def add_user(self, key_file : str, random_len : int, user_name : str, password : str):
        self.users.append((key_file, random_len, user_name, password))

    def receive_file(self, file_name : str, all_bits : str):
        '''
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
        '''
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


        #all_bits = padding_start + add_one_and_check(all_bits) + padding_end
        all_bits = add_one_and_check(all_bits)
        print("all bits len : {}".format(len(all_bits)))

        return all_bits 

