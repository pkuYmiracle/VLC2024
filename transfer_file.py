# file gen
import os
import codecs
import random
import string

def create_file(file_name, size_in_bytes):
    with codecs.open(file_name, 'w', 'utf-8') as f:
        while os.path.getsize(file_name) < size_in_bytes:
            random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(1024))
            f.write(random_string)
import filecmp

def check_file(file1,file2):
    # 比较文件
    result = filecmp.cmp(file1, file2)
    return result


# run client
# gen keys
import rsa_helper
#rsa_helper.generate_keys("keys/Bob/")
import trans_helper
import random
client = trans_helper.Client("keys/Bob/",random_len=10,user_name="Bob", password="password")

file_name=input("Which file are you planning to transfer?\n")
print("Start Transmission.")
send_bits = client.send_file(file_name)

before_bits = send_bits
for i in range(0, len(send_bits), 16):
    pos = random.randint(i,i + 15)
    assert(i <= pos <= i + 15)
    flag = random.randint(0,1) >= 1
    if flag :
        send_bits = send_bits[:pos] + '1' +  send_bits[pos + 1 : ]
    else:
        send_bits = send_bits[:pos] + '0' +  send_bits[pos + 1 : ]
     

diff = sum([send_bits[i] != before_bits[i] for i in range(len(send_bits))])/ len(send_bits)
print("diff rate " , diff)


# send_bits='10100111'
send_data=send_data=bytes(int(send_bits[i:i+8], 2) for i in range(0, len(send_bits), 8))
data_len=len(send_data)
send_data=data_len.to_bytes(2,byteorder='big')+send_data
print(send_data)

import serial
import time
# Configure the serial connections
# You might need to change the COM port name and the baud rate

ser = serial.Serial(
    port='/dev/cu.usbserial-110',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2  # Timeout for read operation, in seconds
)

ser.write(send_data)
ser.readline()
print("Transmission Over.")
ser.close()
