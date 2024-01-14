import serial
import time
import math
from collections import deque
# Configure the serial connections
# You might need to change the COM port name and the baud rate

import pprint
def get_signal():
    ser = serial.Serial(
        port='COM3',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=2  # Timeout for read operation, in seconds
    )
    data_points = []
    is_start=False
    head_padding=0
    len_head=0
    cnt=0
    total_len = -1
    data_get=[]
    data_get_val=''
    converted_data = ''
    print("Padding start....")
    val_0=0
    val_1=0
    
    lastbit = '0'
    try:
        while True:
            if ser.in_waiting >= 4:  # Check if at least 4 bytes are in the buffer
                # Read 4 bytes from the serial port
                data = ser.read(4)
                # Convert bytes to uint32_t (adjust 'little' or 'big' based on your device)
                number = int.from_bytes(data, byteorder='little', signed=False)
                data_points.append(number)
                min_val=min(data_points)
                max_val=max(data_points)
                mid_val=(min_val+max_val)/2
                if is_start == False:
                    if number<mid_val-100:
                        head_padding+=1
                        if head_padding==64:
                            is_start=True
                            val_0=max_val
                            val_1=min_val
                            print("Is start...")
                    else:
                        head_padding=0
                
                
                if is_start:
                    data_get.append(number)
                    bit=''

                    mid_low = (val_1 * 2 + val_0) / 3
                    mid_high = (val_1 + val_0 * 2) / 3

                    if number <= mid_low:
                        bit = '1'
                    elif number <= mid_high:
                        bit = '2'
                    else:
                        bit = '0'
                                    
                    
                    if lastbit == '2' and bit != '2':
                        converted_data += bit
                        
                        if len(converted_data) == 16 and total_len == -1:
                            total_len = int(converted_data, 2)
                            converted_data = ''
                        
                        if total_len != -1 and len(converted_data) == total_len * 8:
                            return converted_data
                        
                    # if total_len != -1:
                    #     print(total_len)
                    # print(bit)
                    
                    if len(converted_data) % 100 == 0 and len(converted_data) > 0:
                        print(total_len,len(converted_data))
                    
                    lastbit = bit

                # print(number<mid_val-100,number,min_val,max_val,mid_val)    
                # print(head_padding)
    except KeyboardInterrupt:
        print("Exiting program")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if len_head !=16:
            ser.close()
            print("Serial connection closed")  



def get_data():
    data_0=get_signal()
    return data_0

if __name__ == "__main__":
    data_0 = get_signal()
    hex_str = hex(int(data_0, 2))[2:]
    print(bytes.fromhex(hex_str).decode('utf-8'))