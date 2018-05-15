import serial
import time
import os

DEBUG = True
#DEBUG = False



SHOT    = "171\n"
USB_OFF = "162\n"
USB_ON  = "170\n"
FOC_ON  = "186\n"
FOC_OFF = "178\n"

TRIG = True

def get_com(com):

    while True:
        try:
            readOut = com.readline().decode('ascii')
            break
        except:
            pass
    com.flush()                                             #clean serial bufers
    return readOut


flag = True
d = ''
while flag:
    for devises in os.listdir('/dev/'):
        if 'ttyUSB' in devises:
            ser = serial.Serial('/dev/' + devises, 115200)
            if 'PULT' in get_com(ser):
                d = devises
                flag = False
            else:
                print("The device could not be connected..\n")
    time.sleep(2)
print("The device is connected successfully.. ", d, "\n")



def init_serial(*args):
    flag = True
    d = ''
    while flag:
        for devises in os.listdir('/dev/'):
            if 'ttyUSB' in devises:
                com = serial.Serial('/dev/' + devises, 115200)
                if 'PULT' in get_com(com):
                    d = devises
                    flag = False
                else:
                    print("The device could not be connected..\n")
        time.sleep(2)
    print("The device is connected successfully.. ", d, "\n")
    return com



def shot(*args):
    ser.flush()
    ser.write(str(SHOT).encode())
    result = get_com(ser)
    return result

def focus_on(*args):
    ser.flush()
    ser.write(str(FOC_ON).encode())
    result = get_com(ser)
    return result

def focus_off(*args):
    ser.flush()
    ser.write(str(FOC_OFF).encode())
    result = get_com(ser)
    return result

def usb_on(*args):
    ser.flush()
    ser.write(str(USB_ON).encode())
    result = get_com(ser)
    return result

def usb_off(*args):
    ser.flush()
    ser.write(str(USB_OFF).encode())
    result = get_com(ser)
    return result


#while True:

#    if TRIG:
#        print("Writing: ", USB_ON)
#        ser.write(str(USB_ON).encode())                           #send to serial
#    else:
#        print("Writing: ", USB_OFF)
#        ser.write(str(USB_OFF).encode())
#    TRIG = not(TRIG)
#    time.sleep(1)
#    while True:
#        try:
#            print ("Attempt to Read")
#            readOut = ser.readline().decode('ascii')        #read in serial
#            time.sleep(1)
#            print ("Reading: ", readOut)
#            break
#        except:
#            pass
#    print ("Restart")
#    ser.flush()                                             #clean serial bufers
