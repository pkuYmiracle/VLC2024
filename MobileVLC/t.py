import threading
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
# %matplotlib notebook

# Set up the serial port (for example, COM3, 9600 baud rate)
ser = serial.Serial(
    port='/dev/cu.usbserial-1120',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2  # Timeout for read operation, in seconds
)

# Deque for storing data points
data_points = deque(maxlen=400)
data_lock = threading.Lock()  # Thread lock for safe data access

def read_from_port(ser):
    print("Start read port:")
    try:
        while True:
            if ser.in_waiting >= 400:
                for _ in range(100):
                    data = ser.read(4)
                    number = int.from_bytes(data, byteorder='little', signed=False)
                    
                    with data_lock:  # Acquire lock to update data_points
                        data_points.append(number)
    except KeyboardInterrupt:
        print("Exiting program")
        
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        ser.close()
        print("Serial connection closed")

def animate(i):
    with data_lock:
        if data_points:
            line.set_data(range(len(data_points)), list(data_points))
            ax.relim()  # Recalculate limits
            ax.autoscale_view()  # Auto-scale
        print(data_points)
    return line,

# Set up the plot
fig, ax = plt.subplots()
line, = ax.plot(data_points)
ax.set_xlim(0, 200)
ax.set_ylim(0, 4095)  # Adjust based on your ADC resolution

# Start the thread for reading serial data
thread = threading.Thread(target=read_from_port, args=(ser,))
thread.daemon = True
thread.start()

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, interval=100, blit=True)

plt.show()