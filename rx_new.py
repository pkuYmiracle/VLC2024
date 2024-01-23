import serial
import time
import math
from collections import deque
# Configure the serial connections
# You might need to change the COM port name and the baud rate

ser = serial.Serial(
    port='/dev/cu.usbserial-1120',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2  # Timeout for read operation, in seconds
)
print(type(ser))
import statistics
def remove_outliers(nums:deque, threshold=2):
    if len(nums)==1:
        return nums
    # 创建双端队列
    num_deque = nums.copy()
    
    # 计算均值和标准差
    mean_value = statistics.mean(num_deque)
    std_dev = statistics.stdev(num_deque)
    
    # 定义异常值的阈值，通常为均值加减标准差的倍数
    threshold_value = threshold * std_dev
    
    # 从队列两端去除偏离均值过多的异常数
    while len(num_deque) > 0 and abs(num_deque[0] - mean_value) > threshold_value:
        num_deque.popleft()
    
    while len(num_deque) > 0 and abs(num_deque[-1] - mean_value) > threshold_value:
        num_deque.pop()
    
    return list(num_deque)

import pprint
data_points = deque(maxlen=400)
def get_signal():
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
            if ser.in_waiting >= 400:  # Check if at least 4 bytes are in the buffer
                # Read 4 bytes from the serial port
                for _ in range(100):
                    data = ser.read(4)
                    cnt+=1
                    if cnt<=100:
                        continue
                    # Convert bytes to uint32_t (adjust 'little' or 'big' based on your device)
                    number = int.from_bytes(data, byteorder='little', signed=False)
                    print(number)
                    data_points.append(number)
                    min_val=min(remove_outliers(data_points))
                    max_val=max(remove_outliers(data_points))
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
                            
                        if total_len != -1:
                            pass
                            print(total_len)
                        # print(bit)
                        print(converted_data,val_0,val_1)
                        
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

data_0=get_signal()
pprint.pprint(data_0)

hex_str = hex(int(data_0, 2))[2:]

print(hex_str)

print(bytes.fromhex(hex_str).decode('utf-8'))
