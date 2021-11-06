from serial_tools.setup_serial import *
from serial_tools.clean import *
from serial_tools.read import *

def send_command(serial, command):
    waiting_for_ok = False
    while True:

        if serial==None or not serial.isOpen():
            serial = Setup_serial("COM4")
            print("Reconnecting")
        else:
            _, bundle = Read(serial, False)
            message = Clean(bundle)

            if message=="Ok":
                waiting_for_ok = False
                print("Ok")
                break

            if waiting_for_ok:
                if not message:
                    continue

            if command=="START":
                if message=="READY":
                    print("READY")
                    waiting_for_ok = True
                    serial.write(b'START')
            else:
                if not waiting_for_ok:
                    print("MOTORS RESET")
                    waiting_for_ok = True
                    serial.write(bytes(command, 'utf-8'))
    return serial
