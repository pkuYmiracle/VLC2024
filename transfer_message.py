import serial
import time
# Configure the serial connections
# You might need to change the COM port name and the baud rate

ser = serial.Serial(
    port='/dev/cu.usbserial-1140',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2  # Timeout for read operation, in seconds
)

def convert_to_frame(text:str):
    frame=text.encode('utf-8')
    text_len=len(frame)
    print(f"VLC Transmit Message: {text}")
    print(f"Message Length: {text_len}")
    frame=text_len.to_bytes(2,byteorder='big')+frame
    return frame


text=input("Please input message to transfer.\n")
print("Start Transmission...")
frame=convert_to_frame(text+'\n')
ser.write(frame)

ser.readline()
print("Transmission Over.\n")
ser.close()