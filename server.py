# gen keys
import rsa_helper
rsa_helper.generate_keys("keys/Alice/")
import trans_helper

import rx

server = trans_helper.Server()
server.add_user("keys/Alice/",10,"Alice")

import time

while True:

    received_bits = rx.rx_receive()

    server.receive_file("test2.txt",received_bits)
    
    time.sleep(5)