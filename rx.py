import serial.tools.list_ports
import pprint
import serial

import trans_helper


import threading
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
# %matplotlib notebook

# Set up the serial port (for example, COM3, 9600 baud rate)




port_data = []
for port in serial.tools.list_ports.comports():
    info = dict({"Name": port.name, "Description": port.description, "Manufacturer": port.manufacturer,
                 "Hwid": port.hwid})
    port_data.append(info)
pprint.pprint (port_data)

ser = serial.Serial(
    port='/dev/cu.usbserial-1120',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2  # Timeout for read operation, in seconds
)

# Deque for storing data points
data_points = deque(maxlen=200)
data_lock = threading.Lock()  # Thread lock for safe data access

data_all = []


def read_from_port(ser):
    print("Start read port:")
    try:
        while True:
            if ser.in_waiting >= 4:
                data = ser.read(4)
                number = int.from_bytes(data, byteorder='little', signed=False)
                data_all.append(number)
                    
                with data_lock:  # Acquire lock to update data_points
                    data_points.append(number)
                    
    except KeyboardInterrupt:
        print("Exiting program")
        
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        ser.close()
        print("Serial connection closed")

# Start the thread for reading serial data
thread = threading.Thread(target=read_from_port, args=(ser,))
thread.daemon = True
thread.start()

# Set up plot to call animate() function periodically
# ani = animation.FuncAnimation(fig, animate, interval=30, blit=True)

# plt.show()


def rx_receive() :
    
    print(data_all)
    
    ret = ['0' if i > 2000 else '1' for i in data_all]
    
    return ''.join(ret)