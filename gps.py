#!/home/evoart/miniforge3/envs/pyqt-env/bin/python


import serial

ser = serial.Serial("/dev/ttyTHS1", 9600, timeout=1)

while True:
    try:
        line = ser.readline().decode('ascii', errors='replace').strip()
        if line:
            print(line)
    except Exception as e:
        print("Hata:", e)
        break
