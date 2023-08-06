import serial.tools.list_ports as l_p

def func():
    for p in l_p.comports():
        print(p)

if __name__ == "__main__":
    func()
