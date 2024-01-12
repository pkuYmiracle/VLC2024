# gen keys
import rsa_helper
rsa_helper.generate_keys("keys/Alice/")
import trans_helper

client = trans_helper.Client("keys/Alice/",random_len=10,user_name="Alice")

server = trans_helper.Server()
server.add_user("keys/Alice/",10,"Alice")
send_bits = client.send_file("test.txt")

send_bits += trans_helper.generate_random_binary_string(233) # 模拟padding后面的一些随机串
server.receive_file("test2.txt",send_bits[1150:])