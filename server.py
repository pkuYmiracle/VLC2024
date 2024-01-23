# server 

import trans_helper
import rx_new
import time

server = trans_helper.Server()
server.add_user("keys/Bob/",10,"Bob", password="password")

receive_bits = ''

try:
    # while True:
    receive_bits += str(rx_new.get_data())
    
    print(receive_bits)

except KeyboardInterrupt:
    pass
finally:
    server.receive_file("received.txt",receive_bits)