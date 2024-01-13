# gen keys
import rsa_helper
rsa_helper.generate_keys("keys/Bob/",key_len=256)
import trans_helper
import random
client = trans_helper.Client("keys/Bob/",random_len=10,user_name="Bob", password="password")

server = trans_helper.Server()
server.add_user("keys/Bob/",10,"Bob", password="password")
send_bits = client.send_file("test.txt")

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
 
server.receive_file("test2.txt",send_bits)